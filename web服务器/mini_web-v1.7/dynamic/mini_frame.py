# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/30 14:42
import re
import time
from pymysql import connect

URL_FUNC_DICT = dict()


def route(path):
    """路由装饰器"""

    def set_func(func):
        # URL_FUNC_DICT['/index.py'] = index
        URL_FUNC_DICT[path] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        return call_func

    return set_func


@route(r'/add/(\d+)\.html')
def add_focus(ret):
    # 1. 获取股票代码
    stock_code = ret.group(1)
    # 2. 判断是否有这个股票代码
    conn = connect(host='localhost', port=3306, user='root', password='te666666', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = """SELECT * FROM info WHERE code = %s"""
    cs.execute(sql, stock_code)
    stock_info = cs.fetchone()
    if not stock_info:
        cs.close()
        conn.close()
        return '大哥，我们是创业公司，还请手下留情。。。。'
    # 3. 判断是否已经关注过
    sql = """SELECT * FROM info AS i JOIN focus AS f ON i.id = f.info_id WHERE i.code = %s;"""
    cs.execute(sql, stock_code)
    if cs.fetchone():
        return "您已经关注过该股票(%s)" % stock_code
    sql = """INSERT INTO focus (info_id) SELECT id FROM info WHERE CODE = %s"""
    cs.execute(sql, stock_code)
    conn.commit()
    cs.close()
    conn.close()
    return '关注[%s]ok...' % stock_code


@route('/index.html')
def index(ret):
    with open('./templates/index.html') as f:
        content = f.read()
    conn = connect(host='localhost', port=3306, user='root', password='te666666', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = """select * from info;"""
    cs.execute(sql)
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()
    tr_template = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>
        </tr>
    """
    html = ''
    for line_info in stock_infos:
        html += tr_template % (
            line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6],
            line_info[7], line_info[1])
    content = re.sub(r'\{%content%\}', html, content)
    return content


@route('/center.html')
def center(ret):
    with open('./templates/center.html') as f:
        content = f.read()
    conn = connect(host='localhost', port=3306, user='root', password='te666666', database='stock_db', charset='utf8')
    cs = conn.cursor()
    sql = """
        SELECT i.code, i.short, i.chg, i.turnover, i.price, i.highs, f.note_info FROM info as i JOIN focus as f ON i.id = f.info_id;
    """
    cs.execute(sql)
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    tr_template = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td style="color:red">%s</td>
            <td></td>
            <td>del</td>
        </tr>
    """
    html = ''
    for line_info in stock_infos:
        html += tr_template % (
            line_info[0], line_info[1], line_info[2], line_info[3], line_info[4], line_info[5], line_info[6])
    content = re.sub(r'\{%content%\}', html, content)
    return content


# URL_FUNC_DICT = {
#     '/index.py': index,
#     '/center.py': center
# }


def application(env, start_response):
    file_name = env['PATH_INFO']
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8;')])
    # if file_name == '/index.py':
    #     return index()
    # elif file_name == '/center.py':
    #     return center()
    # elif file_name == '/register.py':
    #     return '---register.py---'
    try:
        for url, func in URL_FUNC_DICT.items():
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            return "请求的url(%s)没有对应的函数...." % file_name
    except Exception as ret:
        return '产生了异常---%s' % str(ret)
