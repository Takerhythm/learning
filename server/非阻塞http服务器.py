from socket import *
import re
import time
def server(client_socket, recv_data):
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
        response += "Content-Length: %d\r\n" % len(html_content)
        response += "\r\n"
        response = response.encode()+html_content
    finally:
        client_socket.send(response)



def main():
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_server_socket.bind(("", 8081))
    tcp_server_socket.listen(128)
    tcp_server_socket.setblocking(False)
    socket_list = list()
    while True:
        print(socket_list)
        time.sleep(1)
        try:
            new_client_socket, client_address = tcp_server_socket.accept()
        except Exception as error:
            pass
        else:
            new_client_socket.setblocking(False)
            socket_list.append(new_client_socket)
        for client_socket in socket_list:
            try:
                recv_data = client_socket.recv(1024).decode()
            except Exception as error:
                pass
            else:
                if recv_data:
                    server(client_socket, recv_data)
                else:
                    client_socket.close()
                    socket_list.remove(client_socket)

if __name__ == "__main__":
    main()
