# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/14 11:05


"""epoll window用不了 只能在Linux 和 Unix"""
import socket
import time
import select
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

    # 创建一个epoll对象
    epl = select.epoll()
    # 将监听套接字对应的fd注册到epoll中
    print("=------》》》》", tcp_socket.fileno())
    epl.register(tcp_socket.fileno(), select.EPOLLIN)

    fd_event_dict = dict()
    while True:
        # 默认会堵塞，知道os监测到数据到来通过事件通知方式告诉这个程序，此时才会解堵塞
        fd_event_list = epl.poll()
        # [(fd, event), (套接字对应的文件描述符， 这个文件描述符到底是什么事件，例如 可以条用recv接受等)]
        for fd, event in fd_event_list:
            # 等待新客户端的连接
            if fd == tcp_socket.fileno():
                tcp_client_socket, client_addr = tcp_socket.accept()
                epl.register(tcp_client_socket.fileno(), select.EPOLLIN)
                fd_event_dict[tcp_client_socket.fileno()] = tcp_client_socket
            elif event == select.EPOLLIN:
                # 判断已经连接的客户端是否有数据发送过来
                recv_data = fd_event_dict[fd].recv(1024).decode('utf-8')
                if recv_data:
                    handle_client_socket(fd_event_dict[fd], recv_data)
                else:
                    fd_event_dict[fd].close()
                    epl.unregister(fd_event_dict[fd])
                    del fd_event_dict[fd]


if __name__ == '__main__':
    main()
