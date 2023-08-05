import yaml
import copy
import os
import time
import fcntl

class BoardConfig(object):
    def __init__(self, yaml_file):
        self.total_config = ''
        self.yaml_file = yaml_file
        if not os.path.exists(yaml_file):
            os.system('touch ' + yaml_file)

    def read_yaml(self):
        with open(self.yaml_file, "r") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX) #加锁
            self.total_config = yaml.load(f)
            if not self.total_config:
                self.total_config = {}
            return self.total_config

    def write_yaml(self):
        with open(self.yaml_file, "w") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX) #加锁
            yaml.dump(self.total_config, f, default_flow_style=False, indent = 4)

    def get_client_info(self, arch = '', chip = '', board = '', signal = '', usb_type = '',\
            os = ''):
        idle_list = []
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if arch and board_msg['arch'] != arch:
                    continue
                if chip and board_msg['chip'] != chip:
                    continue
                if board and board_msg['board'] != board:
                    continue
                if signal and board_msg['signal'] != signal:
                    continue
                if usb_type and board_msg['usb_storage_type'] != usb_type:
                    continue
                if os and board_msg['os'] != os:
                    continue
                ip = client.split('@')[0]
                port = client.split('@')[1]
                idle_list.append((ip, port, board_name))
        return idle_list

    def get_idle_board_list(self, arch = '', chip = '', board = '', signal = '', usb_type = ''):
        idle_list = []
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if arch  and board_msg['arch'] != arch:
                    continue
                if chip  and board_msg['chip'] != chip:
                    continue
                if board  and board_msg['board'] != board:
                    continue
                if signal  and board_msg['signal'] != signal:
                    continue
                if usb_type  and board_msg['usb_storage_type'] != usb_type:
                    continue
                if board_msg['mode'] != 'test' and board_msg['mode'] != 'firmware':
                    continue
                if board_msg['status'] == "idle":
                    ip = client.split('@')[0]
                    port = client.split('@')[1]
                    idle_list.append((ip, port, board_name))
        return idle_list
    
    def match_board(self, must_yes, must_no, mode):
        idle_list = []
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                error = 0
                for ky, vy in must_yes.items():
                    if vy and board_msg[ky] != vy:
                        error = 1
                        break
                for kn, vn in must_no.items():
                    if str(board_msg[kn]).upper() == 'TRUE':
                        error = 1
                        break
                if not error:
                    if board_msg['mode'] == mode and board_msg['status'] == "idle":
                        ip = client.split('@')[0]
                        port = client.split('@')[1]
                        idle_list.append((ip, port, board_name))
        return idle_list

    def get_idle_board_list2(self, mode = '', arch = '', chip = '', board = '', signal = '', \
            usb_device = '', usb_gxbus = '', usb_storage_type = '', usb_partition_num = '', \
            web = '', usb_wifi = '', usb_wifi_type = '', secure = '', priority = ''):
        must_yes = {}
        must_no = {}
        key_map = {
                'SIGNAL':'signal',
                'USB_DEVICE':'usb_device',
                'USB_GXBUS':'usb_gxbus',
                'USB_STORAGE_TYPE':'usb_storage_type',
                'USB_PARTITION_NUM':'usb_partition_num',
                'WEB':'web',
                'USB_WIFI':'usb_wifi',
                'USB_WIFI_TYPE':'usb_wifi_type',
                'SECURE':'secure',
                }
        for arg in ['arch', 'chip', 'board', 'signal',\
               'usb_device', 'usb_gxbus', 'usb_storage_type', 'usb_partition_num', \
               'web', 'usb_wifi', 'usb_wifi_type', 'secure']:
            value = eval(arg)
            if value and value != 'no':
                must_yes[arg] = value
            else:
                must_no[arg] = value

        idle_list = self.match_board(must_yes, must_no, mode)
        if len(idle_list) != 0:
            return idle_list

        if not priority:
            priority = ['SIGNAL','USB_DEVICE', 'USB_GXBUS USB_STORAGE_TYPE',\
                    'USB_PARTITION_NUM','USB_WIFI','USB_WIFI_TYPE', 'WEB', 'SECURE']
        for i in priority:
            if key_map[i] in must_no:
                del must_no[key_map[i]]
                must_yes[key_map[i]] = ''
                idle_list = self.match_board(must_yes, must_no, mode)
                if len(idle_list) != 0:
                    return idle_list
        return []

    def get_running_board_list(self):
        running_list = []
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if board_msg['status'] == "busy":
                    ip = client.split('@')[0]
                    port = client.split('@')[1]
                    running_list.append((ip, port, board_name))
        return running_list

    def get_board_list_by_type(self, board = '', os = '', signal = False):
        running_list = []
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if board != '' and board_msg['board'] != board:
                    continue
                if os != '' and board_msg['os'] != os:
                    continue
                if signal != '' and board_msg['signal'] != signal:
                    continue
                if board_msg['status'] == "busy":
                    ip = client.split('@')[0]
                    port = client.split('@')[1]
                    running_list.append((ip, port, board_name))
        return running_list
    
    def get_board_list_by_jenkins(self, jenkins_project = '', jenkins_build = ''):
        running_list = []
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if jenkins_project and \
                        board_msg['running_info']['jenkins_project_name'] != jenkins_project:
                    continue
                if jenkins_build and \
                        board_msg['running_info']['jenkins_build'] != jenkins_build:
                    continue
                if board_msg['status'] == "busy":
                    ip = client.split('@')[0]
                    port = client.split('@')[1]
                    running_list.append((ip, port, board_name))
        return running_list
    
    def get_all_info(self):
        return self.total_config

    def get_info_by_board_name(self, name = ''):
        info = copy.deepcopy(self.total_config)
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if name and board_name != name:
                    del info[client][board_name]
        return info

    def get_info_by_board(self, board = ''):
        info = copy.deepcopy(self.total_config)
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if board != '' and board_msg['board'] != board:
                    del info[client][board_name]
        return info

    def get_info_by_chip(self, chip = ''):
        info = copy.deepcopy(self.total_config)
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if chip != '' and board_msg['chip'] != chip:
                    del info[client][board_name]
        return info

    def get_info_by_jenkins(self, jenkins = ''):
        info = copy.deepcopy(self.total_config)
        for client, boards in self.total_config.items():
            for board_name, board_msg in boards.items():
                if jenkins !='' and board_msg['running_info']['jenkins_project_name'] != jenkins:
                    del info[client][board_name]
        return info

    def get_info_by_ip(self, ip = '', port = ''):
        target = str(ip) + '@' + str(port)
        info = copy.deepcopy(self.total_config)
        for client, boards in self.total_config.items():
            if target != '@' and client != target:
                del info[client]
        return info

    def update_board_status(self, use_board, status):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['status'] = status
        self.write_yaml()

    def update_board_running_info(self, use_board, status):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['running_info']['detail_status'] = status
        self.write_yaml()

    def update_board_gxdebug_info(self, use_board, info):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['gxdebug_info']['status'].update(info)
        self.write_yaml()

    def write_board_test_process_id(self, use_board, test_id):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['running_info']['test_process_id'] = test_id
        self.write_yaml()

    def read_board_test_process_id(self, use_board):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        test_id = self.total_config[client][board_name]['running_info']['test_process_id']
        return test_id

    def write_board_boot_process_id(self, use_board, boot_id):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['running_info']['boot_process_id'] = boot_id
        self.write_yaml()

    def read_board_boot_process_id(self, use_board):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        boot_id = self.total_config[client][board_name]['running_info']['boot_process_id']
        return boot_id

    def write_board_jenkins_project_name(self, use_board, jenkins_project_name):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['running_info']['jenkins_project_name'] = jenkins_project_name
        self.write_yaml()

    def write_board_jenkins_build(self, use_board, jenkins_build):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['running_info']['jenkins_build'] = jenkins_build
        self.write_yaml()

    def write_board_mode(self, use_board, mode):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        self.total_config[client][board_name]['mode'] = mode
        self.write_yaml()

    def read_board_info(self, ip, port, board_name):
        client = str(ip) + "@" + str(port)
        if client in self.total_config:
            if board_name in self.total_config[client]:
                return self.total_config[client][board_name]
            else:
                return {}
        else:
            return {}

    def write_board_info(self, ip, port, board_name, info):
        target = str(ip) + '@' + str(port)
        if target not in self.total_config:
            self.total_config[target] = {}
        self.total_config[target][board_name] = info
        self.write_yaml()

    def add_board(self, ip = '', port = '', board_list = []):
        target = str(ip) + '@' + str(port)
        if target not in self.total_config:
            self.total_config[target] = {}
        for board_msg in board_list:
            name = board_msg['board_name']
            self.total_config[target][name] = board_msg
        self.write_yaml()

    def delete_specify_board(self, ip = '', port = '', spec_board_name = ''):
        target = str(ip) + '@' + str(port)
        back_config = copy.deepcopy(self.total_config)
        for client, boards in back_config.items():
            if target != '@' and client == target:
                for board_name in boards.keys():
                    if board_name == spec_board_name:
                        del self.total_config[target][board_name]
        self.write_yaml()

    def delete_board(self, ip = '', port = '', spec_board_name = '', board = '', chip = ''):
        if ip:
            self.delete_specify_board(msg)
        back_config = copy.deepcopy(self.total_config)
        for client, boards in back_config.items():
            for board_name, board_msg in boards.items():
                if board and board_msg['board'] == board:
                    del self.total_config[client][board_name]
                if chip and board_msg['chip'] == chip:
                    del self.total_config[client][board_name]
        self.write_yaml()

    def is_idle(self, use_board):
        ip = use_board[0]
        port = use_board[1]
        client = ip + '@' + str(port)
        board_name = use_board[2]
        print(use_board)
        if self.total_config[client][board_name]['status'] == 'idle':
            return True
        else:
            return False

    def get_all_client(self):
        client_list = []
        for client, boards in self.total_config.items():
            ip = client.split('@')[0]
            port = client.split('@')[1]
            client_list.append((ip, port))
        return client_list



if __name__ == "__main__":
    yaml_file = "board.yaml"
    bc = BoardConfig(yaml_file)
    boards = bc.read_yaml()
    #print(boards)
    #idle_list = bc.get_idle_board_list2(arch = '', chip = '', board = '', signal = '', \
    #        usb_device = '', usb_gxbus = '', usb_type = '', usb_partition_num = '', \
    #        web = '', usb_wifi = '', usb_wifi_type = '', priority = ['USB_DEVICE', 'WEB', 'SIGNAL'])
    ##bc.update_board_state(idle_list[0], 'busy')
    #print(idle_list)
    info = bc.read_board_info('127.0.0.1', 10001,'kaoji1-1_gx6605s_1')
    bc.write_board_info('127.0.0.1', 10001,'kaoji1-1_gx6605s_1', info)
    print(info)
