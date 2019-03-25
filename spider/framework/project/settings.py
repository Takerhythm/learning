SPIDERS = ['spiders.baidu.BSpider','spiders.douban.DoubanSpider']

PIPELINES = ['pipelines.BaiduPipeline', 'pipelines.DoubanPipeline']

# 启用的默认爬虫中间件类
# SPIDER_MIDDLEWARES = ['middlewares.TestSpiderMiddleware1']

# 启用的默认下载器中间件类
# DOWNLOADER_MIDDLEWARES = ['middlewares.TestDownloaderMiddleware1']

ASYNC_TYPE = 'coroutine'

MAX_ASYNC_THREAD_NUMBER = 4

IS_DISTRIBUTION = False

# SCHEDULER_PERSIST = True