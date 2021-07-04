import socket


def recv_msg(udp_socket):
    recv_data = udp_socket.recvfrom(1024)
    print("%s发过来的---%s" % (recv_data[1][0], recv_data[0].decode('utf-8')))


def send_data(udp_socket):
    # 10.211.55.3:8080
    dest_ip = input("请输入ip")
    dest_port = int(input("请输入port"))
    dest_data = input("请输入要发送的内容")
    udp_socket.sendto(dest_data.encode('utf-8'), (dest_ip, dest_port))


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 7788))
    while True:
        print("---xx聊天系统---")
        print("1---发送信息")
        print("2---接受信息")
        print("0---退出程序")
        ob = input("请输入相应的功能")
        if ob == "1":
            send_data(udp_socket)
        elif ob == "2":
            recv_msg(udp_socket)
        else:
            print("请输入正确的数")
            print("请输入正确的数")


if __name__ == '__main__':
    main()
