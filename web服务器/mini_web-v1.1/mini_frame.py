# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/30 14:42
import time


def application(env, start_response):
    file_name = env['path_info']
    start_response('200 OK', [('Content-Type', 'text/html')])
    if file_name == '/index.py':
        return '---login---.py---%s' % time.time()
    elif file_name == '/login.py':
        return '---login.py---'
    elif file_name == '/register.py':
        return '---register.py---'
