#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import uuid
import random
import database

from selenium.webdriver.common.proxy import *

class Crawler(object):


  def filter_tags(self, htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)

    return s

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
      profile.set_preference('network.proxy.no_proxies_on', 'localhost,127.0.0.1')
      profile.set_preference('network.http.use-cache', False)

      return profile


  """
  创建网络驱动器
  """
  def createDriver(self):
    ua = "Mozilla/5.0"

    profile = webdriver.FirefoxProfile()

    # Selenium Settings - 设置代理 & UA
    # proxy 是形如 127.0.0.1:80 的代理字符串
    # user_agent 是形如 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0' 的 UA 字符串

    proxy = '37.187.116.199:80'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'

    if proxy:

        profile = self.get_firefox_profile_with_proxy_set(profile, proxy)

    if user_agent:

        profile.set_preference("general.useragent.override", user_agent)

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

        company = tycsoup.select(
            "div > div > div > div.app-list-items > div > div.company-item > div.col-2 > div > div.company-title > a")

        data = []

        for link in company:

          print(self.filter_tags(company))
          return

    return data




  def __init__(self):
    self.company_name_url = 'http://www.qixin.com/search?key=内蒙古 公司&page='
    self.host = 'localhost'
    self.username = 'root'
    self.password = 'root'
    self.dbname = 'python'
    try:

      # 获得网络驱动器实例对象
      self.driver = self.createDriver()

      count = 10

      for vo in range(10):

        url = self.company_name_url+str(vo)

        self.crawlerInfo(url)

        print(url)
        return


    #         self.driver



    # db = database.Database

    # conn = db.connect(self.host, self.username, self.password, self.dbname)

    # # result = db.insert(conn, 'company_name_list', 'id, name, update_time', value)
    # # data = db.select(conn, 'company_name_list')


    except Exception as e:
      print(e)





if __name__ == '__main__':

    Crawler()
