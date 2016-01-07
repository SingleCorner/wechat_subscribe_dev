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
    else if MsgType == "event":
      Request = "welcome"
    else:
      Request = "unsupport"

    if Request == "test":
      Message = "真正的秒到账pos，养卡套现神器/::B/::B/::B有需要电话联系哦/::B15821303362"
    else if Request == "?":
      Message = "目前支持的命令\n[1]bind account password\n\n[2]group list"
    else if Request == "welcome":
      Message = "欢迎关注本公众号\n目前已对接运维管理系统\nhttp://ops.siner.us\n帮助请输入 ?"
    else if Request == "unsupport":
      Message = "暂时不支持，有问题联系微信CSZ9227"
    else:
      req_url = "http://ops.siner.us/api"
      req_data = urllib.urlencode({'wechat_key':toUser, 'request':Request}) 
      req = urllib2.Request(url = req_url,data = req_data)
      res = urllib2.urlopen(req).read()
      res_data = json.loads(res)
      if res_data['code'] == 1:
        Message = res_data['message']
      else:
        i = 0
        Message = ""
        for msg in res_data['group']:
          Message = Message + res_data['group'][msg] + "\n"
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