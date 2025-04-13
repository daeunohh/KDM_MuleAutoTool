import error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from options import Options 
import threading
import time
from selenium.common.exceptions import UnexpectedAlertPresentException

my_bbs = 'https://www.mule.co.kr/mymule/mybbs'

def is_id_valid(id):
    if id == '':
        return False
    return True

def set_id(_id):
    if not is_id_valid(_id):
        return error.Error_Type.ID
    else :
        Options.id = _id
        return error.Error_Type.NONE

def is_valid_pw(pw):
    if pw == '':
        return False
    return True

def set_pw(_pw):
    if not is_valid_pw(_pw) :
        return error.Error_Type.PW
    else :
        Options.pw = _pw
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

class StealthBot:
    def __init__(self, headless=False):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        # 사람처럼 보이기 위한 옵션들
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        )

        # options.add_argument("--user-data-dir=C:/Users/사용자이름/AppData/Local/Google/Chrome/User Data")
        # options.add_argument("--profile-directory=Default")  # 또는 "Profile 1", "Profile 2" 등


        self.driver = uc.Chrome(options=options)

    def do_task(self):
        self.human_wait(3, 4)

        self.go(my_bbs)
        self.click_by_index(By.CLASS_NAME, "more-btn", 0)
        self.human_wait(10,20)

        rows = self.driver.find_elements(By.CSS_SELECTOR, "table.small-table tbody tr")
        target_rows = []
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if not tds:
                continue  # 첫 번째 row (헤더)는 제외됨

            board_name = tds[0].text.strip()
            if board_name == "합주실/연습실":
                target_rows.append(row)
        if len(target_rows) <= 2:
            for row in target_rows:
                title = row.find_element(By.TAG_NAME, "a").text
                link = row.find_element(By.TAG_NAME, "a").get_attribute("href")
                print("📌 제목:", title)
                print("🔗 링크:", link)

        # Set post options first
        # self.set_options()
        # Insert title
        self.find_and_type(By.ID, "input-title", Options.title)
        # Insert contents
        self.write_to_editor(Options.contents[0])

        self.check_checkbox(By.CSS_SELECTOR, "div.checker.pointer")
        self.click(By.ID, "bt-save")
        self.human_wait(1)
        return
    
    def login(self):
        self.click(By.ID, "bt-write")
        self.find_and_type(By.ID, "login-user-id", Options.id)
        self.find_and_type(By.ID, "login-user-pw", Options.pw)
        self.click(By.CSS_SELECTOR, "a.login-bt.login")
        self.human_wait(2,3)
        try:
            print("✅ 로그인 성공")
            return error.Error_Type.NONE
        except UnexpectedAlertPresentException:
            print("❌ 로그인 실패 (간접적으로 감지)")  # 예: 로그인 후에만 나오는 메뉴
            return error.Error_Type.LOGINFAIL

    def set_options(self):
        self.find_and_select(By.ID, "input-category", Options.category)
        self.check_checkbox(By.ID, Options.room_option)
        self.click(By.XPATH, "//input[@placeholder='등록시 지도에 표시됩니다.']")
        self.find_and_type(By.ID, "search-map-text", Options.address)
        self.find_and_type_by_xpath("//input[@placeholder='http://를 포함한 전체 경로를 입력하세요.']"
                                , Options.homepage)
        self.find_and_type(By.ID, "input-sell-tel", Options.phone_number)
        self.upload_file(By.ID, "input-main-img", Options.main_photo)

    def go(self, url):
        self.driver.get(url)
        self.human_wait(2, 3)

    def find_and_type(self, by, identifier, text):
        elem = self.driver.find_element(by, identifier)
        for char in text:
            elem.send_keys(char)
            time.sleep(0.1)  # 천천히 타이핑
        self.human_wait(1, 2)

    def find_and_type_by_xpath(self, xpath, text):
        elem = self.driver.find_element(By.XPATH, xpath)
        elem.clear()
        for char in text:
            elem.send_keys(char)
            time.sleep(0.05)
        self.human_wait(0.5, 1)

    def click(self, by, identifier):
        elem = self.driver.find_element(by, identifier)
        elem.click()
        self.human_wait(1, 2)

    def click_by_index(self, by, identifier, index):
        elements = self.driver.find_elements(by, identifier)
        if index < len(elements):
            elements[index].click()
            self.human_wait(0.5, 1)
        else:
            print(f"❌ 해당 인덱스 {index}의 버튼이 없습니다.")

    def find_and_select(self, by, identifier, visible_text):
        element = self.driver.find_element(by, identifier)
        select = Select(element)
        select.select_by_visible_text(visible_text)
        self.human_wait(0.5, 1)
    
    def check_checkbox(self, by, identifier):
        checkbox = self.driver.find_element(by, identifier)
        if not checkbox.is_selected():
            checkbox.click()
        self.human_wait(0.5, 1)

    def upload_file(self, by, identifier, filepath):
        from pathlib import Path
        absolute_path = str(Path(filepath).resolve())
        self.driver.find_element(by, identifier).send_keys(absolute_path)
        self.human_wait(5, 7)

    def write_to_editor(self, text):
        editor = self.driver.find_element(By.CLASS_NAME, "note-editable")
        editor.click()  # 포커스 줘야 할 때도 있음
        editor.send_keys(text)
        self.human_wait(0.5, 1)

    def human_wait(self, min_sec=1, max_sec=2):
        time.sleep(min_sec + (max_sec - min_sec) * 0.5)

    def quit(self):
        self.driver.quit()

####################################################################
def stop_task():
    print('stop')
    return

def run_task():
    bot = StealthBot()
    bot.go('https://www.mule.co.kr/bbs/info/room')
    
    # Login
    res = bot.login()
    if res == error.Error_Type.LOGINFAIL:
        return error.Error_Type.LOGINFAIL

    def periodic_task():
        while True:
            bot.do_task()
            time.sleep(6 * 60 * 60)  # 6시간

    # 스레드로 반복 작업 시작
    threading.Thread(target=periodic_task, daemon=True).start()
    
    bot.close()

    return
