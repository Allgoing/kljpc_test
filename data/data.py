# -- coding: utf-8 --
from common.excelParse import ExcelParser


def read_case_data(file=None, sheet_name='sheet1', row=0, col=0):

    if file:
        excel = ExcelParser(file)
    else:
        excel = ExcelParser(r'/Users/work/kljTest/kljpc/data/testcases.xlsx')

    data = excel.get_all_cells(sheet_name, key_row=row, start_col=col)
    titles = excel.get_cols(sheet_name,col_num=2)
    list_data = list(zip(data, titles))


    return list_data


class Case:
    # MODULE = 0
    # ID = 1
    # CASENAME = 2
    # URL = 3
    # METHOD = 4
    # PARAMS = 5
    # HEADERS = 6
    # BODY = 7
    # BODYTYPE = 8
    # STATUS_CODE = 9
    # MESSAGE = 10
    # RESULT = 11
    # TESTER = 12

    MODULE = 'module'
    ID = 'id'
    CASENAME = 'casename'
    URL = 'url'
    METHOD = 'method'
    PARAMS = 'params'
    HEADERS = 'headers'
    BODY = 'body'
    BODYTYPE = 'bodytype'
    STATUS_CODE = 'status_code'
    MESSAGE = 'message'
    RESULT = 'result'
    TESTER = 'tester'


if __name__ == '__main__':
    # a = read_case_data(sheet_name='sheet1')
    # print(len(a))
    a = ExcelParser(r'/Users/work/kljTest/kljpc/data/testcases.xlsx')
    # print(a.get_cols(sheet='sheet1', col_num=2))
    b = read_case_data(sheet_name='sheet1')
    print(b[1])