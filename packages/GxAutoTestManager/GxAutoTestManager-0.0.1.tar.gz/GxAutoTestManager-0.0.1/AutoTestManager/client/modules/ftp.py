# -*- coding:utf-8 -*-
#---------------------------------------
#
# 功能: 实际操作ftp的功能模块
# 时间: 2019-09-18
#
#---------------------------------------
import os
import sys
import time
from ftplib import FTP

# 登入ftp
class GXFTP:
    def __init__(self):
        """
        connect infor config
        """
        self.host = '192.168.110.253'
        #self.host = '192.168.111.70'
        self.username = 'guoxin'
        self.password = 'Guoxin88156088'
        self.login_port = 21
        #self.login_port = 2121
        #self.ftp_initial_address = 'public/ftp/robot/KO_ACTIVATE_TEST/'
        self.ftp_initial_address = 'public/ftp/AutoTestBin/'

    # 登入ftp
    def FTP_connect(self, platform_dir = ''):
        """"
        ftp connect
        """
        self.ftp = FTP()
        #self.ftp.set_debuglevel(2)
        self.ftp.connect(self.host, self.login_port)
        self.ftp.login(self.username, self.password)
        #设置ftp进入的初始目录
        platform_dir = self.ftp_initial_address + platform_dir
        self.ftp.cwd(platform_dir) # 设置ftp进入的初始目录
        print('\033[1;44;37m欢迎使用FTP服务 ------> %s\033[0m'%self.ftp.getwelcome())
        print('\033[0;43;37m当前FTP进入的平台目录 ----->[ %s]\033[0m'%platform_dir)
        time.sleep(2)

    def downloadfile(self, remotepath, localpath):
        """
        从FTP下载文件到本地
        """
        print ('[从FTP下载文件到本地:] %s ---> %s\n'%(remotepath, localpath))
        try:
            bufsize = 1024
            fp = open(localpath, 'wb')
            self.ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
            #self.ftp.set_debuglevel(0)
            fp.close()
            print ('\033[0;42;37m[从FTP下载文件到本地 SUCCESS :]\033[0m')
        except:
            print ('\033[0;41;37m[从FTP下载文件到本地 FAILED :]\033[0m')
        
    
    def uploadFile(self, localpath, remotepath):
        """
        从本地上传文件到FTP
        """
        try:
            print ('[上传文件到FTP:] %s ---> %s\n'%(localpath, remotepath))
            if not os.path.isfile(localpath):  
                return
            self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))
            print ('\033[0;42;37m[上传文件至FTP SUCCESS :]\033[0m')
        except:
            print ('\033[0;41;37m[上传文件至FTP FAILED :]\033[0m')
    
    def uploadDir(self, localdir='./', remotedir='./'):
        """
        从本地上传文件夹到FTP
        """
        self.ftp.cwd(remotedir)
        tmp_dir = localdir.split('/')[-1]
        if not tmp_dir:
            print('Last path if [/]')
            tmp_dir = localdir.split('/')[-2]
        try:  
            self.ftp.mkd(tmp_dir)
        except:  
            sys.stderr.write('the dir is exists %s\n'%tmp_dir)
        self._uploadDir(localdir,tmp_dir)
        self.ftp.cwd('..') # 退回到原始路径

    def _uploadDir(self, localdir, tmp_dir):
        if not os.path.isdir(localdir):  
            return
        self.ftp.cwd(tmp_dir) 
        #self.ftp.mkd(remotedir)  
        for file in os.listdir(localdir):
            src = os.path.join(localdir, file)
            if os.path.isfile(src):
                self.uploadFile(src, file)
            elif os.path.isdir(src):
                try:  
                    self.ftp.mkd(file)  
                except:  
                    sys.stderr.write('the dir is exists %s\n'%file)
                self.uploadDir(src, file)
        self.ftp.cwd('..')

    def delete_file(self, path):
        """
        删除位于FTP的远程文件
        """
        print ('[删除FTP远程文件:] ---> %s\n'%path)
        self.ftp.delete(path)

    def movefile(self, old_file_path, new_file_path):
        """
        移动远程FTP文件
        """
        try:
            if not os.path.exists('tmp_dir'):
                os.makedirs('tmp_dir')
            filename = old_file_path.split('/')[-1]
            if not filename:
                print('Last path if [/]')
                filename = old_file_path.split('/')[-2]
            tmp_file = 'tmp_dir/'+filename
            self.downloadfile(old_file_path, tmp_file)
            new_file_path = new_file_path + '/' + filename
            self.uploadFile(tmp_file, new_file_path)
            rmcmd = 'rm tmp_dir -r'
            os.system(rmcmd)
            self.delete_file(old_file_path)
            mvinfor = '[移动FTP远程文件: %s ----> %s]\n'%(old_file_path, new_file_path)
            print(mvinfor)
        except:
            print('[Error : movefile]')

    def query_ftp_dir(self,query_dir):
        """
        显示远程FTP目录下的文件列表
        """
        #dir_ftp = self.ftp.dir()#显示目录信息
        #print dir_ftp
        lsit = self.ftp.nlst(query_dir) #显示指定目录下的信息列表
        print(lsit)
        return lsit

    def renameFile(self, currName, reName):
        """
        重命名FTP远程文件
        """
        try:
            self.ftp.rename(currName, reName)
        except:
            print("重命名失败,未找到文件 [%s]\n"%currName)

    def mkdir(self, remote_dir):
        """
        新建远程目录
        """
        try:
            self.ftp.mkd(remote_dir)
        except:
            sys.stderr.write('the dir is exists "%s"\n'%remote_dir)

    def close(self):
        """
        关闭FTP正在进行任务
        """
        self.ftp.close()
    
    def ftp_quit(self):
        """
        退出ftp
        """
        self.ftp.quit()
        time.sleep(8)
        print('\033[1;44;37m退出FTP .......\033[0m')

if __name__ == "__main__":
    gxftp = GXFtp()
    gxftp.movefile('test/11.txt', 'test1/text/')
    gxftp.close()

