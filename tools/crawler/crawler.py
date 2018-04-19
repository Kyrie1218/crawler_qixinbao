import os
import time
import redis
import datetime
import threading
import configparser
from time import sleep
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ..logger.logger import Logger
from .driver import Driver
from ..proxy.proxy import Proxy as proxy


class Crawler(object):


  """
  登录
  """
  def login(self, handle):

    # 所以这里需要选中一下frame，否则找不到下面需要的网页元素
    handle.switch_to.frame("login_frame")

    # 自动点击账号登陆方式
    handle.find_element_by_id("switcher_plogin").click()

    # 账号输入框输入已知qq账号
    handle.find_element_by_id("u").send_keys(self.user)

    # 密码框输入已知密码
    handle.find_element_by_id("p").send_keys(self.pw)

    # 自动点击登陆按钮
    handle.find_element_by_id("login_button").click()

    time.sleep(1)
    driver.refresh()





  """
  加载页面
  """
  def _load_page(self, url):

    fail = 1
    state = False

    while fail < self.request_total:

      try:

        # 设定页面加载限制时间
        # self.handle.set_page_load_timeout(self.load_time)

        # 新窗口打开
        self.handle.get("about:blank")

        self.handle.get(url)

        state = self._ready_state()

        # 结束循环
        break

      except Exception as e:
        info = '第 %s 次请求页面, %s' % (fail, e)
        Logger.warning(info)

        fail += 1

        # 30秒请求一次链接，用于打开页面
        time.sleep(self.interval_time)

    else:

      Logger.error('页面打开失败，请查找原因！！！')

    return state




  """
  获取是否加载就绪
  """
  def _ready_state(self):

    # 就绪状态初始为 False
    state = False

    try:
      # WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
      # EC.presence_of_element_located 确认元素是否已经出现

      # 60秒内每隔10秒扫描一次页面，如果找到停止继续扫描，否则抛出异常
      WebDriverWait(self.handle, self.page_life_cycle, self.page_interval_time).until(EC.presence_of_element_located((By.CLASS_NAME, self.label)))

      state = True

    except Exception as e:

      Logger.error('页面没有加载完成，请查找是否存在标签')

    return state


  # find_element_by_id() 通过元素的id属性来查找元素
  # find_element_by_name() 通过元素的name属性来查找元素
  # find_element_by_class_name() 通过元素的class属性来查找元素
  # find_element_by_tag_name() 通过标签来查找元素 input select
  # find_element_by_link_text() 通过文本链接查找元素
  # find_element_by_partial_link_text() 通过元素标签对之间的部分文本就能点位元素
  # find_element_by_xpath("//标签[@属性名=属性值]") 绝对路径定位
  # driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div/div[2]/input").send_keys("username")
  # div[3] 代表同层第三个元素

  # find_element_by_css_selector 通过css定位

  """
  获取html页面信息
  """
  def get_html_info(self):

    source = self.handle.page_source.encode("utf-8")

    # 创建BeautifulSoup对象
    soup = BeautifulSoup(source, 'html.parser')

    return soup




  """
  获取公司信息
  """
  def get_company_info(self, soup):

    try:

      body = soup.body

      company_list = body.find('div',{'class':'hy_companylist'}) # 获取body部分

      data = company_list.find('ul') # 获取body部分

      lists = data.find_all('li')

      for k, vo in enumerate(lists):

        name = vo.contents[0].contents[0].string

        if '公司' in name:

          # 公司名称
          self.redis_handel.sadd('company_name_list', name)

    except Exception as e:
      Logger.error(e)

    finally:
      self.driver.Quit()


  def _set_only_number(self):

    now = datetime.datetime.now()

    result = now.strftime('%Y%m%d%H%M%S%f')

    return result




  def run(self):

    #
    url = self.redis_handel.rpop('web_url_list')

    # 加载页面是否完成并且查找指定元素是否存在
    load_state = self._load_page(url.decode())

    # 存在的话继续执行
    if load_state:

      # 获取页面数据
      html = self.get_html_info()
      data = self.get_company_info(html)
      print(data)


    else:
      logger.error('因为页面加载失败或无法找到指定元素，程序结束')




  def init(self):

    # 获取根目录下配置文件
    path = os.getcwd()+'\\'+'config.conf'

    cf = configparser.ConfigParser()

    cf.read(path)

    result = {}

    # or
    result['total_page'] = cf.getint("or", "total_page")
    result['url']        = cf.get("or", "url")

    # redis
    result['redis_host']     = cf.get("redis", "host")
    result['redis_port']     = cf.getint("redis", "port")

    # crawler
    result['request_total']      = cf.getint("crawler", "request_total")
    result['load_time']          = cf.getint("crawler", "load_time")
    result['interval_time']      = cf.getint("crawler", "interval_time")
    result['page_life_cycle']    = cf.getint("crawler", "page_life_cycle")
    result['page_interval_time'] = cf.getint("crawler", "page_interval_time")
    result['label']              = cf.get("crawler", "label")

    # log
    result['level']     = cf.get("log", "level")

    return result




  """
  类初始化
  """
  def __init__(self):

    threading.Thread.__init__(self)

    info = self.init()

    Logger.init(info['level'])

    self.request_total      = info['request_total']
    self.load_time          = info['load_time']
    self.interval_time      = info['interval_time']
    self.page_life_cycle    = info['page_life_cycle']
    self.page_interval_time = info['page_interval_time']
    self.label              = info['label']

    self.redis_host = info['redis_host']
    self.redis_port = info['redis_port']

    self.redis_handel = redis.Redis(self.redis_host, self.redis_port)

    # # 初始化 Driver 对象
    self.driver = Driver(self.redis_handel, info['level'])

    self.handle = self.driver.get_driver()


# if __name__ == '__main__':
