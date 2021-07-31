# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/30 11:58
import socket
import multiprocessing
import re
from dynamic import mini_frame
import sys

"""添加配置文件"""


class WSGIServer:
    def __init__(self, port, app, static_path):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(("", port))
        self.tcp_socket.listen(128)
        self.application = app
        self.static = static_path

    def handle_new_socket(self, new_socket):
        request = new_socket.recv(1024)
        request_lines = request.decode('utf-8').splitlines()
        ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
        if ret:
            file_name = ret.group(1)
            print("-->>" * 10, file_name)
            if file_name == '/':
                file_name = '/index.html'
        if not file_name.endswith('.py'):
            try:
                f = open(self.static + file_name, 'rb')
                html_content = f.read()
                f.close()
            except:
                response_body = '<h1>你访问的页面不存在</h1>'
                response_header = 'HTTP/1.1 404 NOT FOUND PAGE\r\n'
                response_header += 'Content-Length:%d\r\n' % len(response_body)
                response_header += '\r\n'
                response = response_header.encode('utf-8') + response_body.encode('gbk')
                new_socket.send(response)
            else:
                response_body = html_content
                response_header = 'HTTP/1.1 200 OK\r\n'
                response_header += 'Content-Length:%d\r\n' % len(response_body)
                response_header += '\r\n'
                new_socket.send(response_header.encode('utf-8'))
                new_socket.send(html_content)
            new_socket.close()
        else:
            # 处理动态文件 .py
            env = dict()
            env['path_info'] = file_name
            response_body = self.application(env, self.set_status_header)
            response_header = 'HTTP/1.1 % s\r\n' % self.status

            for temp in self.header:
                response_header += '%s:%s\r\n' % (temp[0], temp[1])

            response_header += 'Content-Length:%d\r\n' % len(response_body)
            response_header += '\r\n'
            response = response_header.encode('utf-8') + response_body
            new_socket.send(response)

    def set_status_header(self, status, header):
        self.status = status
        self.header = header

    def run_server(self):
        while True:
            new_socket, tcp_client = self.tcp_socket.accept()
            m = multiprocessing.Process(target=self.handle_new_socket, args=(new_socket,))
            m.start()
        self.tcp_socket.close()


def main():
    """控制整体"""
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
            print('-------', port)
            frame_app_name = sys.argv[2]
            print(frame_app_name)
        except Exception as ret:
            print('端口输入错误...')
            return
    else:
        print('请按以下方式启动...')
        print('python3 xxx.py port frame:func')
        return
    ret = re.match(r'([^:]+):(.*)', 'mini_frame:application')
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)
    else:
        print('正则不存在')
        return

    with open('./web_server.conf', 'rb') as f:
        conf_info = eval(f.read())

    sys.path.append('./dynamic')
    frame = __import__(frame_name)

    app = getattr(frame, app_name)
    se = WSGIServer(port, app, conf_info['static_path'])
    se.run_server()


if __name__ == '__main__':
    main()
