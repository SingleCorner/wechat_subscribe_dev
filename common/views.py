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
    elif MsgType == "event":
      Request = "subscribe"
    else:
      Request = "unsupport"

    if Request == "?":
      Message = "目前支持的命令\n\n[1]bind account password\n[2]group list"
    elif Request == "subscribe":
      Message = "欢迎关注本公众号\n目前已对接运维管理平台\nhttp://ops.siner.us\n需要帮助请输入 ?\n\n开源地址https://github.com/SingleCorner/wechat_subscribe_dev \n\n运维管理平台开源开发\n有合作意向联系微信CSZ9227"
    elif Request == "unsupport":
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
    Message = "运维平台遇到问题，暂时无法提供服务"
    response = render(request, "text.xml", locals())
  return HttpResponse(response, content_type="text/xml")

def test(request):
  result = {}
  requrl = "http://localhost:8001/apitest"
  req_data = urllib.urlencode({'wechat_key':'testkey','request':'group list' })
  req = urllib2.Request(url = requrl,data = req_data)
  res_data = urllib2.urlopen(req).read()
  msg = json.loads(res_data)
  result = msg
  return HttpResponse(json.dumps(result), content_type="application/json")