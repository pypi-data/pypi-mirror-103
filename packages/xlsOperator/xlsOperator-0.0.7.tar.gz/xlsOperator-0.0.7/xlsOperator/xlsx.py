import win32com
from win32com.client import Dispatch
import os
import numpy as np


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

class xlsxOperator :
    __path__ = os.getcwd() +'\\'
    __filename__ = ''

    def __init__(self):
        self.xlsxApp = win32com.client.Dispatch('Excel.Application')
        self.xlsxApp.Visible = False
        self.xlsxApp.DisplayAlerts = 0

    def setFile(self,namestr:str):
        self.__filename__ = namestr.split('\\').pop()
        if ":\\" not in namestr:
            self.workBook = self.xlsxApp.Workbooks.Open(self.__path__+'\\'+namestr,True)
        else :
            self.workBook = self.xlsxApp.Workbooks.Open(namestr,True)

    def setSheet(self,namestr):
        self.workSheet =self.workBook.Worksheets(namestr)

    def read(self,row,col):
        " The first cell's LOCATION is : (1,1) "
        return self.workSheet.Cells(row,col).Value

    def readline(self,row):
        result_list = []
        range = self.workSheet.UsedRange
        max_col = range.Columns.Count
        print(max_col)

        i = 0
        while i < max_col :
            result_list.append(self.workSheet.Cells(row,i+1).Value)
            i += 1
        return result_list

    def readcolumn(self,row):
        result_list = []
        range = self.workSheet.UsedRange
        max_row = range.Rows.Count
        print(max_row)

        i = 0
        while i < max_row :
            result_list.append(self.workSheet.Cells(i+1,row).Value)
            i += 1
        return result_list

    def write_data(self,data,row,col):
        '''
        In this function , you can write single data or list with 2 or fewer dimensions .
        在这个函数中，您可以写入单个数据或2维及以下的数组。
        :param data: str,number/[]/[[],[]]
        :return: void
        '''
        ROW = row
        COL = col

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
                    self.workSheet.Cells(trow,tcol + i).Value = item
                    i = i+1
            if (np.array(data).ndim == 2):
                k = 0
                print('[WRITING]more than 1 lines of data is writing. ')
                for item in data :
                    i = 0
                    for single in item :
                        self.workSheet.Cells(trow+k,tcol+i).Value = single
                        i = i+1
                    k = k+1
        else :
            self.workSheet.Cells(ROW,COL).Value = data


    def all_data(self):
        result_list = []
        range = self.workSheet.UsedRange
        max_row = range.Rows.Count
        print(max_row)

        i = 0
        while i < max_row :
            result_list.append(self.readline(i))
            i += 1
        return result_list


    def save(self,namestr=''):
        if namestr == '': # Save in original file
            self.workBook.Close(True)
            self.xlsxApp.quit()
        else :
            if ":\\" in namestr : # Absolute Path
                self.workBook.SaveAs(namestr)
                self.workBook.Close(False)
                self.xlsxApp.quit()
            else:   # Relative Path
                print(self.__path__+namestr)
                self.workBook.SaveAs(self.__path__+namestr)
                self.workBook.Close(False)
                self.xlsxApp.quit()

    def test(self):
        pass

