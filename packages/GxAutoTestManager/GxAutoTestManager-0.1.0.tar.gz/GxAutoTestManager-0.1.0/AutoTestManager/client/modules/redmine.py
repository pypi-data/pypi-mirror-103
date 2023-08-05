#!/usr/bin/python3
#coding:utf-8

import os
import time
from redminelib import Redmine
if (os.path.exists("/usr/local/lib/python2.7/dist-packages/SendEmail.py")):
    from SendEmail import send_email
    enable_email = 1
else:
    enable_email = 0

class GxRedmine():
    def __init__(self, url = 'http://192.168.190.239:3000', key = 'e13cb117c99f6fe8c0fc0b16ffccb3f22a985169', proj_id = 'stb-product', new_redmine = 1, email_receivers = ['chenwei1@nationalchip.com']):
        self.url = url
        self.key = key
        self.proj_id = proj_id
        self.gx_redmine = Redmine(url, key = key)
        self.formal_redmine = Redmine('http://192.168.110.254/redmine', key = '6520dcfee2f3c2bddebfa7fa6df1934b0ed2aea6')
        self.new_redmine = new_redmine
        self.email_receivers = email_receivers
        self.ISOTIMEFORMAT = '%Y-%m-%d-%H-%M-%S'

    def new_issue(self, subject, description, log_name, log_fd):
        issue = self.gx_redmine.issue.new()
        issue.project_id = self.proj_id
        issue.subject = log_name + " " + subject
        issue.description = description
        issue.status_id = 1 # 打开
        issue.priority_id = 2 # 普通
        ret = None
        if self.new_redmine:
            issue.custom_fields = [
                    {'id': 2, 'value': u"随机"}
            ]
        else:
            issue.custom_fields = [
                    {'id': 20, 'value': u"随机"}
            ]
        issue.uploads = []

        try:
            ret = issue.save()
        except Exception as e:
            print("issue.save ", str(e))
            log_fd.write(time.strftime(self.ISOTIMEFORMAT, time.localtime(time.time())) + " issue.save " + str(e))
            if enable_email:
                send_email("可以通过标题中指定的log文件找出问题提交失败的用例", log_name + " issue.save " + str(e), self.email_receivers)

        if ret:
            return ret.id if ret.id else 'unknow'
        else:
            return "unknow"

    def get_board_by_public_id(self, public_id):
        if not public_id:
            return ''
        custom_fields = self.formal_redmine.issue.filter(cf_109=public_id)[0]['custom_fields']
        for custom_field in custom_fields:
            if custom_field['name'] == '板级':
                print(custom_field['value'])
                return custom_field['value']
        return ''

    def comment_issue(self):
        pass

    def modify_issue_status(self):
        pass

    def add_reviewer(self):
        pass

    # redmine.issue.get(redmine.issue.search('e27a872813a70407')[0]['id'])['custom_fields'][12]['value']

if __name__ == '__main__':
    gxredmine = GxRedmine()
    #log_fd = open('redmine_module_log', 'w')
    #issue_id = gxredmine.new_issue('subject', 'description', 'log_name', log_fd)
    #print(issue_id)

    #没有找到通过自定义字段作为筛选条件的搜索方法
    #直接搜索 public id 会搜出多个问题（搜出了所有 redmine 项目的问题）
    #没有找到只搜索某个 redmine 项目中的问题的方法

    gxredmine.get_board_by_public_id('e27a872813a70407')

