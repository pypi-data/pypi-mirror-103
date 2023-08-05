#!/usr/bin/python3
#coding:utf-8

from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager
import serial
import time
import re


class RebootManager(BaseManager):
    pass

def rebootmanager():
    m = RebootManager()
    m.start()
    return m

class Reboot:
    def __init__(self):
        self.serial_dev = []
        self.serial_object = {}
        self.lock = {}
        self._lock = Lock()

    def _add_device(self, name,device):
        with self._lock:
            if not self._is_open(name,device):
                print("%s %s own"%(name, self._lock))
                try:
                    obj = serial.Serial(device, 115200, timeout = 30)
                    print(obj)
                    self.serial_object[device] = obj
                except:
                    return None
                lock = Lock()
                self.lock[device] = lock
                print("%s %s release"%(name, self._lock))
                return obj
            return True

    def remove_device(self, device):
        #with self._lock:
        #    del self.serial_object[device]
        #    del self.lock[device]
        with self._lock:
            with self.lock[device]:
                self.serial_object[device].close()
                del self.serial_object[device]
                del self.lock[device]
            del self._lock

    def _is_open(self, name,device):
        if device in self.serial_object.keys():
            print("%s %s is open"%(name,device))
            return True
        print("%s %s is not open"%(name,device))
        return False

    def _power_control(self, name, device, port, cmd):
        retry_times = 0
        max_retry_times = 5

        while(True):
            print("%s %s"%(name, cmd))
            self.serial_object[device].write(cmd.encode())
            s = self.serial_object[device].readline().decode('utf-8', errors='replace')
            #print("###",s)
            s = self.serial_object[device].readline().decode('utf-8', errors='replace')
            print("###",s)
            if (re.findall(r"success", s)):
                break
            else:
                retry_times += 1

            if (retry_times == max_retry_times):
                return False

        time.sleep(0.3) # min delay


    def reboot(self, device, port, name=''):
        if not self._add_device(name,device):
            return False
        with self.lock[device]:
            cmdon = "setpower on " + str(port) + "\n"
            cmdoff = "setpower off " + str(port) + "\n"
            self._power_control(name, device, port, cmdoff)
            self._power_control(name, device, port, cmdon)

    def power_off(self, device, port, name=''):
        if not self._add_device(name,device):
            return False
        with self.lock[device]:
            cmdoff = "setpower off " + str(port) + "\n"
            self._power_control(name, device, port, cmdoff)

    def power_on(self, device, port, name=''):
        if not self._add_device(name,device):
            return False
        with self.lock[device]:
            cmdon = "setpower on " + str(port) + "\n"
            self._power_control(name, device, port, cmdon)


def task(name, reboot, device, port):
    while 1:
        time.sleep(3)
        reboot.reboot(name, device, port)
        reboot.power_off(name, device, port)
        reboot.power_on(name, device, port)

if __name__ == '__main__':
    RebootManager.register('Reboot', Reboot)
    manager = rebootmanager()
    reboot_obj = manager.Reboot()
    names = ['sub_process_1', 'sub_process_2', 'sub_process_3']
    ports = ['1','2','3']
    ps = []
    i = 0
    for name in names:
        ps.append(Process(target=task,args=(name,reboot_obj,'/dev/ttyUSB0', ports[i])))
        i = i + 1
    for p in ps:
        p.start()
    for p in ps:
        p.join()

