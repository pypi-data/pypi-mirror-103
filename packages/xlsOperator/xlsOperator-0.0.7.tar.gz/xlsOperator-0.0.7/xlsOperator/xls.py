import xlrd
import xlwt
import numpy as np
from xlutils.copy import copy
from xlrd import xldate_as_datetime


def typeof(variate):
    type1 = ''
    if type(variate) == type(1):
        type1 = "int"
    elif type(variate) == type("str"):
        type1 = "str"
    elif type(variate) == type(12.3):
        type1 = "float"
    elif type(variate) == type([1]):
        type1 = "list"
    elif type(variate) == type(()):
        type1 = "tuple"
    elif type(variate) == type({"key1": "123"}):
        type1 = "dict"
    elif type(variate) == type({"key1"}):
        type1 = "set"
    return type1

class xlsOperator :
    __reader__ = xlrd.Book
    __rsheet__ = xlrd.sheet
    __writer__ = xlwt.Workbook
    __wsheet__ = xlwt.Worksheet
    filename = ''
    sheetname = ''
    sheet = None
    def info(self):
        return " Hi . This is a xls operator lib made by @TreemanChou . "

    def setFile(self,namestr):
        self.filename = namestr
        self.__reader__ = xlrd.open_workbook(self.filename)
        self.__writer__ = copy(self.__reader__)

    def setSheet(self,namestr):
        self.sheetname = namestr
        self.__rsheet__ = self.__reader__.sheet_by_name(self.sheetname)
        if not self.__reader__.sheet_loaded(self.sheetname):
            print("======[Failed to load "+self.sheetname+"!]=======")
        self.__wsheet__ = self.__writer__.get_sheet(self.sheetname)
        # print(self.__writer__)

    def readline(self,row):
        return self.__rsheet__.row_values(row)


    def readcolumn(self,col):
        return self.__rsheet__.col_values(col)


    def write_data(self,data,row,col):
        '''
        In this function , you can write single data or list with 2 or fewer dimensions .
        在这个函数中，您可以写入单个数据或2维及以下的数组。
        :param data: str,number/[]/[[],[]]
        :return: void
        '''
        trow = row
        tcol = col
        datatype = typeof(data)
        print(datatype)
        i = 0
        k = 0
        if datatype == 'list' :
            if (np.array(data).ndim == 1):
                print('[WRITING]1 lines of data is writing.')
                for item in data :
                    self.__wsheet__.write(trow,tcol + i,item)
                    i = i+1
            if (np.array(data).ndim == 2):
                k = 0
                print('[WRITING]more than 1 lines of data is writing. ')
                for item in data :
                    i = 0
                    for single in item :
                        self.__wsheet__.write(trow+k,tcol+i,single)
                        i = i+1
                    k = k+1
        else :
            self.__wsheet__.write(trow,tcol,data)

    def all_data(self):
        result_list = []
        rows = self.__rsheet__.nrows
        i = 0
        while i < rows :
            result_list.append(self.readline(i))
            i = i + 1
        return result_list

    def save(self):
        str = self.filename.split('/').pop()
        # print(str)
        self.__writer__.save(self.filename)
        self.__del__()

    def test(self):
        self.setFile("D:\\test.xls")
        self.setSheet("Sheet1")
        c = self.all_data()
        print(c)

    def __del__(self):
        print("Destroyed.\n")
