import sys
import os
import socket
import threading
import time
import json
import copy
import argparse
from getopt import getopt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import sendmsg
import ftp
import msg

class CmdBase(object):
    def __init__(self):
        self.udp_port = 28888
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.sm = sendmsg.SendMsg()
        self.local_host = '192.168.110.244'
        self.local_recv_port = 10001
        self.read_log_port = 10003
        self.udp_host = self.local_host
        self.gm = msg.GenMsg()
        self.message_format = {
            "ip":"",
            "port":"",
            "priority":2,
            "sync":"",
            "receiver":"",
            "message_name":"",
            "message_content":{},
        }

    def get_idle_port(self, port):
        return port
        #while True:
        #    cmd = 'lsof -i:' + str(port)
        #    fd = os.popen(cmd)
        #    ret = fd.read(1024)
        #    fd.close()
        #    if len(ret.split('\n')) >= 2:
        #        break
        #    else:
        #        port += 1
        #return port

    def bind_tcp(self, host = '', port = ''):
        host = '192.168.110.244'
        port = 10000
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((host,port))

    def send_tcp(self, msg):
        print(msg)
        self.s.send(msg)
        print('send success')

    def recv_log(self):
        print(111111)
        port = self.read_log_port
        host = ''
        print(port)
        msg = ''.encode()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(5)
        sock, addr = s.accept()
        end = 0
        start = 0
        while True:
            data = sock.recv(1024)
            print(data.decode())
            if not data:
                break

    def recv_msg(self):
        print(111111)
        port = self.local_recv_port
        host = ''
        msg = ''.encode()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(30)
        sock, addr = s.accept()
        end = 0
        start = 0
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
        #print(msg)
        s.shutdown(2)
        s.close()
        return msg
    
    def process_bar(self, precent, width=50):
        use_num = int(precent*width)
        space_num = int(width-use_num)
        precent = precent*100
        print('[%s%s]%d%%'%(use_num*'#', space_num*' ',precent),file=sys.stdout,flush=True, end='\r')
    
    def recv_file(self, filename, filesize_bytes):
        buffsize = 1024
        port = self.local_recv_port
        host = ''
        msg = ''.encode()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(30)
        sock, addr = s.accept()
        recv_len = 0
        recv_data = b''
        old = time.time()
        f = open(filename, 'wb')
        while recv_len < filesize_bytes:
            percent = recv_len / filesize_bytes
            self.process_bar(percent)
            if filesize_bytes - recv_len > buffsize:
                recv_data = sock.recv(buffsize)
                f.write(recv_data)
                recv_len += len(recv_data)
            else:
                recv_data = sock.recv(filesize_bytes -recv_len)
                recv_len += len(recv_data)
                f.write(recv_data)
        print(recv_len, filesize_bytes)
        now = time.time()
        stamp = int(now - old)
        print('接收用时 : %ds' % stamp)
        f.close()

    def close_tcp(self):
        self.s.close()

class BoardManager(CmdBase):
    def __init__(self):
        CmdBase.__init__(self)
        pass

    def GetClientsInfo(self, sync, receiver, ip = '', port = '', arch = '', chip = '', \
            board = '', bin_os = '', signal = '', usb_storage_type = ''):
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        if receiver == 'server':
            message['receiver'] = receiver
        elif receiver == 'client':
            message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.query_client_info()
        content['specific_client']['client_ip'] = ip
        content['specific_client']['client_port'] = port
        content['filter']['chip'] = chip
        content['filter']['board'] = board
        content['filter']['arch'] = arch
        content['filter']['os'] = bin_os
        content['filter']['signal'] = signal
        content['filter']['usb_storage_type'] = usb_storage_type
        if sync:
            message['sync'] = True
        message['message_name'] = 'query_client_info'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def GetBoardInfo(self, receiver, sync, board = ''):
        board = '6605s'
        self.GetClientsInfo(sync, receiver, board = board)

    def GetChipInfo(self, sync, receiver, chip = ''):
        chip = '6605s'
        self.GetClientsInfo(sync, receiver, chip = chip)

    def Power(self,sync, receiver, ip = '', port = '', name = '', handle = ''):
        receiver = 'client'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.board_power()
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = name
        content['operation'] = handle

        if sync:
            message['sync'] = True
        message['message_name'] = 'board_power'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def AddBoard(self, sync, receiver, dvb = '', ip = '', port = '', name = '', \
            arch = '', board = '', chip = '', \
            electric_relay_port = '', electric_relay_serial = '', mode = '',\
            signal = '', \
            usb_device = '', usb_gxbus = '', usb_storage_type = '', usb_partition_num = '',\
            web = '', usb_wifi = '', usb_wifi_type = '', secure ='', \
            status = '', test_serial = ''):
        receiver = 'client'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.add_board()
        content['client_ip'] = ip
        content['client_port'] = port
        content['dvb_ai'] = dvb
        content['stb_board_dict'][0]['board_name'] = name
        content['stb_board_dict'][0]['arch'] = arch
        content['stb_board_dict'][0]['chip'] = chip
        content['stb_board_dict'][0]['board'] = board
        content['stb_board_dict'][0]['test_serial'] = test_serial
        content['stb_board_dict'][0]['electric_relay_serial'] = electric_relay_serial
        content['stb_board_dict'][0]['electric_relay_port'] = electric_relay_port
        content['stb_board_dict'][0]['signal'] = signal
        content['stb_board_dict'][0]['usb_device'] = usb_device
        content['stb_board_dict'][0]['usb_gxbus'] = usb_gxbus
        content['stb_board_dict'][0]['usb_storage_type'] = usb_storage_type
        content['stb_board_dict'][0]['usb_partition_num'] = usb_partition_num
        content['stb_board_dict'][0]['web'] = web
        content['stb_board_dict'][0]['usb_wifi'] = usb_wifi
        content['stb_board_dict'][0]['usb_wifi_type'] = usb_wifi_type
        content['stb_board_dict'][0]['test_project_bind'] = ''
        content['stb_board_dict'][0]['mode'] = mode
        content['stb_board_dict'][0]['status'] = status
        content['stb_board_dict'][0]['secure'] = secure
        if sync:
            message['sync'] = True
        message['message_name'] = 'add_board'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def UpdateBoard(self, sync, receiver, dvb = '', ip = '', port = '', name = '', \
            arch = '', board = '', chip = '', \
            electric_relay_port = '', electric_relay_serial = '', mode = '', signal = '', \
            usb_device = '', usb_gxbus = '', usb_storage_type = '', usb_partition_num = '',\
            web = '', usb_wifi = '', usb_wifi_type = '', secure = '', \
            status = '', test_serial = ''):
        receiver = 'client'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.update_board()
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = name
        content['dvb_ai'] = dvb
        for arg in ['arch', 'chip', 'board', \
                'electric_relay_port', 'electric_relay_serial','mode', 'signal', \
                'usb_device', 'usb_gxbus', 'usb_storage_type', 'usb_partition_num', \
                'web', 'usb_wifi', 'usb_wifi_type', 'secure', 'status', 'test_serial']:
            value = eval(arg)
            if value:
                content['board_info'][arg] = value
        if sync:
            message['sync'] = True
        message['message_name'] = 'update_board'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def DeleteBoard(self, sync, receiver, ip = '', port = '', name= '', board= '',chip = ''):
        receiver = 'client'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.delete_board()
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = name
        content['board'] = board
        content['chip'] = chip
        if sync:
            message['sync'] = True
        message['message_name'] = 'delete_board'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def SwitchMode(self, sync, receiver, ip = '', port = '', name = '', \
            old_mode = '', new_mode = '', force = ''):
        receiver = 'client'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.switch_mode()
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = name
        content['mode_need_modify'] = old_mode
        content['mode_after_modify'] = new_mode
        content['force'] = force
        if sync:
            message['sync'] = True
        message['message_name'] = 'switch_mode'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

class TaskManager(CmdBase):
    def __init__(self):
        CmdBase.__init__(self)

    def GetTasksInfo(self, sync = '', receiver = '', priority = 'all'):
        sync = True
        receiver = 'server'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = priority
        message['receiver'] = receiver
        content = self.gm.list_message_queue()
        content['priority'] = priority
        if sync:
            message['sync'] = True
        message['message_name'] = 'list_message_queue'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            info = self.recv_msg()
            return info

    def GetChipTasks(self, level = '', chip = ''):
        match_list = []
        sync = True
        receiver = 'server'
        info = self.GetTasksInfo(sync, receiver, level)
        answer = info['answer']
        for level, task_list in answer.items():
            task_list = eval(task_list)
            for task in task_list:
                if task['message_content']['dvb_ai'] == 'dvb':
                    if taskmsg['message_content']['dvb_info']['bin_info']['chip'] == chip:
                        match_list.append(task)
        print(match_list)

    def GetBoardTasks(self, level = '', board = ''):
        match_list = []
        sync = True
        receiver = 'server'
        info = self.GetTasksInfo(sync, receiver, level)
        answer = info['answer']
        for level, task_list in answer.items():
            task_list = eval(task_list)
            for task in task_list:
                if task['message_content']['dvb_ai'] == 'dvb':
                    task_board = task['message_content']['dvb_info']['bin_info']['board']
                else:
                    task_board = task['message_content']['ai_info']['task_info']['board']
                #print(task_board)
                if task_board == board:
                    match_list.append(task)
        print(match_list)

    def GetJenkinsTask(self, level = '', jenkins = ''):
        match_list = []
        sync = True
        receiver = 'server'
        info = self.GetTasksInfo(sync, receiver, level)
        answer = info['answer']
        for level, task_list in answer.items():
            task_list = eval(task_list)
            for task in task_list:
                if task['message_content']['dvb_ai'] == 'dvb':
                    test_jenkins =  taskmsg['message_content']\
                            ['dvb_info']['bin_info']['jenkins_project_name']
                else:
                    test_jenkins =  taskmsg['message_content']\
                            ['ai_info']['jenkins_info']['jenkins_project_name']
                if task_jenkins == jenkins:
                    match_list.append(task)
        print(match_list)

    def DelAllTask(self, sync, receiver, priority = 'all'):
        receiver = 'server'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = receiver
        content = self.gm.clear_message_queue()
        content['priority'] = priority
        if sync:
            message['sync'] = True
        message['message_name'] = 'clear_message_queue'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def DelTask(self, sync, receiver, jenkins = '', ip = '', port='', board = '', chip=''):
        receiver = 'server'
        message = copy.deepcopy(self.message_format)
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['receiver'] = receiver
        content = {
                'jenkins':jenkins,
                'chip':chip,
                'board':board,
                'ip' : ip,
                'port': port
        }
        if sync:
            message['sync'] = True
        message['message_name'] = 'delete_message_from_queue'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def DelTaskByJenkinsProject(self, sync, receiver, jenkins=''):
        self.DelTask(sync, receiver, jenkins = jenkins)

    def DelTaskByClient(self, sync, receiver, ip = '', port = ''):
        self.DelTask(sync, receiver, ip = ip, port = port)

    def DelTaskByChip(self, sync, receiver, chip = ''):
        self.DelTask(sync, receiver, chip = chip)

    def DelTaskByBoard(self, sync, receiver, board):
        self.DelTask(sync, receiver, board = board)

    def _uploadfile(self, local_bin = '', bin_url = '', jenkins_name = '', jenkins_build = '',\
            board = '', dvb = 'dvb', now = ''):
        if local_bin:
            fl = ftp.FtpFunctionLib(\
                    Host = '192.168.110.253', UserName = 'guoxin', Password = 'Guoxin88156088',\
                    FtpLoginBasicPath= 'public/ftp/AutoTestBin/' + dvb, LoginPort = 21)
            ret = fl.FtpLogin()
            print(ret)
            if not jenkins_name:
                jenkins_name = 'no_jenkins'
            if not jenkins_build:
                jenkins_build = 'no_build'
            if bin_url:
                remote_path = os.path.dirname(bin_url)
                remote_bin = os.path.dirname(bin_url) + '/' + now + '@@' + \
                        os.path.basename(bin_url)
            else:
                remote_path = jenkins_name + '/' + jenkins_build + '/' +  board
                remote_bin = remote_path + '/' + now + '@@' + os.path.basename(local_bin)
            fl.Mkdirs(remote_path)
            fl.UploadFile(local_bin, remote_bin)
            fl.FtpQuit()
            bin_url = dvb + '/' + remote_bin
        return bin_url

    #def _renamefile(self):
    #    fl = ftp.FtpFunctionLib(\
    #            Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
    #            FtpLoginBasicPath= './',  LoginPort = 2121)
    #    ret = fl.FtpLogin()
    #    print(ret)
    #    local_file = '[STOP]'
    #    os.system('touch a.txt')
    #    remote_path = 'Test_Entrance'
    #    remote_bin = remote_path + '/' + local_file
    #    fl.Mkdirs(remote_path)
    #    fl.UploadFile('a.txt', remote_bin)
    #    fl.FtpQuit()
    #    os.system('rm "' + local_file + '"')

    def Start(self, sync, receiver,  dvb = '', local_bin = '', bin_url = '', \
            local_boot_file = '', boot_file_url = '', local_boot_tool = '',\
            boot_tool_url = '', jenkins_name = '', jenkins_build = '',\
            arch = '', chip = '', board = '', bin_os = '', mode ='', signal = '',\
            gerrit_id = '', gerrit_patch = '', \
            testlink_project = '', testlink_plan = '', testlink_build = '',\
            client_ip = '', client_port = '', board_name = '', 
            web = '', usb_wifi = '', usb_wifi_type = '', secure ='', \
            usb_device = '', usb_gxbus = '', usb_storage_type = '', usb_partition_num = '',\
            priority = ''):
        receiver = 'server'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = receiver
        time_format = "%Y%m%d_%H%M%S"
        now = time.strftime(time_format, time.localtime())
        content = self.gm.start()
        bin_url = self._uploadfile(local_bin, bin_url, jenkins_name, \
                jenkins_build, board, dvb, now)
        boot_file_url = self._uploadfile(local_boot_file, boot_file_url, jenkins_name, \
                jenkins_build, board, dvb, now)
        boot_tool_url = self._uploadfile(local_boot_tool, boot_tool_url, jenkins_name, \
                jenkins_build, board, dvb, now)
        content['dvb_ai'] = dvb
        content['dvb_info']['test_info']['bin_url'] = bin_url
        content['dvb_info']['test_info']['boot_file_url'] = boot_file_url
        content['dvb_info']['test_info']['boot_tool_url'] = boot_tool_url
        content['dvb_info']['test_info']['os'] = bin_os
        content['dvb_info']['test_info']['mode'] = mode
        content['dvb_info']['auto_board']['arch'] = arch
        content['dvb_info']['auto_board']['chip'] = chip
        content['dvb_info']['auto_board']['board'] = board
        content['dvb_info']['auto_board']['signal'] = signal
        content['dvb_info']['auto_board']['usb_device'] = usb_device
        content['dvb_info']['auto_board']['usb_gxbus'] = usb_gxbus
        content['dvb_info']['auto_board']['usb_storage_type'] = usb_storage_type
        content['dvb_info']['auto_board']['usb_partition_num'] = usb_partition_num
        content['dvb_info']['auto_board']['web'] = web
        content['dvb_info']['auto_board']['usb_wifi'] = usb_wifi
        content['dvb_info']['auto_board']['usb_wifi_type'] = usb_wifi_type
        content['dvb_info']['auto_board']['secure'] = secure
        content['dvb_info']['auto_board']['priority'] = priority
        content['dvb_info']['specific_board']['client_ip'] = client_ip
        content['dvb_info']['specific_board']['client_port'] = client_port
        content['dvb_info']['specific_board']['board_name'] = board_name
        content['dvb_info']['jenkins_info']['jenkins_project_name'] = jenkins_name
        content['dvb_info']['jenkins_info']['jenkins_build_id'] = jenkins_build
        content['dvb_info']['gerrit_info']['gerrit_id'] = gerrit_id
        content['dvb_info']['gerrit_info']['gerrit_patch'] = gerrit_patch
        content['dvb_info']['testlink_info']['testlink_project'] = testlink_project
        content['dvb_info']['testlink_info']['testlink_plan'] = testlink_plan
        content['dvb_info']['testlink_info']['testlink_build'] = testlink_build
        message['message_name'] = 'start'
        message['message_content'] = content
        if sync:
            message['sync'] = True
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def ai_Start(self, sync, receiver,  dvb = '', task_type = '', \
            local_bin = '', bin_url = '', \
            jenkins_name = '', jenkins_build = '', board = '',
            gerrit_id = '', gerrit_patch = '', \
            testlink_project = '', testlink_plan = '', testlink_build = ''):
        receiver = 'server'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = receiver
        time_format = "%Y%m%d_%H%M%S"
        now = time.strftime(time_format, time.localtime())
        content = self.gm.start()
        bin_url = self._uploadfile(local_bin, bin_url, jenkins_name, \
                jenkins_build, board, dvb, now)
        content['dvb_ai'] = dvb
        content['ai_info']['task_type'] = task_type
        content['ai_info']['task_info']['bin_url'] = bin_url
        content['ai_info']['task_info']['board'] = board
        content['ai_info']['jenkins_info']['jenkins_project_name'] = jenkins_name
        content['ai_info']['jenkins_info']['jenkins_build_id'] = jenkins_build
        content['ai_info']['gerrit_info']['gerrit_id'] = gerrit_id
        content['ai_info']['gerrit_info']['gerrit_patch'] = gerrit_patch
        content['ai_info']['testlink_info']['testlink_project'] = testlink_project
        content['ai_info']['testlink_info']['testlink_plan'] = testlink_plan
        content['ai_info']['testlink_info']['testlink_build'] = testlink_build
        message['message_name'] = 'start'
        message['message_content'] = content
        if sync:
            message['sync'] = True
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def Stop(self, sync, receiver, stop_type = 'all', ip = '', port = '', name = '', \
            jenkins_name = '', jenkins_build = '', \
            arch = '', chip = '', board = '', bin_os = '', signal = '', usb_storage_type = ''):
        receiver = 'client'
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        receiver = 'server'
        message['receiver'] = receiver
        content = self.gm.stop()
        content['type'] = stop_type
        content['jenkins_info']['jenkins_project_name'] = jenkins_name
        content['jenkins_info']['jenkins_build_id'] = jenkins_build
        content['specific_board']['client_ip'] = ip
        content['specific_board']['client_port'] = port
        content['specific_board']['board_name'] = name
        content['board_info']['chip'] = chip
        content['board_info']['board'] = board
        content['board_info']['arch'] = arch
        content['board_info']['os'] = bin_os
        content['board_info']['signal'] = signal
        content['board_info']['usb_storage_type'] = usb_storage_type

        if sync:
            message['sync'] = True
        message['message_name'] = 'stop'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()
        #self._renamefile()

    def ServerStash(self, sync, receiver):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 0
        receiver = 'server'
        message['receiver'] = receiver
        content = self.gm.server_stash()
        if sync:
            message['sync'] = True
        message['message_name'] = 'server_stash'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def ServerResume(self, sync, receiver):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 0
        receiver = 'server'
        message['receiver'] = receiver
        content = self.gm.server_resume()
        if sync:
            message['sync'] = True
        message['message_name'] = 'server_resume'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

    def GetTestResult(self, sync, receiver, task):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 1
        receiver = 'server'
        message['receiver'] = receiver
        content = self.gm.get_test_result()
        content['task_bin'] = task
        if sync:
            message['sync'] = True
        message['message_name'] = 'get_test_result'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()

        answer1 = self.recv_msg()
        answer2 = self.recv_msg()
        if isinstance(answer1['answer'], dict):
            answer = answer1
        else:
            answer = answer2
        print(answer1)
        print(answer2)
        filename = answer['answer']['filename']
        filesize_bytes = answer['answer']['filesize_bytes']
        self.recv_file(filename, filesize_bytes)
        #filename = answer['answer']['filename']
        #filesize_bytes = answer['answer']['filesize_bytes']
        #self.recv_file(filename, filesize_bytes)



class LogManager(CmdBase):
    def __init__(self):
        CmdBase.__init__(self)

    def ReadServerLog(self, sync, receiver, level = '', key = '', \
            time_before = '', time_after = ''):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        receiver = 'server'
        message['receiver'] = receiver
        content = self.gm.server_log()
        content['level'] = level
        content['msg_filter'] = key
        content['time_before'] = time_before
        content['time_after'] = time_after
        if sync:
            message['sync'] = True
        message['message_name'] = 'server_log'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()

        answer = self.recv_msg()
        filename = answer['answer']['filename']
        filesize_bytes = answer['answer']['filesize_bytes']
        self.recv_file(filename, filesize_bytes)

    def ReadClientLog(self, sync, receiver, ip = '', port = '', level = '', key = '', \
            time_before = '', time_after = ''):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.client_log()
        content['client_ip'] = ip
        content['client_port'] = port
        content['level'] = level
        content['msg_filter'] = key
        content['time_before'] = time_before
        content['time_after'] = time_after
        if sync:
            message['sync'] = True
        message['message_name'] = 'client_log'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()

        answer1 = self.recv_msg()
        answer2 = self.recv_msg()
        time.sleep(2)
        if isinstance(answer1['answer'], dict):
            answer = answer1
        else:
            answer = answer2
        filename = answer['answer']['filename']
        filesize_bytes = answer['answer']['filesize_bytes']
        self.recv_file(filename, filesize_bytes)

    def ReadBoardLog(self, sync, ip = '',port = '', board_name = '', filename = '', size = 1024):
        '''
        获取板子打印信息
        '''
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        content = self.gm.board_log()
        receiver = 'client'
        message['receiver'] = '@'.join([receiver, ip, port])
        content['type'] = 'read'
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = board_name
        content['file_name'] = filename
        content['size'] = size
        if sync:
            message['sync'] = True
        message['message_name'] = 'board_log'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()

        if sync:
            self.recv_msg()
        self.recv_file(filename, size)

    def GetBoardLogInfo(self, sync, receiver, ip = '',port = '', board_name = ''):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.board_log()
        content['type'] = 'list'
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = board_name
        if sync:
            message['sync'] = True
        message['message_name'] = 'board_log'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()
            self.recv_msg()

    def CleanLog(self, sync, receiver, ip = '',port = '', board_name = '', filename=''):
        sync = True
        message = self.gm.msg_format()
        message['ip'] = self.local_host
        message['port'] = self.local_recv_port
        message['priority'] = 2
        message['receiver'] = '@'.join([receiver, ip, port])
        content = self.gm.board_log()
        content['type'] = 'delete'
        content['client_ip'] = ip
        content['client_port'] = port
        content['board_name'] = board_name
        content['file_name'] = filename
        if sync:
            message['sync'] = True
        message['message_name'] = 'board_log'
        message['message_content'] = content
        self.bind_tcp()
        self.send_tcp(self.sm.pack(message))
        self.close_tcp()
        if sync:
            self.recv_msg()

def func_GetClientsInfo(args):
    clientmanager = BoardManager()
    clientmanager.GetClientsInfo(args.sync, args.receiver, args.ip, args.port, \
            args.arch, args.chip, args.board, args.os, args.signal, args.usb_storage_type)

def func_GetBoardInfo(args):
    clientmanager = BoardManager()
    clientmanager.GetBoardInfo(args.sync, args.receiver, args.board)

def func_GetChipInfo(args):
    clientmanager = BoardManager()
    clientmanager.GetChipInfo(args.sync, args.receiver, args.chip)

def func_Power(args):
    clientmanager = BoardManager()
    clientmanager.Power(args.sync, args.receiver, args.ip, args.port, args.name, args.operation)

def func_AddBoard(args):
    clientmanager = BoardManager()
    clientmanager.AddBoard(args.sync, args.receiver, args.dvb, args.ip, args.port, args.name, \
            args.arch, args.board, args.chip, \
            args.elec_port, args.elec_serial, args.mode, args.signal, \
            args.usb_device, args.usb_gxbus, args.usb_storage_type, args.usb_partition_num, \
            args.web, args.usb_wifi, args.usb_wifi_type, args.secure, \
            args.status, args.test_serial)

def func_UpdateBoard(args):
    clientmanager = BoardManager()
    clientmanager.UpdateBoard(args.sync, args.receiver, args.dvb, args.ip, args.port, args.name, \
            args.arch, args.board, args.chip, \
            args.elec_port, args.elec_serial, args.mode, args.signal, \
            args.usb_device, args.usb_gxbus, args.usb_storage_type, args.usb_partition_num, \
            args.web, args.usb_wifi, args.usb_wifi_type, args.secure, \
            args.status, args.test_serial)

def func_DeleteBoard(args):
    clientmanager = BoardManager()
    clientmanager.DeleteBoard(args.sync, args.receiver, args.ip, args.port, args.name, \
            args.board, args.chip)

def func_Start(args):
    taskmanager = TaskManager()
    if args.dvb == 'dvb':
        taskmanager.Start(args.sync, args.receiver, args.dvb, args.local_bin, args.bin_url, \
                args.local_boot_file, args.boot_file_url, args.local_boot_tool, \
                args.boot_tool_url, args.jenkins_name, args.jenkins_build, \
                args.arch, args.chip, args.board, args.os, args.mode, args.signal, \
                args.gerrit_id, args.gerrit_patch, \
                args.testlink_project, args.testlink_plan, args.testlink_build,\
                args.ip, args.port, args.name,\
                args.web, args.usb_wifi, args.usb_wifi_type, args.secure, \
                args.usb_device, args.usb_gxbus, args.usb_storage_type, args.usb_partition_num, \
                args.priority)

def func_aiStart(args):
    taskmanager = TaskManager()
    taskmanager.ai_Start(args.sync, args.receiver, args.dvb, args.type, \
            args.local_bin, args.bin_url, \
            args.jenkins_name, args.jenkins_build, args.board, \
            args.gerrit_id, args.gerrit_patch, \
            args.testlink_project, args.testlink_plan, args.testlink_build)

def func_Stop(args):
    taskmanager = TaskManager()
    taskmanager.Stop(args.sync, args.receiver, args.type, args.ip, args.port, args.name, \
            args.jenkins_name, args.jenkins_build, \
            args.arch, args.chip, args.board, args.os, args.signal, args.usb_storage_type)

def func_GetTasksInfo(args):
    taskmanager = TaskManager()
    taskmanager.GetTasksInfo(args.sync, args.receiver,  args.level)

def func_GetChipTasks(args):
    taskmanager = TaskManager()
    taskmanager.GetChipTasks(args.level, args.chip)

def func_GetBoardTasks(args):
    taskmanager = TaskManager()
    taskmanager.GetBoardTasks(args.level, args.board)

def func_GetJenkinsTask(args):
    taskmanager = TaskManager()
    taskmanager.GetJenkinsTask(args.level, args.jenkins)

def func_DelAllTask(args):
    taskmanager = TaskManager()
    taskmanager.DelAllTask(args.sync, args.receiver, args.level)

def func_DelTaskByJenkinsProject(args):
    taskmanager = TaskManager()
    taskmanager.DelTaskByJenkinsProject(args.sync, args.receiver, args.jenkins)

def func_DelTaskByClient(args):
    taskmanager = TaskManager()
    taskmanager.DelTaskByClient(args.sync, args.receiver, args.ip, args.port)

def func_DelTaskByChip(args):
    taskmanager = TaskManager()
    taskmanager.DelTaskByChip(args.sync, args.receiver, args.chip)

def func_DelTaskByBoard(args):
    taskmanager = TaskManager()
    taskmanager.DelTaskByBoard(args.sync, args.receiver, args.board)

def func_ReadServerLog(args):
    logmanager =  LogManager()
    logmanager.ReadServerLog(args.sync, args.receiver, args.level, args.key, \
            args.timebefore, args.timeafter)

def func_ReadClientLog(args):
    logmanager =  LogManager()
    logmanager.ReadClientLog(args.sync, args.receiver, args.ip, args.port, \
            args.level, args.key, args.timebefore, args.timeafter)

def func_ReadBoardLog(args):
    logmanager =  LogManager()
    logmanager.ReadBoardLog(args.sync, args.receiver, args.ip, args.port, args.board_name, \
            args.file_name, args.byte)

def func_GetBoardLogInfo(args):
    logmanager =  LogManager()
    logmanager.GetBoardLogInfo(args.sync, args.receiver, args.ip, args.port, args.board_name)

def func_CleanLog(args):
    logmanager =  LogManager()
    logmanager.CleanLog(args.sync, args.receiver, args.ip, args.port, \
            args.board_name, args.file_name)

def func_SwitchMode(args):
    clientmanager = BoardManager()
    clientmanager.SwitchMode(args.sync, args.receiver, args.ip, args.port, \
            args.board_name, args.old_mode, args.new_mode, args.force)

def func_ServerStash(args):
    taskmanager = TaskManager()
    taskmanager.ServerStash(args.sync, args.receiver)

def func_ServerResume(args):
    taskmanager = TaskManager()
    taskmanager.ServerResume(args.sync, args.receiver)

def func_GetTestResult(args):
    taskmanager = TaskManager()
    taskmanager.GetTestResult(args.sync, args.receiver, args.task)

def func_GetTestWav(args):
    fl = ftp.FtpFunctionLib(\
            Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
            FtpLoginBasicPath= './', LoginPort = 2121)
    fl.FtpLogin()
    wavlist = fl.ShowDir('Test_Entrance')
    print(wavlist)
    fl.FtpQuit()

def main():
    parent_parser = argparse.ArgumentParser(add_help = False)
    #parser.add_argument('-s', '--sync', dest = 'SYNC', default=False, help='是否为同步消息')
    parent_parser.add_argument('-s', dest = 'sync', action='store_const',const=True,\
            default=False, help='加-s 为同步消息')
    parent_parser.add_argument('-r', dest = 'receiver', type = str, default = 'server', \
            help='指定是接收方是server还是client')

    parser = argparse.ArgumentParser(prog='cmdclient')

    subparsers = parser.add_subparsers(help = 'sub-command help')

    #添加子命令 GetClientsInfo
    cmd_GetClientsInfo = subparsers.add_parser('GetClientsInfo', help='获取所有客户端信息',\
            parents = [parent_parser])
    cmd_GetClientsInfo.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_GetClientsInfo.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_GetClientsInfo.add_argument('-a', dest = 'arch', type = str, help='csky 或者 arm')
    cmd_GetClientsInfo.add_argument('-b', dest = 'board', type = str, help='板子类型')
    cmd_GetClientsInfo.add_argument('-c', dest = 'chip', type = str, help='芯片')
    cmd_GetClientsInfo.add_argument('-o', dest = 'os', type = str, help='操作系统')
    cmd_GetClientsInfo.add_argument('-sig', dest = 'signal', type = str, help='信号线')
    cmd_GetClientsInfo.add_argument('-usb', dest = 'usb_storage_type', type = str, help='FAT32 或者 NTFS')
    cmd_GetClientsInfo.set_defaults(func = func_GetClientsInfo)
    #添加子命令 GetBoardInfo 
    cmd_GetBoardInfo = subparsers.add_parser('GetBoardInfo', help='获取指定板子信息',\
            parents = [parent_parser])
    cmd_GetBoardInfo.add_argument('-b', dest = 'board', type = str, help='筛选板子类型')
    cmd_GetBoardInfo.set_defaults(func = func_GetBoardInfo)
    #添加子命令 GetChipInfo 
    cmd_GetChipInfo = subparsers.add_parser('GetChipInfo', help='获取所有客户端信息',\
            parents = [parent_parser])
    cmd_GetChipInfo.add_argument('-c', dest = 'chip', type = str, help='筛选芯片')
    cmd_GetChipInfo.set_defaults(func = func_GetChipInfo)
    #添加子命令 SetPower
    cmd_PowerOn = subparsers.add_parser('SetPower', help='控制板子电源开关',\
            parents = [parent_parser])
    cmd_PowerOn.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_PowerOn.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_PowerOn.add_argument('-n', dest = 'name', type = str, help='板子名字')
    cmd_PowerOn.add_argument('-o', dest = 'operation', type = str, help='对板子的电源操作 on/off/reboot')
    cmd_PowerOn.set_defaults(func = func_Power)
    #添加子命令 AddBoard
    cmd_AddBoard = subparsers.add_parser('AddBoard', help='添加板子',\
            parents = [parent_parser])
    cmd_AddBoard.add_argument('-d', dest = 'dvb', type = str, default = 'dvb', \
            help='指定是dvb还是ai')
    cmd_AddBoard.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_AddBoard.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_AddBoard.add_argument('-n', dest = 'name', type = str, help='板子名字')
    cmd_AddBoard.add_argument('-a', dest = 'arch', type = str, help='csky 或者 arm')
    cmd_AddBoard.add_argument('-b', dest = 'board', type = str, help='板子类型')
    cmd_AddBoard.add_argument('-c', dest = 'chip', type = str, help='芯片')
    cmd_AddBoard.add_argument('-ep', dest = 'elec_port', type = str, help='继电器端口')
    cmd_AddBoard.add_argument('-es', dest = 'elec_serial', type = str, help='继电器串口')
    cmd_AddBoard.add_argument('-m', dest = 'mode', type = str, help='板子类型， test/firmware/gxdebug')
    cmd_AddBoard.add_argument('-sig', dest = 'signal', type = str, help='信号线')
    cmd_AddBoard.add_argument('-ud', dest = 'usb_device', type = str, help='是否有USB设备')
    cmd_AddBoard.add_argument('-ug', dest = 'usb_gxbus', type = str, help='USB设备是否包含gxbus测试文件')
    cmd_AddBoard.add_argument('-ut', dest = 'usb_storage_type', type = str, help='USB 设备文件系统类型: \
        AddBoardAT32 或者 NTFS')
    cmd_AddBoard.add_argument('-upn', dest = 'usb_partition_num', type = str, help='USB设备分区数量')
    cmd_AddBoard.add_argument('-w', dest = 'web', type = str, help='是否有网线')
    cmd_AddBoard.add_argument('-uw', dest = 'usb_wifi', type = str, help='是否有USB WIFI')
    cmd_AddBoard.add_argument('-uwt', dest = 'usb_wifi_type', type = str, help='USB WIFI的型号，7601, 5370')
    cmd_AddBoard.add_argument('-sc', dest = 'secure', type = str, help='芯片是否支持安全测试')
    cmd_AddBoard.add_argument('-st', dest = 'status', type = str, help='板子运行状态')
    cmd_AddBoard.add_argument('-ts', dest = 'test_serial', type = str, help='板子串口')
    cmd_AddBoard.set_defaults(func = func_AddBoard)
    #添加子命令 UpdateBoard
    cmd_AddBoard = subparsers.add_parser('UpdateBoard', help='修改板子信息',\
            parents = [parent_parser])
    cmd_AddBoard.add_argument('-d', dest = 'dvb', type = str, default = 'dvb', \
            help='指定是dvb还是ai')
    cmd_AddBoard.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_AddBoard.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_AddBoard.add_argument('-n', dest = 'name', type = str, help='板子名字')
    cmd_AddBoard.add_argument('-a', dest = 'arch', type = str, help='csky 或者 arm')
    cmd_AddBoard.add_argument('-b', dest = 'board', type = str, help='板子类型')
    cmd_AddBoard.add_argument('-c', dest = 'chip', type = str, help='芯片')
    cmd_AddBoard.add_argument('-ep', dest = 'elec_port', type = str, help='继电器端口')
    cmd_AddBoard.add_argument('-es', dest = 'elec_serial', type = str, help='继电器串口')
    cmd_AddBoard.add_argument('-m', dest = 'mode', type = str, help='板子类型， test/firmware/gxdebug')
    cmd_AddBoard.add_argument('-sig', dest = 'signal', type = str, help='信号线')
    cmd_AddBoard.add_argument('-ud', dest = 'usb_device', type = str, help='是否有USB设备')
    cmd_AddBoard.add_argument('-ug', dest = 'usb_gxbus', type = str, help='USB设备是否包含gxbus测试文件')
    cmd_AddBoard.add_argument('-ut', dest = 'usb_storage_type', type = str, help='USB 设备文件系统类型: \
        AddBoardAT32 或者 NTFS')
    cmd_AddBoard.add_argument('-upn', dest = 'usb_partition_num', type = str, help='USB设备分区数量')
    cmd_AddBoard.add_argument('-w', dest = 'web', type = str, help='是否有网线')
    cmd_AddBoard.add_argument('-uw', dest = 'usb_wifi', type = str, help='是否有USB WIFI')
    cmd_AddBoard.add_argument('-uwt', dest = 'usb_wifi_type', type = str, help='USB WIFI的型号，7601, 5370')
    cmd_AddBoard.add_argument('-sc', dest = 'secure', type = str, help='芯片是否支持安全测试')
    cmd_AddBoard.add_argument('-st', dest = 'status', type = str, help='板子运行状态')
    cmd_AddBoard.add_argument('-ts', dest = 'test_serial', type = str, help='板子串口')
    cmd_AddBoard.set_defaults(func = func_UpdateBoard)
    #添加子命令 DeleteBoard
    cmd_DeleteBoard = subparsers.add_parser('DeleteBoard', help='删除板子',\
            parents = [parent_parser])
    cmd_DeleteBoard.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_DeleteBoard.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_DeleteBoard.add_argument('-n', dest = 'name', type = str, help='板子名字')
    cmd_DeleteBoard.add_argument('-b', dest = 'board', type = str, help='筛选板子类型')
    cmd_DeleteBoard.add_argument('-c', dest = 'chip', type = str, help='筛选芯片')
    cmd_DeleteBoard.set_defaults(func = func_DeleteBoard)
    #添加子命令 aiStart
    cmd_Start = subparsers.add_parser('aiStart', help='提交AI测试',\
            parents = [parent_parser])
    cmd_Start.add_argument('-d', dest = 'dvb', type = str, default = 'dvb', \
            help='指定是dvb还是ai')
    cmd_Start.add_argument('-t', dest = 'type', type = str, \
            help='任务类型, record/algorithm/solution/API')
    cmd_Start.add_argument('-lb', dest = 'local_bin', type = str, help='指定本地bin文件')
    cmd_Start.add_argument('-burl', dest = 'bin_url', type = str, \
            help='指定bin文件所在的ftp路径')
    cmd_Start.add_argument('-jn', dest = 'jenkins_name', type = str, help='指定jenkins名称')
    cmd_Start.add_argument('-jb', dest = 'jenkins_build', type = str, help='指定jenkins构建')
    cmd_Start.add_argument('-b', dest = 'board', type = str, help='板子类型')
    cmd_Start.add_argument('-gid', dest = 'gerrit_id', type = str, help='gerrit_id')
    cmd_Start.add_argument('-gp', dest = 'gerrit_patch', type = str, help='gerrit_patch')
    cmd_Start.add_argument('-tj', dest = 'testlink_project', type = str, help='testlink项目')
    cmd_Start.add_argument('-tp', dest = 'testlink_plan', type = str, help='testlink测试计划')
    cmd_Start.add_argument('-tb', dest = 'testlink_build', type = str, help='testlink测试构建')
    cmd_Start.set_defaults(func = func_aiStart)
    #添加子命令 Start
    cmd_Start = subparsers.add_parser('Start', help='提交STB测试',\
            parents = [parent_parser])
    cmd_Start.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_Start.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_Start.add_argument('-n', dest = 'name', type = str, help='板子名字')
    cmd_Start.add_argument('-d', dest = 'dvb', type = str, default = 'dvb', \
            help='指定是dvb还是ai')
    cmd_Start.add_argument('-lb', dest = 'local_bin', type = str, help='指定本地bin文件')
    cmd_Start.add_argument('-burl', dest = 'bin_url', type = str, \
            help='指定bin文件所在的ftp路径')
    cmd_Start.add_argument('-lf', dest = 'local_boot_file', type = str, help='指定本地boot_file')
    cmd_Start.add_argument('-furl', dest = 'boot_file_url', type = str, \
            help='指定boot_file所在的ftp路径')
    cmd_Start.add_argument('-lt', dest = 'local_boot_tool', type = str, help='指定本地boot_tool')
    cmd_Start.add_argument('-turl', dest = 'boot_tool_url', type = str, \
            help='指定boot_tool所在的ftp路径')
    cmd_Start.add_argument('-jn', dest = 'jenkins_name', type = str, help='指定jenkins名称')
    cmd_Start.add_argument('-jb', dest = 'jenkins_build', type = str, help='指定jenkins构建')
    cmd_Start.add_argument('-a', dest = 'arch', type = str, help='csky 或者 arm')
    cmd_Start.add_argument('-b', dest = 'board', type = str, help='板子类型')
    cmd_Start.add_argument('-c', dest = 'chip', type = str, help='芯片')
    cmd_Start.add_argument('-o', dest = 'os', type = str, help='操作系统')
    cmd_Start.add_argument('-m', dest = 'mode', type = str, help='板子类型, test还是firmware')
    cmd_Start.add_argument('-sig', dest = 'signal', type = str, help='信号线')
    cmd_Start.add_argument('-ud', dest = 'usb_device', type = str, help='是否有USB设备')
    cmd_Start.add_argument('-ug', dest = 'usb_gxbus', type = str, help='USB设备是否包含gxbus测试文件')
    cmd_Start.add_argument('-ut', dest = 'usb_storage_type', type = str, help='USB 设备文件系统类型: \
            FAT32 或者 NTFS')
    cmd_Start.add_argument('-upn', dest = 'usb_partition_num', type = str, help='USB设备分区数量')
    cmd_Start.add_argument('-w', dest = 'web', type = str, help='是否有网线')
    cmd_Start.add_argument('-uw', dest = 'usb_wifi', type = str, help='是否有USB WIFI')
    cmd_Start.add_argument('-uwt', dest = 'usb_wifi_type', type = str, help='USB WIFI的型号，7601, 5370')
    cmd_Start.add_argument('-sc', dest = 'secure', type = str, help='芯片是否支持安全测试')
    cmd_Start.add_argument('-gid', dest = 'gerrit_id', type = str, help='gerrit_id')
    cmd_Start.add_argument('-gp', dest = 'gerrit_patch', type = str, help='gerrit_patch')
    cmd_Start.add_argument('-tj', dest = 'testlink_project', type = str, help='testlink项目')
    cmd_Start.add_argument('-tp', dest = 'testlink_plan', type = str, help='testlink测试计划')
    cmd_Start.add_argument('-tb', dest = 'testlink_build', type = str, help='testlink测试构建')
    cmd_Start.add_argument('-prio', dest = 'priority', type = str, nargs = '+', help='板子分配优先级')
    cmd_Start.set_defaults(func = func_Start)
    #添加子命令 Stop
    cmd_Stop = subparsers.add_parser('Stop', help='停止测试',\
            parents = [parent_parser])
    cmd_Stop.add_argument('-t', dest = 'type', type = str, help='all/jenkins/specific/filter')
    cmd_Stop.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_Stop.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_Stop.add_argument('-n', dest = 'name', type = str, help='板子名字')
    cmd_Stop.add_argument('-jn', dest = 'jenkins_name', type = str, help='指定jenkins名称')
    cmd_Stop.add_argument('-jb', dest = 'jenkins_build', type = str, help='指定jenkins构建')
    cmd_Stop.add_argument('-a', dest = 'arch', type = str, help='csky 或者 arm')
    cmd_Stop.add_argument('-b', dest = 'board', type = str, help='板子类型')
    cmd_Stop.add_argument('-c', dest = 'chip', type = str, help='芯片')
    cmd_Stop.add_argument('-o', dest = 'os', type = str, help='操作系统')
    cmd_Stop.add_argument('-sig', dest = 'signal', type = str, help='信号线')
    cmd_Stop.add_argument('-usb', dest = 'usb_storage_type', type = str, help='FAT32 或者 NTFS')
    cmd_Stop.set_defaults(func = func_Stop)
    #添加子命令 GetTasksInfo
    cmd_GetTasksInfo = subparsers.add_parser('GetTasksInfo', help='获取服务端任务队列信息',\
            parents = [parent_parser])
    cmd_GetTasksInfo.add_argument('-l', dest = 'level', type = str, help='任务优先级 all/0/1/2/3')
    cmd_GetTasksInfo.set_defaults(func = func_GetTasksInfo)
    #添加子命令 GetChipTasks
    cmd_GetChipTasks = subparsers.add_parser('GetChipTasks', help='根据芯片筛选任务',\
            parents = [parent_parser])
    cmd_GetChipTasks.add_argument('-c', dest = 'chip', type = str, help='筛选芯片')
    cmd_GetChipTasks.add_argument('-l', dest = 'level', type = str, default = 'all', \
            help='任务优先级 all/0/1/2/3')
    cmd_GetChipTasks.set_defaults(func = func_GetChipTasks)
    #添加子命令 GetBoardTasks
    cmd_GetBoardTasks = subparsers.add_parser('GetBoardTasks', help='根据板子筛选任务',\
            parents = [parent_parser])
    cmd_GetBoardTasks.add_argument('-b', dest = 'board', type = str, help='筛选板子类型')
    cmd_GetBoardTasks.add_argument('-l', dest = 'level', type = str, default = 'all', \
            help='任务优先级 all/0/1/2/3')
    cmd_GetBoardTasks.set_defaults(func = func_GetBoardTasks)
    #添加子命令 GetJenkinsTask
    cmd_GetJenkinsTask = subparsers.add_parser('GetJenkinsTask', help='根据jenkins筛选任务',\
            parents = [parent_parser])
    cmd_GetJenkinsTask.add_argument('-j', dest = 'jenkins', type = str, help='jenkins项目')
    cmd_GetJenkinsTask.add_argument('-l', dest = 'level', type = str, default = 'all', \
            help='任务优先级 all/0/1/2/3')
    cmd_GetJenkinsTask.set_defaults(func = func_GetJenkinsTask)
    #添加子命令 DelAllTask
    cmd_DelAllTask = subparsers.add_parser('DelAllTask', help='删除全部任务',\
            parents = [parent_parser])
    cmd_DelAllTask.add_argument('-l', dest = 'level', type = str, help='任务优先级 all/0/1/2/3')
    cmd_DelAllTask.set_defaults(func = func_DelAllTask)
    #添加子命令 DelTaskByJenkinsProject
    cmd_DelTaskByJenkinsProject = subparsers.add_parser('DelTaskByJenkinsProject', \
            help='删除jenkins任务', parents = [parent_parser])
    cmd_DelTaskByJenkinsProject.add_argument('-j', dest = 'jenkins', type = str, \
            help='jenkins项目')
    cmd_DelTaskByJenkinsProject.set_defaults(func = func_DelTaskByJenkinsProject)
    #添加子命令 DelTaskByClient
    cmd_DelTaskByClient = subparsers.add_parser('DelTaskByClient', \
            help='删除指定客户端任务', parents = [parent_parser])
    cmd_DelTaskByClient.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_DelTaskByClient.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_DelTaskByClient.set_defaults(func = func_DelTaskByClient)
    #添加子命令 DelTaskByChip
    cmd_DelTaskByChip = subparsers.add_parser('DelTaskByChip', \
            help='删除指定芯片任务', parents = [parent_parser])
    cmd_DelTaskByChip.add_argument('-c', dest = 'chip', type = str, help='筛选芯片')
    cmd_DelTaskByChip.set_defaults(func = func_DelTaskByChip)
    #添加子命令 DelTaskByBoard
    cmd_DelTaskByBoard = subparsers.add_parser('DelTaskByBoard', \
            help='删除指定板级任务', parents = [parent_parser])
    cmd_DelTaskByBoard.add_argument('-b', dest = 'board', type = str, help='筛选板子类型')
    cmd_DelTaskByBoard.set_defaults(func = func_DelTaskByClient)
    #添加子命令 ReadSerLogByLevel
    cmd_ReadSerLogByLevel = subparsers.add_parser('ReadServerLog', \
            help='获取服务端log', parents = [parent_parser])
    cmd_ReadSerLogByLevel.add_argument('-l', dest = 'level', type = str, help='log等级')
    cmd_ReadSerLogByLevel.add_argument('-k', dest = 'key', type = str, help='log关键字')
    cmd_ReadSerLogByLevel.add_argument('-tb', dest = 'timebefore', type = str, \
            help='在指定之间之前')
    cmd_ReadSerLogByLevel.add_argument('-ta', dest = 'timeafter', type = str, \
            help='在指定之间之后')
    cmd_ReadSerLogByLevel.set_defaults(func = func_ReadServerLog)
    #添加子命令 ReadClientLogByLevel
    cmd_ReadClientLogByLevel = subparsers.add_parser('ReadClientLog', \
            help='获取客户端log', parents = [parent_parser])
    cmd_ReadClientLogByLevel.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_ReadClientLogByLevel.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_ReadClientLogByLevel.add_argument('-l', dest = 'level', type = str, help='log等级')
    cmd_ReadClientLogByLevel.add_argument('-k', dest = 'key', type = str, help='log关键字')
    cmd_ReadClientLogByLevel.add_argument('-tb', dest = 'timebefore', type = str, \
            help='在指定之间之前')
    cmd_ReadClientLogByLevel.add_argument('-ta', dest = 'timeafter', type = str, \
            help='在指定之间之后')
    cmd_ReadClientLogByLevel.set_defaults(func = func_ReadClientLog)
    #添加子命令 ReadBoardLog
    cmd_ReadBoardLog = subparsers.add_parser('ReadBoardLog', \
            help='获取板子log', parents = [parent_parser])
    cmd_ReadBoardLog.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_ReadBoardLog.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_ReadBoardLog.add_argument('-n', dest = 'board_name', type = str, help='板子名字')
    cmd_ReadBoardLog.add_argument('-f', dest = 'file_name', type = str, help='文件名字')
    cmd_ReadBoardLog.add_argument('-b', dest = 'byte', type = str, help='文件大小')
    cmd_ReadBoardLog.set_defaults(func = func_ReadBoardLog)
    #添加子命令 GetBoardLogInfo
    cmd_GetBoardLogInfo = subparsers.add_parser('GetBoardLogInfo', \
            help='查询板子log文件信息', parents = [parent_parser])
    cmd_GetBoardLogInfo.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_GetBoardLogInfo.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_GetBoardLogInfo.add_argument('-n', dest = 'board_name', type = str, help='板子名字')
    cmd_GetBoardLogInfo.set_defaults(func = func_GetBoardLogInfo)
    #添加子命令 CleanLog
    cmd_CleanLog = subparsers.add_parser('CleanLog', \
            help='删除板子log文件', parents = [parent_parser])
    cmd_CleanLog.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_CleanLog.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_CleanLog.add_argument('-n', dest = 'board_name', type = str, help='板子名字')
    cmd_CleanLog.add_argument('-f', dest = 'file_name', type = str, help='文件名字')
    cmd_CleanLog.set_defaults(func = func_CleanLog)
    #添加子命令 SwitchMode
    cmd_SwitchMode = subparsers.add_parser('SwitchMode', \
            help='切换板子模式', parents = [parent_parser])
    cmd_SwitchMode.add_argument('-i', dest = 'ip', type = str, help='指定客户端ip')
    cmd_SwitchMode.add_argument('-p', dest = 'port', type = str, help='指定客户端端口')
    cmd_SwitchMode.add_argument('-n', dest = 'board_name', type = str, help='板子名字')
    cmd_SwitchMode.add_argument('-old', dest = 'old_mode', type = str, help='原始模式')
    cmd_SwitchMode.add_argument('-new', dest = 'new_mode', type = str, help='修改模式')
    cmd_SwitchMode.add_argument('-f', dest = 'force', type = str, help='强制修改')
    cmd_SwitchMode.set_defaults(func = func_SwitchMode)
    #添加子命令 ServerStash
    cmd_ServerStash = subparsers.add_parser('ServerStash', \
            help='停止服务器运行, 暂存任务, 停止客户端上报', parents = [parent_parser])
    cmd_ServerStash.set_defaults(func = func_ServerStash)
    #添加子命令 ServerResume
    cmd_ServerResume = subparsers.add_parser('ServerResume', \
            help='恢复服务器运行, 恢复任务，恢复客户端上报', parents = [parent_parser])
    cmd_ServerResume.set_defaults(func = func_ServerResume)
    #添加子命令 GetTestResult
    cmd_GetTestResult = subparsers.add_parser('GetTestResult', \
            help='获取测试结果', parents = [parent_parser])
    cmd_GetTestResult.add_argument('-t', dest = 'task', type = str, help='指定测试任务')
    cmd_GetTestResult.set_defaults(func = func_GetTestResult)
    #添加子命令 GetTestWav
    cmd_GetTestWav = subparsers.add_parser('GetTestWav', \
            help='获取测试语料', parents = [parent_parser])
    cmd_GetTestWav.set_defaults(func = func_GetTestWav)

    
    args = parser.parse_args()
    args.func(args)
    
if __name__ == '__main__':
    main()
    
