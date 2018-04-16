from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..logger.logger import Logger
from ..proxy.proxy import Proxy

class Driver(object):


  def get_driver(self):

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

      if ip_address:
        profile = self._set_proxy(profile, ip_address)

      # 获得初始化生成的 User Agent 信息 样式：'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
      user_agent = self.proxy.get_user_agent()

      if user_agent:
        profile = self._set_user_agent(profile, user_agent)

      driver = webdriver.Firefox(profile, executable_path='lib/geckodriver.exe')

      # 设置 Cookie 信息
      self._set_cookie(driver)

    except Exception as e:
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

    except Exception as e:

      Logger.error(e)

    finally:

      Logger.info('代理 IP 设置完成')

    return profile



  """
  设置 User Agent 信息
  """
  def _set_user_agent(self, profile, user_agent):

    try:

      profile.set_preference("general.useragent.override", user_agent)

    except Exception as e:

      Logger.error(e)

    finally:

      Logger.info('User Agent 设置完成')

    return profile


  """
  获取网站 Cookie 信息
  """
  def _get_cookie(self, driver):

    try:

      cookie = driver.get_cookies()

      if cookie:

        for vo in cookie:
          Logger.info("%s -> %s" % (cookie['name'], cookie['value']))

    except Exception as e:

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

      if info:
        # 添加cookie信息
        driver.add_cookie(info)

    except Exception as e:

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
  def __init__(self, host = '127.0.0.1', port = 6379, level = 'info'):

    # 初始化日志类
    Logger.init(level)

    # 加载代理类
    self.proxy = Proxy(host, port, level)


# if __name__ == '__main__':

#   driver = Driver()
