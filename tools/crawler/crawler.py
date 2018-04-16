
from time import sleep
from ..logger.logger import Logger
from ..proxy.proxy import Proxy as proxy


class Crawler(object):



  def get_html_info(self):

    fail = 1

    while fail < 31:

      try:

        self.handle.set_page_load_timeout(10)

        self.handle.get("about:blank")

        self.handle.get(url)

        break

      except Exception as e:

        Logger.error(e)

        fail += 1

        # 30秒请求一次链接，用于打开页面
        time.sleep(30)

      finally:
        Logger.warning('第 '.fail.' 次请求页面')

    else:

      Logger.error('页面打开失败，请查找原因！！！')




  """
  获取 html 页面数据
  """
  def get_html_info(self):

    try:

      # WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
      WebDriverWait(self.driver, 60, 30).until(

      EC.presence_of_element_located((By.CLASS_NAME, "footerV2")))

    except Exception as e:

      print(e)

    finally:

      source = self.driver.page_source.encode("utf-8")

      tycsoup = BeautifulSoup(source, 'html.parser')







  """
  获取公司信息
  """
  def get_company_info(self, data):

    html = data.select("div.huangye_main")

    print(html)
    return
    for tag in html:

      # <class 'bs4.element.Tag'>
      name = tag.string

      result = self.handle.sadd('company_name_list', name)
      # print(name)
      # return
    # db.close2()







  """
  类初始化
  """
  def __init__(self, host = '127.0.0.1', port = 6379, level = 'info'):

    Logger.init(level)

    # 初始化 Driver 对象
    driver = Driver(host, prot, level)

    self.handle = driver.get_driver()

    print(handle)



# if __name__ == '__main__':
































