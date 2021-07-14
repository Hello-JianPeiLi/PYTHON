import socket
import time


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setblocking(False)
    tcp_socket.bind(("", 7890))
    tcp_socket.listen(128)

    new_socket_list = list()

    while True:
        time.sleep(1)
        try:
            new_socket, client_addr = tcp_socket.accept()
        except Exception as ret:
            print("-----没有新客户端到来-----")
        else:
            new_socket.setblocking(False)
            new_socket_list.append(new_socket)
            print("-----没产生异常，就代表有新的客户端到来有新的客户端到来-----")
        for client_socket in new_socket_list:
            try:
                recv_data = client_socket.recv(1024)
            except:
                print("-----没有收到数据-----")
            else:
                if recv_data:
                    print("客户端发来了数据")
                    print(recv_data)
                else:
                    client_socket.close()
                    new_socket_list.remove(client_socket)


if __name__ == '__main__':
    main()
