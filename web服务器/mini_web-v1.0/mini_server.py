import socket
import re
import multiprocessing
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
                response_header += 'Content-Type:text/html; charset=utf-8;\r\n'
                response_header += '\r\n'
                response = response_header + response_body
                new_socket.send(response.encode('utf-8'))
            else:
                response_body = html_content
                response_header = 'HTTP/1.1 200 OK\r\n'
                response_header += 'Content-Length:%d\r\n' % len(response_body)
                response_header += '\r\n'
                response = response_header.encode('utf-8') + response_body
                new_socket.send(response)
        else:
            env = dict()
            env['path_info'] = file_name
            print(env)
            body = mini_frame.application(env, self.set_status_header)
            header = 'HTTP/1.1 %s\r\n' % self.status
            for temp in self.headers:
                header += '%s:%s\r\n' % (temp[0], temp[1])
            header += '\r\n'
            response = header + body
            new_socket.send(response.encode('utf-8'))
        new_socket.close()

    def set_status_header(self, status, header):
        self.status = status
        self.headers = [('Server-Version', 'django3.2.3')]
        self.headers += header

    def run_server(self):
        while True:
            new_socket, client_addr = self.tcp_socket.accept()
            p = multiprocessing.Process(target=self.handle_new_socket, args=(new_socket,))
            p.start()


if __name__ == '__main__':
    se = WSGIServer()
    se.run_server()
