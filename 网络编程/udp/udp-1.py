import socket


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        send_data = input('请发送内容：')
        if send_data == 'exit':
            break
        udp_socket.sendto(send_data.encode('utf-8'), ("10.211.55.3", 8080))

    udp_socket.close()


if __name__ == '__main__':
    main()
