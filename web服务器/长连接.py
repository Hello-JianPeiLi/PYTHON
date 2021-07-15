# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/14 11:05

import socket
import time
import re


def handle_client_socket(client_socket, request):
    request_lines = request.splitlines()
    ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
    if ret:
        file_name = ret.group(1)
        if file_name == '/':
            file_name = '/index.html'
        print(">" * 20, file_name)
    try:
        f = open('./html' + file_name, 'rb')
    except Exception as EC:
        print(EC)
        response_body = '<h1>-----NOT FOUND PAGE-----</h1>'
        response_header = 'HTTP/1.1 404 NOT FOUND\r\n'
        response_header += 'Content-Length:%d\r\n' % len(response_body.encode('utf-8'))
        response_header += '\r\n'
        response = response_header + response_body
        client_socket.send(response.encode('utf-8'))
    else:
        html_content = f.read()
        f.close()
        response_body = html_content
        response_header = 'HTTP/1.1 200 OK\r\n'
        response_header += 'Content-Length:%d\r\n' % len(response_body)
        response_header += '\r\n'
        response = response_header.encode('utf-8') + response_body
        print(response_header.encode('utf-8'))
        client_socket.send(response)
        # client_socket.send(html_content)


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", 7890))
    tcp_socket.listen(128)
    tcp_socket.setblocking(False)

    client_socket_list = list()
    while True:
        try:
            tcp_client_socket, client_addr = tcp_socket.accept()
        except Exception as ret:
            # print("-----没有新的客户端到来-----")
            pass
        else:
            tcp_client_socket.setblocking(False)
            client_socket_list.append(tcp_client_socket)
            # print("-----有新的客户端到来-----")

        for client_socket in client_socket_list:
            try:
                recv_data = client_socket.recv(1024).decode('utf-8')
            except Exception as ret:
                # print("-----没有数据到来-----")
                pass
            else:
                if recv_data:
                    handle_client_socket(client_socket, recv_data)
                    # print("-----收到数据-----")
                else:
                    client_socket.close()
                    client_socket_list.remove(client_socket)


if __name__ == '__main__':
    main()
