from socket import *
import select
import re


def server(new_client_socket, recv_data):
    request = re.match(r"[^/]+([^ ]*)", recv_data).group(1)
    if request == "/":
        request = "/index.html"
    try:
        with open("html"+request, "rb") as html:
           html_content = html.read()
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response = response.encode()
    else:
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Length:%d\r\n" % len(html_content)
        response += "\r\n"
        response = response.encode()+html_content
        # print(response)
    finally:
        new_client_socket.send(response)


def main():
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    # tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    epoll = select.epoll()
    epoll.register(tcp_server_socket.fileno(), select.EPOLLIN)
    tcp_server_socket.bind(("", 8081))
    tcp_server_socket.listen(128)
    fd_socket_dict = dict()
    while True:
        fd_event_list = epoll.poll()
        for fd, event in fd_event_list:
            if fd == tcp_server_socket.fileno():
                new_client_socket, client_address = tcp_server_socket.accept()
                epoll.register(new_client_socket.fileno(), select.EPOLLIN)
                fd_socket_dict[new_client_socket.fileno()] = new_client_socket
            elif event == select.EPOLLIN:
                recv_data = fd_socket_dict[fd].recv(1024).decode()
                if recv_data:
                    server(fd_socket_dict[fd], recv_data)
                else:
                    fd_socket_dict[fd].close()
                    del fd_socket_dict[fd]


if __name__ == "__main__":
    main()
