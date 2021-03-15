from common.excelParse import ExcelParser
from common.httpClient import HttpClient
from caseTitle import CaseTitle
from readConfig import ReadConfig
import json
import requests


# e = ExcelParser('test1.xlsx')
# h = HttpClient()
# c = CaseTitle()
# j = e.get_all_cells('aaa')[1]
# r = ReadConfig()
#
# # print(type(r.get_header('header')))
# headers = json.loads(j[c.HEADER])
# data = json.loads(json.dumps(j[c.DATA]))
# print(type(data))


# res = h.send_request('get', j[c.HOST]+j[c.URL], requestData=j[c.DATA])
# try:
#     assert res.status_code == 200, 'code码错误'
#     assert res.json()['message'] == 'success', '接口msg错误'
#     print('测试通过')
# except:
#     print('测试失败')

# print(type(j[c.DATA]))
# a = json.loads(json.dumps(eval(j[c.DATA])))
# print(a, type(a))

# res = h.send_request('post', j[c.HOST]+j[c.URL], requestData=j[c.DATA], requestHeader=j[c.HEADER])
# print(res.json())
#
# res = requests.post(j[c.HOST]+j[c.URL], data=j[c.DATA], headers=headers)
# print(res.json())

# url = 'https://petstore.swagger.io/v2/pet'
# headers = {"content-type": "application/json"}
# # headers = {"accept": "application/json"}
# data = '''
# {
#   "id": 1003,
#   "category": {
#     "id": 0,
#     "name": "string"
#   },
#   "name": "habahaba",
#   "photoUrls": [
#     "string"
#   ],
#   "tags": [
#     {
#       "id": 0,
#       "name": "hahah1"
#     }
#   ],
#   "status": "available"
# }
# '''
#
# res = requests.post(url=url, headers=headers, data=data)
# print(res.status_code)
# print(res.json())


a = [1, 2, 3]
b = [4, 5, 6]
c = list(zip(a, b))
print(c)
