from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.core.cache import cache


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # 获取本来应该返回的exception的response

    if response is not None:
        response.data['status_code'] = response.status_code  # 可添加status_code
        # response.data['error_code'] = 1
        try:
            response.data["message"] = response.data['detail']  # 增加message这个key
            del response.data['detail']
        except:
            pass
    if response is None:
        return HttpResponse("禁止单独测试接口")

    return response


class myException422(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


def jwt_response_username_userid_token(token, user=None, request=None):
    """
    自定义验证成功后的返回数据处理函数
    :param token:
    :param user:
    :param request:
    :return:
    """

    if user.check == 0:
        data = {
            # jwt令牌
            'status_code': 200,
            "message":"等待管理员审核账号"
        }
    else:
        data = {
            # jwt令牌
            'status_code': 200,
            'token': token,
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        }

    return data





import xlwt,datetime
from xlwt import *

import os
# 写入excel文件函数
def wite_to_excel(name,head_data,records):
    #获取时间戳
    timestr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 工作表
    wbk = xlwt.Workbook()
    sheet1 = wbk.add_sheet('sheet1',cell_overwrite_ok=True)

    #写入表头
    for filed in range(0,len(head_data)):
        sheet1.write(0,filed,head_data[filed],excel_head_style())


    #写入数据记录
    for row in range(1,len(records)+1):

        for col in range(0,len(head_data)):
            sheet1.write(row,col,records[row-1][col],excel_record_style())
            #设置默认单元格宽度
            sheet1.col(col).width = 256*15

    cur_path = os.path.abspath('.')
    # 设置生成文件所在路径
    download_url = cur_path + '/media/download/'

    wbk.save(download_url+name+'-'+timestr+'.xls')
    return '/media/download/' + name +'-'+timestr+'.xls'

# 定义导出文件表头格式
def excel_head_style():
    # 创建一个样式
    style = XFStyle()
    #设置背景色
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['light_green']  # 设置单元格背景色
    style.pattern = pattern


    # 设置字体
    # font0 = xlwt.Font()
    # font0.name = u'微软雅黑'
    # font0.bold = True
    # font0.colour_index = 0
    # font0.height = 240
    # style.font = font0
    #设置文字位置
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    style.alignment = alignment
    # 设置边框
    borders = xlwt.Borders()  # Create borders
    borders.left = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.right = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.top = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.bottom = xlwt.Borders.THIN  # 添加边框-虚线边框
    style.borders = borders



    return style

# 定义导出文件记录格式
def excel_record_style():
    # 创建一个样式
    style = XFStyle()
    #设置字体
    font0 = xlwt.Font()
    font0.name = u'微软雅黑'
    font0.bold = False
    font0.colour_index = 0
    font0.height = 200
    style.font = font0
    #设置文字位置
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    style.alignment = alignment
    # 设置边框
    borders = xlwt.Borders()  # Create borders
    borders.left = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.right = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.top = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.bottom = xlwt.Borders.THIN  # 添加边框-虚线边框
    style.borders = borders

    return style
