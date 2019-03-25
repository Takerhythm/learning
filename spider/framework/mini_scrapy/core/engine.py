import importlib
from datetime import datetime
import time
from mini_scrapy.http.request import Request    # 导入Request对象
from ..conf.settings import *
from mini_scrapy.utils.log import logger
if ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool
elif ASYNC_TYPE == 'coroutine':
    from mini_scrapy.async.coroutine import Pool
else:
    raise Exception('不支持的异步方式')
if IS_DISTRIBUTION:
    from mini_scrapy.utils.collector import RedisStatsCollector as Collector
else:
    from mini_scrapy.utils.collector import NormalStatsCollector as Collector
from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline


class Engine(object):
    '''
    a. 对外提供整个的程序的入口
    b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    '''

    def __init__(self):
        self.spiders =  self._auto_import_instances(SPIDERS, isspider=True) # 接收爬虫对象
        self.pipelines = self._auto_import_instances(PIPELINES)
        self.collector = Collector()
        self.scheduler = Scheduler(self.collector)    # 初始化调度器对象
        self.downloader = Downloader()    # 初始化下载器对象
        self.pipeline = Pipeline()    # 初始化管道对象
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)
        # self.requests_num = 0
        # self.responses_num = 0
        self.pool = Pool()
        self.is_running = True

    def _start_request(self):
        def _func(spider_name, spider):
            start_requests = spider.start_requests()
            for start_request in start_requests:
                # 2. 把初始请求添加给调度器
                start_request.spider_name = spider_name
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                self.scheduler.add_request(start_request)
                # self.requests_num += 1
                self.collector.incr(self.collector.request_nums_key)
        for spider_name, spider in self.spiders.items():
            self.pool.apply_async(_func, args=(spider_name, spider))

    def _auto_import_instances(self, path=[], isspider=False):
        '''通过配置文件，动态导入类并实例化
        path: 表示配置文件中配置的导入类的路径
        isspider: 由于爬虫需要返回的是一个字典，因此对其做对应的判断和处理
        '''
        instances = {} if isspider else []
        for p in path:
            module_name = p.rsplit(".", 1)[0]  # 取出模块名称
            cls_name = p.rsplit(".", 1)[1]  # 取出类名称
            ret = importlib.import_module(module_name)  # 动态导入爬虫模块
            cls = getattr(ret, cls_name)  # 根据类名称获取类对象
            if isspider:
                instances[cls.name] = cls()  # 组装成爬虫字典{spider_name:spider(),}
            else:
                instances.append(cls())  # 实例化类对象
                # 把管道中间件分别组装成 管道列表=[管道类1(),管道类2()] / 中间件列表 = [中间件类1(),中间件类2()]
        return instances  # 返回类对象字典或列表

    def _execute_request_response_item(self):
        request = self.scheduler.get_request()
        # 4. 利用下载器发起请求
        if not request:
            return
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)
        response = self.downloader.get_response(request)
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)
        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        spider = self.spiders[request.spider_name]
        parse = getattr(spider, request.parse)
        results = parse(response)
        for result in results:
            # 6. 判断结果对象
            # 6.1 如果是请求对象，那么就再交给调度器
            if isinstance(result, Request):
                # 利用爬虫中间件预处理请求对象
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                result.spider_name = request.spider_name
                self.scheduler.add_request(result)
                # self.requests_num += 1
                self.collector.incr(self.collector.request_nums_key)
            # 6.2 否则，就交给管道处理
            else:
                for pipeline in self.pipelines:
                    pipeline.process_item(result, spider)
        # self.responses_num += 1
        self.collector.incr(self.collector.response_nums_key)

    def _errorback(self, e):
        raise e

    def _callback(self, item):
        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._errorback)

    def _start_engine(self):
        '''依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)'''
        # 1. 爬虫模块发出初始请求
        self.pool.apply_async(self._start_request, error_callback=self._errorback)
        # 3. 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        for i in range(MAX_ASYNC_THREAD_NUMBER):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._errorback)
        timed_spider_all = sum([spider.timed_task for spider in self.spiders.values()])
        while True:
            time.sleep(0.001)
            if timed_spider_all == 0:
                if self.collector.request_nums != 0:
                    if self.collector.response_nums+self.collector.repeat_request_nums >= self.collector.request_nums:
                        self.is_running = False
                        break
        self.pool.close()

    def start(self):
        '''启动整个引擎'''
        start = datetime.now()  # 起始时间
        logger.info("开始运行时间：%s" % start)  # 使用日志记录起始运行时间
        self._start_engine()
        stop = datetime.now()  # 结束时间
        logger.info("开始运行时间：%s" % stop)  # 使用日志记录结束运行时间
        logger.info("耗时：%.2f" % (stop - start).total_seconds())  # 使用日志记录运行耗时
        logger.info('请求数%s' % self.collector.request_nums)
        logger.info('重复数%s' % self.collector.repeat_request_nums)
        logger.info('响应数%s' % self.collector.response_nums)
        self.collector.clear()