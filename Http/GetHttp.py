# coding=utf-8

# 引入外部库
from urllib import request


# 引入内部库


class GetHttp:
    def __init__(self, url: str, headers=None, charset='gbk'):
        if headers is None:
            headers = {}
        self._response = ''
        try:
            self._response = request.urlopen(request.Request(url=url, headers=headers))
        except Exception as e:
            print(e)
        self._c = charset

    @property
    def get_page_content(self):
        try:
            return self._response.read().decode(self._c)
        except Exception as e:
            print(e)
            return ''
