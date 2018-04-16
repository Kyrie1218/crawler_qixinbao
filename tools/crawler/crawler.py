
from time import sleep
from ..logger.logger import Logger
from ..proxy.proxy import Proxy as proxy


class Crawler(object):



  def load(self):

    fail = 1

    while fail < 31:

      try:

        # 设定页面加载限制时间
        self.handle.set_page_load_timeout(10)

        # 新窗口打开
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
  等待就绪状态
  """
  def wait_for_ready_state(self):

    try:
      # WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
      # EC.presence_of_element_located 确认元素是否已经出现

      # 60秒内每隔10秒扫描一次页面，如果找到停止继续扫描，否则抛出异常
      WebDriverWait(self.driver, 60, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "footerV2")))

    except Exception as e:

      print(e)

    finally:

      source = self.driver.page_source.encode("utf-8")

      # 创建BeautifulSoup对象
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



def get_data(html_text,sheet):
    global sum
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body=bs.body
    # a = body.find_all('div',{'class':'container-fluid'}) # 获取body部分
    # b = a[0].contents[1]
    # c = b.find('div',{'class':'col-sm-8'})
    # grid = c.contents[1]
    # gridcontext = grid.find('div',{'id':'data-grid-container'})
    # e = gridcontext[0].contents[0]
    # f = e.contents[3]
    #datacanvas = f.find_all('div',{'class':'grid-canvas'})
    datacanvas=body.find('div',{'class':'grid-canvas'})
    for data in datacanvas.children:    #data=每个酒店
        sheet.write(sum, 0, data.contents[0].contents[0].string)    #写第一个属性link
        print data.contents[1].string
        for i in range(1,len(data.contents)):    #simple单个酒店下各属性
            sheet.write(sum,i,data.contents[i-1].string)
sum=sum+1




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
































