import socket
import time
import ast

class SendMsg(object):
    def __init__(self):
        pass

    def pack(self, msg):
        msg = '§§START§§' + str(msg) + '§§END§§'
        data = msg.encode()
        return data

    def unpack(self, data):
        #print(data)
        data = data.decode().split('§§START§§')[1].split('§§END§§')[0]
        msg = ast.literal_eval(data)
        return msg

    def send_to_server(self, msg):
        host = '192.168.110.244'
        port = 10000
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(self.pack(msg))
        s.close()

    def send_to_client(self, host, port, msg):
        port = int(port)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(self.pack(msg))
        s.close()
    
    def sendall(self, msg, data):
        time.sleep(3)
        host = msg['ip']
        port = int(msg['port'])
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(data)
        s.close()

    def answer_msg(self, msg):
        host = msg['ip']
        port = int(msg['port'])
        print(host, port)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(self.pack(msg))
        s.close()

    def send_to_client_list(self, msg, client_list):
        for client in client_list:
            host = client[0]
            port = client[1]
            self.send_to_client(host, port, msg)

if __name__ == '__main__':
    sm = SendMsg()
    msg = {'ip': "127.0.0.1",
            'port':10000,
            'timestamp': 'now',
            }
    
    data = sm.pack(msg)
    print(data)
    msg = sm.unpack(data)
    print(msg)
    print(type(msg))

