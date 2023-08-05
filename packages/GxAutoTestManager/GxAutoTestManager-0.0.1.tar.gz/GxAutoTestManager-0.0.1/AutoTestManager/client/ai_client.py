# -*- coding: utf-8 -*-

import socket
import time
import sys
import threading 
import json
import os
import multiprocessing
sys.path.append('../server/modules')
import log
import ftp
import msg
import sendmsg

class AiClient(object):
    def __init__(self):
        self.rl = log.RunningLog()
        self.local_host = '192.168.111.101'
        self.local_port = '29999'
        self.sm = sendmsg.SendMsg()
        self.gm = msg.GenMsg()
        self.test_entrance = 'Test_Entrance'

    def tcp_bind(self):
        ip = ''
        port = int(self.local_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen(30)
        return s

    def recv_msg(self, sock, addr):
        msg = ''.encode()
        start = 0
        end = 0
        buffer_size = 4096
        while True:
            data = sock.recv(buffer_size)
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
        sock.close()
        return msg

    def process_msg(self):
        tfd = self.tcp_bind()
        print(tfd)
        while True:
            sock, addr = tfd.accept()
            print(sock, addr)
            msg = self.recv_msg(sock, addr)
            self.msg_handler(msg)

    def _uploadfile(self, local_bin = '', bin_url = '', jenkins_name = '', jenkins_build = '',\
            board = '', dvb = 'dvb', now = ''):
        if local_bin:
            fl = ftp.FtpFunctionLib(\
                    Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
                    FtpLoginBasicPath= './' + dvb, LoginPort = 2121)
            ret = fl.FtpLogin()
            print(ret)
            if not jenkins_name:
                jenkins_name = 'no_jenkins'
            if not jenkins_build:
                jenkins_build = 'no_build'
            if bin_url:
                remote_path = os.path.dirname(bin_url)
                remote_bin = os.path.dirname(bin_url) + '/' + now + '_' + \
                        os.path.basename(bin_url)
            else:
                #remote_path = jenkins_name + '/' + jenkins_build + '/' +  board 
                #remote_bin = remote_path + '/' + now + '_' + os.path.basename(local_bin)
                remote_path = 'Test_Entrance'
                remote_bin = remote_path + '/' + os.path.basename(local_bin)
            fl.Mkdirs(remote_path)
            fl.UploadFile(local_bin, remote_bin)
            fl.FtpQuit()
            bin_url = dvb + '/'  + remote_bin
        return bin_url

    def _movefile(self, bin_url = '', move_url = ''):
        fl = ftp.FtpFunctionLib(\
                Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
                FtpLoginBasicPath= './', LoginPort = 2121)
        ret = fl.FtpLogin()
        print(ret)
        new_name = os.path.dirname(bin_url) + '/' + os.path.basename(bin_url).split('@@')[-1]
        fl.RenameFile(bin_url, new_name)
        fl.MoveFile(new_name, move_url)
        #fl.RenameFile(new_name, bin_url)
        fl.FtpQuit()

    def _renamefile(self):
        fl = ftp.FtpFunctionLib(\
                Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
                FtpLoginBasicPath= './',  LoginPort = 2121)
        ret = fl.FtpLogin()
        print(ret)
        local_file = '[STOP]'
        os.system('touch a.txt')
        remote_path = 'Test_Entrance'
        remote_bin = remote_path + '/' + local_file
        fl.Mkdirs(remote_path)
        fl.UploadFile('a.txt', remote_bin)
        fl.FtpQuit()
        os.system('rm "' + local_file + '"')

    def _download(self, remote_path):
        fl = ftp.FtpFunctionLib(\
                Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
                FtpLoginBasicPath= './',  LoginPort = 2121)
        ret = fl.FtpLogin()
        local_path = os.path.basename(remote_path)
        fl.DownloadFile(remote_path, local_path)
        fl.FtpQuit()
        return local_path
        

    def start_test(self, msg):
        bin_url = msg['message_content']['ai_info']['task_info']['bin_url']
        #move_url = self.test_entrance + '/' + os.path.basename(bin_url).split('@@')[-1]
        #self._movefile(bin_url, move_url)
        self._movefile(bin_url, self.test_entrance)

    def stop_test(self, msg):
        self._renamefile()

    def _find_result(self, task_bin):
        fl = ftp.FtpFunctionLib(\
                Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
                FtpLoginBasicPath= './',  LoginPort = 2121)
        ret = fl.FtpLogin()
        file_list = fl.QueryRemoteFileList('./Test_Entrance/history')
        print(file_list)
        result_path = None
        excel_list = []
        for i in file_list:
            if i.endswith(task_bin):
                result_path = './Test_Entrance/history/' + i + '/' + i
                print('>>>>>>>>>>>>>>>')
                print(result_path)
                excel_list = fl.QueryRemoteFileList(result_path)
                print(excel_list)
                print('>>>>>>>>>>>>>>>')
                break
        for i in excel_list:
            if i.endswith('xlsx'):
                result_path += '/' + i
        fl.FtpQuit()
        return result_path

    def get_test_result(self, msg):
        print('>>>>>>>>>>>>>')
        print(msg)
        print('>>>>>>>>>>>>>')
        task_bin = msg['message_content']['task_bin']
        result_path = self._find_result(task_bin)
        print(result_path)
        filename = self._download(result_path)
        filesize_bytes = os.path.getsize(filename)
        info = {
                'filename': filename, 
                'filesize_bytes': filesize_bytes, 
                }
        msg['answer'] = info
        if msg['sync'] == True:
            print(11111111111)
            self.sm.answer_msg(msg)
            with open(filename, 'rb') as f:
                data = f.read()
                self.sm.sendall(msg, data)
        #self._download()
        


    def msg_handler(self, msg):
        if msg['message_name'] == 'start':
            self.start_test(msg)
        elif msg['message_name'] == 'stop':
            self.stop_test(msg)
        elif msg['message_name'] == 'get_test_result':
            self.get_test_result(msg)

    def heartbeat(self):
        while True:
            u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = {
                    'client_ip':self.local_host,
                    'client_port':self.local_port,
                    }
            data_dumped = json.dumps(data)
            u.sendto(data_dumped.encode(), (self.remote_ip, self.remote_heartbeet_port))
            u.close()
            time.sleep(5)

    def start(self):
        #p_heartbeat = multiprocessing.Process(target = self.heartbeat)
        #p_heartbeat.start() 
        self.process_msg()


if __name__ == "__main__":
    ac = AiClient()
    ac.start()
        

