## **XLS operator @TreemanChou Documents**
###English Document
there's no english documents right now , It will be finished later .

###Simplified Chinese Document
###简 体 中 文 文 档
####一 XlsOperator简介
XlsOperator是一款用于读写xls/xlsx文件的库。在作者开发过程中，曾尝试使用xlwt与xlrd操作xls文件，使用openpyxl和pandas操作xlsx文件。但是操作过程中，他们均存在不同程度的问题。就xlrd而言，即要做到对同一文件的读写需要同时使用两种库；而openpyxl虽然在其他方面较为优秀，但在文件中包含图表并设置了图表附加元素时，使用openpyxl修改并保存后，会导致图标元素设置丢失。这给excel自动化流程造成了极大的不便。

为解决此问题，我将对xls文件和对xlsx文件的常用操作打包成此库xlsOperator. 它由两个文件组成，xls.py包含着操作xls的类xlsOperator , xlsx.py包含着操作xlsx文件的类xlsxOperator . 二者功能都比较简单，且拥有相同的方法名，可以非常简单地学习使用这两个库。

需要注意，本库仅将最基本的excel操作打包封装，并拥有一个能直接向excel写入单独元素/数组/二维数组的方法。如需使用设置格式、VBA、绘图等高级功能，请仍选择openpyxl、xlwt或win32com(pypiwin32).

####二 XlsOperator安装
在安装本库前，请确保您已经安装了 xlwt / xlrd / numpy / pypiwin32.
使用以下命令安装该库：

    pip install xlsOperator  

随后，在python中使用
>from xlsOperator import xls  
>from xlsoperator import xlsx

即可调用库中的两个py文件。

####三 初始化
使用以下以下语句创建类实例：
>testexcel = xls.xlsOperator()

或对于xlsx文件，使用：
>testexcel = xlsx.xlsxOperaotor()

其他函数名称、用法皆相同。使用以下方法设置文件及工作表:
>testexcel.setFile('xxxx.xxxx')  
>testexcel.setSheet('Sheetxxx')

####四 读取数据
共有三个与读取有关的方法。

【注意】在xlsOperator中，excel单元格坐标从(1,1)开始。您也可以使用(1,'A')方式定位单元格.
1. readline
   参数指定行数即可。
   >testexcel.readline(1)
2. readcolumn
   参数指定列数即可
   >testexcel.readcolumn(1)
3. all_data

这个函数不需要填入参数。其会返回一个二维list，里面是该Sheet全部表格内容。使用此方法提取出数据后可以轻易地使用Python本身的字符串处理等函数处理数据。  
>exceldate = testexcel.all_data()

####五 写入数据
共有一个写入有关的方法write_data(data,row,col)
三个参数分别是：要填入的数据data，要填入的行列坐标row和col。data可以是单一元素或一维、二位数组。当data是数组时，write_data方法会按照数组的行列排列向excel从起始位置由左到右，由上到下写入。
>data = 1  
>data = ['asd','sdf','sad','asd']  
>data = [['S','F'],['G','H']] 

比如，从表格最左上的单元格开始写入：
>testexcel.write_data(data,1,1)
####六 保存
>testexcel.save()

在xlsOperator中，使用save()方法会保存对源文件的修改。

在xlsxOperator中，save()方法可以不给参数，也可以给绝对路径或纯粹的文件名。

当参数未填写时，将直接保存对源文件的修改。

当参数为新的文件名时，将把修改后的文件另存为指定文件名，源文件不会被修改。

当参数为绝对路径时，文件将保存至指定路径。
