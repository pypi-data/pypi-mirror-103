#!/usr/bin/python3
#encoding:utf-8

import copy
import json
import signal
import re
import serial
import sys
import os
import time
import socket
import ast
import multiprocessing
import threading
from goto import with_goto # pip3 install goto_statement
import subprocess
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR,"../server/modules"))
import board_manager
import log
from log import RunningLog
import ftp
import sendmsg
from modules import reboot
from modules import redmine
from modules import gerrit
from modules import testlink
from modules import detect
from multiprocessing.managers import BaseManager
import psutil
if (os.path.exists("/usr/local/lib/python3.6/dist-packages/SendEmail.py")):
    #from SendEmail import send_email
    import SendEmail
    enable_email = 1
else:
    enable_email = 0

class LogManager(BaseManager):
    pass

def logManager():
    m = LogManager()
    m.start()
    return m

class MyThread(threading.Thread):
    def __init__(self, target, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.target = target
        self.args = args
        self.result = self.target(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class AutoClient():
    def __init__(self, remote_ip, remote_port, remote_heartbeat_port, email_receivers):
        LogManager.register('runninglog', RunningLog)
        manager = logManager()
        self.rl = manager.runninglog() # 进程间共享
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.remote_heartbeat_port = remote_heartbeat_port
        self.local_host = os.environ.get('CLIENT_IP')
        self.local_port = os.environ.get('CLIENT_PORT')
        #self.local_host = '127.0.0.1'
        #self.local_port = 5000
        self.server_control = multiprocessing.Manager().dict()
        self.server_control['operation'] = ''
        self.email_receivers = email_receivers

        self.board_change = 0
        self.yaml_file = 'a.yaml'
        self.bc = board_manager.BoardConfig(self.yaml_file)
        self.bc.read_yaml()
        self.rl.write(self.bc.total_config, 'debug', 'MAIN {}'.format(self.recursive_get_pid(os.getpid())))
        self.sm = sendmsg.SendMsg()

        self.message_format = {
            "ip":"",
            "port":"",
            "priority":3,
            "sync":"",
            "receiver":"",
            "name":"",
            "message_content":{},
        }

    def check_download_log_success(self, download_log):
        if os.path.exists(download_log):
            fileobj = open(download_log, errors='replace')
            data = fileobj.read()
            download_success_flag = False
            if (re.findall(r"Write to flash address", data)):
                download_success_flag = True
            fileobj.close()
            return download_success_flag
        else:
            return False

    @with_goto
    def download_sub(self, reboot, device, port, cmd, use_board):
        retry_times = 0
        max_retry_times = 5
        download_timeout = 30 * 60
        download_time = 0

        label .start_download
        self.rl.write('start download', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
        reboot.power_off(device = device, port = port)

        process = subprocess.Popen(cmd, shell = True, close_fds = True, preexec_fn = os.setsid)
        self.rl.write('download process pid %d'%process.pid, 'debug', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
        # 记录烧写进程 ID
        self.bc.read_yaml()
        self.bc.write_board_boot_process_id(use_board, process.pid+1)
        time.sleep(5)
        reboot.power_on(device = device, port = port)

        time_start = int(time.time())
        while True:
            download_time = int(time.time()) - time_start
            if process.poll() != None: #  子进程终止
                if self.check_download_log_success(cmd.split(' ')[-1]):
                    return True
            elif download_time >= download_timeout:
                if retry_times == max_retry_times:
                    self.rl.write('download retry max times', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                    os.killpg(process.pid, signal.SIGUSR1)
                    return False
                else:
                    self.rl.write('download retry', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                    retry_times += 1
                    os.killpg(process.pid, signal.SIGUSR1)
                    time.sleep(3)
                    goto .start_download

    def streamxpress_process(self, share_dict_stop, share_list_streamxpress):
        while True:
            if len(share_list_streamxpress) != 0:
                pass
            else:
                if share_dict_stop['stop_test'] == True:
                    return True

    def testlink_process(self, share_dict_stop, share_list_testlink, testlink_info):
        #testlink_url = 'http://192.168.110.254/testlink/lib/api/xmlrpc.php'
        #testlink_key = 'b5968cdffc0c9bc6d0dd80267dc170e2'
        testlink_product = testlink_info['testlink_project']
        testlink_plan = testlink_info['testlink_plan']
        testlink_build = testlink_info['testlink_build']
        testlink_url = 'http://192.168.110.246/testlink/lib/api/xmlrpc.php'
        testlink_key = '3eedeb22542762c580acbeec406505cb'
        #testlink_product = 'GoXceed_V1.9'
        #testlink_plan = 'GoXceed_v1.9.8-7_alpha3_gx6605s_6605s_ecos'
        #testlink_build = '第一轮'

        tl_server = testlink.AutotestTestlinkThreading(testlink_url, testlink_key, testlink_product, testlink_plan, testlink_build)
        if tl_server.thread_start() == False:
            self.rl.write('testlink connect error!!!', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
        while True:
            if len(share_list_testlink) != 0:
                issue = share_list_testlink.pop(0)
                #self.rl.write('testlink issue {}'.format(issue), 'debug', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                self.rl.write('testlink issue {}'.format(issue), 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                ret = tl_server.report_result(issue['case_id'], issue['case_result'], issue['redmine_issue_id'])
                self.rl.write('testlink process ret {}'.format(ret), 'debug', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
            else:
                if share_dict_stop['stop_test'] == True:
                    return True

    def redmine_process(self, share_dict_stop, share_list_redmine):
        gx_redmine = redmine.GxRedmine()
        while True:
            time.sleep(1)
            if len(share_list_redmine) != 0:
                issue = share_list_redmine.pop(0)
                self.rl.write('testlink issue {}'.format(issue), 'debug', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                gx_redmine.new_issue(issue['subject'], issue['description'], issue['log_name'], issue['log_fd'])
            else:
                if share_dict_stop['stop_test'] == True:
                    return True
    def redmine_prepare(self, share_list, subject, description, log_name, log_fd):
        #issue = {'subject':subject, 'description':description, 'log_name':log_name, 'log_fd':log_fd}
        issue = {'subject':subject, 'description':description, 'log_name':log_name, 'log_fd':'log_fd reserve'} # TODO log_fd 放入字典后类型改变导致无法使用
        share_list.append(issue)

    def testlink_prepare(self, share_list, case_id, case_result, redmine_issue_id):
        issue = {'case_id':case_id, 'case_result':case_result, 'redmine_issue_id':redmine_issue_id}
        share_list.append(issue)

    def crash_handling(self, running_case, dead_msg, share_list_redmine, log_name, log_fd, share_list_testlink, redmine_issue_id, reboot, device, port, share_dict_stop, have_quesion, board_name, gx_gerrit, gerrit_info):
        print('crash handling start')
        if running_case:
            subject = running_case + " 死机"
        else:
            subject = '未执行用例，死机'
        s_len = len(dead_msg)
        msg = dead_msg[(s_len-8192 if(s_len-8192>0) else 0):]
        description = "<pre>\n" + msg + "\n</pre>"
        SendEmail.send_email(description, subject, self.email_receivers)
        self.redmine_prepare(share_list_redmine, subject, description, log_name, log_fd)
        if running_case:
            casenums = self.get_case_id_list(running_case)
            case_status = 'f'
            redmine_issue_id = ''
            if casenums == None:
                print("this case has no num in it's name: {}".format(running_case))
            else:
                for case_id in casenums:
                    self.testlink_prepare(share_list_testlink, case_id, case_status, redmine_issue_id)
            reboot.reboot(device = device, port = port)
        else:
            share_dict_stop['stop_test'] = True
            code_review = -1 if have_quesion else 1
            gx_gerrit.code_review(gerrit_info['gerrit_id'], gerrit_info['gerrit_patch'], code_review = code_review)
            self.rl.write('crash before start test, test finish', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
            self.bc.read_yaml()
            use_board = [self.local_host, self.local_port, board_name]
            self.bc.update_board_status(use_board, 'idle')
            self.bc.update_board_running_info(use_board, 'stop')
            self.update_client_status()
        print('crash handling end')

    def get_caseid_byname(self,casename):
        alist = re.findall('(?<=from_)\d+', casename)
        blist = re.findall('(?<=to_)\d+', casename)
        clist = re.findall('(?<=_)\d+', casename)
        dlist = re.findall('(?<=_n)\d+', casename)
        idlist = []
        if len(alist) != len(blist):
            return None
        for i in range(len(clist)):
            if clist[i] not in alist and clist[i] not in blist:
                idlist.append(clist[i])
        for i in range(len(alist)):
            if int(alist[i]) > int(blist[i]):
                for num in range(int(blist[i]),int(alist[i])+1):
                    idlist.append(str(num))
            if int(blist[i]) > int(alist[i]):
                for num in range(int(alist[i]),int(blist[i])+1):
                    idlist.append(str(num))
            if int(blist[i]) == int(alist[i]):
                return None
        for i in range(len(dlist)):
            if dlist[i] not in idlist:
                idlist.append(dlist[i])
        if idlist == []:
            return None
        return idlist

    def get_case_id_list(self, test_reslut_str):
        caseid_num = self.get_caseid_byname(test_reslut_str)
        if caseid_num == None:
            print("this test_reslut_str has no num in it's name:")
            print(test_reslut_str)
            return None
        return caseid_num

    def log_process(self, share_dict_stop, share_list_redmine, share_list_testlink, share_list_streamxpress, test_serial, gerrit_info, reboot, device, port, board_name):
        ISOTIMEFORMAT = '%Y-%m-%d-%H-%M-%S'
        serial_obj = serial.Serial(test_serial, 115200, timeout = 10)
        log_file_path = 'log'
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        #logfilename = self.local_host + "_" + self.type + "_" + self.board_info + "_" + time.strftime(ISOTIMEFORMAT, time.localtime( time.time() ) ) + ".txt"
        logfilename = '{}_{}_{}_{}.txt'.format(self.local_host, 'gxbus', board_name, time.strftime(ISOTIMEFORMAT, time.localtime(time.time())))
        logfilefullname = '{}/{}'.format(log_file_path, logfilename)
        log_fd = open(logfilefullname, 'w')
        dead_msg = ''
        dead_msg_line = 0
        timeout_counter = 0
        running_case = ''
        d_print_count = 0
        minifs_print_count = 0
        overflow_print_count = 0
        have_quesion = False

        gx_gerrit = gerrit.GxGerrit()
        line_num = 0

        while True:
            s = serial_obj.readline().decode('utf-8', errors='replace')
            if s:
                timeout_counter = 0
                #print(s, end='')
                log_fd.write(time.strftime(ISOTIMEFORMAT, time.localtime(time.time())) + " " + s)
                line_num += 1
                if line_num >= 200:
                    line_num = 0
                    log_fd.flush()
                if dead_msg_line == 20000:
                    dead_msg = ""
                    dead_msg_line = 0
                dead_msg += s
                dead_msg_line += 1

                # 检测到用例开始打印
                if re.findall(r"case start: .+", s) or re.findall(r"\[Run     \] .+ ...", s):
                    # 记录当前执行用例名称
                    case_start = re.findall(r"case start: (.+)",s)
                    if not case_start:
                        case_start = re.findall(r"\[Run     \] .+ ...", s)
                    running_case = case_start[0]
                    # 特殊错误打印计数器清零
                    d_print_count = 0
                    minifs_print_count = 0
                    overflow_print_count = 0
                    
                # 检测到用例结束打印
                elif re.findall(r"testcase---", s) or re.findall(r"\[  FAILED\] (.+)", s) or re.findall(r"\[OK\] (.+)", s):
                    if re.findall(r"testcase---(.+)---pass---", s) or re.findall(r"\[OK\] (.+)", s):
                        #self.testlink_prepare(share_list_testlink, self.get_case_id_list(running_case), 'p', redmine_issue_id)
                        self.testlink_prepare(share_list_testlink, self.get_case_id_list(running_case), 'p', 'reserve') # redmine_issue_id reserve
                    if re.findall(r"testcase---(.+)---failed---", s) or re.findall(r"\[  FAILED\] (.+)", s):
                        #self.testlink_prepare(share_list_testlink, self.get_case_id_list(running_case), 'f', redmine_issue_id)
                        self.testlink_prepare(share_list_testlink, self.get_case_id_list(running_case), 'f', 'reserve')
                    if re.findall(r"testcase---(.+)---lock---", s):
                        #self.testlink_prepare(share_list_testlink, self.get_case_id_list(running_case), 'b', redmine_issue_id)
                        self.testlink_prepare(share_list_testlink, self.get_case_id_list(running_case), 'b', 'reserve')
                # 检测到特殊错误打印
                elif re.findall(r"d!!!", s):
                    d_print_count += 1
                    if d_print_count >= 10000:
                        have_quesion = True
                        d_print_count = 0
                        minifs_print_count = 0
                        overflow_print_count = 0
                        self.crash_handling(running_case, dead_msg, share_list_redmine, logfilefullname, log_fd, share_list_testlink, 'reserve', reboot, device, port, share_dict_stop, have_quesion, board_name, gx_gerrit, gerrit_info)
                        if not running_case:
                            return False
                elif re.findall(r"minifs \[/view_info_db\] create", s):
                    minifs_print_count += 1
                    if overflow_print_count >= 1000:
                        have_quesion = True
                        d_print_count = 0
                        minifs_print_count = 0
                        overflow_print_count = 0
                        self.crash_handling(running_case, dead_msg, share_list_redmine, logfilefullname, log_fd, share_list_testlink, 'reserve', reboot, device, port, share_dict_stop, have_quesion, board_name, gx_gerrit, gerrit_info)
                        if not running_case:
                            return False
                elif re.findall(r"decode_writed_callback 1508 overflow 1", s):
                    overflow_print_count += 1
                    if minifs_print_count >= 1000:
                        have_quesion = True
                        d_print_count = 0
                        minifs_print_count = 0
                        overflow_print_count = 0
                        self.crash_handling(running_case, dead_msg, share_list_redmine, logfilefullname, log_fd, share_list_testlink, 'reserve', reboot, device, port, share_dict_stop, have_quesion, board_name, gx_gerrit, gerrit_info)
                        if not running_case:
                            return False
                elif re.findall(r"Kernel panic", s) or re.findall(r"rcu_sched self-detected stall on", s):
                    have_quesion = True
                    d_print_count = 0
                    minifs_print_count = 0
                    overflow_print_count = 0
                    self.crash_handling(running_case, dead_msg, share_list_redmine, logfilefullname, log_fd, share_list_testlink, 'reserve', reboot, device, port, share_dict_stop, have_quesion, board_name, gx_gerrit, gerrit_info)
                    if not running_case:
                        return False
                elif re.findall(r"failed description:(.+); file:", s, re.S):
                    have_quesion = True
                    subject = re.findall(r"failed description:(.+); file:", s, re.S)[0]
                    description = re.findall(r"file:.+", s)[0]
                    s_len = len(dead_msg)
                    msg = dead_msg[(s_len-8192 if(s_len-8192>0) else 0):]
                    description += "\n<pre>\n" + msg + "\n</pre>"
                    self.redmine_prepare(share_list_redmine, subject, description, logfilefullname, log_fd)

                elif re.findall(r"gxtest_reboot", s):
                    reboot.reboot(device = device, port = port)
                elif re.findall(r"TODO调制器交互", s):
                    pass
                elif re.findall(r"ALL_CASE_HAVE_RUN", s) or re.findall(r"CMock: Finished", s):
                    share_dict_stop['stop_test'] = True
                    code_review = -1 if have_quesion else 1
                    gx_gerrit.code_review(gerrit_info['gerrit_id'], gerrit_info['gerrit_patch'], code_review = code_review)
                    self.rl.write('test finish', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                    self.bc.read_yaml()
                    use_board = [self.local_host, self.local_port, board_name]
                    self.bc.update_board_status(use_board, 'idle')
                    self.bc.update_board_running_info(use_board, 'stop')
                    self.update_client_status()
                    return True
            else:
                timeout_counter += 1
                if timeout_counter >= 180: # 180*10/60=30 分钟内没有打印，算做死机
                    have_quesion = True
                    d_print_count = 0
                    minifs_print_count = 0
                    overflow_print_count = 0
                    self.crash_handling(running_case, dead_msg, share_list_redmine, logfilefullname, log_fd, share_list_testlink, 'reserve', reboot, device, port, share_dict_stop, have_quesion, board_name, gx_gerrit, gerrit_info)
                    if not running_case:
                        return False

    def getbin(self, boot_tool_url, boot_file_url, bin_file_url, bin_file, boot_file, boot_tool):
        dir_bin_file = 'AutoTestBin/{}'.format(os.path.dirname(bin_file_url))
        if not os.path.exists(dir_bin_file):
            os.makedirs(dir_bin_file)

        gx_ftp = ftp.FtpFunctionLib(FtpLoginBasicPath='public/ftp/AutoTestBin/')
        gx_ftp.FtpLogin('')
        gx_ftp.DownloadFile(bin_file_url, bin_file)
        gx_ftp.DownloadFile(boot_file_url, boot_file)
        gx_ftp.DownloadFile(boot_tool_url, boot_tool)
        gx_ftp.FtpQuit()

    def download(self, reboot, test_board_serial, control_board_serial, control_board_port, bin_file, boot_file, boot_tool, use_board):
        download_log = os.environ['HOME'] + "/download_log_" + test_board_serial.split("/")[2]

        cmd = 'chmod +x {}'.format(boot_tool)
        os.system(cmd)
        cmd = './' + boot_tool + " -b " + boot_file + " -d " + test_board_serial + " -c serialdown 0x0     " + bin_file + " > " + download_log

        power_on_flag = [0]
        exit_flag = [0]
        pid = [0]
        t_download = MyThread(target = self.download_sub, args = (reboot, control_board_serial, control_board_port, cmd, use_board))
        t_download.start()
        t_download.join()

        return t_download.get_result()

    def test_process(self, msg, reboot):
        boot_tool_url = msg['message_content']['dvb_info']['test_info']['boot_tool_url']
        boot_file_url = msg['message_content']['dvb_info']['test_info']['boot_file_url']
        bin_file_url = msg['message_content']['dvb_info']['test_info']['bin_url']

        bin_file = 'AutoTestBin/{}'.format(bin_file_url)
        boot_file = 'AutoTestBin/{}'.format(boot_file_url)
        boot_tool = 'AutoTestBin/{}'.format(boot_tool_url)

        self.getbin(boot_tool_url, boot_file_url, bin_file_url, bin_file, boot_file, boot_tool)

        board_name = msg['message_content']['dvb_info']['specific_board']['board_name']

        gerrit_info = msg['message_content']['dvb_info']['gerrit_info']
        testlink_info = msg['message_content']['dvb_info']['testlink_info']

        self.bc.read_yaml()
        board_info = self.bc.get_info_by_board_name(board_name)
        client_name = list(board_info.keys())[0]
        test_board_serial = board_info[client_name][board_name]['test_serial']
        control_board_serial = board_info[client_name][board_name]['electric_relay_serial']
        control_board_port = board_info[client_name][board_name]['electric_relay_port']

        self.bc.read_yaml()
        use_board = [self.local_host, self.local_port, board_name]
        self.bc.write_board_jenkins_project_name(use_board, msg['message_content']['dvb_info']['jenkins_info']['jenkins_project_name'])
        self.bc.write_board_jenkins_build(use_board, msg['message_content']['dvb_info']['jenkins_info']['jenkins_build_id'])
        self.bc.update_board_status(use_board, 'busy')
        self.bc.update_board_running_info(use_board, 'downloading')
        self.update_client_status()

        ret = self.download(reboot, test_board_serial, control_board_serial, control_board_port, bin_file, boot_file, boot_tool, use_board)

        share_dict_stop = multiprocessing.Manager().dict()
        share_dict_stop['stop_test'] = False
        share_list_redmine = multiprocessing.Manager().list()
        share_list_testlink = multiprocessing.Manager().list()
        share_list_streamxpress = multiprocessing.Manager().list()

        if ret == True:
            # 清除烧写进程 ID
            self.bc.read_yaml()
            self.bc.write_board_boot_process_id(use_board, '')
            self.rl.write('download success', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
            p_testlink_process = multiprocessing.Process(target = self.testlink_process, args = (share_dict_stop, share_list_testlink, testlink_info))
            p_streamxpress_process = multiprocessing.Process(target = self.streamxpress_process, args = (share_dict_stop, share_list_streamxpress))
            p_redmine_process = multiprocessing.Process(target = self.redmine_process, args = (share_dict_stop, share_list_redmine))
            p_log_process = multiprocessing.Process(target = self.log_process, args = (share_dict_stop, share_list_redmine, share_list_testlink, share_list_streamxpress,  test_board_serial, gerrit_info, reboot, control_board_serial, control_board_port, board_name))

            p_testlink_process.start()
            p_streamxpress_process.start()
            p_redmine_process.start()
            p_log_process.start()

            reboot.reboot(device = control_board_serial, port = control_board_port)
            self.bc.read_yaml()
            use_board = [self.local_host, self.local_port, board_name]
            self.bc.update_board_status(use_board, 'busy')
            self.bc.update_board_running_info(use_board, 'running')
            self.update_client_status()

            p_log_process.join()
            p_testlink_process.join()
            p_streamxpress_process.join()
            p_redmine_process.join()

        else:
            self.rl.write('download failed', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
            self.bc.read_yaml()
            use_board = [self.local_host, self.local_port, board_name]
            self.bc.update_board_status(use_board, 'error')
            self.bc.update_board_running_info(use_board, 'download_failed')
            self.update_client_status()
        # 清除测试进程 ID
        self.bc.read_yaml()
        self.bc.write_board_jenkins_project_name(use_board, '')
        self.bc.write_board_jenkins_build(use_board, '')
        self.bc.write_board_test_process_id(use_board, '')

    def start_test(self, msg, reboot):
        board_name = msg['message_content']['dvb_info']['specific_board']['board_name']
        use_board = [self.local_host, self.local_port, board_name]
        p = multiprocessing.Process(target=self.test_process,args=(msg, reboot))
        # 记录测试进程 ID
        self.bc.read_yaml()
        p.start()
        self.bc.write_board_test_process_id(use_board, p.pid)

    def kill_process_and_subprocess(self, pid):
        if pid:
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()

    def recursive_kill_process(self, pid):
        try:
            if pid:
                parent = psutil.Process(pid)
                for child in parent.children(recursive=False):
                    self.recursive_kill_process(child.pid)
                    parent.kill()
        except Exception as e:
            print(e)
    def recursive_get_pid(self, pid, pid_str=''):
        if not pid_str:
            pid_str = str(pid)
        if pid:
            cur_process = psutil.Process(pid)
            parent_process = cur_process.parent()
            if parent_process:
                pid_str = '{}-{}'.format(parent_process.pid, pid_str)
                pid_str = self.recursive_get_pid(parent_process.pid, pid_str)
            return pid_str

    def reset_test_board_without_update(self):
        self.bc.read_yaml()
        client = self.bc.get_all_info()
        for client_name, boards in client.items():
            for board_name_local, board_info in boards.items():
                if board_info['mode'] != 'gxdebug':
                    self.stop_test_sub(board_info)

    def reset_test_board(self):
        self.bc.read_yaml()
        client = self.bc.get_all_info()
        for client_name, boards in client.items():
            for board_name_local, board_info in boards.items():
                if board_info['mode'] != 'gxdebug':
                    self.stop_test_sub(board_info)
        self.update_client_status()

    def stop_test_sub(self, board_info):
        test_process_id = board_info['running_info']['test_process_id']
        boot_process_id = board_info['running_info']['boot_process_id']
        self.recursive_kill_process(test_process_id)
        try:
            if boot_process_id:
                self.rl.write('kill boot process {}'.format(boot_process_id), 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                os.kill(boot_process_id, signal.SIGKILL)
        except Exception as e:
            print(e)
        board_name = board_info['board_name']
        use_board = [self.local_host, self.local_port, board_name]
        self.bc.read_yaml()
        self.bc.update_board_status(use_board, 'idle')
        self.bc.update_board_running_info(use_board, 'stop')
        self.bc.write_board_boot_process_id(use_board, '')
        self.bc.write_board_test_process_id(use_board, '')
        self.bc.write_board_jenkins_project_name(use_board, '')
        self.bc.write_board_jenkins_build(use_board, '')
        #self.update_client_status()

    def stop_test(self, msg):
        self.bc.read_yaml()
        client = self.bc.get_all_info()

        _type = msg['message_content']['type']
        if _type == 'all':
            for client_name, boards in client.items():
                for board_name_local, board_info in boards.items():
                    if board_info['mode'] != 'gxdebug' and board_info['status'] == 'busy':
                        self.stop_test_sub(board_info)
        elif _type == 'jenkins':
            jenkins_project_name = msg['message_content']['jenkins_info']['jenkins_project_name']
            jenkins_build = msg['message_content']['jenkins_info']['jenkins_build_id']
            for client_name, boards in client.items():
                for board_name_local, board_info in boards.items():
                    if board_info['running_info']['jenkins_project_name'] == jenkins_project_name and board_info['running_info']['jenkins_build_id'] == jenkins_build:
                        self.stop_test_sub(board_info)
        elif _type == 'specific':
            board_name = msg['message_content']['specific_board']['board_name']
            for client_name, boards in client.items():
                for board_name_local, board_info in boards.items():
                    if board_info['board_name'] == board_name:
                        self.stop_test_sub(board_info)
        elif _type == 'filter':
            chip = msg['message_content']['board_info']['chip']
            board = msg['message_content']['board_info']['board']
            arch = msg['message_content']['board_info']['arch']
            os = msg['message_content']['board_info']['os']
            signal = msg['message_content']['board_info']['signal']
            usb_storage_type = msg['message_content']['board_info']['usb_storage_type']

            for client_name, boards in client.items():
                for board_name_local, board_info in boards.items():
                    if chip and board_info['chip'] != chip:
                        continue
                    if board and board_info['board'] != board:
                        continue
                    if arch and board_info['arch'] != arch:
                        continue
                    if os and board_info['os'] != os:
                        continue
                    if signal and board_info['signal'] != signal:
                        continue
                    if usb_storage_type and board_info['usb_storage_type'] != usb_storage_type:
                        continue
                    self.stop_test_sub(board_info)
        self.update_client_status()

    def add_board(self, msg):
        ip = msg['message_content']['client_ip']
        port = msg['message_content']['client_port']
        board_list = msg['message_content']['stb_board_dict']
        self.bc.read_yaml()
        self.bc.add_board(ip, port, board_list)
        self.update_client_status()

    def update_board(self, msg):
        ip = msg['message_content']['client_ip']
        port = msg['message_content']['client_port']
        board_name = msg['message_content']['board_name']
        dvb_ai = msg['message_content']['dvb_ai']
        board_info = msg['message_content']['board_info']

        self.bc.read_yaml()
        board_info_modified = self.bc.read_board_info(ip, port, board_name)
        for k, v in board_info.items():
            board_info_modified[k] = v
        self.bc.write_board_info(ip, port, board_name, board_info_modified)

        self.update_client_status()

    def delete_board(self, msg):
        ip = msg['message_content']['client_ip']
        port = msg['message_content']['client_port']
        board_name = msg['message_content']['board_name']
        board = board = msg['message_content']['board']
        chip = msg['message_content']['chip']
        self.bc.read_yaml()
        self.bc.delete_board(ip, port, board_name, board, chip)
        self.update_client_status()

    def client_log(self, msg, filename='runninglog.txt'):
        ret = 0
        try:
            level = msg['message_content']['level']
            msg_filter = msg['message_content']['msg_filter']
            time_before = msg['message_content']['time_before']
            time_after = msg['message_content']['time_after']
            filename = self.rl.read(level, msg_filter, time_before, time_after)
            os.system('cp ' + filename + ' cplog.txt')
            filemsg = 'cplog.txt'
            filesize_bytes = os.path.getsize(filemsg)
            info = {
                'filename': filename,
                'filesize_bytes': filesize_bytes,
                }
            ret = 1
        except:
            info = "get client log failed"
        msg['answer'] = info
        if msg['sync'] == True:
            self.sm.answer_msg(msg)
            with open(filemsg, 'rb') as f:
                data = f.read()
                self.sm.sendall(msg, data)
        return ret

    def switch_mode(self, msg):
        name = msg['message_content']['board_name']
        mode_need_modify = msg['message_content']['mode_need_modify']
        mode_after_modify = msg['message_content']['mode_after_modify']
        force = msg['message_content']['force']

        self.bc.read_yaml()
        client = self.bc.get_all_info()
        for client_name, boards in client.items():
            for board_name_local, board_info in boards.items():
                if board_info['board_name'] == name:
                    use_board = [self.local_host, self.local_port, name]
                    if not force:
                        if board_info['status'] == 'busy':
                            self.rl.write('switch mode failed, board is busy', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                            return
                    self.stop_test_sub(board_info)
                    self.bc.write_board_mode(use_board, mode_after_modify)
                    self.update_client_status()

    def board_power(self, msg, reboot):
        operation = msg['message_content']['operation']
        board_name = msg['message_content']['board_name']
        client_ip = msg['message_content']['client_ip']
        client_port = msg['message_content']['client_port']
        client_name = '{}@{}'.format(client_ip, client_port)
        device = ''
        port = ''

        self.bc.read_yaml()
        for board_name_local, board_info in self.bc.get_all_info()[client_name].items():
            if board_name_local == board_name:
                device = board_info['electric_relay_serial']
                port = board_info['electric_relay_port']
        if device and port:
            if operation == 'off':
                reboot.power_off(device = device, port = port)
            elif operation == 'on':
                reboot.power_on(device = device, port = port)
            elif operation == 'reboot':
                reboot.reboot(device = device, port = port)
            return True
        else:
            return False

    def board_log(self, msg):
        operation_type = msg['message_content']['type']
        board_name = msg['message_content']['board_name']
        client_ip = msg['message_content']['client_ip']
        client_port = msg['message_content']['client_port']
        client_name = '{}@{}'.format(client_ip, client_port)
        file_name = msg['message_content']['file_name']
        size = msg['message_content']['size']

        if operation_type == 'list':
            log_file_list = os.listdir('log')
            log_list = [{f:os.path.getsize('log/' + f)} for f in log_file_list]
            msg['answer'] = log_list
            if msg['sync'] == True:
                self.sm.answer_msg(msg)
        elif operation_type == 'read':
            send_file_name = '' + file_name
            with open('log/' + file_name, 'rb') as f:
                data = f.read()
                self.sm.sendall(msg, data)

    def server_stash(self, msg):
        self.server_control['operation'] = 'stash'

    def server_resume(self, msg):
        self.server_control['operation'] = 'resume'
        self.update_client_status()

    def msg_handler(self, msg, reboot):
        self.rl.write('msg handle', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))

        if msg['message_name']=='start':
            self.start_test(msg, reboot)
        elif msg['message_name']=='stop':
            self.stop_test(msg)
        elif msg['message_name']=='add_board':
            self.add_board(msg)
        elif msg['message_name']=='update_board':
            self.update_board(msg)
        elif msg['message_name']=='delete_board':
            self.delete_board(msg)
        elif msg['message_name']=='hardware_detect':
            self.hardware_detect()
        elif msg['message_name']=='board_log':
            self.board_log(msg)
        elif msg['message_name']=='client_log':
            self.client_log(msg)
        elif msg['message_name']=='switch_mode':
            self.switch_mode(msg)
        elif msg['message_name']=='board_power':
            self.board_power(msg, reboot)
        elif msg["message_name"] == "server_stash":
            ret = self.server_stash(msg)
        elif msg["message_name"] == "server_resume":
            ret = self.server_resume(msg)

    def tcp_bind(self):
        ip = ''
        port = int(self.local_port)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((ip,port))
        s.listen(30)
        self.rl.write('waiting for connection...', 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
        return s

    def recv_msg(self, sock, addr):
        self.rl.write('Accept new connection from %s:%s'%addr, 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
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
                self.rl.write(msg, 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))
                break
        sock.close()
        self.rl.write('Connection form %s: %s closed' %addr, 'info', 'PROCESS_MSG {}'.format(self.recursive_get_pid(os.getpid())))

        return msg

    def process_msg(self, reboot):
        tfd = self.tcp_bind()
        while True:
            sock, addr = tfd.accept()
            msg = self.recv_msg(sock, addr)
            self.msg_handler(msg, reboot)

    def heartbeat(self):
        while True:
            u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = {
                    'client_ip':self.local_host,
                    'client_port':self.local_port,
                   }
            data_dumped = json.dumps(data)
            u.sendto(data_dumped.encode(), (self.remote_ip, self.remote_heartbeat_port))
            u.close()
            time.sleep(5)

    def update_client_status(self):
        if self.server_control['operation'] != 'stash':
            client_name = self.local_host + '@' + str(self.local_port)
            msg = copy.deepcopy(self.message_format)

            msg['ip'] = self.local_host
            msg['port'] = self.local_port
            msg['priority'] = 0
            msg['sync'] = 'async'
            msg['receiver'] = 'server'
            msg['message_name'] = 'add_board'

            msg['message_content'] = {}
            msg['message_content']['client_ip'] = self.local_host
            msg['message_content']['client_port'] = self.local_port
            msg['message_content']['client_name'] = client_name
            msg['message_content']['ai_stb'] = 'stb'

            msg['message_content']['ai_board_dict'] = []
            msg['message_content']['stb_board_dict'] = []
            msg['message_content']['stb_board_dict'] = []
            self.bc.read_yaml()
            #for board_name, board_info in self.bc.get_all_info()[client_name].items():
            #    msg['message_content']['stb_board_dict'].append(board_info)

            client = self.bc.get_all_info()
            for client_name, boards in client.items():
                for board_name_local, board_info in boards.items():
                    msg['message_content']['stb_board_dict'].append(board_info)

            self.sm.send_to_server(msg)

    def hardware_detect(self):
        self.bc.read_yaml()
        boards_list = {}
        for k, boards_info in self.bc.total_config.items():
            boards_list = boards_info

        hd = detect.HardwareDetect(boards_list)
        bind_serial = hd.hardware_detect()

        ip = self.local_host
        port = self.local_port
        #ip = '192.168.111.28'
        #port = '5000'
        self.bc.read_yaml()
        self.bc.add_board(ip, port, bind_serial)
        self.update_client_status()

    def hardware_check(self):
        pass

    def start(self, remote_ip, remote_port, remote_heartbeat_port):
        reboot.RebootManager.register('Reboot', reboot.Reboot)
        manager = reboot.rebootmanager()
        reboot_obj = manager.Reboot()

        self.reset_test_board_without_update()
        self.hardware_detect()
        self.update_client_status()

        p_deal_msg = multiprocessing.Process(target = self.process_msg, args=(reboot_obj,))
        p_heartbeat = multiprocessing.Process(target = self.heartbeat)
        p_hardware_check = multiprocessing.Process(target = self.hardware_check)

        p_heartbeat.start()
        p_deal_msg.start()
        p_hardware_check.start()

        while True:
            time.sleep(1)

def main():
    remote_ip = '192.168.110.244'
    remote_port = 10000
    remote_heartbeat_port = 28888
    email_receivers = ['chenwei1@nationalchip.com']
    auto_client = AutoClient(remote_ip, remote_port, remote_heartbeat_port, email_receivers)
    auto_client.start(remote_ip, remote_port, remote_heartbeat_port)

if __name__ == '__main__':
    main()
