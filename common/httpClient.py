# -- coding: utf-8 --
import json

import requests


class HttpClient(object):

    def __init__(self, url, method, bodytype=None, params=None):
        self.__url = url
        self.__method = method
        self.__bodytype = bodytype
        self.__params = params

        self.__headers = {}
        self.__body = {}

        self.__response = None

    def add_header(self, name, value):
        '''
        添加请求头信息：add_header('Accept-Language','zh_CN')
        :param name:请求头名称
        :param value:请求头值
        :return:
        '''
        self.__headers[name] = value

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    def set_body(self, body):

        '''
        设置post请求的数据
        如果body数据是xml或其它文本数据，body格式如下：body = {'text':''xml或其它文本数据}
        :param body: 字典格式的数据
        :return:
        '''
        if body is None or body == '':
            return
        else:
            body = json.loads(body)
        if isinstance(body, dict):
            self.__body = body
        else:
            raise Exception ('body数据必须是字典，xml或其它文本格式是：body = {“text":"xml文本或其它文本数据}"')

    def send(self):
        if self.__method == Method.GET:
            self.__response = requests.get (url=self.__url, headers=self.__headers, params=self.__params)
        elif self.__method == Method.POST:
            self.add_header ('Content-Type', self.__bodytype)

            if self.__bodytype == BodyType.URL_ENCODE:
                self.__response = requests.post (url=self.__url, headers=self.__headers, data=self.__body)
            elif self.__bodytype == BodyType.FORM_DATA:
                self.__response = requests.post (url=self.__url, headers=self.__headers, data=self.__body)
            elif self.__bodytype == BodyType.JSON:
                self.__response = requests.post (url=self.__url, headers=self.__headers, json=self.__body)
            elif self.__bodytype == BodyType.XML:
                self.__response = requests.post (url=self.__url, headers=self.__headers,
                                                 data=self.__body.get ('text'))
            else:
                raise Exception ('数据格式不支持')
        return self.__response

    @property
    def text(self):
        if self.__response is not None:
            return self.__response.text

    @property
    def json(self):
        if self.__response is not None:
            return self.__response.json

    @property
    def status_code(self):
        if self.__response is not None:
            return self.__response.status_code

    @property
    def response(self):
        return self.__response


class Method:
    GET = 'get'
    POST = 'post'


class BodyType:
    FORM_DATA = 'multipart/form-data'
    JSON = 'application/json'
    XML = 'application/xml'
    URL_ENCODE = 'application/x-www-form-urlencoded'


if __name__ == '__main__':
    pass
    # client = HttpClient(url='https://petstore.swagger.io/v2/pet/1000', method=Method.GET)
    # client.add_header('content-type', 'application/json')
    # client.send()
    # print(client.text)
    # print(client.status_code)
    #
    # print(client.headers)

    # def __init__(self):
    #     pass
    #
    # def __get(self, url, params=None, headers=None, timeout=10, **kwargs):
    #     '''
    #     封装get方法
    #     :param url:接口的完整地址
    #     :param params: 入参
    #     :param headers: header
    #     :param timeout:超时时间
    #     :return: 返回response对象
    #     '''
    #     response = requests.get(url, params=json.loads(json.dumps(eval(params))), headers=headers, timeout=timeout)
    #     return response
    #
    # def __post(self, url, data=None, json=None, headers=None, timeout=10, **kwargs):
    #     '''
    #     封装post方法
    #     :param url:接口完整地址
    #     :param data: 入参
    #     :param headers: header
    #     :param json: json格式化
    #     :param timeout: 超时时长
    #     :param kwargs:
    #     :return: 返回response对象
    #     '''
    #     response = requests.post(url=url, data=data, json=json, headers=headers, timeout=timeout)
    #     return response
    #
    # def send_request(self, requestMethod, requestUrl, requestData=None, requestJson=None, requestHeader=None, timeout=10):
    #     '''
    #     发送接口请求
    #     :param requestMethod:请求方式
    #     :param requestUrl: 请求url
    #     :param requestData: 请求的数据
    #     :param requestHeader: 请求头
    #     :return: response对象
    #     '''
    #     if requestMethod.lower() == 'get':
    #         response = self.__get(url=requestUrl, params=requestData, headers=requestHeader, timeout=timeout)
    #         return response
    #     elif requestMethod.lower() == 'post':
    #         response = self.__post(url=requestUrl, data=None, json=requestData, headers=requestHeader, timeout=timeout)
    #         return response
