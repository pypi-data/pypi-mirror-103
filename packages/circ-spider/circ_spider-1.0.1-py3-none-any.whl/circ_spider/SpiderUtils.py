from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from .captcha_utils import captcha_reader
import json
import os
import uuid


class CircSpider:
    def __init__(self, executable_path, practicecode=None, name=None, cardno=None):
        """
        :param executable_path: 驱动路径
        :param practicecode: 执业证编号
        :param name: 从业人员姓名
        :param cardno: 身份证号
        """
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        self.__error_count = 3
        self.__driver = webdriver.Firefox(executable_path=executable_path, options=firefox_options)
        self.__wait = WebDriverWait(self.__driver, 10)
        self.__url = 'http://iir.circ.gov.cn/ipq/insuranceEmp.html'
        self.__original_window = None
        self.__practicecode = practicecode
        self.__name = name
        self.__cardno = cardno
        self.__cache_path = '.cache/img'
        self.__create_cache_folder()

    def __create_cache_folder(self):
        folder = os.path.exists(self.__cache_path)
        if not folder:
            os.makedirs(self.__cache_path)

    def login(self):
        self.__driver.get(self.__url)
        self.__driver.implicitly_wait(20)
        # 存储原始窗口的 ID
        self.__original_window = self.__driver.current_window_handle
        if self.__practicecode is not None:
            self.__driver.find_element_by_id('practicecode').send_keys(self.__practicecode)
        if self.__name is not None:
            self.__driver.find_element_by_id('name').send_keys(self.__name)
        if self.__cardno is not None:
            self.__driver.find_element_by_id('cardno').send_keys(self.__cardno)
        # 识别验证码
        while self.__error_count > 0:
            try:
                self.__handle_captcha()
                alert_window = self.__driver.switch_to.alert
                if alert_window is not None and alert_window.text == '验证码错误':
                    self.__error_count = self.__error_count - 1
                    # print('------验证码错误------')
                    alert_window.accept()
                elif alert_window is not None and alert_window.text == '请输入验证码':
                    self.__error_count = self.__error_count - 1
                    # print('------请输入验证码------')
                    alert_window.accept()
            except NoAlertPresentException:
                break
        self.__driver.implicitly_wait(20)
        self.__wait.until(EC.number_of_windows_to_be(2))

    def get_result(self):
        # 循环执行，直到找到一个新的窗口句柄
        for window_handle in self.__driver.window_handles:
            if window_handle != self.__original_window:
                self.__driver.switch_to.window(window_handle)
                break
        # 等待新标签页完成加载内容
        self.__wait.until(EC.title_is("保险中介从业人员查询详情"))
        # self.__wait.until(EC.visibility_of_element_located((By.ID, 'name')))
        time.sleep(2)
        name = self.__driver.find_element_by_id('name').text
        # 性别
        gender = self.__driver.find_element_by_id('gender').text
        # 身份证后四位
        cardno = self.__driver.find_element_by_id('cardno').text
        # 资格证书号码
        ualificano = self.__driver.find_element_by_id('ualificano').text
        # 资格证书类型
        validStatus = self.__driver.find_element_by_id('validStatus').text
        # 执业证编号
        practicecode = self.__driver.find_element_by_id('practicecode').text
        # 执业证状态
        is_status = self.__driver.find_element_by_id('is_status').text
        # 业务范围
        businesscope = self.__driver.find_element_by_id('businesscope').text
        # 执业区域
        practicearea = self.__driver.find_element_by_id('practicearea').text
        # 所属公司
        insurnnce_code = self.__driver.find_element_by_id('insurnnce_code').text
        result = {}
        result['name'] = name
        result['gender'] = gender
        result['cardno'] = cardno
        result['ualificano'] = ualificano
        result['validStatus'] = validStatus
        result['practicecode'] = practicecode
        result['is_status'] = is_status
        result['businesscope'] = businesscope
        result['practicearea'] = practicearea
        result['insurnnce_code'] = insurnnce_code
        return json.dumps(result, ensure_ascii=False)
        





    def __handle_captcha(self):
        """
        处理验证码
        :return:
        """
        # 截图
        screenshot_path = '{base_path}/screenshot_{uuid}.png'.format(base_path=self.__cache_path, uuid=str(uuid.uuid1()))
        captcha_path = '{base_path}/code_{uuid}.png'.format(base_path=self.__cache_path, uuid=str(uuid.uuid1()))
        # print('screenshot_path = ', screenshot_path)
        # print('captcha_path = ', captcha_path)
        self.__driver.get_screenshot_as_file(screenshot_path)
        # 获取验证码的位置
        captcha_element = self.__driver.find_element_by_id('captcha')
        left = int(captcha_element.location['x'])
        top = int(captcha_element.location['y'])
        right = int(captcha_element.location['x'] + captcha_element.size['width'])
        bottom = int(captcha_element.location['y'] + captcha_element.size['height'])
        # 通过Image截取验证码
        im = Image.open(screenshot_path)
        im = im.crop((left, top, right, bottom))
        im.save(captcha_path)
        # 识别验证码
        code = captcha_reader(captcha_path=captcha_path)
        code = code.replace(' ', '')
        os.remove(screenshot_path)
        os.remove(captcha_path)
        # 输入验证码
        self.__driver.find_element_by_id('yzm').send_keys(code)
        self.__driver.find_element_by_id('chaxun').click()


if __name__ == '__main__':
    spider = CircSpider(executable_path='../../geckodriver', name='杨忠洋')
    spider.login()
    result = spider.get_result()
    print(result)