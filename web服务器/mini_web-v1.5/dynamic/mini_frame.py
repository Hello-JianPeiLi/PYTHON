# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/30 14:42
import time

URL_FUNC_DICT = dict()


def route(path):
    def set_func(func):
        # URL_FUNC_DICT['/index.py'] = index
        URL_FUNC_DICT[path] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)

        return call_func

    return set_func


@route('/index.py')
def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read()
    return content


@route('/center.py')
def center():
    with open('./templates/center.html', 'rb') as f:
        content = f.read()
    return content


# URL_FUNC_DICT = {
#     '/index.py': index,
#     '/center.py': center
# }


def application(env, start_response):
    file_name = env['path_info']
    start_response('200 OK', [('Content-Type', 'text/html')])
    # if file_name == '/index.py':
    #     return index()
    # elif file_name == '/center.py':
    #     return center()
    # elif file_name == '/register.py':
    #     return '---register.py---'
    try:
        return URL_FUNC_DICT[file_name]()
    except Exception as ret:
        return '产生了异常---%s' % str(ret)
