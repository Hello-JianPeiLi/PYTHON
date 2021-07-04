import socket
import threading


def recv_msg(udp_socket):
    while True:
        recv_data = udp_socket.recvfrom(1024)
        print("收到--%s--发的内容->%s " % (recv_data[1], recv_data[0].decode("utf-8")))


def send_data(udp_socket, dest_ip, dest_port):
    while True:
        send_msg = input("请输入发送的内容")
        udp_socket.sendto(send_msg.encode("utf-8"), (dest_ip, dest_port))


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest_ip = input("请输入要发送的ip")
    dest_port = int(input("请输入要绑定的port"))

    t1 = threading.Thread(target=send_data, args=(udp_socket, dest_ip, dest_port))
    t2 = threading.Thread(target=recv_msg, args=(udp_socket,))

    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
