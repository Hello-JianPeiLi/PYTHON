# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/30 11:58
import socket
import multiprocessing
import re
import mini_frame


class WSGIServer:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(("", 7890))
        self.tcp_socket.listen(128)

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
                f = open('../html' + file_name, 'rb')
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
            env = dict()
            env['path_info'] = file_name
            response_body = mini_frame.application(env, self.set_status_header)
            response_header = 'HTTP/1.1 % s\r\n' % self.status

            for temp in self.header:
                response_header += '%s:%s\r\n' % (temp[0], temp[1])

            response_header += 'Content-Length:%d\r\n' % len(response_body)
            response_header += '\r\n'
            response = response_header + response_body
            new_socket.send(response.encode('utf-8'))

    def set_status_header(self, status, header):
        self.status = status
        self.header = header

    def run_server(self):
        while True:
            new_socket, tcp_client = self.tcp_socket.accept()
            m = multiprocessing.Process(target=self.handle_new_socket, args=(new_socket,))
            m.start()
        self.tcp_socket.close()


if __name__ == '__main__':
    se = WSGIServer()
    se.run_server()
