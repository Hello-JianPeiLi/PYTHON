# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/30 14:42
import time


def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read()
    return content


def center():
    with open('./templates/center.html', 'rb') as f:
        content = f.read()
    return content


def application(env, start_response):
    file_name = env['path_info']
    start_response('200 OK', [('Content-Type', 'text/html')])
    if file_name == '/index.py':
        return index()
    elif file_name == '/center.py':
        return center()
    elif file_name == '/register.py':
        return '---register.py---'
