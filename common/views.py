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
    MsgType = xml.find('MsgType').text
    if MsgType == "text":      
      Request = xml.find('Content').text
      command = Request.split(' ')[0]
    else:
      Request = ""
      command = ""
    if Request == "test":
      Message = "真正的秒到账pos，养卡套现神器/::B/::B/::B有需要电话联系哦/::B15821303362"
    else:
      if command == "group":
        req_url = "http://ops.siner.us/api"
        req_data = urllib.urlencode({'wechat_key':toUser, 'request':Request, 'command':command}) 
        req = urllib2.Request(url = requrl,data = req_data)
        res = urllib2.urlopen(req).read()
        res_data = json.loads(res)
        if res_data['code'] == 1:
          Message = res_data['message']
        else:
          i = 0
          Message = ""
          for msg in res_data['group']:
            Message = Message + res_data['group'][msg] + "\n"
      else:
        Message = Request
    if MsgType == "event":
      Message = "欢迎关注单边角落\n目前已对接http://ops.siner.us\n支持命令\nbind 用户名 密码\ngroup list"
    response = render(request, "text.xml", locals())
  except:
    Message = "test"
    response = render(request, "text.xml", locals())
  return HttpResponse(response, content_type="text/xml")

def test(request):
  result = {}
  requrl = "http://ops.siner.us/apitest"
  req_data = urllib.urlencode({'wechat_key':'o4UAIuOcShDerXe0xLaImYfBkfzw', 'command':'group', 'request':'group list' })
  req = urllib2.Request(url = requrl,data = req_data)
  res_data = urllib2.urlopen(req).read()
  msg = json.loads(res_data)
  result = msg
  return HttpResponse(json.dumps(result), content_type="application/json")