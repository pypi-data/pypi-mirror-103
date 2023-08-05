import yaml
import json
import os
import time
import datetime
import logging
from cloghandler import ConcurrentRotatingFileHandler
#from logging.handlers import RotatingFileHandler


class HeartLog(object):
    def __init__(self, yaml_file):
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.yaml_file = yaml_file
        if not os.path.exists(yaml_file):
            os.system('touch ' + yaml_file)
        self.client_heart = None
        self.read_yaml()
        if self.client_heart == None:
            self.client_heart = {}

    def read_yaml(self):
        with open(self.yaml_file, "r") as f:
            #@self.client_heart = yaml.load(f, Loader=yaml.FullLoader)
            self.client_heart = yaml.load(f)
            return self.client_heart

    def write_yaml(self):
        with open(self.yaml_file, "w") as f:
            yaml.dump(self.client_heart, f, default_flow_style=False, indent = 4)

    def update_heart(self, data):
        host = data['client_ip']
        port = data['client_port']
        if host not in self.client_heart:
            self.client_heart[host] = {}
        if port not in self.client_heart[host]:
            self.client_heart[host][port] = {}
        now = time.strftime(self.time_format, time.localtime())
        self.client_heart[host][port]['timestamp'] = now
    
    def check_outtime(self):
        print(self.client_heart)
        now = datetime.datetime.now()
        outtime_list = []
        for client in self.client_heart:
            for port in self.client_heart[client]:
                print(client)
                print(port)
                print(self.client_heart[client][port]['timestamp'])
                heart = datetime.datetime.strptime(\
                        self.client_heart[client][port]['timestamp'], self.time_format)
                sub = (now - heart).total_seconds()
                print(sub)
                if sub >= 120:
                    outtime_list.append((client, port))
        self.write_yaml()
        return outtime_list

    def write_down_dict(self, data):
        with open('task_stash.yaml', "w") as f:
            yaml.dump(data, f, default_flow_style=False, indent = 4)

    def read_task_from_file(self, yaml_file = 'task_stash.yaml'):
        with open(yaml_file, "r") as f:
            save_task = yaml.load(f)
            return save_task


class RunningLog(object):
    def __init__(self):
        #self.time_format = "%Y-%m-%d %H:%M:%S"
        #self.log_file = log_file
        #if not os.path.exists(log_file):
        #    os.system('touch ' + log_file)
        #self.fd = open(self.log_file, 'w')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level = logging.DEBUG)
        #formatter = logging.Formatter(\
        #        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter(\
                '%(asctime)s - %(app_name)s - %(levelname)s - %(message)s')
        rHandler = ConcurrentRotatingFileHandler("runninglog.txt",maxBytes = 1024*1024*10,backupCount = 5)
        rHandler.setLevel(logging.DEBUG)
        rHandler.setFormatter(formatter)
        self.logger.addHandler(rHandler)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def write(self, msg, leval, name = 'default'):
        if leval == 'debug':
            self.logger.debug(str(msg), extra = {'app_name': name})
        if leval == 'info':
            self.logger.info(str(msg), extra = {'app_name': name})
        if leval == 'warning':
            self.logger.warning(str(msg), extra = {'app_name': name})
        if leval == 'error':
            self.logger.error(str(msg), extra = {'app_name': name})
        if leval == 'critical':
            self.logger.critical(str(msg), extra = {'app_name': name})

    def add_tcp(self, host, port):
        formatter = logging.Formatter(\
                '%(asctime)s - %(app_name)s - %(levelname)s - %(message)s')
        tconsole = MySocketHandler(host, port)
        tconsole.setLevel(logging.INFO)
        tconsole.setFormatter(formatter)
        self.logger.addHandler(tconsole)

    def read(self, leval='', msg_filter = '', time_before = '', time_after = ''):
        logfilename = 'runninglog.txt'
        new_logname = logfilename
        if leval:
            new_logname = leval + '_' + logfilename
            os.system('cat ' + logfilename + ' | grep ' + leval + ' > '  + new_logname)
            logfilename = new_logname
        if msg_filter:
            new_logname = msg_filter + '_' + logfilename
            os.system('cat ' + logfilename + ' | grep ' + msg_filter + ' > ' + new_logname)
            logfilename = new_logname
        if time_before:
            new_logname = time_before.replace(' ', '_').replace(':','~') + '_' + logfilename
            if not time_after:
                new_logname = 'before_' +  new_logname
            content = ''
            with open(logfilename, 'r') as f:
                for line in f:
                    d = line.split(' - ')[0]
                    if d <= time_before:
                        content += line
            with open(new_logname, 'w') as o:
                o.write(content)
            logfilename = new_logname
        if time_after:
            new_logname = time_after.replace(' ', '_').replace(':','~') + '_' + logfilename
            if not time_before:
                new_logname = 'after_' +  new_logname
            content = ''
            with open(logfilename, 'r') as f:
                for line in f:
                    d = line.split(' - ')[0]
                    if d >= time_after:
                        content += line
            with open(new_logname, 'w') as o:
                o.write(content)
            logfilename = new_logname
        return  logfilename

class MySocketHandler(logging.handlers.SocketHandler):
    def makePickle(self, record):
        return self.format(record).encode()


class ResultLog(object):
    pass

if __name__ == "__main__":
    yaml_file = "../task_stash.yaml"
    bc = HeartLog(yaml_file)
    print(bc.client_heart)
