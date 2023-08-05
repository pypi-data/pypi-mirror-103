# -*- coding: utf-8 -*-

class GenMsg(object):
    def __init__(self):
        pass

    def msg_format(self):
        message_format = {
            "ip":"",
            "port":"",
            "priority":2,
            "sync":"",
            "receiver":"",
            "name":"",
            "message_content":{},
            "answer":"",
            }
        return message_format

    def query_client_info(self):
        content = {
            "specific_client":{ # 指定具体某个客户端，
                "client_ip":"",
                "client_port":"",        
                },
            "filter":{ # 包含下列筛选条件的板子的客户端
                "chip":"",
                "board":"", # 必填
                "arch":"", # csky arm
                "os":"",
                "signal":"",
                "usb_storage_type":"", # FAT32、NTFS
                },
            }
        return content

    def board_power(self):
        content = {
            "client_ip":'',
            "client_port":'',
            "board_name":'',
            "operation":'',
                }
        return content

    def add_board(self):
        content = {
                'client_name':'',
                "client_ip":"",
                "client_port":"",
                "dvb_ai":"",
                "ai_board_dict":[],
                "stb_board_dict":[
                    {
                        "board_name":"",
                        "arch":"",
                        "chip":"",
                        "board":"",
                        "test_serial":"",
                        "electric_relay_serial":"",
                        "electric_relay_port":"",
                        "signal":"",
                        "usb_device":"",
                        "usb_gxbus":"",
                        "usb_storage_type":"", # FAT32、NTFS
                        "usb_partition_num":"",
                        "web":"",
                        "usb_wifi":"",
                        "usb_wifi_type":"",# 7601, 5370
                        "test_project_bind":"", # gxbus\api\solution
                        "secure":"", #true, false
                        "mode":"", # 运行模式:"test","gxdebug","firmware"
                        "status":"", # "idle"、"busy"
                        "running_info":{
                            "os":"",
                            "running_status":"", #“downloading”、“running”、“download_failed”、“drop_out”、“delete”
                            "jenkins_project_name":"",
                            "jenkins_build":"",
                            "test_process_id":"", # 中途停止测试时需要关闭对应测试进程
                            "boot_process_id":"", # 中途停止测试时需要关闭对应 boot 进程
                        },
                        "gxdebug_info":{
                            "ip_port":"", # 例如 3001
                            "board_serial":"", # 例如 /dev/ttyUSBGX6
                            "board_name":"", # 例如 sirius_6613H2-NNE
                            "jlink_control_serial":"",
                            "post_ip":"", # 例如 192.168.111.41
                            "board_control_port":"", # 例如 1
                            "gdbport":"", # 例如 2333
                            "jkink_control_port":"", #　例如 1
                            "ip":"", # 例如 192.168.111.201
                            "board_control_serial":"", # 例如 /dev/ttyUSBGX1
                            "gdbnum":"", # 例如 CKLink_Pro_V1-003-018
                        },
                    },
                ],
        }
        return content

    def update_board(self):
        content = {
                "client_ip":"",
                "client_port":"",
                "board_name":"",
                "dvb_ai":"",
                "board_info":{}
                }
        return content

    def delete_board(self):
        content = {
                "client_ip":'',
                "client_port":'',
                "board_name":'',
                "board":'',
                "chip":'',
                }
        return content

    def list_message_queue(self):
        content = {
            "priority": '' # 0,1,2,3,all
                }
        return content

    def clear_message_queue(self):
        content = {
            "priority": '' # 0,1,2,3,all
                }
        return content

    def delete_task(self):
        content = {
            "jenkins_project_name":"",
            "jenkins_build":"",
            }
        return content

    def start(self):
        content = {
            "dvb_ai":"", # 必填
            "dvb_info":{
                "test_info":{
                    "bin_url":"", # 必填
                    "boot_file_url":"", # 必填
                    "boot_tool_url":"", # 必填
                    "os":"",
                    "mode":"", #必填 test firmware
                    },
                "auto_board":{ # 必填
                    "arch":"", # csky arm
                    "chip":"",
                    "board":"", # 必填
                    "signal":"", # true false
                    "usb_device":"", # true false
                    "usb_device_gxbus":"", # true false
                    "usb_storage_type":"", # FAT32、NTFS
                    "usb_partition_num":"",# 1,2,3
                    "web":"", # true false
                    "usb_wifi":"", # True False
                    "usb_wifi_type":"", # 7601, 5370
                    "secure":"", #true, false
                    "priority":"", 
                    },
                "specific_board":{ # 可选，指定使用某块板子进行测试，若命令客户端未指定则由服务端自动填写
                    "client_ip":"",
                    "client_port":"",
                    "board_name":"",
                    },
                "jenkins_info":{ # 可选
                    "jenkins_project_name":"",
                    "jenkins_build_id":"",
                    },
                "gerrit_info":{ # 可选
                    "gerrit_id":"",
                    "gerrit_patch":"",
                    },
                "testlink_info":{ # 可选
                    "testlink_project":"",
                    "testlink_plan":"",
                    "testlink_build":"",
                    },
                },
            "ai_info":{ # 预留
                "task_type":"",
                "task_info":{
                    "bin_url":"",
                    "board":"",
                    },
                "jenkins_info":{ # 可选
                    "jenkins_project_name":"",
                    "jenkins_build_id":"",
                    },
                "gerrit_info":{ # 可选
                    "gerrit_id":"",
                    "gerrit_patch":"",
                    },
                "testlink_info":{ # 可选
                    "testlink_project":"",
                    "testlink_plan":"",
                    "testlink_build":"",
                    },
                },
            } 
        return content

    def stop(self):
        content = {
            "type":"", # all/jenkins/specific/filter
            "jenkins_info":{ # 指定某一个 Jenkins 工程的某一次构建的所有 bin
                "jenkins_project_name":"",
                "jenkins_build_id":"",
            },
            "specific_board":{ # 指定具体某一块板子，
                "client_ip":"",
                "client_port":"",
                "board_name":"",        
            },
            "board_info":{ #或者某一型号板子
                "chip":"",
                "board":"", # 必填
                "arch":"", # csky arm
                "os":"",
                "signal":"",
                "usb_storage_type":"", # FAT32、NTFS
            },
        }
        return content

    def switch_mode(self):
        content = {
            "client_ip":"",
            "client_port":"",
            "board_name":"",
            "mode_need_modify":"",
            "mode_after_modify":"",
            "force":"",
            }
        return content

    def hardware_detect(self):
        content = {
            "client_ip":"",
            "client_port":"",
            "board_name":"",
            }
        return content

    def board_log(self):
        content = {
                "type":"",
                "client_ip" : "",
                "client_port": "",
                "board_name":"",
                'file_name':"",
                'size':"",
            }
        return content

    def client_log(self):
        content = {
                "type":"",
                "client_ip" : "",
                "client_port": "",
                'file_name':"",
                'size':"",
                'level':"",
                'msg_filter':"",
                'time_before':"",
                'time_after':"",
            }
        return content
    
    def server_log(self):
        content = {
                "type":"",
                'file_name':"",
                'level':"",
                'msg_filter':"",
                'time_before':"",
                'time_after':"",
            }
        return content

    def server_stash(self):
        content = {}
        return content

    def server_resume(self):
        content = {}
        return content

    def get_test_result(self):
        content = {
                'task_bin':''
                }
        return content
