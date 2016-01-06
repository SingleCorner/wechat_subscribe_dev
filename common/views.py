# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import *
from lxml import etree

import hashlib, random, string, re
import datetime, time
#import json, netsnmp
import json
import urllib,urllib2

#from common.models import Account, Logrecord
#from AutoO.apps.models import Project

def cuser(request):
  try:
    xml_body = request.body
    xml = etree.fromstring(xml_body)
    toUser = xml.find('FromUserName').text
    timestamp = xml.find('CreateTime').text
    Request = xml.find('Content').text
    command = Request.split(',')[0]
    if Request == "test":
      Message = "真正的秒到账pos，养卡套现神器/::B/::B/::B有需要电话联系哦/::B15821303362"
    else:
      if command == "group":
        req_url = "http://weixin.siner.us/openneer"
        req_data = urllib.Request({'wechat_key':toUser, 'request':Request, 'command':command}) 
        req = urllib2.Request(url = requrl,data = req_data)
        res = urllib2.urlopen(req).read()
        res_data = json.loads(res)
        if res_data['code'] == 1:
          Message = res_data['message']
        else:
          i = 0
          for msg in res_data['group']:
            Message = Message + msg.i + "<br>"
      else:
        Message = Request
    MsgType = xml.find('MsgType').text
    if MsgType == "event":
      Message = "欢迎关注单边角落的私人订阅号<br/>测试换行" 
    else:
      pass
    a = render(request, "text.xml", locals())
  except:
    a = ""
  return HttpResponse(a, content_type="text/xml")

def test(request):
  result = {}
  requrl = "http://localhost:8001/api"
  req_data = urllib.urlencode({'wechat_key':'gh_ddkjfkjkd', 'command':'group', })
  req = urllib2.Request(url = requrl,data = req_data)
  res_data = urllib2.urlopen(req).read()
  msg = json.loads(res_data)
  result['code'] = msg['Token']
  result['message'] = msg['command']
  return HttpResponse(json.dumps(result), content_type="application/json")