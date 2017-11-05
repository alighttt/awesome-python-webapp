#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import requests
import time

class XiaoHong(object):
    def __init__(self):
        self.session = requests.Session()

    def login(self):
        params = json.dumps({"username": "5707", "password": "870909"})
        headers = {'content-type': 'application/json'}
        r = self.session.post('http://sales.baixing.com.cn/api/v1/session', data=params, headers=headers)
        r.encoding = 'utf-8'
        data = json.loads(r.text)
        return data.get("status")

    def refresh(self):
        params = json.dumps({"fields": {"lead_top_category": "fuwu"}, "per_page": "20", "page": "1"})
        headers = {'content-type': 'application/json'}
        r = self.session.post('https://sales.baixing.com.cn/api/v1/taomi', data=params, headers=headers)
        r.encoding = 'utf-8'
        return json.loads(r.text)

    def grab(self, id):
        params = json.dumps({"lead_ids": id})
        headers = {'content-type': 'application/json'}
        r = self.session.post('https://sales.baixing.com.cn/api/v1/taomi/grab_leads_from_public_sea', data=params, headers=headers)
        r.encoding = 'utf-8'
        return json.loads(r.text)

if __name__ == '__main__':
    xh = XiaoHong()
    if xh.login() != 0:
        print "log in failed, please try again"
    else:
        print "log in success, start to grab customer..."
        lasttime = int(time.time())

        while 1:
            time.sleep(3)        
            data = xh.refresh()
            if data.get("status") != 0:
                if xh.login() != 0:
                    print "log in failed, please try again"
                    break
                else:
                    print "re log  in success, start to grab customer..."
            nowtime = data.get("result").get("leads")[0].get("create_time")
            if nowtime > lasttime:
                grabdata = xh.grab(data.get("result").get("leads")[0].get("id"))
                if grabdata.get("status") == 0:
                    print "grab a customer: ", data.get("result").get("leads")[0].get("short_name")
                    lasttime = nowtime
