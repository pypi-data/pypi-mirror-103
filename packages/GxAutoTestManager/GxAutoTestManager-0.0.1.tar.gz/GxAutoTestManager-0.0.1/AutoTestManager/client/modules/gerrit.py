#!/usr/bin/python3
#coding:utf-8

from requests.auth import HTTPDigestAuth
from pygerrit2.rest import GerritRestAPI, GerritReview

class GxGerrit():
    def __init__(self, url = 'http://git.nationalchip.com/gerrit', user = 'chenwei1', passwd = 'AflJWyRfICejpz0mXkaaM4IkRULiFwpbjP+4ojLwdQ'):
        self.url = url
        self.user = user
        self.passwd = passwd

        self.auth = HTTPDigestAuth(self.user, self.passwd)
        self.rest = GerritRestAPI(url = self.url, auth = self.auth)

    def code_review(self, change_id, revision, code_review, message = 'test result'):
        if not change_id or not revision:
            print('change_id = {}, revision = {}'.format(change_id, revision))
            return False
        gr = GerritReview()
        gr.set_message(message)
        gr.add_labels({'Verified': 0, 'Code-Review': code_review})
        self.rest.review(change_id, revision, review = gr)

    def get_change_newest_revision_by_id(self, change_id):
        endpoint = "/changes/" + str(change_id) + "/detail"
        changes = self.rest.get(endpoint = endpoint)
        newest_revision = 0
        for msg in changes['messages']:
            if msg['_revision_number'] > newest_revision:
                newest_revision = msg['_revision_number']
        return newest_revision

    # 后面是预留接口

    def get_topic_by_change(self, change):
        endpoint = "/changes/" + str(change) + "/topic"
        topic = self.rest.get(endpoint = endpoint)
        return topic

    def get_changes_by_topic(self, topic):
        # 没找到实现方法
        pass

    def get_change_by_id(self, change_id):
        endpoint = "/changes/" + str(change_id)
        changes = self.rest.get(endpoint = endpoint)
        return changes


if __name__ == '__main__':
    gx_gerrit = GxGerrit()
    #newest_revision = gx_gerrit.get_change_newest_revision_by_id(change_id = '72820')
    #print(newest_revision)
    print("test")
    gx_gerrit.code_review(change_id = '73360', revision = '1', code_review = -1)
    gx_gerrit.code_review(change_id = '73360', revision = '1', code_review = +1)
    #gx_gerrit.get_change_by_id(change_id = '72820')
    #gx_gerrit.get_change_by_topic(topic = '72820')
    #gx_gerrit.get_change_by_topic(topic = '269590')
