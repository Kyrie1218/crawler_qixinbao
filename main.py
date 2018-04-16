#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# import re
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver import Firefox
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support import expected_conditions as expected
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.proxy import *
# import time
# import uuid
# import random

# import os


# from tools.database.mysql import mysql
# from tools.database.redis import redis
# from tools.proxy.proxy import proxy

import configparser
from tools.crawler.crawler import Crawler




# class Crawler(object):


#   def filter_tags(self, htmlstr):
#     print(htmlstr)
#     return
#     #先过滤CDATA
#     # re_cdata   = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
#     # re_script  = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
#     # re_style   = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
#     # re_br      = re.compile('<br\s*?/?>')#处理换行
#     re_h       = re.compile('</?\w+[^>]*>')#HTML标签
#     # re_comment = re.compile('<!--[^>]*-->')#HTML注释
#     # html          = re_cdata.sub('',htmlstr)#去掉CDATA


#     # html          = re_script.sub('',html) #去掉SCRIPT
#     # html          = re_style.sub('',html)#去掉style
#     # html          = re_br.sub('\n',html)#将br转换为换行
#     html          = re_h.sub('',htmlstr) #去掉HTML 标签
#     # html          = re_comment.sub('',html)#去掉HTML注释
#     #去掉多余的空行
#     # blank_line = re.compile('\n+')
#     # html          = blank_line.sub('\n',html)

#     return html



#   def __init__(self):

#     conf = self.getConfig()

#     self.company_name_url = conf.get('url')
#     self.host             = conf.get('host')
#     self.username         = conf.get('username')
#     self.password         = conf.get('password')
#     self.dbname           = conf.get('dbname')
#     self.total_page       = conf.get('total_page')

#     self.redis_host       = conf.get('redis_host')
#     self.redis_port       = conf.get('redis_port')

#     # self.db = database.Database

#     # self.conn = self.db.connect(self.host, self.username, self.password, self.dbname)
#     self.handle = redis.Redis(self.redis_host, self.redis_port)


#     try:

#       # 获得网络驱动器实例对象
#       self.driver = self.createDriver()

#       for vo in range(1, self.total_page):

#         url = self.company_name_url +str(vo)

#         self.crawlerInfo(url)
#         time.sleep(20)

#     except Exception as e:
#       print(e)


def init():

  cf = configparser.ConfigParser()

  cf.read("config.conf")

  result = {}

  # database
  result['host']     = cf.get("db", "host")
  result['port']     = cf.getint("db", "port")
  result['username'] = cf.get("db", "username")
  result['password'] = cf.get("db", "password")
  result['dbname']   = cf.get("db", "dbname")

  # or
  result['total_page'] = cf.getint("or", "total_page")
  result['url']        = cf.get("or", "url")

  # redis
  result['redis_host']     = cf.get("redis", "host")
  result['redis_port']     = cf.getint("redis", "port")

  # log
  result['level']     = cf.get("log", "level")

  return result



if __name__ == '__main__':

  # 获得配置文件信息
  init = init()

  # 初始化 Crawler 对象
  crawler = Crawler(init['redis_host'], init['redis_port'], init['level'])

  handle = crawler.get_driver()

  print(handle)

