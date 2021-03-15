# -- coding: utf-8 --

import traceback

import xlrd, xlwt


class ExcelParser(object):

    def __init__(self, file_path):

        '''
        初始化ExcelParser，文件不存在时异常
        :param file_path: excel文件路径
        :return 返回book对象
        '''

        try:
            self.book = xlrd.open_workbook(file_path)
        except FileNotFoundError:
            print('没有发现待解析的文件')
            traceback.print_exc()
            self.book = None

    def get_sheet(self, sheet_name):

        '''
        获取sheet对象
        :param sheet_name:sheet名称
        :return: 放回sheet对象
        '''

        if self.book is not None:
            try:
                self.sheet = self.book.sheet_by_name(sheet_name)
                return self.sheet
            except xlrd.biffh.XLRDError:
                traceback.print_exc()
                self.sheet = None

    def get_sheets(self):
        '''
        获取所有sheet名称
        :return: list
        '''
        return self.book.sheet_names()

    def get_rows(self, sheet, row_num):

        '''
        获取特定行的数据
        :param sheet: sheet名称
        :param row_num: 需要获取的行的位置
        :return: 返回改行的所有数据
        '''

        rows = []
        if self.book is not None:
            try:
                sheet = self.get_sheet(sheet)
                rows = sheet.row_values(row_num)
            except(ValueError, IndexError):
                traceback.print_exc()
        return rows

    def get_col_index(self, sheet, row_num, name):

        '''
        获取特定列的下标值
        :param sheet: sheet页名称
        :param row_num: 行数
        :param name: 需要确定的名称
        :return: 返回特定列名的下标值
        '''

        col_index = None
        rows = self.get_rows(sheet, row_num)
        if rows is not []:
            col_index = rows.index(name)
        return col_index

    def get_cols(self, sheet, col_num):
        '''
        获取特定列数据
        :param sheet: sheet名称
        :param col_num: 列数
        :return: 返回特定列的数据
        '''
        cols = []
        if self.book is not None:
            try:
                sheet = self.get_sheet(sheet)
                cols = sheet.col_values(col_num)
            except(ValueError, IndexError):
                traceback.print_exc()
        return cols

    def get_row_index(self, sheet, col_num, name):
        '''
        获取行号
        :param sheet: sheet页名称
        :param col_num: 列号
        :param name: 需要确定的名称
        :return: 返回该参数的行号
        '''
        row_index = None
        cols = self.get_cols(sheet, col_num)
        if cols is not []:
            row_index = cols.index(name)
        return row_index

    def get_cell(self, sheet_name, row_num, col_num):
        '''
        获取单元格数据
        :param sheet_name: sheet页名称
        :param row_num: 行号
        :param col_num: 列号
        :return: 返回单元格数据
        '''
        cell_value = None
        if self.book is not None:
            try:
                sheet = self.book.sheet_by_name(sheet_name)
                cell_value = sheet.cell_value(row_num, col_num)
            except(ValueError, IndexError):
                print("请检查sheet名称或单元格地址")
                traceback.print_exc()
        return cell_value

    def get_all_cells(self, sheet_name, key_row=0, start_col=0):
        '''
        获取sheet页内所有的单元格数据，并存储为字典格式
        :param sheet_name: sheet页名称
        :param key_row: 设置为关键字的行数
        :param start_col: 列的起始列数
        :return: 返回sheet页所有单元格数据
        '''
        cells_list = []

        if self.book is not None:
            sheet = self.get_sheet(sheet_name)
            merge = []
            if sheet.merged_cells is not None:
                merge = sheet.merged_cells
            # merge = sheet.merged_cells
            try:
                row_key_name = sheet.row_values(key_row) #获取第一行数据作为dict的key
                for r in range(key_row+1, sheet.nrows):
                    cells = []
                    # cells = dict.fromkeys(row_key_name)
                    for c in range(start_col, sheet.ncols):
                        cell_value = sheet.row_values(r)[c]
                        if cell_value is None or cell_value == '':
                            for (rlow, rhigh, clow, chigh) in merge:
                                if rlow <= r < rhigh:
                                    if clow <= c < chigh:
                                        cell_value = sheet.cell_value(rlow, clow)
                                        break
                        cells.append(cell_value)
                    cell_dict = dict(zip(row_key_name, cells))
                    cells_list.append(cell_dict)

            except (ValueError, IndexError):
                print("请检查sheet名称或单元格地址")
                traceback.print_exc()
        return cells_list

    def get_all_cells_list(self, sheet_name, key_row=0, start_col=0):
        '''
        获取列表形式的excel数据
        :param sheet_name:
        :param key_row:
        :param start_col:
        :return:
        '''
        cells_list = []

        if self.book is not None:
            sheet = self.get_sheet(sheet_name)
            merge = []
            if sheet.merged_cells is not None:
                merge = sheet.merged_cells
            # merge = sheet.merged_cells
            try:
                row_key_name = sheet.row_values(key_row)  # 获取第一行数据作为dict的key
                for r in range(key_row + 1, sheet.nrows):
                    cells = []
                    # cells = dict.fromkeys(row_key_name)
                    for c in range(start_col, sheet.ncols):
                        cell_value = sheet.row_values(r)[c]
                        if cell_value is None or cell_value == '':
                            for (rlow, rhigh, clow, chigh) in merge:
                                if rlow <= r < rhigh:
                                    if clow <= c < chigh:
                                        cell_value = sheet.cell_value (rlow, clow)
                                        break
                        cells.append(cell_value)
                    # cell_dict = dict (zip (row_key_name, cells))
                    cells_list.append(cells)

            except (ValueError, IndexError):
                print("请检查sheet名称或单元格地址")
                traceback.print_exc()
        return cells_list


if __name__ == '__main__':

    pass

    # e = ExcelParser('test1.xlsx')
    # sheets = e.get_sheets()
    # print(sheets)
    # print(e.sheet_names())
    # jiekou = e.get_all_cells('aaa')
    # print(jiekou)
    # e = ExcelParser('test.xlsx')
    # print(e.sheet_names())
    # a = e.get_sheet('ccc')
    # print(e.get_all_cells('aaa'))
    # print(a.merged_cells)
    # wb = xlrd.open_workbook('test1.xlsx')
    # sheets = wb.sheet_names()
    # print(sheets)