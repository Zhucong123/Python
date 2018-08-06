import os
import shutil
import uuid

import xlrd

import pymssql


# 读取excel
def read_excel():

    # 打开基础数据模板 （参数是路径）
    ExcelFile = xlrd.open_workbook(
        r"C:/Users/localhost/Desktop/邓文婷数据/兰卫（LQMS文件管理）基础数据模板_陈莹.xlsx")

    # 打卡excel的sheet子页（参数是sheet名字）
    sheet = ExcelFile.sheet_by_name("文件管理")
    parse_excel_data(sheet)

# 解析excel数据，单行格式化成字典


def parse_excel_data(sheet):
    dic_row_data = {}
    for row in range(sheet.nrows):
        if(row == 0 or row == 1):
            continue
        dic_row_data["FileType"] = sheet.cell_value(row, 0)  # 文件类别
        dic_row_data["FileName"] = sheet.cell_value(row, 1)  # 文件名称
        dic_row_data["EffectDate"] = sheet.cell_value(row, 3)  # 生效日期
        dic_row_data["CreateDate"] = sheet.cell_value(row, 3)  # 创建日期
        dic_row_data["ApplyDeptName"] = sheet.cell_value(row, 5)  # 申请部门
        dic_row_data["CreateUserName"] = sheet.cell_value(row, 6)  # 申请人（创建人）
        # dic_row_data["ApplyTypeId"]=1   #申请类别（默认为新增）
        # dic_row_data["ApplyRemarkId"]=1 #申请原因（默认新增）
        dic_row_data["FileNo"] = sheet.cell_value(row, 9)  # 文件编号
        dic_row_data["FileVersion"] = sheet.cell_value(row, 10)  # 文件版本号
        # dic_row_data["Level"]=5 #保密级别
        dic_row_data["ApproverUserName"] = sheet.cell_value(row, 15)  # 审核人
        dic_row_data["AuditUserName"] = sheet.cell_value(row, 17)  # 审批人
        # +str(dic_row_data["FileType"])+"/"

        # 原文件所在路径
        FolderPath = "C:/Users/localhost/Desktop/邓文婷数据/文件/"
        FilePath = search(FolderPath, dic_row_data["FileName"])
        if FilePath is not None:
            # print (FilePath)
            dic_row_data["FileContent"] = str(uuid.uuid1()).replace(
                "-", "").upper()+os.path.splitext(os.path.basename(FilePath))[1]
            dic_row_data["FilePath"] = FilePath

        con = pymssql.connect(host='.', user='sa',
                              password='123456', database='LQMS')
        cur = con.cursor()
        sql = "select * from dbo.FileModel where FileName='%s'"
        cur.execute(sql % dic_row_data["FileName"])
        result = cur.fetchall()
        if len(result) <= 0:
            exce_proc(dic_row_data)
            # 移动文件
            move_File(dic_row_data)


# 执行存储过程
def exce_proc(dic_row_data):
    # 先插入数据
    # 数据库主外键不完全，先保留
    try:
        # 数据库配置
        con = pymssql.connect(host='.', user='sa',
                              password='123456', database='LQMS')
        cur = con.cursor()
        sql = "exec InputExcelData "
        for dic_row in dic_row_data.keys():
            if dic_row != "FilePath":
                sql = sql+"@"+dic_row+"='%("+dic_row+")s',"
        curs = cur.execute((sql[:-1] % dic_row_data))
        con.commit()
        con.close()
    except:

        # 错误日志路径
        fo = open("C:/Users/localhost/Desktop/debug.txt", "w")
        print(bytes(sql, encoding="utf8"))
        fo.writelines(dic_row_data)
        fo.close()


# 移动文件
def move_File(dic_row_data):

    # 将改名的文件移动到指定路径下面
    basePath = "C:/Users/localhost/Desktop/doc/"
    oldFilePath = dic_row_data["FilePath"]  # 原文件位置
    newFilePath = basePath+dic_row_data["FileContent"]  # 移动到
    print(oldFilePath)
    print(newFilePath)
    print("*"*100)
    shutil.copyfile(oldFilePath, newFilePath)



# 递归遍历文件夹
def search(Path, name):
    for filename in os.listdir(Path):
        fp = os.path.join(Path, filename)
        if os.path.isfile(fp) and name in filename:
            if fp is not None and fp != "None":
                return fp
        elif os.path.isdir(fp):
            FilePath = search(fp, name)
            if FilePath is not None and FilePath != "None":
                return FilePath


if __name__ == "__main__":
    read_excel()
