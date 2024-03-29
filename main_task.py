import time
import finding_jobs
import chat_poe_edition2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


#%%先实现将工作description打印出写入poe机器人
                    #1.登录程序
                    #2.筛选想要的工作
                    #3.按推荐寻找与按分类寻找，写两个不同函数: 都写在finding_jobs里
                    #其实并不麻烦，只要不使用select_dropdown_option就可行，稍微修改get_job_description_by_index即可




def send_response_to_chat_box(driver,response):
    # 定位聊天输入框
    chat_box = driver.find_element(By.XPATH, "//*[@id='chat-input']")

    # 清除输入框中可能存在的任何文本
    chat_box.clear()
    print(response)
    # 将响应粘贴到输入框
    chat_box.send_keys(response,Keys.NULL
                       )
    time.sleep(5)
    chat_box.send_keys("\n")
    # 模拟按下回车键来发送消息
    time.sleep(1)

def go_forward_send_response_and_go_back(driver,index, response):
    # 调用函数发送响应

    #这步好像在inding_jobs.get_job_description_by_index_2里点击过了
    # element = driver.find_element(By.XPATH,f"//*[@id='wrap']/div[2]/div[2]/div/div/div[1]/ul/li[{index}]/div[1]")
    # element.click()
    # time.sleep(2)

    element = driver.find_element(By.XPATH,f"//*[@id='wrap']/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/a[2]")
    element.click()
    time.sleep(5)

    send_response_to_chat_box(driver,response)

    time.sleep(10)
    # 返回到上一个页面
    driver.back()
    for i in range(int(index/10)+1):                    #下拉页面,否则work 数量会有限制
        job_selector = f"//*[@id='wrap']/div[2]/div[2]/div/div/div[1]/ul/li[{15*i}]"
        job_element = driver.find_element(By.XPATH, job_selector)
        job_element.click()
    time.sleep(3)

def choose_intern(driver):
    #选择实习

    #鼠标悬停
    collect = driver.find_element(By.XPATH,"//*[@id='wrap']/div[2]/div[1]/div/div[2]/div[1]/div[1]/span")
    ActionChains(driver).move_to_element(collect).perform()
    time.sleep(1)
    element = driver.find_element(By.XPATH,"//*[@id='wrap']/div[2]/div[1]/div/div[2]/div[1]/div[2]/ul/li[4]")
    element.click()

def write_and_send(url,browser_type):
    #登录Boss
    finding_jobs.open_browser_with_options(url,browser_type)
    # finding_jobs.log_in()               #自动化二维码
    chat_poe_edition2.open_chrome_hand()

    driver = finding_jobs.get_driver()
    # choose_intern(driver)               #要保证只有一个boss界面，否则会报错

    job_index = 10
    index_need = 5 #需要回答的索引，第五条回答开始才是我需要的
    while True:
        try:
            # 开始前给20s自己操作的时间
            time.sleep(20)
            job_description = finding_jobs.get_job_description_by_index_2(driver,job_index)
            if ("ython" in job_description)or("数据分析" in job_description):         #完成工作筛选！,规避python大小写区别
            # if ("大便" in job_description):
                chat_poe_edition2.chat_to_poe(job_description)
                print(f"index.{job_index} is  my job!!!")
                chat_poe_edition2.determine_answer_com(index_need)                  #等待回答生成
                response  = chat_poe_edition2.get_valid_response(index_need)
                # print(response)                                                   #检查response
                go_forward_send_response_and_go_back(driver,job_index,response)     #发送！

                index_need += 2  # 每次循环要回答两条
            else:
                print(f"index.{job_index} is not my job")
            job_index+=1

        except Exception as e:
            print(f"An error occurred:{e}")
            break


if __name__ == '__main__':
    url = "https://www.zhipin.com/web/geek/job-recommend?ka=header-job-recommend"
    browser_type = "chrome"
    write_and_send(url,browser_type)
