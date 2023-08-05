#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Testlink API Sample Python Client implementation
"""
python2=2
python3=3
python = 0
import re
import sys
version=re.match('3\.\d',sys.version)
if version:
    python=python3
version=re.match('2\.\d',sys.version)
if version:
    python=python2


import codecs
import os
if python==python2:
    import xmlrpclib
if python==python3:
    import xmlrpc.client
import unittest
import time
import threading

class TestlinkAPIClient:
    server_url = "http://192.168.110.254/testlink/lib/api/xmlrpc.php"
    def __init__(self, devKey=None, server_url=None):
        if devKey != None:
            self.devKey = devKey
        if server_url != None:
            self.server_url=server_url
        if python == python3:
            self.server = xmlrpc.client.Server(self.server_url)
        if python ==python2:
            self.server = xmlrpclib.Server(self.server_url)

    def addkeyvalue(self,dic,key,value):
        dic[key]=value
        return dic
    def reportTCResult(self, tcid, tpid, status,tbid=None,notes=None):	# 提交测试结果
        data = {"devKey":self.devKey, "testcaseid":tcid, "testplanid":tpid,\
                "status":status}
        if tbid != None:
            data = self.addkeyvalue(data,"buildid",tbid)
        else:
            data = self.addkeyvalue(data,"guess",True)
        if notes != None:
            data = self.addkeyvalue(data,"notes",notes)
        return self.server.tl.reportTCResult(data)

    def getInfo(self): # testlink版本信息
        return self.server.tl.about()

    def getProjects(self): # 获取所有项目
        key={"devKey":self.devKey}
        return self.server.tl.getProjects(key)

    def getTestProjectByName(self,name): # 根据项目名获取项目信息
        data={"devKey":self.devKey,"testprojectname":name}
        return self.server.tl.getTestProjectByName(data)

    def createBuild(self, plan_id, name, notes):
        data={"devKey":self.devKey,"testplanid":plan_id, "buildname":name}
        return self.server.tl.createBuild(data)

    def getProjectTestPlans(self, projid): # 根据项目id获取测试计划列表
        data = {"devKey":self.devKey, "testprojectid":projid}
        return self.server.tl.getProjectTestPlans(data)

    def getBuildsForTestPlan(self, tplanid): # 根据测试计划id获取指派的版本列表
        data = {"devKey":self.devKey, "testplanid":tplanid}
        return self.server.tl.getBuildsForTestPlan(data)

    def getLatestBuildForTestPlan(self, tplanid): # 根据测试计划id获取指派的最新版本版本
        data = {"devKey":self.devKey, "testplanid":tplanid}
        return self.server.tl.getLatestBuildForTestPlan(data)

#    def getTestBuildsForTestPlan(self, tplanid):
#        data = {"devKey":self.devKey, "testplanid":tplanid}
#        return self.server.tl.getTestBuildsForTestPlan(data)

    def getTestSuitesForTestPlan(self, tplanid): # 测试计划中所有用例的测试集列表
        data = {"devKey":self.devKey, "testplanid":tplanid}
        return self.server.tl.getTestSuitesForTestPlan(data)

    def getPlanIdByName(self, projid,name): # 根据项目id和测试计划名获取测试计划的id
        data = {"devKey":self.devKey, "testprojectid":projid}
        plans = self.server.tl.getProjectTestPlans(data)
        for plan in plans:
            if "name" in plan and plan["name"] == name:
                return plan["id"]
        return None

    def getTestCasesForTestPlan(self,tplanid,keywords,buildid,testcaseid = None,executed=None,executiontype=None): # 获取测试用例
        data = {"devKey":self.devKey, "testplanid":tplanid}
        if testcaseid != None:
            data = self.addkeyvalue(data,"testcaseid", testcaseid)
        if keywords != None:
            data = self.addkeyvalue(data,"keywords",keywords)
        if buildid != None:
            data = self.addkeyvalue(data,"buildid",buildid)
        if executed != None:
            data = self.addkeyvalue(data,"executed",executed)
            print ("executed",executed)
        if executiontype != None:
            data = self.addkeyvalue(data,"executiontype",executiontype)
        return self.server.tl.getTestCasesForTestPlan(data)

    def getTestCasesForTestSuite(self, tsuiteid, deep = None): # 获取测试集里的测试用例，deep为False时只包括当前测试集下的用例
        data = {"devKey":self.devKey, "testsuiteid":tsuiteid, "details":"full"}
        if deep != None:
            data = self.addkeyvalue(data,"deep", deep)
        return self.server.tl.getTestCasesForTestSuite(data)

    def getTestCaseCustomFieldDesignValue(self,externalid,projid,\
            customfieldname,version): # 根据用例标识id获取指定用例某自定义字段的值
        data = {"devKey":self.devKey, "testcaseexternalid":externalid,\
                "testprojectid":projid,"customfieldname":customfieldname,\
                "version":version}
        return self.server.tl.getTestCaseCustomFieldDesignValue(data)

#    def getKeywordSet(self,projid):
#        data = {}
#        self.addkeyvalue(data,"testprojectid",projid)
#        self.addkeyvalue(data,"devKey", self.devKey)
#        return self.server.tl.getKeywordsForProject(data)

    def createTestSuite(self,proj_id,suite_name,details,parentid,order,checkDuplicatedName,actionOnDuplicatedName): # 在测试项目有中创建测试集
        data = {"devKey":self.devKey}
        self.addkeyvalue(data,"testprojectid",proj_id)
        self.addkeyvalue(data,"testsuitename",suite_name)
        if checkDuplicatedName:
            self.addkeyvalue(data,"checkduplicatedname",checkDuplicatedName)
        if actionOnDuplicatedName:
            self.addkeyvalue(data,"actiononduplicatedname",actionOnDuplicatedName)
        if parentid:
            self.addkeyvalue(data,"parentid",parentid)
        if details:
            self.addkeyvalue(data,"details",details)
        if order:
            self.addkeyvalue(data,"order",order)
        return self.server.tl.createTestSuite(data);

    def getFirstLevelTestSuitesForTestProject(self,proj_id): # 获取第一级的测试集列表
        data = {"devKey":self.devKey,"testprojectid":proj_id}
        return self.server.tl.getFirstLevelTestSuitesForTestProject(data)

    def createTestCase(self, proj_id,suite_id,case_name,summary,preconditions,steps,importance,execution_type): # 创建测试用例
        data = {"devKey":self.devKey,"testprojectid":proj_id,\
                "testsuiteid":suite_id,"testcasename":case_name,
                "authorlogin":"wangshj"}
        if summary:
            self.addkeyvalue(data,"summary",summary)
        if preconditions:
            self.addkeyvalue(data,"preconditions",preconditions)
        if steps:
            self.addkeyvalue(data,"steps",steps)
            #steps = [{"step_number":1,"actions":"do what you want to do in this step","expected_result":"what it should be","execution_type":1},]
        return self.server.tl.createTestCase(data)
    def getTestSuitesForTestSuite(self,testsuiteid): # 根据测试集查找该测试集下所有的测试集
        data = {"devKey":self.devKey, "testsuiteid":testsuiteid}
        return self.server.tl.getTestSuitesForTestSuite(data)

    def getTestCase(self,testcase_id=None,external_id=None,version_number=None): # 根据用例id或标识获取测试用例
        data = {"devKey":self.devKey}
        if external_id != None:
            data = self.addkeyvalue(data,"testcaseexternalid",external_id)
        if version_number != None:
            data = self.addkeyvalue(data,"version",version_number)
        if testcase_id != None:
            data = self.addkeyvalue(data,"testcaseid",testcase_id)
        return self.server.tl.getTestCase(data)


    def addTestCaseToTestPlan(self, tprojid, tplanid, tc_external_id, version=None): # 根据测试用例标识id添加测试用例到测试计划
        data = {"devKey":self.devKey}
        if tc_external_id != None:
            data = self.addkeyvalue(data,"testcaseexternalid",tc_external_id)
        if version != None:
            data = self.addkeyvalue(data,"version",version)
        if tprojid != None:
            data = self.addkeyvalue(data,"testprojectid", tprojid)
        if tplanid != None:
            data = self.addkeyvalue(data,"testplanid", tplanid)
        return self.server.tl.addTestCaseToTestPlan(data)


class TestlinkClient(TestlinkAPIClient):
    def switchProjectToRun(self, proj_num = None,proj_name = None): # 选择项目
        projects = self.getProjects()
        if proj_name != None:
            for project in projects:
#                if project.has_key('name') == False:
                if 'name' not in project:
                    return -1
                elif project['name'] == proj_name:
                    return project["id"]
        if proj_num != None:
            return projects[proj_num]["id"]
        project_num = 0
        print ("In put the project num which you want to run:")
        for project in projects:
            print (project_num,":", project["name"])
            project_num += 1
        project_total_num = project_num
        project_num = int(sys.stdin.readline())
        if(project_num > project_total_num - 1):
            return -1
        return projects[project_num]["id"]

    def switchPlanToRun(self, projectid, plan_num = None, plan_name=None): # 选择项目的测试计划
        plans = self.getProjectTestPlans(projectid)
        if plan_name != None:
            for plan in plans:
#                if False == plan.has_key('name'):
                if 'name' not in plan:
                    return -1
                elif plan['name'] == plan_name:
                    return plan['id']
        if plan_num != None:
            return plans[plan_num]["id"]
        plan_num = 0
        print ("In put the plan num which you want to run:")
        for plan in plans:
            print (plan_num,":",plan["name"])
            plan_num += 1
        plan_total_num = plan_num
        plan_num = int(sys.stdin.readline())
        if plan_num > plan_total_num - 1:
            return -1
        return plans[plan_num]["id"]

    def switchBuildToRun(self,tplanid, build_num = None, build_name=None): #选择测试计划指派的版本
        builds = self.getBuildsForTestPlan(tplanid)
        if build_name != None:
            for build in builds:
#                if build.has_key('name') == False:
                if 'name' not in build:
                    return -1
                elif build['name'] == build_name:
                    return build['id']
        if build_num != None:
            return builds[build_num]["id"]
        build_num = 0
        print ("In put the build num which you want to run:")
        for build in builds:
            print (build_num,":",build["name"])
            build_num += 1
        build_total_num = build_num
        build_num = int(sys.stdin.readline())
        if build_num > build_total_num - 1:
            return -1
        return builds[build_num]["id"]

    def addTestSuit(self):
        return 0

    def createBuildAdvanced(self, project_name, plan_name, build_name, notes):
        project_info = self.getTestProjectByName(project_name)
        plan_id = self.getPlanIdByName(project_info[0]['id'], plan_name)
        build_list = self.getBuildsForTestPlan(plan_id)
        build_name_list = []
        build_name_final = build_name
        for build in build_list:
            build_name_list.append(build['name'])
        while 1:
            if build_name_final in build_name_list:
                build_name_final = build_name_final + "_" + build_name
            else:
                break;
        ret = self.createBuild(plan_id,build_name_final,notes)
        if ret[0]['status'] == True:
            return build_name_final
        else:
            return False

class TestlinkCaseManager:
    def __init__(self,userKey, proj_name = None):
        self.client = TestlinkClient(userKey)
        self.proj_name = proj_name

    def get_project_id_byname(self,proj_name = None): # 根据项目名获取项目id 
        return self.client.switchProjectToRun(proj_name=proj_name)

    def get_testcase_from_testlink(self, _run_type, _keyword, _build, _project, _plan): #获取指定项目测试计划版本的测试用例 
        if self.client == None:
            return None
        _testcases = []
        projid = self.client.switchProjectToRun(proj_name=_project)
        planid = self.client.switchPlanToRun(projid, _plan)
        buildid = self.client.switchBuildToRun(planid, _build)
        testcases_orign = self.client.getTestCasesForTestPlan(planid, _keyword, buildid, None, None, _run_type)
        if type(testcases_orign) == type({}):
            for _key,testcase in testcases_orign.items():
                _testcases.append(testcase[0])
        return _testcases,projid,planid,buildid

    def distribute_testcases(self, testcases,_key,_value): # 根据键值选择用例
        _expected = []
        _unexpected = []
        if testcases:
            for testcase in testcases:
                if testcase[_key] == _value:
                    _unexpected.append(testcase)
                else:
                    _expected.append(testcase)

        return _unexpected, _expected

    def get_run_cases(self,testcases_list,projid,_module):
        _cases = testcases_list
        casessuite = self.client.getTestCasesForTestSuite(\
                testcases_list[0]["testsuite_id"],"false")
        pre_external = casessuite[0]["external_id"]
        pre_external = re.sub("\d+","",pre_external)
        _run_cases = []
        for _testcase in testcases_list:
            external_id = _testcase["external_id"]
            external_id = pre_external + external_id
            _run_module = self.client.getTestCaseCustomFieldDesignValue(\
                external_id,projid, "module", int(_testcase["version"]))
            if _run_module == _module:
                _config = self.client.getTestCaseCustomFieldDesignValue(\
                external_id,projid, "config", int(_testcase["version"]))
                if _config != "Yes":
                    _run_cases.append(_testcase)
        return _run_cases

    def createTestSuite(self,proj_name,suite_name,parentid=None,details=None): # 创建测试用例集
        proj_id = self.get_project_id_byname(proj_name)
        self.client.createTestSuite(proj_id,suite_name,parentid,details,None,None,None)
        
    def getFirstLevelTestSuitesForTestProject(self,proj_id): # 获取第一级的测试集列表
        return self.client.getFirstLevelTestSuitesForTestProject(proj_id)

    def help(self):
        project_id = self.client.switchProjectToRun(None,None)
        plan_id = self.client.switchPlanToRun(project_id,None)
        build_id = self.client.switchBuildToRun(plan_id,None)
        return 


def copy_project(client,current_suiteid,case_prefix,current_suitename,to_parentsuiteid,to_projid): # 复制测试项目测试集
    print("copy",current_suitename,"...............")
    cur_cases=client.getTestCasesForTestSuite(current_suiteid,0)
    to_suite=None
    to_suite=client.createTestSuite(to_projid,current_suitename,None,to_parentsuiteid,None,None,None)
    if type(to_suite) == type([]):
        to_suite=to_suite[0]
    if to_suite["id"] == 0:
        if to_parentsuiteid == None:
            tmp_suites=client.getFirstLevelTestSuitesForTestProject(to_projid)
            for tmp_suite in tmp_suites:
                if tmp_suite["name"] == current_suitename:
                    to_suite=tmp_suite
                    break
        else:
            tmp_suites=client.getTestSuitesForTestSuite(to_parentsuiteid)
            if "id" in tmp_suites:
                to_suite=tmp_suites
            else:
                for key,tmp_suite in tmp_suites.items():
                    if tmp_suite["name"] == current_suitename:
                        to_suite=tmp_suite
            #if "id" in tmp_suites:
    #print(to_suite)
    #print(len(cur_cases))
    if len(cur_cases) > 0:
        for cur_case in cur_cases:
            testcase=client.getTestCase(testcase_id=None,external_id=case_prefix+"-"+cur_case["tc_external_id"],version_number=None)
            testcase=testcase[0]
            client.createTestCase(to_projid,to_suite["id"],testcase["name"],cur_case["summary"], \
                    cur_case["preconditions"],testcase["steps"],cur_case["importance"],cur_case["execution_type"])
    next_lever_suites=client.getTestSuitesForTestSuite(current_suiteid)
    #print(next_lever_suites)
    #print(type(next_lever_suites))
    print(type(" "))
    print("next_lever_suites:",type(next_lever_suites))
    if type(next_lever_suites) != type(" "):
        print(next_lever_suites.items())
        for key,next_lever_suite in next_lever_suites.items():
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(type(next_lever_suite))
            print(type(to_suite))

            print("next_lever:",next_lever_suite)
            print("to_suite:",to_suite)
            print("######################################################################")
            #print(next_lever_suite["name"])
            if "id" not in next_lever_suites:
                copy_project(client,next_lever_suite["id"],case_prefix,next_lever_suite["name"],to_suite["id"],to_projid)  
            else:
                #print(type(next_lever_suites))
                #print(next_lever_suites)
                copy_project(client,next_lever_suites["id"],case_prefix,next_lever_suites["name"],to_suite["id"],to_projid)  
                break
    return


class AutotestTestlinkThreading: # 提交测试报告线程类
    server_url = "http://192.168.110.254/testlink/lib/api/xmlrpc.php"
    userkey = "b5968cdffc0c9bc6d0dd80267dc170e2" # autotest
    project_name = None 
    plan_name = None 
    build_name = None
    client = None
    projid = -1
    project = None
    planid = -1
    buildid = -1
    cases_list = []
    _thread = None
    ThreadStatus = False
    tl_status = False # testlink网络通信是否正常 
    timeout = 300 # 等待提交结果结束的超时时间5min
    result_fw = None

    def __init__(self, server_url, userkey, project_name, plan_name, build_name):
        if server_url != None:
            self.server_url=server_url
        if userkey != None:
            self.userkey=userkey
        if project_name != None:
            self.project_name=project_name
        if plan_name != None:
            self.plan_name=plan_name
        if build_name != None:
            self.build_name=build_name

    def __del__(self):
        if self._thread != None:
            self._thread.join()

    def report_testlink_thread(self): # 提交测试结果子线程
        _time = 0
        self.ThreadStatus = True
        print("testlink threading start !!!")
        while True:
            case_dict={'externalid_list': None, 'status': None, 'notes': None}
            externalid_list = None
            status = None
            notes = None
            if self.ThreadStatus == False:
                break
            if len(self.cases_list) > 0:
                case_dict = self.cases_list[0] 
                externalid_list = case_dict['externalid_list']
                status = case_dict['status']
                notes = case_dict['notes']
                if len(self.cases_list) > 0:
                    del self.cases_list[0]
            if externalid_list != None:
                num = 0
                while True:
                    if num > len(externalid_list)-1:
                        break
                    externalid = externalid_list[num]
                    case_result = "case:"+externalid+", case status:"+status
                    externalid = self.project['prefix'] + '-' + externalid
                    try:
                        testcase=self.client.getTestCase(None, externalid, None)[0]
                        #if testcase.has_key('testcase_id') == False:
                        if 'testcase_id' not in testcase:
                            print(externalid ," : testlink case does not exist!!")
                            print(testcase)
                            case_result = case_result+", report status:case not exist\n"
                        else:
                            case=self.client.getTestCasesForTestPlan(self.planid,None,self.buildid,testcase['testcase_id'],None,None)
                            if type(case) != type({}):
                                print(externalid, " : testlink case no exist in plan(" + self.plan_name + ")!!")
                                print(case)
                                case_result = case_result+", report status:case not exist in plan("+self.plan_name+")\n"
                            else:
                                if python==python2:
                                    case=case.values()[0]
                                else:
                                    case=list(case.values())[0]

                                case=case[0]
                                #if case.has_key('exec_status') == False:
                                if 'exec_status' not in case:
                                    print(externalid, " : testlink case no exist in plan(" + self.plan_name + ")!!")
                                    print(case)
                                    case_result = case_result+", report status:case not exist in plan("+self.plan_name+")\n"
                                elif case['exec_status'] == 'f': 
                                    # 用例原来的执行结果为失败时，不改变执行结果
                                    case_result = case_result+", report status:report result ignore, "
                                    case_result = case_result+"original status: f, final status: f\n" 
                                    pass
                                elif case['exec_status'] == 'b' and status != 'f': 
                                    # 用例原来执行结果为锁定，只有自动化执行为失败时改变执行结果
                                    case_result = case_result+", report status:report result ignore, "
                                    case_result = case_result+"original status: b, final status: b\n" 
                                    pass
                                elif case['exec_status'] == 'p' and status == 'p':
                                    case_result = case_result+", report status:report result ignore, "
                                    case_result = case_result+"original status: p, final status: p\n" 
                                    pass
                                else:
                                    ret=self.client.reportTCResult(testcase['testcase_id'], self.planid, status, self.buildid, notes)
                                    if ret[0]['message'] != 'Success!':
                                        print(externalid, ": testlink report result failed!!")
                                        print(ret[0])
                                        case_result = case_result+", report status:report result failed, " 
                                        case_result = case_result+"original status: "+case['exec_status']+'\n'
                                        case_result = case_result+", final status: "+case['exec_status']+'\n' 
                                    else:
                                        case_result = case_result+", report status:report result success,"
                                        case_result = case_result+"original status: "+case['exec_status']+'\n'
                                        case_result = case_result+", final status: "+status+'\n'
                    except:
                            self.tl_status = False
                            time.sleep(5)
                            _time = _time+1
                            if _time == 100: # testlink重新连接100次，如果打印连接出错,继续重新连接
                                print("testlink communication error !!!") 
                                _time = 0
                            self.client=TestlinkClient(self.userkey, self.server_url) # testlink网络通信不正常,重新连接
                    else:
                        self.tl_status = True
                        num = num+1
                        _time = 0
                        self.result_fw.write(case_result)
                        self.result_fw.flush()
            else:
                time.sleep(1)
        print("testlink threading finish !!!")

    def thread_start(self): # 创建提交测试结果线程
        if self.userkey == None or self.server_url == None or self.project_name == None or self.plan_name == None or self.build_name == None:
            return False
        self.client=TestlinkClient(self.userkey, self.server_url)
#       self.projid=self.client.switchProjectToRun(None, self.project_name)
        self.project = self.client.getTestProjectByName(self.project_name)
        if type(self.project) == type([]):
            self.project = self.project[0]
#        if type(self.project) != type({}) or self.project.has_key('id') == False:
        if type(self.project) != type({}) or 'id' not in self.project == False:
            print(self.project_name, " : testlink project does not exist!!")
            return False
        self.projid = self.project['id']
        self.planid=self.client.switchPlanToRun(self.projid, None, self.plan_name)
        if self.planid == -1:
            print(self.plan_name, " : testlink plan does not exist!!")
            return False
        self.buildid=self.client.switchBuildToRun(self.planid, None, self.build_name)
        if self.buildid == -1:
            print(self.build_name, " : testlink build does not exist!!")
            return False
        self.tl_status = True
        TIMEFORMAT ='%Y-%m-%d-%H-%M-%S'
        result_file = time.strftime(TIMEFORMAT, time.localtime( time.time() ) ) + "_result.txt"
        self.result_fw = open(result_file, "w")
        self._thread = threading.Thread(target=self.report_testlink_thread)
        self._thread.setDaemon(True)
        self._thread.start()

    def thread_stop(self): # 中断提交测试结果的线程
	    self.ThreadStatus = False 

    def thread_wait(self): # 等待提交测试结果的过程结束
        _time = 0
        print("testlink threading is running，please wait a little later ...")
        while len(self.cases_list):
            if self.tl_status == False:
                break
            elif _time == self.timeout:
                break
            else:
                time.sleep(1)
                _time = _time+1
        self.ThreadStatus = False 
        if self._thread != None:
            self._thread.join()
        if len(self.cases_list) > 0:
            for tmp_dict in self.cases_list:
                for externalid in tmp_dict['externalid_list']:
                    case_result = "case:"+externalid+", case status:"+tmp_dict['status']+", report status:have not reported\n"
                    self.result_fw.write(case_result)
                    self.result_fw.flush()
        self.result_fw.close

    def report_result(self, externalid_list = None, status = None, notes = None): # 提交测试结果
        if externalid_list == None or status == None or externalid_list == []:
            return False
        result_dict = {'externalid_list': None, 'status': None, 'notes': None}
        result_dict['externalid_list'] = externalid_list
        result_dict['status'] = status
        result_dict['notes'] = notes
        self.cases_list.append(result_dict)
        return True
