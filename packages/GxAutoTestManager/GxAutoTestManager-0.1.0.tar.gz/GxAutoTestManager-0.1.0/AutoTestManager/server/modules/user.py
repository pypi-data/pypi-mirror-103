import socket
import threading
import time
import sendmsg
from getopt import getopt

class CmdClient(object):
    def __init__(self, msg):
        self.msg = msg
        self.udp_host = '127.0.0.1'
        self.udp_port = 28888
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.sm = sendmsg.SendMsg()

    def bind_tcp(self, host = '', port = ''):
        host = '127.0.0.1'
        #host = '192.168.111.97'
        port = 28002
        #port = 10001
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((host,port))

    def send_tcp(self, msg):
        self.s.send(msg)

    def recv_msg(self):
        port = 27000
        host = ''
        msg = ''.encode()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(30)
        sock, addr = s.accept()
        while True:
            data = sock.recv(1024)
            if data.find('§§START§§'.encode()) >= 0:
                start = 1
            if start:
                msg += data
                if msg.find('§§END§§'.encode()) >= 0:
                    start = 0
                    end = 1
            if end:
                msg = self.sm.unpack(msg)
                break
        print(msg)



    def close_tcp(self):
        self.s.close()

    def bind_udp(self):
        self.u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_udp(self, msg):
        msg = str(msg).encode()
        self.u.sendto(msg, (self.udp_host, self.udp_port))

    def send_heart(self):
        now = time.strftime(self.time_format, time.localtime())
        msg = {
                'host': "127.0.0.1",
                'port':10000,
                #'board_name':'kaoji1-1_gx6605s_1',
                'timestamp': now,
                }
        self.send_udp(msg)

    def start(self):
        self.bind_udp()
        self.bind_tcp()
        t = threading.Thread(target = self.recv_msg)
        t.setDaemon(True)
        t.start()
        self.send_tcp(self.sm.pack(self.msg))
        self.close_tcp()
        #@while True:
        i = 0
        while i < 9:
            print(11111111)
            self.send_heart()
            time.sleep(1)
            i += 1

if __name__ == '__main__':
    message = {
        "host":"",
        "port":"",
        "client_name":"", 
        "jenkins_name":"",
        "jenkins_build":"",
        "type":"",
        "name":"",
        "message_content":{},
    }
    content = {
        "dvb_ai":"", # 必填
        "dvb_info":{
            "bin_info":{ # 必填
                "bin_url":"", # 必填
                "jenkins_project_name":"",
                "jenkins_build_id":"",
                "arch":"",
                "chip":"",
                "board":"6605s", # 必填
                "os":"ecos",
                },
            "signal":"",
            "gerrit_info":{ # 可选
                "gerrit_id":"",
                "gerrit_patch":"",
                },
            "testlink_info":{ # 可选
                "testlink_project":"",
                "testlink_plan":"",
                "testlink_build":"",
                },
            "specific_board_info":{ # 可选，指定使用某块板子进行测试
                "client_ip":"",
                "board_name":"",
                },
            },
    "ai_info":{ # 预留
        "reserved":"",
        },
    }
    message['type'] = 'task'
    message['name'] = 'start'
    message['message_content'] = content
    cc = CmdClient(message)
    cc.start()
