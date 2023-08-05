# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import ast
import multiprocessing
import threading
import datetime
from multiprocessing.managers import BaseManager
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import save_task
from modules import board_manager
from modules import queuelib
from modules import log
from modules.log import RunningLog
from modules.log import MySocketHandler
from modules import sendmsg

class LogManager(BaseManager):
    pass

def logManager():
    m = LogManager()
    m.start()
    return m

class Server(object):
    def __init__(self):
        self.level0_msg_list = multiprocessing.Manager().list()
        self.level1_msg_list = multiprocessing.Manager().list()
        self.level2_msg_list = multiprocessing.Manager().list()
        self.level3_msg_list = multiprocessing.Manager().list()
        self.server_control = multiprocessing.Manager().dict()
        self.ai_task_client = save_task.task_client
        self.server_control['operation'] = ''
        self.board_change = 0
        self.yaml_file = 'a.yaml'
        self.bc = board_manager.BoardConfig(self.yaml_file)
        self.bc.read_yaml()
        self.ql = queuelib.QueueLib()
        self.sm = sendmsg.SendMsg()
        self.hl = log.HeartLog('heart_log.yaml')
        #self.rl = log.RunningLog()
        LogManager.register('runninglog', RunningLog)
        manager = logManager()
        self.rl = manager.runninglog()#进程间共享

    def listen_heart(self):
        port = 28888
        host = ''
        u = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        u.bind((host,port))
        count = 0
        while True:
            data,addr = u.recvfrom(1024)
            data = ast.literal_eval(data.decode())
            print(data, addr)
            self.hl.update_heart(data)
            count += 1
            if count == 5:
                count = 0 
                outtime_list = self.hl.check_outtime()
                if len(outtime_list) >= 1:
                    self.deal_outtime(outtime_list)

    def deal_outtime(self, outtime_list):
        dead_msg = {
                'host':'',
                'port':'',
                'priority':0,
                'sync':'',
                'receiver':'server',
                'message_name':'dead_client',
                'message_content': outtime_list
                }
        self.sm.send_to_server(dead_msg)

    def tcp_bind(self):
        port = 10000
        host = ''
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(30)
        print("waiting for connection...")
        return s

    def tcp_link(self, sock, addr):
        print("Accept new connection from %s:%s..." %addr)
        msg = ''.encode()
        start = 0
        end = 0
        while True:
            data = sock.recv(1024)
            print(data)
            if data.find('§§START§§'.encode()) >= 0:
                start = 1
            if start:
                msg += data
                if msg.find('§§END§§'.encode()) >= 0:
                    start = 0
                    end = 1
            if end:
                msg = self.sm.unpack(msg)
                self.rl.write(msg, 'info', 'RECV_MSG')
                print(msg['priority'])
                if str(msg['priority']) == '0':
                    self.ql.add_message_to_queue(self.level0_msg_list, msg)
                if str(msg['priority']) == '1':
                    self.ql.add_message_to_queue(self.level1_msg_list, msg)
                if str(msg['priority']) == '2':
                    self.ql.add_message_to_queue(self.level2_msg_list, msg)
                if str(msg['priority']) == '3':
                    self.ql.add_message_to_queue(self.level2_msg_list, msg)
                break
        sock.close()
        print('Connection form %s: %s closed' %addr)

    def recv_msg(self):
        tfd = self.tcp_bind()
        while True:
            sock, addr = tfd.accept()
            print(addr[0])
            t = threading.Thread(target = self.tcp_link(sock, addr))
            t.setDaemon(True)
            t.start()

    def start_test(self, msg):
        # 指定具体某块板子
        ret = 0
        info = ''
        if msg['message_content']['dvb_info']['specific_board']['client_ip'] :
            client_ip = msg['message_content']['dvb_info']['specific_board']['client_ip']
            client_port = msg['message_content']['dvb_info']['specific_board']['client_port']
            board_name = msg['message_content']['dvb_info']['specific_board']['board_name']
            use_board = (client_ip, client_port, board_name)
            if self.bc.is_idle(use_board):
                self.bc.update_board_status(use_board, 'busy')
                self.board_change = 1
                try:
                    self.sm.send_to_client(client_ip, client_port, msg)
                    info = 'send to specific_board success '
                    ret = 1
                except:
                    info = 'send to specific_board failed '
                    self.rl.write('connect client error : ip ' + client_ip + ' port : ' + \
                            client_port, 'error', 'start_test')
            elif msg not in self.level2_msg_list:
                info = 'specific_board is busy'
                self.ql.add_message_to_queue(self.level2_msg_list, msg)
        # 不指定具体板子，根据任务调节分配板子
        else:
            mode = msg['message_content']['dvb_info']['auto_board']['mode']
            arch = msg['message_content']['dvb_info']['auto_board']['arch']
            chip = msg['message_content']['dvb_info']['auto_board']['chip']
            board = msg['message_content']['dvb_info']['auto_board']['board']
            signal = msg['message_content']['dvb_info']['auto_board']['signal']
            usb_device = msg['message_content']['dvb_info']['auto_board']['usb_device']
            usb_gxbus = msg['message_content']['dvb_info']['auto_board']['usb_gxbus']
            usb_type = msg['message_content']['dvb_info']['auto_board']['usb_storage_type']
            usb_partition_num = msg['message_content']['dvb_info']\
                    ['auto_board']['usb_partition_num']
            web = msg['message_content']['dvb_info']['auto_board']['web']
            usb_wifi = msg['message_content']['dvb_info']['auto_board']['usb_wifi']
            usb_wifi_type = msg['message_content']['dvb_info']['auto_board']['usb_wifi_type']
            priority = msg['message_content']['dvb_info']['auto_board']['priority']
            if msg['message_content']['dvb_ai'] == 'ai':
                board = msg['message_content']['ai_info']['task_info']['board']
                idle_boards = self.bc.get_idle_board_list(arch, chip, board, signal, usb_type)
            else:
                idle_boards = self.bc.get_idle_board_list2(mode, arch, chip, board, signal,\
                        usb_device, usb_gxbus, usb_type, usb_partition_num, \
                        web, usb_wifi, usb_wifi_type, priority)
            print(idle_boards)
            if len(idle_boards) > 0:
                use_board = idle_boards.pop()
                client_ip = use_board[0]
                client_port = use_board[1]
                board_name = use_board[2]
                self.bc.update_board_status(use_board, 'busy')
                self.board_change = 1
                if msg['message_content']['dvb_ai'] == 'dvb': 
                    msg['message_content']['dvb_info']['specific_board']['client_ip'] \
                            = client_ip
                    msg['message_content']['dvb_info']['specific_board']['client_port'] \
                            = client_port
                    msg['message_content']['dvb_info']['specific_board']['board_name'] \
                            = board_name
                try:
                    self.sm.send_to_client(client_ip, client_port, msg)
                    if msg['message_content']['dvb_ai'] == 'ai': 
                        task_bin = board = msg['message_content']\
                                ['ai_info']['task_info']['bin_url']
                        self.ai_task_client.append({task_bin:use_board})
                    info = 'send to auto_board success '
                    ret = 1
                except:
                    info = 'send to auto_board failed '
                    self.rl.write('connect client error : ip ' + client_ip + ' port : ' + \
                            client_port, 'error', 'start_test')
            elif msg not in self.level2_msg_list:
                info = 'no auto_board idle '
                self.ql.add_message_to_queue(self.level2_msg_list, msg)
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def stop_test(self, msg):
        ret = 0
        info = 'send to client success'
        # 停止所有板子
        try:
            #if msg['message_content']['type'] == 'all':
            #    running_boards = self.bc.get_running_board_list()
            #    self.sm.send_to_client_list(running_boards)
            ## 停止指定 Jenkins 工程某次构建的测试任务
            #elif msg['message_content']['jenkins_info']['jenkins_project_name']:
            #    jenkins_porject = msg['message_content']['jenkins_info']['jenkins_project_name']
            #    jenkins_build = msg['message_content']['jenkins_info']['jenkins_build_id']
            #    jenkins_boards = self.bc.get_board_list_by_jenkins(jenkins_porject, \
            #            jenkins_build)
            #    self.sm.send_to_client_list(jenkins_boards)
            ## 停止指定型号的板子
            #elif msg['message_content']['board_info'] != {}:
            #    type_boards = self.bc.get_board_list_by_type()
            #    self.sm.send_to_client_list(type_boards)
            ## 停止具体某一个块板子
            #ret = 1

            client_list = self.bc.get_all_client()
            print(client_list)
            self.sm.send_to_client_list(msg, client_list)
            ret = 1
        except:
            info = 'send to client failed'
            self.rl.write('connect client error', 'error', 'stop_test')
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def list_message_queue(self, msg):
        print(1111111111111111)
        ret = 0
        info = 'get success'
        try:
            queue_name = str(msg['message_content']['priority'])
            if queue_name == 'all':
                info = {
                        'level0_msg':str(self.level0_msg_list),
                        'level1_msg':str(self.level1_msg_list),
                        'level2_msg':str(self.level2_msg_list),
                        'level3_msg':str(self.level3_msg_list),
                        }
            elif queue_name == '0':
                info = {
                        'level0_msg':str(self.level0_msg_list),
                        }
            elif queue_name == '1':
                info = {
                        'level1_msg':str(self.level1_msg_list),
                        }
            elif queue_name == '2':
                info = {
                        'level2_msg':str(self.level2_msg_list),
                        }
            elif queue_name == '3':
                info = {
                        'level3_msg':str(self.level3_msg_list),
                        }
            ret = 1
        except:
            info = 'get leavl' + queue_name + 'failed'
        if msg['sync'] == True:
            #msg['answer'] = str(info)
            msg['answer'] = info
            print(str(info))
            self.sm.answer_msg(msg)
        return ret
    
    def clear_message_queue(self, msg):
        ret = 0
        info = 'clear success'
        try:
            queue_name = str(msg['message_content']['priority'])
            if queue_name == 'all':
                self.level3_msg_list[:] = []
                self.level2_msg_list[:] = []
                self.level1_msg_list[:] = []
                self.level0_msg_list[:] = []
            if queue_name == '0':
                self.level0_msg_list[:] = []
            if queue_name == '1':
                self.level1_msg_list[:] = []
            if queue_name == '2':
                self.level2_msg_list[:] = []
            if queue_name == '3':
                self.level3_msg_list[:] = []
            ret = 1
        except:
            info = 'clear leavl' + queue_name + 'failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def delete_task(self, msg):
        ret = 0
        if msg['sync'] == True:
            info = 'del success'
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def query_client_info(self, msg):
        ret = 0
        info = 'query success'
        try:
            content = msg['message_content']
            board = content['filter']['board']
            chip = content['filter']['chip']
            arch = content['filter']['arch']
            os = content['filter']['os']
            signal = content['filter']['signal']
            usb_type = content['filter']['usb_storage_type']
            ip = content['specific_client']['client_ip']
            port = content['specific_client']['client_port']
            if ip :
                info = self.bc.get_info_by_ip(ip,port)
            else:
                info = self.bc.get_client_info(arch , chip, board, signal, usb_type, os)
            ret = 1
        except:
            info = 'query failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def update_client_status(self, msg):
        ret = 0
        info = 'update success'
        try:
            content = msg['message_content']
            ip = content['client_ip']
            port = content['client_port']
            board_name = content['stb_board_dict'][0]['board_name']
            use_board = (ip, port, board_name)
            running_info = content['stb_board_dict'][0]['running_info']
            debug_info = content['stb_board_dict'][0]['gxdebug_info']
            if debug_info != {}:
                bc.update_board_gxdebug(use_board, debug_info)
            else:
                bc.update_board_detail(use_board, status)
            self.board_change = 1
            ret = 1
        except:
            info = 'update failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def switch_mode(self, msg):
        ret = 0
        info = 'send success'
        try:
            ip = msg['message_content']['client_ip']
            port = msg['message_content']['client_port']
            self.sm.send_to_client(ip, port, msg)
            ret = 1
        except:
            info = 'send failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def add_board(self, msg):
        ret = 0
        info = 'add success'
        try:
            ip = msg['message_content']['client_ip']
            port = msg['message_content']['client_port']
            board_list = msg['message_content']['stb_board_dict']
            self.bc.add_board(ip, port, board_list)
            self.board_change = 1
            ret = 1
        except:
            info = 'add failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def delete_board(self, msg):
        ret = 0
        info = 'delete success'
        try:
            ip = msg['message_content']['client_ip'] 
            port = msg['message_content']['client_port'] 
            board_name = msg['message_content']['board_name'] 
            board = board = msg['message_content']['board']
            chip = msg['message_content']['chip']
            self.bc.delete_board(ip, port, board_name, board, chip)
            self.board_change = 1
            ret = 1
        except:
            info = 'delete failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret

    def board_power(self, msg):
        ret = 0
        info = 'send success'
        try:
            ip = msg['message_content']['client_ip']
            port = msg['message_content']['client_port']
            self.sm.send_to_client(ip, port, msg)
            ret = 1
        except:
            info = 'send failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret
    
    def client_log(self, msg):
        ret = 0
        info = 'send success'
        try:
            ip = msg['message_content']['client_ip']
            port = msg['message_content']['client_port']
            self.sm.send_to_client(ip, port, msg)
            ret = 1
        except:
            info = 'send failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        return ret
    
    def board_log(self, msg):
        ret = 0
        info = 'send success'
        try:
            ip = msg['message_content']['client_ip']
            port = msg['message_content']['client_port']
            self.sm.send_to_client(ip, port, msg)
            ret = 1
        except:
            info = 'send failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)

    def get_server_log(self, msg, filename='runninglog.txt'):
        ret = 0
        try:
            level = msg['message_content']['level']
            msg_filter = msg['message_content']['msg_filter']
            time_before = msg['message_content']['time_before']
            time_after = msg['message_content']['time_after']
            filename = self.rl.read(level, msg_filter, time_before, time_after)
            os.system('cp "' + filename + '" cplog.txt')
            filemsg = 'cplog.txt'
            filesize_bytes = os.path.getsize(filemsg)
            info = {
                'filename': filename,
                'filesize_bytes': filesize_bytes,
                }
            ret = 1
        except:
            info = "get server log failed"
        msg['answer'] = info
        if msg['sync'] == True:
            self.sm.answer_msg(msg)
            with open(filemsg, 'rb') as f:
                data = f.read()
                self.sm.sendall(msg, data)
        return ret
        #head_info = json.dumps(dirc)

    def server_log(self, msg):
        ret = 0
        try:
            host = msg['host']
            port = msg['port']
            print('send tcp log')
            print(host)
            print(port)
            ret = 1
        except:
            pass
        if msg['sync'] == True:
            self.rl.add_tcp('192.168.111.101', 10003)
        return ret

    def server_stash(self, msg):
        ret = 0
        info = 'send success'
        try:
            client_list = self.bc.get_all_client()
            self.sm.send_to_client_list(msg, client_list)
            ret = 1
        except:
            info = 'send failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        self.server_control['operation'] = 'stash'

    def server_resume(self, msg):
        ret = 0
        info = 'send success'
        try:
            client_list = self.bc.get_all_client()
            self.sm.send_to_client_list(msg, client_list)
        except:
            info = 'send failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)
        self.server_control['operation'] = 'resume'

    def transpond_to_client(self, msg):
        ret = 0
        info = 'transpond success'
        try:
            tmp = msg['receiver'].split('@')
            ip = tmp[1]
            port = tmp[2]
            self.sm.send_to_client(ip, port, msg)
            ret = 1
        except:
            info = 'transpond failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)

    def get_test_result(self, msg):
        ret = 0
        info = 'transpond success'
        try:
            task = msg['message_content']['task_bin']
            use_board = self.ai_task_client[task]
            client_ip = use_board[0]
            client_port = use_board[1]
            board_name = use_board[2]
            self.sm.send_to_client(client_ip, client_port, msg)
            ret = 1
        except:
            info = 'transpond failed'
        if msg['sync'] == True:
            msg['answer'] = str(info)
            self.sm.answer_msg(msg)

    def msg_handler(self, msg):
        ret = 0
        print(msg['message_name'])
        self.rl.write(msg, 'info', 'DEAL_MSG')
        if msg['receiver'].startswith('server'):
            if msg['message_name'] == "start":
                ret = self.start_test(msg)
            elif msg["message_name"] == "stop":
                ret = self.stop_test(msg)
            elif msg["message_name"] == "list_message_queue":
                ret = self.list_message_queue(msg)
            elif msg["message_name"] == "clear_message_queue":
                ret = self.clear_message_queue(msg)
            elif msg["message_name"] == "delete_task":
                ret = self.delete_task(msg)
            elif msg["message_name"] == "query_client_info":
                ret = self.query_client_info(msg)
            elif msg["message_name"] == "update_client_status":
                ret = self.update_client_status(msg)
            elif msg["message_name"] == "switch_mode":
                ret = self.switch_mode(msg)
            elif msg["message_name"] == "add_board":
                ret = self.add_board(msg)
            elif msg["message_name"] == "delete_board":
                ret = self.delete_board(msg)
            elif msg["message_name"] == "board_power":
                ret = self.board_power(msg)
            elif msg["message_name"] == "client_log":
                ret = self.client_log(msg)
            elif msg["message_name"] == "board_log":
                ret = self.board_log(msg)
            elif msg["message_name"] == "server_log":
                ret = self.get_server_log(msg)
                #ret = self.server_log(msg)
            elif msg["message_name"] == "server_stash":
                ret = self.server_stash(msg)
            elif msg["message_name"] == "server_resume":
                ret = self.server_resume(msg)
            elif msg["message_name"] == "get_test_result":
                ret = self.get_test_result(msg)
        elif msg['receiver'].startswith('client'):
            ret = self.transpond_to_client(msg)
        return ret
    
    def deal_msg(self):
        while True:
            ret = 0
            if self.board_change:
                self.board_change = 0
                self.bc.read_yaml()
            print(self.level0_msg_list)
            print(self.level1_msg_list)
            print(self.level2_msg_list)
            print(self.level3_msg_list)
            time.sleep(2)
            # 处理level0信息，处理失败则继续下一条，处理成功重新循环
            for msg in self.level0_msg_list:
                self.level0_msg_list.remove(msg)
                ret = self.msg_handler(msg)
                if ret:
                    break
            if ret:
                continue

            # 处理level1信息
            for msg in self.level1_msg_list:
                self.level1_msg_list.remove(msg)
                ret = self.msg_handler(msg)
                if ret:
                    break
            if ret:
                continue

            # 处理level2信息
            for msg in self.level2_msg_list:
                self.level2_msg_list.remove(msg)
                ret = self.msg_handler(msg)
                if ret:
                    break
            if ret:
                continue

            # 处理level3信息
            for msg in self.level3_msg_list:
                self.level3_msg_list.remove(msg)
                ret = self.msg_handler(msg)
                if ret:
                    break
            if ret:
                continue

    def save_list(self):
        data = {}
        data['level0'] = list(self.level0_msg_list)
        data['level1'] = list(self.level1_msg_list)
        data['level2'] = list(self.level2_msg_list)
        data['level3'] = list(self.level3_msg_list)
        self.hl.write_down_dict(data)

    def reload_list(self):
        save_task = self.hl.read_task_from_file()
        self.level0_msg_list.extend(save_task['level0'])
        self.level1_msg_list.extend(save_task['level1'])
        self.level2_msg_list.extend(save_task['level2'])
        self.level3_msg_list.extend(save_task['level3'])

    def start(self):
        self.heart = multiprocessing.Process(target = self.listen_heart)
        self.heart.daemon = True
        self.heart.start()
        self.p_recv_msg = multiprocessing.Process(target = self.recv_msg)
        self.p_recv_msg.daemon = True
        self.p_recv_msg.start()
        self.p_deal_msg = multiprocessing.Process(target = self.deal_msg)
        self.p_deal_msg.daemon = True
        self.p_deal_msg.start()
        need_check = True
        count = 0
        while True:
            #if count == 5:
            #    self.server_control['operation'] = 'stash'
            if self.server_control['operation'] != '':
                if self.server_control['operation'] == 'stash':
                    self.save_list()
                    sys.exit()
                if self.server_control['operation'] == 'resume':
                    self.reload_list()
            self.rl.write('check alive', 'info')
            if not self.heart.is_alive() and need_check:
                self.clean_udp_port()
                self.heart = multiprocessing.Process(target = self.listen_heart)
                self.heart.start()
            if not self.p_recv_msg.is_alive() and need_check:
                self.clean_tcp_port()
                self.p_recv_msg = multiprocessing.Process(target = self.recv_msg)
                self.p_recv_msg.start()
            if not self.p_deal_msg.is_alive() and need_check:
                self.p_deal_msg = multiprocessing.Process(target = self.deal_msg)
                self.p_deal_msg.start()
            time.sleep(3)
            count += 1

def main():
    sv = Server()
    sv.start()

if __name__ == '__main__':
    main()

