# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/13 17:09
import socket
import re
import multiprocessing
import threading
from gevent import monkey
import gevent

monkey.patch_all()


def handle_new_socket(new_socket):
    request = new_socket.recv(1024)
    request_lines = request.decode('utf-8').splitlines()
    ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
    if ret:
        file_name = ret.group(1)
        print("-->>" * 10, file_name)
        if file_name == '/':
            file_name = '/index.html'

    try:
        f = open('./html' + file_name, 'rb')
        html_content = f.read()
        f.close()
    except:
        response = 'HTTP/1.1 404 NOT FOUND PAGE\r\n'
        response += '\r\n'
        response += '<h1>你访问的页面不存在</h1>'
        new_socket.send(response.encode('utf-8'))
    else:
        response = 'HTTP/1.1 200 OK\r\n'
        response += '\r\n'
        new_socket.send(response.encode('utf-8'))
        new_socket.send(html_content)

    new_socket.close()


def mian():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcp_socket.bind(("", 7890))
    tcp_socket.listen(128)
    print("---等待客户端连接---")
    while True:
        new_socket, client_addr = tcp_socket.accept()
        gevent.spawn(handle_new_socket, new_socket)


if __name__ == '__main__':
    mian()
