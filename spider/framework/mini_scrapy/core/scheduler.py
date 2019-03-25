import six
import w3lib.url
from mini_scrapy.conf.settings import IS_DISTRIBUTION
if IS_DISTRIBUTION:
    from mini_scrapy.utils.queue import Queue
    from mini_scrapy.utils.set import RedisFilterContainer as Container
else:
    from six.moves.queue import Queue
    from mini_scrapy.utils.set import NoramlFilterContainer as Container
from hashlib import  sha1
from mini_scrapy.utils.log import logger


class Scheduler(object):
    '''
    1. 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重判断
    '''
    def __init__(self, collector):
        self.queue = Queue()
        self._filter_container = Container()
        # self.repeat_request_num = 0
        self.collector = collector

    def add_request(self, request):
        '''添加请求对象'''
        self._filter_request(request)

    def get_request(self):
        '''获取一个请求对象并返回'''
        try:
            request = self.queue.get(False)
        except Exception:
            return None
        return request

    def _filter_request(self, request):
        '''请求去重'''
        # 暂时不实现
        request.fp = self._gen_fp(request)  # 给request对象增加一个fp指纹属性
        if request.filter:
            if not self._filter_container.exists(request.fp):
                self.queue.put(request)
                self._filter_container.add_fp(request.fp)  # 向指纹容器集合添加一个指纹
                return True
            else:
                self.collector.incr(self.collector.repeat_request_nums_key)
                logger.info("发现重复的请求：<{} {}>".format(request.method, request.url))
                return False
        else:
            self.queue.put(request)

    def _gen_fp(self, request):
        """生成并返回request对象的指纹
        用来判断请求是否重复的属性：url，method，params(在url中)，data
        为保持唯一性，需要对他们按照同样的排序规则进行排序
        """
        # 1. url排序：借助w3lib.url模块中的canonicalize_url方法
        url = w3lib.url.canonicalize_url(request.url)
        # 2. method不需要排序，只要保持大小写一致就可以 upper()方法全部转换为大写
        method = request.method.upper()
        # 3. data排序：如果有提供则是一个字典，如果没有则是空字典
        data = request.data if request.data is not None else {}
        data = sorted(data.items(), key=lambda x: x[0])  # 用sorted()方法 按data字典的key进行排序
        # items()返回元祖 key参数表示按什么进行排序 x表示data.items() x[0]表示元祖第一个值,也就是data的键

        # 4. 利用sha1计算获取指纹
        s1 = sha1()
        s1.update(self._to_bytes(url))  # sha1计算的对象必须是字节类型
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))

        fp = s1.hexdigest()
        return fp

    def _to_bytes(self, string):
        """为了兼容py2和py3，利用_to_bytes方法，把所有的字符串转化为字节类型"""
        if six.PY2:
            if isinstance(string, str):
                return string
            else:  # 如果是python2的unicode类型，转化为字节类型
                return string.encode('utf-8')
        elif six.PY3:
            if isinstance(string, str):  # 如果是python3的str类型，转化为字节类型
                return string.encode("utf-8")
            else:
                return string