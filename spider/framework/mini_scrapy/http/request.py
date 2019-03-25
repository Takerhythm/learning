class Request(object):
    '''框架内置请求对象，设置请求信息'''

    def __init__(self, url, method='GET',headers=None, params=None, data=None, parse='parse', meta={}, filter=True):
        self.url = url    # 请求地址
        self.method = method    # 请求方法
        self.headers = headers    # 请求头
        self.params = params    # 请求参数
        self.data = data    # 请求体
        self.parse = parse
        self.meta = meta
        self.filter = True