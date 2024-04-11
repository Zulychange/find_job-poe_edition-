#chatgpt对话模块
import time
import os
import subprocess
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys


path1=r'E:\Users\zz\PycharmProjects\job_find(poe edition)\introduce.txt'
file1=open(path1,'r', encoding = "utf-8")
ask_response =file1.read()
file1.close()
# print(ask_response)
global poer

def get_poer():
    global poer
    return poer

def open_chrome_hand():
    ##操作已打开浏览器
    global poer
    os.chdir(r"C:\Program Files\Google\Chrome\Application")

    subprocess.Popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="E:\selenium\AutomationProfile"')

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    poer = webdriver.Chrome(service=Service(r"E:\Users\zz\PycharmProjects\py selenu\chromedriver.exe"),options=options)


def chat_to_poe(txt):
    ##与poe交流
    poer = get_poer()
    xpath_searchterm = "//*[@id='__next']/div/div[1]/div/main/div/div/div/footer/div/div/div[1]/textarea"
    # WebDriverWait(poer, 30).until(
    #     EC.element_to_be_clickable((By.XPATH, xpath_searchterm))              #此处加一个等待的话有时会报错
    # )
    element = poer.find_element(By.XPATH, xpath_searchterm)
    element.send_keys(f'''您好\n''')


    element.send_keys(f'请结合我的个人信息与招聘信息写一段我的自荐信,最后不需要写我的名字和任何落款,不超过200字。1.招聘信息:{txt}2.{ask_response}',Keys.NULL                   #取消文本中空格的作用
                      )
    time.sleep(5)        ##等待poe输入完，再对上述问题进行提问
    element.send_keys("\n")


def determine_answer_com(index_need):
        ##判断回答是否完成
    poer = get_poer()
    try:
        xpath_determine = f"//*[@id='__next']/div/div[1]/div/main/div/div/div/div[2]/div[{index_need}]/section[2]/button"
        WebDriverWait(poer, 60).until(
        EC.presence_of_element_located((By.XPATH, xpath_determine))
        )
    except NoSuchElementException:
        print(f"No job found at index {index_need}.")
        return None



def get_valid_response(index_need):
    ##获取有效回答
    poer = get_poer()
    xpath_response = f"//*[@id='__next']/div/div[1]/div/main/div/div/div/div[2]/div[{index_need}]/div[2]/div[2]/div[2]/div/div[1]/div/div"
    element = poer.find_element(By.XPATH,xpath_response)
    response = element.text
    return response

