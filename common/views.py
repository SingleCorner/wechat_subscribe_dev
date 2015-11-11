# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import *
from lxml import etree

import hashlib, random, string, re
import datetime, time
#import json, netsnmp
import json

#from common.models import Account, Logrecord
#from AutoO.apps.models import Project

def cuser(request):
  if 'echostr' in request.GET:
    a = request.GET['echostr']
  else:
    try:
      xml_body = request.body
      xml = etree.fromstring(xml_body)
      toUser = xml.find('FromUserName').text
      timestamp = xml.find('CreateTime').text
      Request = xml.find('Content').text
      if Request == "广告":
        Message = "真正的秒到账pos，养卡套现神器/::B/::B/::B有需要电话联系哦/::B15821303362"
      else:
        Message = Request
      MsgType = xml.find('MsgType').text
      if MsgType == "event":
        Message = "欢迎关注单边角落的私人订阅号" 
      else:
        pass
      a = render(request, "text.xml", locals())
    except:
      a = ""
  return HttpResponse(a, content_type="text/xml")
