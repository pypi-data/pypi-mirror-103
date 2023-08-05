#!/usr/bin/python3
#encoding:utf-8

import os
import serial
import threading
import re
import time
import sys
import copy
from modules import redmine

stop_threads = False

class MyThread(threading.Thread):
    def __init__(self, target, args):
        super(MyThread, self).__init__()
        self.target = target
        self.args = args

    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

class HardwareDetect():
    def __init__(self, boards_list):
        self.serial_list_all = []
        self.serial_list_filtered = []
        self.control_serial_dict = {}
        self.test_serial_dict = {}
        self.bind_serial_dict = {}
        self.bind_serial_list = []
        self.boards_list = boards_list

    def _get_serial(self):
        self.serial_list_all = ['/dev/' + s for s in os.listdir('/dev') if 'gxUSB' in s]
        print('=================================================================')
        print('all serial: {}'.format(self.serial_list_all))

    def _filter_used_test_serial(self):
        self.serial_list_filtered = self.serial_list_all
        for board_name, board_info in self.boards_list.items():
            print(board_info)
            if board_info['test_serial'] in self.serial_list_filtered:
                self.serial_list_filtered.remove(board_info['test_serial'])
        print('=================================================================')
        print('serial filtered:')
        for serial_name in self.serial_list_filtered:
            print('\t{}'.format(serial_name))

    def _distinguish_control_serial_and_test_serial(self):
        for s in self.serial_list_filtered:
            serial_obj = serial.Serial(s, 115200, timeout = 0.1)
            serial_obj.readline()
            serial_obj.write(b'setpower off 1\n')
            log_1 = serial_obj.readline()
            log_2 = serial_obj.readline()
            #print(log_1)
            #print(log_2)
            if log_1 == b'setpower off 1\r\r\n' and log_2 == b'success\r\n':
                self.control_serial_dict[s] = {'obj':serial_obj, 'port':[1,2,3]}
                self.bind_serial_dict[s] = {}
            else:
                self.test_serial_dict[s] = {'obj':serial_obj}
        print('=================================================================')
        print('control serial:')
        for serial_name, serial_info in self.control_serial_dict.items():
            print('\t{}'.format(serial_name))
        print('=================================================================')
        print('test serial:')
        for serial_name, serial_info in self.test_serial_dict.items():
            print('\t{}'.format(serial_name))

    def _filter_used_control_serial_and_port(self):
        for board_name, board_info in self.boards_list.items():
            electric_relay_serial = board_info['electric_relay_serial']
            electric_relay_port = board_info['electric_relay_port']
            if int(electric_relay_port) in self.control_serial_dict[electric_relay_serial]['port']:
                self.control_serial_dict[electric_relay_serial]['port'].remove(int(electric_relay_port))
            if self.control_serial_dict[electric_relay_serial]['port'] == []:
                self.control_serial_dict.pop(electric_relay_serial)
        print('=================================================================')
        print('idle control serial and port: ')
        for serial_name, serial_info in self.control_serial_dict.items():
            print('\t{} {}'.format(serial_name, serial_info['port']))

    def test_serial(self, serial):
        global stop_threads
        info = {
                'arch':'',
                'chip':'',
                'board':'',
                'public_id':'',
                }
        while True:
            if stop_threads:
                break
            try:
                s = serial.readline().decode('utf-8', errors='replace')
                if s:
                    #print(s)
                    list_info = s.split(":")
                    if len(list_info) == 2:
                        if "cpu family" in list_info[0]:
                            info['arch'] = list_info[1].strip().lower()
                            #print('find arch')
                        elif "chip model" in list_info[0]:
                            info['chip'] = list_info[1].strip()
                            #print('find chip')
                        elif "board type" in list_info[0]:
                            info['board'] = list_info[1].strip()
                            #print('find board')
                        elif "public id" in list_info[0]:
                            info['public_id'] = list_info[1].strip()
                            #print('find public_id')
                    if info['arch'] and info['chip'] and info['board'] and info['public_id']:
                        print('find relative serial! info: {}'.format(info))
                        return info
            except:
                pass

    def _modify_same_public_id_1(self, public_id):
        for k, v in self.bind_serial_dict.items():
            for kk, vv in v.items():
                if public_id == vv['public_id']:
                    print('find same public_id!')
                    ret = public_id.split('_')
                    if len(ret) == 2:
                        subscript = ret[1]
                    else:
                        subscript = '1'
                    public_id = ret[0]
                    public_id = public_id + '_' + str(int(subscript) + 1)
                    public_id = self._modify_same_public_id_1(public_id)
        return public_id

    def _modify_same_public_id_2(self, public_id):
        for board_name, board_info in self.boards_list.items():
            if public_id == board_name:
                print('find same public_id!')
                ret = public_id.split('_')
                if len(ret) == 2:
                    subscript = ret[1]
                else:
                    subscript = '1'
                public_id = ret[0]
                public_id = public_id + '_' + str(int(subscript) + 1)
                public_id = self._modify_same_public_id_1(public_id)
        return public_id

    def _bind_control_serial_and_test_serial(self):
        global stop_threads
        for k,v in self.control_serial_dict.items():
            for i in v['port']:
                for kk,vv in self.control_serial_dict.items():
                    for ii in vv['port']:
                        vv['obj'].write('setpower off {}\n'.format(ii).encode('utf-8'))
                        time.sleep(0.1)
                t_test_serial_list = []
                for kk,vv in self.test_serial_dict.items():
                    t_test_serial = MyThread(target = self.test_serial, args = (vv['obj'],))
                    t_test_serial_list.append({kk:t_test_serial})
                    t_test_serial.daemon = True
                    stop_threads = False
                    t_test_serial.start()

                v['obj'].write('setpower on {}\n'.format(i).encode('utf-8'))
                print('-------------------------------------')
                print('control serial {} port {} power on'.format(k, i))
                t_test_serial_list_copy = copy.copy(t_test_serial_list)
                count = 0
                find_relative_board = False
                while True:
                    for t in t_test_serial_list_copy:
                        if not t[list(t.keys())[0]].isAlive():
                            stop_threads = True
                            result = t[list(t.keys())[0]].get_result()
                            if result:
                                if result['board'] == '6605s':
                                    gxredmine = redmine.GxRedmine()
                                    result['board'] = gxredmine.get_board_by_public_id(result['public_id'])
                                    if result['board'] == 'pegasus':
                                        result['chip'] = 'pegasus'
                                result['public_id'] = self._modify_same_public_id_1(result['public_id'])
                                print(result['public_id'])
                                result['public_id'] = self._modify_same_public_id_2(result['public_id'])
                                print(result['public_id'])
                                self.bind_serial_dict[k].update({i:{'test_serial':list(t.keys())[0], 'public_id':result['public_id'], 'arch':result['arch'], 'chip':result['chip'], 'board':result['board']}})
                                find_relative_board = True
                        if find_relative_board:
                            break
                    count += 1
                    if count == 3:
                        stop_threads = True
                    if stop_threads == True:
                        for t in t_test_serial_list_copy:
                                for a in t_test_serial_list_copy:
                                    for ka,va in a.items():
                                        va.join()
                        break
                    time.sleep(1)

        board_info_def = {
            'arch': '',
            'board': '',
            'board_name': '',
            'chip': '',
            'electric_relay_port': '',
            'electric_relay_serial': '',
            'gxdebug_info':{
                'board_control_port': '',
                'board_control_serial': '',
                'board_name': '',
                'board_serial': '',
                'gdbnum': '',
                'gdbport': '',
                'ip': '',
                'ip_port': '',
                'jkink_control_port': '',
                'jlink_control_serial': '',
                'post_ip': ''},
            'mode': 'test',
            'running_info':{
                'boot_process_id': '',
                'detail_status': '',
                'jenkins_build': '',
                'jenkins_project_name': '',
                'os': '',
                'running_status': '',
                'test_process_id': ''},
            'signal': 'true',
            'status': 'idle',
            'test_project_bind': '',
            'test_serial': '',
            'usb_device': 'true',
            'usb_gxbus': 'true',
            'usb_storage_type': 'NTFS', # FAT32、NTFS
            'usb_partition_num': '1',
            'web': 'false',
            'usb_wifi': 'false',
            'usb_wifi_type': '', # 7601、5370
        }

        for electric_relay_serial, electric_info in self.bind_serial_dict.items():
            for electric_relay_port, board_bind_info in electric_info.items():
                test_serial = board_bind_info['test_serial']
                public_id = board_bind_info['public_id']
                arch = board_bind_info['arch']
                chip = board_bind_info['chip']
                board = board_bind_info['board']

                board_info = copy.deepcopy(board_info_def)
                board_info['board_name'] = public_id
                board_info['test_serial'] = test_serial
                board_info['electric_relay_serial'] = electric_relay_serial
                board_info['electric_relay_port'] = electric_relay_port
                board_info['arch'] = arch
                board_info['chip'] = chip
                board_info['board'] = board
                self.bind_serial_list.append(board_info)
        print('-------------------------------------')
        print('bind_serial_list: {}'.format(self.bind_serial_list))

    def hardware_detect(self):
        self._get_serial()
        self._filter_used_test_serial()
        self._distinguish_control_serial_and_test_serial()
        self._filter_used_control_serial_and_port()
        self._bind_control_serial_and_test_serial()
        return self.bind_serial_list


if __name__ == '__main__':
    #boards_list = {
    #            'gx6605s_1':{
    #                'electric_relay_port':'1',
    #                'electric_relay_serial':'/dev/ttyUSB0',
    #                'test_serial':'/dev/ttyUSB2',
    #                }
    #}
    boards_list = {
    }

    hd = HardwareDetect(boards_list)
    hd.hardware_detect()
