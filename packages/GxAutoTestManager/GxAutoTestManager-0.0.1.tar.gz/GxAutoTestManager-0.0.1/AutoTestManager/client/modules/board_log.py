#!/usr/bin/python3
#coding:utf-8

'''
TODO 板子 log 解析需要封装成库
'''


class BoardLog():
    def __init__(self, case_start_string, case_end_string, question_string, crash_string, test_end_string, cumulative_question_string):
        self.case_start_string = case_start_string
        self.case_end_string = case_end_string
        self.question_string = question_string
        self.crash_string = crash_string
        self.test_end_string = test_end_string
        self.cumulative_question_string = cumulative_question_string
        #self.reboot_string = []
        #self.streamxpress_string = []

    def get_running_case(self):
        pass


if __name__ == '__main__':
    case_start_string = [
            'case start: ',
            '\[case start\]: '
            ]
    case_end_string = [
            'testcase---.+---pass---',
            'testcase---.+---failed---',
            'testcase---.+---lock---',
            '\[OK\] ',
            '\[  FAILED\] '
            ]
    test_end_string = [
            'ALL_CASE_HAVE_RUN'
            ]
    question_string = [
            'failed description:.+; file:'
            ]
    cumulative_question_string = [
            'd!!!', 'minifs \[/view_info_db\] create',
            'decode_writed_callback 1508 overflow 1'
            ]
    crash_string = [
            'Kernel panic',
            'rcu_sched self-detected stall on'
            ]
    board_log = BoardLog(case_start_string, case_end_string, question_string, crash_string, test_end_string, cumulative_question_string)

