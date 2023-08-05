#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
#--------------------------------------------------
#
# 功能: FTP 操作库，根据ftp仅限的基础功能，
#       封装出一些常用的模块
# 时间: 2019-09-18
#
#----------------------------------------------------
import os, sys, time
from ftplib import FTP

class FtpFunctionLib:
    def __init__(self, Host = '192.168.110.253', UserName = 'guoxin', Password = 'Guoxin88156088', 
                FtpLoginBasicPath = 'public/ftp/robot/ai_algorithm/KO_ACTIVATE_TEST/',
                LoginPort = 21):
        """
            功能:   初始化参数信息
            参数：  /
            返回值: /
        """
        self.Host = Host
        self.UserName = UserName
        self.Password = Password
        self.LoginPort = LoginPort
        #self.LoginPort = 2121
        self.FtpLoginBasicPath = FtpLoginBasicPath
        self.show_list = []

    def FtpLogin(self, PlatformPath = ''):
        """
            功能:   登入ftp 服务器指定地址
            参数:   PlatformPath: 平台名称/路径
            返回值: Bool True/False
        """
        try:
            self.ftp = FTP()
            #开启debug打印
            #self.ftp.set_debuglevel(2)
            self.ftp.connect(self.Host, self.LoginPort)
            #解决中文乱码问题
            self.ftp.encoding = 'utf-8'#文件名中文解决，但是中文文件名的文件内容为空

            #输入用户名，密码
            self.ftp.login(self.UserName, self.Password)
            #设置ftp进入的初始目录
            PlatformPath = os.path.join(self.FtpLoginBasicPath, PlatformPath)

            self.ftp.cwd(PlatformPath) # 设置进入平台地址
            print('\033[1;44;37m[FTP 服务模块 ] 欢迎使用FTP服务: %s\033[0m'%self.ftp.getwelcome())
            print('\033[0;36;33m[FTP 服务模块 ] 当前FTP进入的平台目录 -> %s\033[0m'%PlatformPath)
            time.sleep(2)
            return True
        except:
            return False

    def DownloadFile(self, RemotePath, LocalPath):
        """
            功能:   从FTP下载文件到本地
            参数:   RemotePath: ftp 远程路径
                    LocalPath:  本地路径
            返回值: Bool True/False
        """
        print ('[FTP 服务模块 ] 从FTP: %s 下载文件到: %s\n'%(RemotePath, LocalPath))
        try:
            bufsize = 1024
            fp = open(LocalPath, 'wb')
            self.ftp.retrbinary('RETR ' + RemotePath, fp.write, bufsize)
            self.ftp.set_debuglevel(0)
            fp.close()
            print ('\033[0;42;37m[FTP 服务模块 ] 从FTP下载文件到本地 SUCCESS\033[0m')
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] 从FTP下载文件到本地 FAILED \033[0m')
            return False
        
    
    def UploadFile(self, LocalPath, RemotePath):
        """
            功能:   从本地上传文件到FTP远程目录
            参数:   RemotePath: ftp 远程路径
                    LocalPath:  本地路径
            返回值: Bool True/False
        """
        try:
            print ('[FTP 服务模块 ] 从本地: %s 上传文件到FTP: %s\n'%(LocalPath, RemotePath))
            if not os.path.isfile(LocalPath):  
                print ('\033[0;41;37m[FTP 服务模块 ] 本地无该文件\033[0m')
                return False
            self.ftp.storbinary('STOR ' + RemotePath, open(LocalPath, 'rb'))
            print ('\033[0;42;37m[FTP 服务模块 ] 上传文件至FTP SUCCESS\033[0m')
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] 上传文件至FTP FAILED\033[0m')
            return False

    def Mkdirs(self, RemotePath):
        """
            功能:   在FTP远程创建层级目录
            参数:   RemotePath: 需要创建的层级路径
            返回值: 无
        """
        dir_name = RemotePath.strip('/').split('/')
        back_path = ''
        for i in dir_name:
            try:
                self.ftp.cwd(i)
                back_path += '../'
            except:
                self.ftp.mkd(i)
                self.ftp.cwd(i)
                back_path += '../'
        self.ftp.cwd(back_path)
        #print(self.ftp.pwd())
        #self.FtpQuit()
    
    def UploadDir(self, localdir='./', remotedir='./'):
        """
            功能:   从本地上传文件夹到FTP远程目录
            参数:   RemotePath: ftp 远程路径
                    LocalPath:  本地路径
            返回值: /
        """
        self.ftp.cwd(remotedir)
        tmp_dir = localdir.split('/')[-1]
        if not tmp_dir:
            print('Last path if [/]')
            tmp_dir = localdir.split('/')[-2]
        try:  
            self.ftp.mkd(tmp_dir)
        except:  
            print ('\033[0;41;37m[FTP 服务模块 ] 上传目录时创建目录 FAILED\033[0m')
        self._UploadDir(localdir, tmp_dir)
        self.ftp.cwd('..') # 退回到原始路径

    def _UploadDir(self, localdir, tmp_dir):
        """
            功能:   递归从本地上传文件夹到FTP远程目录
            参数:   RemotePath: ftp 远程路径
                    LocalPath:  本地路径
            返回值: /
        """
        if not os.path.isdir(localdir):  
            return
        self.ftp.cwd(tmp_dir) 
        #self.ftp.mkd(remotedir)  
        for file in os.listdir(localdir):
            src = os.path.join(localdir, file)
            if os.path.isfile(src):
                self.UploadFile(src, file)
            elif os.path.isdir(src):
                try:  
                    self.ftp.mkd(file)  
                except:  
                    print('[FTP 服务模块 ] the dir is exists %s\n'%file)
                self.UploadDir(src, file)
        self.ftp.cwd('..')

    def DeleteFile(self, RemotePath):
        """
            功能:   删除FTP远程文件
            参数:   RemotePath: ftp 远程路径
            返回值: Bool True/False
        """
        print ('[FTP 服务模块 ] 删除FTP远程文件: -> %s\n'%RemotePath)
        try:
            self.ftp.delete(RemotePath)
            print ('\033[0;42;37m[FTP 服务模块 ] FTP远程文件删除 SUCCESS\033[0m')
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] FTP远程文件删除 FAILED\033[0m')
            return True

    def MoveFile(self, OldRemotePath, NewRemotePath):
        """
            功能:   移动FTP远程文件
            参数:   OldRemotePath: 移动前FTP远程路径
                    NewRemotePath: 移动后FTP远程路径
            返回值: Bool True/False
        """
        print('[FTP 服务模块 ] 移动FTP远程文件: %s to %s\n'%(OldRemotePath, NewRemotePath))
        try:
            if not os.path.exists('tmp_dir'):
                os.makedirs('tmp_dir')
            filename = OldRemotePath.split('/')[-1]
            if not filename:
                print('Last path if [/]')
                filename = OldRemotePath.split('/')[-2]
            tmp_file = 'tmp_dir/'+filename
            self.DownloadFile(OldRemotePath, tmp_file)
            NewRemotePath = NewRemotePath + '/' + filename
            self.UploadFile(tmp_file, NewRemotePath)
            rmcmd = 'rm tmp_dir -r'
            os.system(rmcmd)
            self.DeleteFile(OldRemotePath)
            print ('\033[0;42;37m[FTP 服务模块 ] 移动FTP远程文件 SUCCESS\033[0m')
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] 移动FTP远程文件 FAILED\033[0m')
            return False

    def QueryRemoteFileList(self, RemotePath):
        """
            功能:   获取FTP远程文件列表
            参数:   RemotePath: 需要访问的路径
            返回值: lsit
        """
        print(self.ftp.dir())
        remote_file_list = []
        try:
            #显示指定目录下的信息列表
            remote_file_list = self.ftp.nlst(RemotePath)
            print('[FTP 服务模块 ] 查询FTP远程文件信息: %s 下文件信息 %s\n'%(RemotePath, remote_file_list)) 
            return remote_file_list
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] 查询FTP远程文件信息 FAILED 路径: %s\033[0m'%RemotePath)
            return remote_file_list

    def RenameFile(self, OriRemoteFileName, NewRemoteFileName):
        """
            功能:   重命名FTP远程文件
            参数:   OriRemoteFileName: 重命名之前名称
                    NewRemoteFileName: 重命名之后名称
            返回值: Bool True/False
        """
        try:
            self.ftp.rename(OriRemoteFileName, NewRemoteFileName)
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] 重命名FTP远程文件 FAILED [%s --> %s]\033[0m'%(OriRemoteFileName, NewRemoteFileName))

    def Mkdir(self, RemoteDir):
        """
            功能:   在FTP远程创建目录
            参数:   OriRemoteFileName: 重命名之前名称
            返回值: Bool True/False
        """
        try:
            self.ftp.mkd(RemoteDir)
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] 创建FTP远程目录 FAILED 路径: %s\033[0m'%RemoteDir)
            return False

    def Close(self):
        """
            功能:   关闭FTP正在进行任务及连接
            参数:   /
            返回值: Bool True/False
        """
        try:
            self.ftp.close()
            print ('\033[0;42;37m[FTP 服务模块 ] FTP CLOSE SUCCESS\033[0m')
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] FTP CLOSE FAILED\033[0m')
            return False
    
    def FtpQuit(self):
        """
            功能:   退出FTP服务
            参数:   /
            返回值: Bool True/False
        """
        try:
            self.ftp.quit()
            print ('\033[0;42;37m[FTP 服务模块 ] START FTP 退出 \033[0m')
            time.sleep(4)
            print ('\033[0;42;37m[FTP 服务模块 ] FTP 退出 SUCCESS\033[0m')
            return True
        except:
            print ('\033[0;41;37m[FTP 服务模块 ] FTP 退出 FAILED\033[0m')
            return False

    def ShowDir(self, path):
        self.ftp.cwd(path)
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.startswith('d'):
                path_a = self.ftp.pwd() + '/' + f[55:] + '/'
                self.ShowDir(path_a)
                self.ftp.cwd('..')
            else:
                filepath = self.ftp.pwd() + '/' + f[55:0]
                self.show_list.append(filepath)
                print(filepath)
        return self.show_list

if __name__ == "__main__":
    #gxftp = FtpFunctionLib(Host='192.168.111.73', LoginPort=2121)
    #gxftp.FtpLogin('.')
    #gxftp.QueryRemoteFileList(".")
    #gxftp.DownloadFile("LSK.txt", "hsh.txt")
    #gxftp.UploadFile("LSK_file", "LSK_file.TXT")
    #gxftp.UploadDir("./LSK_dir", "LSK_dir")
    #gxftp.FtpQuit()
    gxftp = FtpFunctionLib(\
            Host = '192.168.111.101', UserName = 'guoxin', Password = 'Guoxin88156088',\
            FtpLoginBasicPath= './',  LoginPort = 2121)
    gxftp.FtpLogin('.')
    file_list = gxftp.ShowDir('Test_Entrance')
    gxftp.FtpQuit()
    print(file_list)

     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
