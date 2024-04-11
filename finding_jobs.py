#Boss直聘对话脚本
import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# 全局 WebDriver 实例
driver = None

def get_driver():
    global driver
    driver.implicitly_wait(10)
    return driver


def open_browser_with_options(url, browser):
    global driver
    options = Options()
    os.chdir(r"C:\Program Files\Google\Chrome\Application")

    subprocess.Popen('chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\selenium\AutomationProfile2"')

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    driver = webdriver.Chrome(service=Service(r"E:\Users\zz\PycharmProjects\py selenu\chromedriver.exe"), options=options)

    # if browser == "chrome":
    #  driver = webdriver.Chrome(service=Service(r"E:\Users\zz\gh\auto_job__find__chatgpt__rpa\auto_job_find\chromedriver.exe"),options=options)
    # driver.maximize_window()


    #网页
    # driver.get(url)

    # 等待直到页面包含特定的 XPath 元素
    # xpath_locator = "//*[@id='header']/div[1]/div[3]/div/a"
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, xpath_locator))
    # )

def log_in():
    global driver

    # 点击按钮
    login_button = driver.find_element(By.XPATH, "//*[@id='header']/div[1]/div[3]/div/a")
    login_button.click()

    # 等待boss直聘登录按钮出现
    xpath_locator_wechat_login = "//*[@id='wrap']/div/div[2]/div[2]/div[1]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_locator_wechat_login))
    )

    wechat_button = driver.find_element(By.XPATH, "//*[@id='wrap']/div/div[2]/div[2]/div[1]")
    wechat_button.click()


    # xpath_locator_wechat_logo = "//*[@id='wrap']/div/div[2]/div[2]/div[1]/div[2]/div[1]/img"
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, xpath_locator_wechat_logo))
    # )

    xpath_locator_login_success = "// *[ @ id = 'header'] / div[1] / div[3] / ul / li[2] / a / img"
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpath_locator_login_success))
    )


def get_job_description():

    global driver

    # 使用给定的 XPath 定位职位描述元素
    xpath_locator_job_description = "//*[@id='wrap']/div[2]/div[2]/div/div/div[2]/div/div[2]/p"

    # 确保元素已加载并且可以获取文本
    job_description_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_locator_job_description))
    )

    # 获取职位描述文本
    job_description = job_description_element.text
    print(job_description)  # 打印出职位描述，或者你可以在这里做其他处理


    return job_description

def select_dropdown_option(driver, label):
    # 尝试在具有特定类的元素中找到文本
    trigger_elements = driver.find_elements(By.XPATH, "//*[@class='recommend-job-btn has-tooltip']")

    # 标记是否找到元素
    found = False

    for element in trigger_elements:
        if label in element.text:
            # 确保元素可见并且可点击
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable(element))
            element.click()  # 点击找到的元素
            found = True
            break

    # 如果在按钮中找到了文本，就不再继续下面的操作
    if found:
        return

    # 如果在按钮中没有找到文本，执行原来的下拉列表操作
    trigger_selector = "//*[@id='wrap']/div[2]/div[1]/div/div[1]/div"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, trigger_selector))
    ).click()  # 打开下拉菜单

    dropdown_selector = "ul.dropdown-expect-list"
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, dropdown_selector))
    )

    option_selector = f"//li[contains(text(), '{label}')]"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, option_selector))
    ).click()  # 选择下拉菜单中的选项


def get_job_description_by_index(index):
    try:

        job_selector = f"//*[@id='wrap']/div[2]/div[2]/div/div/div[1]/ul/li[{index}/div[1]"
        job_element = driver.find_element(By.XPATH, job_selector)
        job_element.click()
        description_selector = "//*[@id='wrap']/div[2]/div[2]/div/div/div[2]/div/div[2]/p"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, description_selector))
        )
        job_description_element = driver.find_element(By.XPATH, description_selector)
        return job_description_element.text

    except NoSuchElementException:
        print(f"No job found at index {index}.")
        return None



##按照推荐找工作，而非分类
def get_job_description_by_index_2(driver,index):
    try:
        job_selector = f"//*[@id='wrap']/div[2]/div[2]/div/div/div[1]/ul/li[{index}]/div[1]"
        job_element = driver.find_element(By.XPATH, job_selector)
        job_element.click()

        description_selector = "//*[@id='wrap']/div[2]/div[2]/div/div/div[2]/div/div[2]/p"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, description_selector))
        )
        job_description_element = driver.find_element(By.XPATH, description_selector)

        print(job_description_element.text)

        return job_description_element.text



    except NoSuchElementException:
        print(f"No job found at index {index}.")
        return None

# Variables
url = "https://www.zhipin.com/web/geek/job-recommend?ka=header-job-recommend"
browser_type = "chrome"



