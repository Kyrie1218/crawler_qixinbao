from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from ..netlib.requests import my_session
from ..toollib.logger import Logger
from ..toollib.answer import _get_answers

from ..proxy.proxy import Proxy as proxy
import logging

class Crawler(object):


  def _get_driver(self):
    try:

      profile = webdriver.FirefoxProfile()

      # 禁止不安全提示
      profile.set_preference("security.insecure_field_warning.contextual.enabled", False)

      # 禁止下载和加载图片
      profile.set_preference('permissions.default.image', 2)
      # 禁用图片 某些需要加上这个
      profile.set_preference('browser.migration.version', 9001)

      # 禁止自动更新
      profile.set_preference("app.update.enabled", False)

      # 禁用样式表文件
      profile.set_preference('permissions.default.stylesheet', 2)

      # 禁用flash
      profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

      # 禁止 Javascript 的执行
      profile.set_preference('javascript.enabled', False)

      # 强制刷新缓存
      profile.set_preference("browser.cache.check_doc_frequency", 1)
      profile.set_preference("browser.cache.disk.enable", False)
      profile.set_preference("browser.cache.memory.enable", False)
      profile.set_preference("browser.cache.offline.enable", False)
      profile.set_preference("network.http.use-cache", False)
      profile.set_preference("browser.cache.disk_cache_ssl", False)

      # 获得初始化生成的IP随机地址 样式：'119.28.152.208:80'
      ip_address = self.proxy.get_ip_address()

      if proxy:
        profile = self._set_proxy(profile, ip_address)

      # 获得初始化生成的 User Agent 信息 样式：'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
      user_agent = self.proxy._set_user_agent()

      if user_agent:
        profile = self._set_user_agent(profile, user_agent)

      driver = webdriver.Firefox(profile, executable_path='lib/geckodriver.exe')

      # 设置 Cookie 信息
      self._set_cookie(driver)

    except WebDriverException as e:
      Logger.error(e)

    return driver




  """
  设置IP代理
  """
  def _set_proxy(self, profile, proxy_host):

    try:

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

    except WebDriverException as e:

      Logger.error(e)

    return profile



  """
  设置 User Agent 信息
  """
  def _set_user_agent(self, profile, user_agent):

    try:

      profile.set_preference("general.useragent.override", user_agent)

    except WebDriverException as e:

      Logger.error(e)

    return profile


  """
  获取网站 Cookie 信息
  """
  def _get_cookie(self, driver):

    try:

      cookie = driver.get_cookies()

      for vo in cookie:
        Logger.info("%s -> %s" % (cookie['name'], cookie['value']))

    except WebDriverException as e:

      Logger.error(e)

    return cookie



  """
  设置网站 Cookie 信息
  """
  def _set_cookie(self, driver):

    try:

      info = self._get_cookie(driver)

      # out1={ u'domain':u'www.factual.com',u'expiry':2147385600, u'httpOnly':True ,
      # u'secure': False ,u'name':u'_www_session',u'value':u'ekRNZHU2YkxUK3JiNTlJcEhWWGs5'}
      # 删除一个特定的cookie
      # driver.delete_cookie("CookieName")

      # 删除所有cookie
      driver.delete_all_cookies()

      # 添加cookie信息
      driver.add_cookie(info)

    except WebDriverException as e:

      Logger.error(e)

    finally:
      Logger.info('Cookie 设置完成')




  """
  类初始化
  """
  def _start_load_plugin():

    if firebug == 1:
      profile.add_extension(capture_path + '/firebug-2.0.8.xpi')
      profile.set_preference("extensions.firebug.currentVersion", "2.0.8")
      profile.set_preference("extensions.firebug.allPagesActivation", "on")
      profile.set_preference("extensions.firebug.defaultPanelName", "net")
      profile.set_preference("extensions.firebug.net.enableSites", True)
      profile.set_preference("extensions.firebug.delayLoad", False)
      profile.set_preference("extensions.firebug.onByDefault", True)
      profile.set_preference("extensions.firebug.showFirstRunPage", False)
      profile.set_preference("extensions.firebug.net.defaultPersist", True)
    if netexport == 1:
      profile.add_extension(capture_path + '/netExport-0.9b7.xpi')
      profile.set_preference("extensions.firebug.DBG_NETEXPORT", True)
      profile.set_preference("extensions.firebug.netexport.alwaysEnableAutoExport", True)
      profile.set_preference("extensions.firebug.netexport.defaultLogDir", capture_path + "/har/"+url)
      profile.set_preference("extensions.firebug.netexport.includeResponseBodies", True)




  """
  类初始化
  """
  def __init__(self, incognito=False, user_agent=None, profile_path=None):

    self.proxy = proxy.Proxy()

        self.driver = None
        self.name = None
        self.incognito = incognito
        self.agent = user_agent
self.profile_path = profile_path



if __name__ == '__main__':

  Logger.init('debug')






# http://www.51sole.com/huhehaote/
  """
  创建网络驱动器
  """
  def createDriver(self):

    # 无头参数
    options = Options()
    options.add_argument('-headless')















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
      # WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
      WebDriverWait(self.driver, 60, 30).until(

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


























def _get_driver():
    driver = webdriver.PhantomJS(desired_capabilities=_set_driver_ua())
    Logger.info('Initialize PhantomJS Webdriver')
    _set_cookies(driver, my_session().cookies)
    Logger.info('Initialize Webdriver Cookies')
    _set_driver_window_size(driver)
    Logger.info('Initialize Webdriver Finished')
    return driver


def _set_driver_ua():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (_get_user_agent())
    return dcap


def _set_cookies(driver, cookies):
    for c in cookies:
        driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires, 'domain': c.domain})


def _set_driver_window_size(driver):
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)


def _open_question_description(driver):
    els = driver.find_elements_by_xpath(
        '//button[@type="button"][@class="Button QuestionRichText-more Button--plain"]')
    # if element not exist, find_elements is fast than find_element
    if len(els) > 0:
        Logger.info('{} Question Description Read More Button Found'.format(driver.current_url))
        els[0].click()
        Logger.info('Click Load More, Wait...')


def _open_load_more(driver, recur_depth=0, max_depth=3):
    recur_depth = recur_depth
    if recur_depth > max_depth:
        return
    els = driver.find_elements_by_class_name('zu-button-more')
    if len(els) > 0:
        Logger.info('URL {} Found Load More Button'.format(driver.current_url))
        els[0].click()
        Logger.info('Click Load More, Wait...')
        sleep(1)
        return _open_load_more(driver, recur_depth + 1)


def _get_question_h4_answer_count(driver):
    try:
        return int(driver.find_element_by_class_name('List-headerText').text.split(' ')[0])
    except Exception as e:
        Logger.warning('Get Answer Count Error {}'.format(str(e)))
        return 0


def _open_question_load_more(driver, recur_depth=1, max_depth=10):
    answer_count = len(_get_answers(_to_bs(driver.page_source)))
    recur_depth = recur_depth
    if recur_depth > max_depth:
        return
    try:
        title_count = _get_question_h4_answer_count(driver)
        if title_count > 20 and answer_count < title_count:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//button[@class="Button QuestionMainAction"]')))
    except TimeoutException:
        Logger.error('Question {} Load More Timeout'.format(driver.current_url))
    els = driver.find_elements_by_xpath('//button[@class="Button QuestionMainAction"]')
    if len(els) > 0:
        Logger.info('Question {} Found Load More Button'.format(driver.current_url))
        els[0].click()
        Logger.info('Click Load More, Wait...')
        sleep(1)
        return _open_question_load_more(driver, recur_depth + 1)
    answer_count = len(_get_answers(_to_bs(driver.page_source)))
    Logger.info('Summary: Question {} Answer Count {}'.format(driver.current_url, answer_count))
