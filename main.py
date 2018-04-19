#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tools.crawler.crawler import Crawler
import os

if __name__ == '__main__':

  result = os.system('ping %s' % '121.31.93.157')
  print(result)

#   # 初始化 Crawler 对象
#   c1 = Crawler()
#   # c2 = Crawler()

# # 开启线程
#   c1.run()
#   # c2.start()


