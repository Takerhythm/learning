from socket import *
import re
import threading


def service(new_socket):
    recv_data = new_socket.recv(1024).decode("utf-8")
    if recv_data:
        recv_data_list = recv_data.splitlines()
        head_request = recv_data_list[0]
        file_name = re.match(r"[^/]+([^ ]*)", head_request).group(1)
        if file_name == "/":
            file_name = "/index.html"
        try:
            with open("./html"+file_name, "rb") as file:
                file_content = file.read()
        except:
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            response += "\r\n"
            response += "<h1>file not found</h1>"
            new_socket.send(response.encode("utf-8"))
            new_socket.close()
        else:
            response = "HTTP/1.1 200 OK\r\n"        
            response += "\r\n"
            new_socket.send(response.encode())    
            new_socket.send(file_content)
            new_socket.close()
    else:
        new_socket.close()

def main():
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_server_socket.bind(("", 8081))  
    tcp_server_socket.listen(128)
    while True:
        new_socket, client_address = tcp_server_socket.accept()
        t = threading.Thread(target=service, args=(new_socket,))
        t.start()
    tcp_server_socket.close()


if __name__ == "__main__":
    main()
