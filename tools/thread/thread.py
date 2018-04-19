#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from time import time
import threading

class Thread(threading.Thread):



  def __init__(self, threadID, name):

    threading.Thread.__init__(self)

    self.threadID = threadID

    self.name = name

    s = range(1, 30)
    print(s)

  #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
  def run(self):

    print(self.name)


# 创建新线程
thread1 = Thread(1, "Thread-1")
thread2 = Thread(2, "Thread-2")

# 开启线程
thread1.start()
thread2.start()

print("Exiting Main Thread")
