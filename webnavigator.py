import error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

title = ''
contents = list()

def is_title_valid(title):
    if title == '':
        return False
    return True

def is_valid_content(content):
    if content == '':
        return False
    return True

def set_title(_title):
    if not is_title_valid(_title):
        return error.Error_Type.TITLE
    else :
        title = _title
        return error.Error_Type.NONE

def set_contents(content1, content2):
    if not is_valid_content(content1) and not is_valid_content(content2):
        return error.Error_Type.CONTENT
    else :
        return error.Error_Type.NONE
####################################################################

class SeleniumBot:
    def __init__(self, driver_path="chromedriver.exe"):
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)

    def open(self, url):
        self.driver.get(url)

    def open_mule(self):
        self.open('https://www.mule.co.kr/')

    def search_google(self, keyword):
        self.driver.get("https://www.google.com")
        box = self.driver.find_element(By.NAME, "q")
        box.send_keys(keyword)
        box.submit()

    def click_by_text(self, tag, text):
        elements = self.driver.find_elements(By.TAG_NAME, tag)
        for e in elements:
            if text in e.text:
                e.click()
                break

    def wait(self, seconds):
        time.sleep(seconds)

    def close(self):
        self.driver.quit()  


####################################################################
def stop_task():
    print('stop')
    return

def run_task():    
    print(title)
    for content in contents:
        print(content)

    bot = SeleniumBot()
    bot.open_mule()
    bot.wait(5)
    bot.close()

    return
