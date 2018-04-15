#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import time
import random
import os
import redis
import urllib2

from selenium.webdriver.common.proxy import *

class Crawler(object):


  def filter_tags(self, htmlstr):
    print(htmlstr)
    return
    #先过滤CDATA
    # re_cdata   = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    # re_script  = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    # re_style   = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    # re_br      = re.compile('<br\s*?/?>')#处理换行
    re_h       = re.compile('</?\w+[^>]*>')#HTML标签
    # re_comment = re.compile('<!--[^>]*-->')#HTML注释
    # html          = re_cdata.sub('',htmlstr)#去掉CDATA


    # html          = re_script.sub('',html) #去掉SCRIPT
    # html          = re_style.sub('',html)#去掉style
    # html          = re_br.sub('\n',html)#将br转换为换行
    html          = re_h.sub('',htmlstr) #去掉HTML 标签
    # html          = re_comment.sub('',html)#去掉HTML注释
    #去掉多余的空行
    # blank_line = re.compile('\n+')
    # html          = blank_line.sub('\n',html)

    return html

  # 用于快速设置 profile 的代理信息的方法
  def get_firefox_profile_with_proxy_set(self, profile, proxy_host):
    # proxy_host
    proxy_list = proxy_host.split(':')
    agent_ip = proxy_list[0]
    agent_port = proxy_list[1]

    profile.set_preference('network.proxy.type', 1)  # 使用代理
    profile.set_preference('network.proxy.share_proxy_settings', True)  # 所有协议公用一种代理配置
    profile.set_preference('network.proxy.http', agent_ip)
    profile.set_preference('network.proxy.http_port', int(agent_port))
    profile.set_preference('network.proxy.ssl', agent_ip)
    profile.set_preference('network.proxy.ssl_port', int(agent_port))
    # 对于localhost的不用代理，这里必须要配置，否则无法和 webdriver 通讯
    # profile.set_preference('network.proxy.no_proxies_on', 'localhost,127.0.0.1')
    # profile.set_preference('network.http.use-cache', False)

    return profile


  """
  创建网络驱动器
  """
  def createDriver(self):

    profile = webdriver.FirefoxProfile()

    # # 不下载和加载图片
    # profile.set_preference('permissions.default.image', 2)

    # # 禁用图片 某些需要加上这个
    # profile.set_preference('browser.migration.version', 9001)

    # # 禁用样式表文件
    # profile.set_preference('permissions.default.stylesheet', 2)

    # # 禁用flash
    # profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

    # # 禁止 Javascript 的执行
    # profile.set_preference('javascript.enabled', False)


    # Selenium Settings - 设置代理 & UA
    # proxy 是形如 127.0.0.1:80 的代理字符串
    # user_agent 是形如 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0' 的 UA 字符串

    # proxy = '119.28.152.208:80'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'

    # if proxy:

    #     profile = self.get_firefox_profile_with_proxy_set(profile, proxy)

    if user_agent:

      profile.set_preference("general.useragent.override", user_agent)


    profile.update_preferences()

    driver = webdriver.Firefox(profile, executable_path='lib/geckodriver.exe')

    return driver








  def crawlerInfo(self, url):

    fails = 1

    while fails < 31:

      try:

        self.driver.set_page_load_timeout(10)

        self.driver.get("about:blank")

        self.driver.get(url)

        break

      except Exception as e:

        print(e)

        print('error wait 30 secs tyc_data1')

        time.sleep(30)

    else:

      raise

    try:

      WebDriverWait(self.driver, 60).until(

      EC.presence_of_element_located((By.CLASS_NAME, "footerV2"))

      )

    except Exception as e:

      print(e)

    finally:

      source = self.driver.page_source.encode("utf-8")

      tycsoup = BeautifulSoup(source, 'html.parser')

      html = tycsoup.select(
          "div.huangye_main")

      print(html)
      return
      for tag in html:

        # <class 'bs4.element.Tag'>
        name = tag.string

        result = self.handle.sadd('company_name_list', name)
        # print(name)
        # return
      # db.close2()


  def __init__(self):


    url="http://www.51sole.com/huhehaote-anfang/p1"

    headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"

    ]

    '''''
    @获取403禁止访问的网页
    '''
    randdom_header=random.choice(headers)

    req=urllib2.Request(url)
    req.add_header("User-Agent",randdom_header)
    req.add_header("Host","blog.csdn.net")
    req.add_header("Referer","http://blog.csdn.net/")
    req.add_header("GET",url)

    content=urllib2.urlopen(req).read()

    print(content)

    # conf = self.getConfig()

    # self.company_name_url = conf.get('url')
    # self.host             = conf.get('host')
    # self.username         = conf.get('username')
    # self.password         = conf.get('password')
    # self.dbname           = conf.get('dbname')
    # self.total_page       = conf.get('total_page')

    # self.redis_host       = conf.get('redis_host')
    # self.redis_port       = conf.get('redis_port')

    # # self.db = database.Database

    # # self.conn = self.db.connect(self.host, self.username, self.password, self.dbname)
    # self.handle = redis.Redis(self.redis_host, self.redis_port)


    # try:

    #   # 获得网络驱动器实例对象
    #   self.driver = self.createDriver()

    #   for vo in range(1, self.total_page):

    #     url = self.company_name_url +str(vo)

    #     self.crawlerInfo(url)
    #     time.sleep(20)

    # except Exception as e:
    #   print(e)


  def getConfig(self):

    cf = configparser.ConfigParser()

    cf.read("config.conf")

    #return all section
    secs = cf.sections()

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

    return result

if __name__ == '__main__':

  Crawler()
