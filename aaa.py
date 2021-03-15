# # -- coding: utf-8 --
# import requests, pytest
#
#
# def test_comment():
#
#     url = 'http://api.kunlunjue.com/Content/comments'
#     data = {
#         'commentContent': '哈哈哈',
#         'token': '16e06e86306137098a00ea6b830bdcbb3227650',
#         'itemId': 6507,
#         'type': 1
#     }
#
#     r = requests.post(url, data=data)
#     result = r.json()
#     assert
#
#
#opresponce.py
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@author:ht
@desc：根据数据表中的信息对response的结果做断言（code，参数完整性）操作，并将断言结果写入数据表中
思考：接口返回的对象有可能不是json哦，比如xml，那么我们这个类应该具有可扩展性才对

'''
from mylogging import mylogger
from opmysql import OpMysql
import json

class compare_param:
    def compare_json_code(self,case_data,result_data):
        '''
        当接口返回结果是json格式的数据，通过这个方法，你可以对比返回的状态码code，并将结果写回数据库
        :param case_data: dict=>数据库中存储的测试case的数据，一条数据
        :param result_data: dict=》调用接口返回的json格式的数据
        :return:
        1.{'code': 200, 'message': 'code相等', 'content': ''}
        2.{'code': 300, 'message': 'code不相等', 'content': ''}
        3.{'code': 301, 'message': 'code不存在', 'content': ''}
        4.{'code': 400, 'message': 'code比较出现异常', 'content': ''}
        '''
        try:
            op_sql = OpMysql()
            update_sql = "UPDATE case_interface SET result_interface=%s ,code_actual=%s ,result_code_compare=%s WHERE id = %s"

            code_expected = case_data.get("code_to_compare") #获取数据库中保存的code值
            if 'resultCode' in result_data:
                result_code = result_data.get("resultCode")# 获取返回结果中的code值
                if code_expected == result_code:
                    op_sql.op_sql(update_sql,(str(result_data),result_code,0,case_data.get("id"))) # code比较结果，0-pass
                    result = {'code': 200, 'message': 'code相等', 'content': ''}
                else:
                    op_sql.op_sql(update_sql, (str(result_data), result_code, 1, case_data.get("id"))) # 1-fail
                    result = {'code': 300, 'message': 'code不相等', 'content': ''}
            else:
                op_sql.op_sql(update_sql, (str(result_data), None, 2, case_data.get("id"))) #2-无待比较参数
                result = {'code': 301, 'message': 'code不存在', 'content': ''}
        except BaseException as e:
            op_sql.op_sql(update_sql, (str(result_data), None, 4, case_data.get("id"))) # 5-系统异常
            mylogger.info("[compare_json_code 测试用例的信息]-%s"%str(case_data))
            mylogger.info("[compare_json_code 接口返回的信息]-%s"%str(result_data))
            mylogger.exception(e)
            result = {'code': 400, 'message': 'code比较出现异常', 'content': ''}

        return result
    def jsondata_to_set(self,dict_ob, set_ob):
        '''
        将json格式的数据进行去重操作：这是一个递归
        :param dict_ob: dict：json格式的数据
        :param set_ob: 传入的set对象（没有内容）
        :return:
        1.{"code":200,"message":"json：参数去重成功","content":set_ob}
        2.{"code": 400, "message": "json：参数去重出现异常", "content": ""}
        '''
        try:
            for key, value in dict_ob.items():
                set_ob.add(key)
                if isinstance(value, dict):
                    self.jsondata_to_set(value, set_ob)
                elif isinstance(value, list):
                    for li in value:
                        self.jsondata_to_set(li, set_ob)

            result = {"code":200,"message":"json：参数去重成功","content":set_ob}
        except BaseException as e:
            mylogger.info("[jsondata_to_set params]-(dict_ob:%s,set_ob:%s)"%(str(dict_ob),str(set_ob)))
            mylogger.exception(e)
            result = {"code": 400, "message": "json：参数去重出现异常", "content": ""}
        return result
    def compare_json_params(self,case_data,result_data):
        '''
        当接口返回结果是json格式的数据，通过这个方法，你可以对比返回的参数和数据库中的预期参数，并将结果写入数据库中
        :param case_data: 数据库返回的用例信息，dict=》一条数据
        :param result_data: 接口返回的json数据，dict
        :return:
        1. {"code": 200, "message": "参数完整性相等", "content": ""}
        2. {"code": 301, "message": "参数完整性不相等", "content": ""}
        3. {"code": 300, "message": "去重失败：获取参数集错误", "content": ""}
        4. {"code": 400, "message": "参数完整性比较出现异常", "content": ""}
        '''
        try:
            op_sql = OpMysql()
            # 获取预期参数
            case_params = case_data.get("params_to_compare")
            case_params_set = eval(case_params)
            #更新数据的sql语句
            update_sql = "UPDATE case_interface set params_actual=%s, result_params_compare=%s WHERE id=%s"

            #对json数据进行去重操作
            params_set = set()
            set_result = self.jsondata_to_set(result_data,params_set)
            if set_result.get("code") == 200:
                #判断是否包含
                if case_params_set.issubset(params_set):
                    #跟新数据表
                    op_sql.op_sql(update_sql,(str(params_set),0,case_data.get("id"))) #0 pass
                    result = {"code": 200, "message": "参数完整性相等", "content": ""}
                else:
                    op_sql.op_sql(update_sql,(str(params_set),1,case_data.get("id"))) #1 fail
                    result = {"code": 301, "message": "参数完整性不相等", "content": ""}
            elif set_result.get("code") == 400:
                op_sql.op_sql(update_sql, (None, 2, case_data.get("id")))  # 2 去重错误
                result = {"code": 300, "message": "去重失败：获取参数集错误", "content": ""}
                # raise BaseException("我就是测试一下罗")
        except BaseException as e:
            op_sql.op_sql(update_sql, (None, 5, case_data.get("id")))  # 5 系统异常
            mylogger.info("[compare_json_params params -（case_data:%s,result_data:%s）]"%(str(case_data),str(result_data)))
            mylogger.exception(e)
            result = {"code": 400, "message": "参数完整性比较出现异常", "content": ""}
        return result

    # (预留方法):当接口返回结果是xml格式的数据的时候，可以使用这个方法来对比返回的状态码code，并将结果写回到数据库
    def compare_xml_code(self):
        pass
    # (预留方法)：当接口返回结果是xml格式的数据，通过这个方法，你可以对比返回的参数和数据库中的预期参数，并将结果写入数据库中
    def compare_xml_params(self):
        pass

if __name__ == "__main__":
    #获取数据库的测试用例的信息：id=1
    mysql_op = OpMysql()
    case_data = mysql_op.select_one("SELECT * FROM  case_interface WHERE id = 1")
    #创建一个compare对象
    cmp_obj = compare_param()

    # test：compare_json_params：参数完整性相等
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos":"测试环境店铺","resultCode": "000","totalPage": 66746}'
    # cmpare_result = cmp_obj.compare_json_params(case_data,json.loads(result_interface))
    # print(cmpare_result)
    # test：compare_json_params：参数完整性不相等
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos11":"测试环境店铺","resultCode": "000","totalPage": 66746}'
    # cmpare_result = cmp_obj.compare_json_params(case_data,json.loads(result_interface))
    # print(cmpare_result)
    # test：compare_json_params：去重失败
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos11":"测试环境店铺","resultCode": "000","totalPage": 66746}'
    # cmpare_result = cmp_obj.compare_json_params(case_data,result_interface)
    # print(cmpare_result)
    # test：compare_json_params：参数完整性比较出现异常，前提是直接在代码中raise一个异常出来，因为我也想不到这里在什么情况下会走这条分支
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos":"测试环境店铺","resultCode": "000","totalPage": 66746}'
    # cmpare_result = cmp_obj.compare_json_params(case_data,result_interface)
    # print(cmpare_result)


    #测试递归调用函数
    # dict01 = {"name":"ht","pass":"123","family":[{"name1":{"new":"new_value","haha":"ss"},"age":1},{"name2":"老公","age3":18}],"lover":{"lover01":"吃","lover02":"喝"}}
    # my_set = set()
    # result = cmp_obj.jsondata_to_set(dict01,my_set)
    # if result.get("code") == 200:
    #     print(result.get("code"))
    #     print(result.get("message"))
    #     print(result.get("content"))
    result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos": [{"phone": "15100000000","star": 5,"totalQualityEvaluation": 0,"photoUrls": "","latitude": 0},{"phone": "15200000000","detail": null,"sex": null,"serviceFrequency": 0}],"resultCode": "000","totalPage": 66746}'
    my_set = set()
    result = cmp_obj.jsondata_to_set(json.loads(result_interface),my_set)
    if result.get("code") == 200:
        print(result.get("code"))
        print(result.get("message"))
        print(result.get("content"))


    # test_compare_json_code:200-code相等
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos":"测试环境店铺","resultCode": "000","totalPage": 66746}'
    # compare_result = cmp_obj.compare_json_code(case_data, json.loads(result_interface))
    # print(compare_result)

    # test_compare_json_code:300-code不相等
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos":"测试环境店铺","resultCode": "001","totalPage": 66746}'
    # compare_result = cmp_obj.compare_json_code(case_data, json.loads(result_interface))
    # print(compare_result)

    # test_compare_json_code:301-code不存在
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos":"测试环境店铺","totalPage": 66746}'
    # compare_result = cmp_obj.compare_json_code(case_data, json.loads(result_interface))
    # print(compare_result)

    # test_compare_json_code:400-code比较出现异常
    # result_interface = '{"message": "获取附近服务商成功","nextPage": 1,"pageNo": 0,"merchantInfos":"测试环境店铺","resultCode": "000","totalPage": 66746}'
    # compare_result = cmp_obj.compare_json_code(case_data, result_interface) #传入错误的参数
    # print(compare_result)