#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import redis
import requests
from ..logger.logger import Logger

class Proxy(object):


  """
  获得代理IP
  """
  def get_proxy_zhima(self):

    url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0' \
          '&city=0&yys=0&port=11&pack=8241&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='

    while True:

      header = self.get_user_agent()

      request = requests.get(url, headers=header, timeout=5)

      Logger.warning('Zhima Proxy: %s', request.json())

      if not request.json()['data']:

        Logger.warning('No Zhima Proxy anymore or too fast. Retrying')

        time.sleep(5)

        continue

      try:

        proxy_ip = request.json()['data'][0]['ip']

        proxy_port = request.json()['data'][0]['port']

        good_proxies = proxy_ip + ':' + str(proxy_port)

        good_proxies = {"http": good_proxies, "https": good_proxies}

        Logger.info('Zhima get proxy, using proxy: %s', good_proxies)

        return header, good_proxies

      except:

        Logger.warning('No Zhima Proxy now. Retrying')

        time.sleep(5)

        continue




  """
  获得代理IP
  """
  def get_ip_address(self):

    try:

      ip_address = self.handle.srandmember("ip_address_list", 1)

      data = ip_address[0].decode()

    except Exception as e:

      Logger.error(e)

    return data





  """
  根据用户代理列表，随机获取 User Agent
  """
  def get_user_agent(self):

    try:

      user_agent = self.handle.srandmember("user_agent_list", 1)

      data = user_agent[0].decode()

    except Exception as e:

      Logger.error(e)

    return data





  """
  检查代理是否可以使用
  """
  @staticmethod
  def check(proxy, header):

    Logger.info('Validating name proxy: %s', proxy)

    cr = Crawler(proxy)

    info = cr.get_jd_item('5089253')  # Iphone X

    if info:

      return True

    return False




  """
  类初始化方法
  """
  def __init__(self, host = '127.0.0.1', port = 6379, level = 'info'):

    Logger.init(level)

    self.handle = redis.Redis(host=host, port=port, db=0)



# if __name__ == '__main__':

#   proxy = Proxy()

