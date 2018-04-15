#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import redis
import logging
import requests
from crawler_selenium import Crawler
from CONFIG import PROXY_POOL_IP



class Proxy(object):

  """
  根据用户代理列表，随机获取 User Agent
  """
  @staticmethod
  def check_jd(proxy, header):

    logging.info('Validating name proxy: %s', proxy)

    cr = Crawler(proxy)

    item_name = cr.get_jd_item('5089253')  # Iphone X

    if item_name:

      return True

    return False


  """
  根据用户代理列表，随机获取 User Agent
  """
  def get_proxy(self):

    r = redis.Redis(host=PROXY_POOL_IP, port=6379, db=0)

    while True:

      good_proxies = r.srandmember("good_proxies", 1)

      if good_proxies:

        good_proxies = good_proxies[0].decode("utf-8")  # byte to str
        good_proxies = {"http": good_proxies, "https": good_proxies}
        header = self.get_user_agent()

        if not self.check_jd(good_proxies, header):
                logging.warning('Validate proxy failure, retrying')
                continue
        logging.info('Validate SUCCESS，using proxy: %s', good_proxies)
        return header, good_proxies

      else:
        logging.critical('No proxy now from remote server, retrying')
        time.sleep(5)



  """
  根据用户代理列表，随机获取 User Agent
  """
  def get_proxy_zhima(self):

    url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0' \
          '&city=0&yys=0&port=11&pack=8241&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='

    while True:

      header = self.get_user_agent()

      request = requests.get(url, headers=header, timeout=5)

      logging.warning('Zhima Proxy: %s', request.json())

      if not request.json()['data']:

        logging.warning('No Zhima Proxy anymore or too fast. Retrying')

        time.sleep(5)

        continue

      try:

        proxy_ip = request.json()['data'][0]['ip']

        proxy_port = request.json()['data'][0]['port']

        good_proxies = proxy_ip + ':' + str(proxy_port)

        good_proxies = {"http": good_proxies, "https": good_proxies}

        logging.info('Zhima get proxy, using proxy: %s', good_proxies)

        return header, good_proxies

      except:

        logging.warning('No Zhima Proxy now. Retrying')

        time.sleep(5)

        continue

  """
  根据用户代理列表，随机获取 User Agent
  """
  @staticmethod
  def get_user_agent():

    user_agent = random.choice(USER_AGENT_LIST)

    user_agent = {'user-agent': user_agent}  # dict

    logging.debug('Generating header: %s', user_agent)

    return user_agent


if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG)

  proxy = Proxy()

  proxy.get_user_agent()

  # p.get_proxy()
  proxy.get_proxy_zhima()