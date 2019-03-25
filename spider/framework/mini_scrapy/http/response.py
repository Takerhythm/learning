import json
import re
from lxml import etree
from bs4 import BeautifulSoup

class Response(object):
    '''框架内置Response对象'''
    def __init__(self, url, status_code, headers, body, request):
        self.url = url    # 响应url
        self.status_code = status_code    # 响应状态码
        self.headers = headers    # 响应头
        self.body = body    # 响应体
        self.request = request
        self.meta = self.request.meta

    def xpath(self, rule):
        '''提供xpath方法'''
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        '''提供json解析
        如果content是json字符串，是才有效
        '''
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        '''封装正则的findall方法'''
        if data is None:
            data = self.body
        return re.findall(rule, data)

    def css(self, selector):
        html = BeautifulSoup(self.body, 'lxml')
        return html.css(selector)