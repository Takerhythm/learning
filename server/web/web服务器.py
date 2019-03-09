import socket
import re
import multiprocessing
import sys


class Server:
    def __init__(self, port, app, static_path):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(("", port))
        self.tcp_socket.listen(128)
        self.app = app
        self.static_path = static_path

    def server(self,new_socket):
        recv_data = new_socket.recv(1024).decode()        
        if recv_data:
            ret = re.match(r"[^/]+(/[^ ]*)", recv_data).group(1)
            if not ret.endswith(".html"):
                try:
                    print(self.static_path+ret)
                    with open(self.static_path+ret,"rb") as f:
                        content = f.read()
                except:
                    print("未找到文件")
                    response_body = "not found"
                    response_header = "HTTP/1.1 404 NOT FONUD\r\n"
                    response_header += "Content-Length:%d\r\n" % len(response_body)
                    response_header += "\r\n"
                    response = response_header + response_body
                    new_socket.send(response.encode())
                else:
                    response_body = content
                    response_header = "HTTP/1.1 200 OK\r\n"
                    response_header += "Content-Length:%d\r\n" % len(response_body)
                    response_header += "\r\n"
                    response = response_header.encode() + response_body
                    new_socket.send(response)
            else:
                env = dict()
                env["path"] = ret
                response_body = self.app(env, self.set_header)
                response_header = "HTTP/1.1 %s\r\n" % self.status
                for temp in self.header:
                    response_header += "%s:%s\r\n" %(temp[0], temp[1])
                #response_header += "Content-Length:%d\r\n" % len(response_body)
                response_header += "\r\n"
                response = response_header+ response_body
                new_socket.send(response.encode())
        else:
            new_socket.close()            

    def set_header(self, status, headers):
        self.status = status
        self.header = headers

    def run_forover(self):
        while True:
            new_socket,client_address = self.tcp_socket.accept()
            p = multiprocessing.Process(target=self.server, args=(new_socket,))
            p.start()
            new_socket.close()
        



def main():
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
            frame_app_name = sys.argv[2]
        except:
            print("端口错误")
            return
    else:
        print("请按照python3 web服务器.py port frame_name:app_name 方式输入")
        return
    ret = re.match(r"([^:]+):(.*)", frame_app_name)
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)
    else:      
        print("请按照python3 web服务器.py port frame_name:app_name 方式输入")
        return
    with open("./web服务器.cnf", "r") as f:
        cnf_info = eval(f.read())
    sys.path.append(cnf_info["dynamic_path"])
    frame = __import__(frame_name)
    app = getattr(frame, app_name)
    server = Server(port, app, cnf_info["static_path"])
    server.run_forover()


if __name__ == "__main__":
    main()
