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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert

app = None
my_bbs = 'https://www.mule.co.kr/mymule/mybbs'
status = 'idle'
static_id = 'Libera1'

def set_app(_app):
    global app
    app = _app

def is_id_valid(id):
    if static_id in id:
        return True 
    return False

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

# class SeleniumBot:
#     def __init__(self, driver_path="chromedriver.exe"):
#         service = Service(executable_path=driver_path)
#         self.driver = webdriver.Chrome(service=service)

#     def open(self, url):
#         self.driver.get(url)

#     def open_mule(self):
#         self.open('https://www.mule.co.kr/')

#     def search_google(self, keyword):
#         self.driver.get("https://www.google.com")
#         box = self.driver.find_element(By.NAME, "q")
#         box.send_keys(keyword)
#         box.submit()

#     def click_by_text(self, tag, text):
#         elements = self.driver.find_elements(By.TAG_NAME, tag)
#         for e in elements:
#             if text in e.text:
#                 e.click()
#                 break

#     def wait(self, seconds):
#         time.sleep(seconds)

#     def close(self):
#         self.driver.quit()  

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
        
        self.driver = uc.Chrome(options=options)

    def do_task(self):
        self.human_wait(3, 4)

        self.go(my_bbs)
        self.click_by_index(By.CSS_SELECTOR, "div.more-btn.clickable", 0)
        self.human_wait(10,20)

        box = self.driver.find_elements(By.CSS_SELECTOR, "div.mymule-box")[3]
        rows = box.find_elements(By.CSS_SELECTOR, "table.small-table tbody tr")
        # rows = self.driver.find_elements(By.CSS_SELECTOR, "table.small-table tbody tr")
        target_rows = []
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if not tds:
                continue  # 첫 번째 row (헤더)는 제외됨

            board_name = tds[0].text.strip()
            if board_name == "합주실/연습실":
                target_rows.append(row)
        # print("👉 현재 끌올 예정 글 갯수:",  len(target_rows))
        if len(target_rows) <= 2:
            for row in target_rows:
                try:
                    link_element = row.find_element(By.TAG_NAME, "a")
                    title = link_element.text
                    print("👉 현재 끌올 중 인 글:", title)

                    # 클릭 (같은 탭에서 열림)
                    link_element.click()
                    self.human_wait(2,3) 
                    # 페이지 로딩 대기 (필요 시 WebDriverWait으로 바꿔도 됨)

                    try:
                        self.click(By.XPATH, "//a[contains(text(), '최신글로 올리기')]")
                        self.human_wait(3, 5)

                        # 클릭 후 alert이 떠 있는지 확인
                        alert = self.driver.switch_to.alert
                        alert_text = alert.text
                        print("🚨 알림창 감지:", alert_text)

                        if "6시간 이후에 가능합니다" in alert_text:
                            print("❌ 최신글 등록 실패 (쿨타임 중)")
                        else:
                            alert.accept()  # 확인 눌러서 닫기
                            print("✅ 최신글 등록 성공")
                        alert.accept()  # 확인 눌러서 닫기

                    except NoAlertPresentException:
                        print("✅ 알림 없이 최신글 등록 완료")

                    except UnexpectedAlertPresentException as e:
                        print("❌ 예외 발생:", e)

                    except Exception as e:
                        print("❌ 예외 발생:", e)
                    
                    finally:
                        self.driver.back()
                        self.human_wait(2, 3)

                except NoSuchElementException:
                    print("❌ 링크 클릭 실패: a 태그 없음")
        
        self.human_wait(1)
        return
    
    def login(self):
        self.click(By.ID, "bt-write")
        self.find_and_type(By.ID, "login-user-id", Options.id)
        self.find_and_type(By.ID, "login-user-pw", Options.pw)
        try:
            self.click(By.CSS_SELECTOR, "a.login-bt.login")
            self.human_wait(3, 5)

            # 클릭 후 alert이 떠 있는지 확인
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print("🚨 알림창 감지:", alert_text)
            print("❌ 로그인 실패 (간접적으로 감지)")  # 예: 로그인 후에만 나오는 메뉴
            alert.accept()  # 확인 눌러서 닫기

            return error.Error_Type.LOGINFAIL         

        except NoAlertPresentException:
            print("✅ 로그인 성공")
            return error.Error_Type.NONE

        except UnexpectedAlertPresentException as e:
            print("❌ 예외 발생:", e)
            return error.Error_Type.UNKNOWN

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
    global status
    if status == 'running':
        print("🚨 최신글 등록 작업 중에는 중지 불가합니다.")
        print("중지를 원하시면 크롬창을 닫아주세요.")
        return True
    status = 'stopped'
    return False

def run_task(on_login_fail=None, on_task_finished=None, on_all_done=None):
    global status
    status = 'running'

    bot = StealthBot()
    bot.go('https://www.mule.co.kr/bbs/info/room')
    
    # Login
    try:
        res = bot.login()
        if res == error.Error_Type.LOGINFAIL:
            bot.quit()
            if on_login_fail:
                app.after(0, on_login_fail)
            return
    except Exception as e:
        print("❌ 로그인 중 예외 발생:")
        status = 'idle'
        bot.quit()
        if on_all_done:
            app.after(0, on_all_done)
        return

    def periodic_task():
        global status
        status = 'running'

        while status == 'running':
            try:
                status = 'running'
                bot.do_task()
            except Exception as e:
                print("❌ do_task 중 예외 발생:")
                status = 'idle'
                if on_all_done:
                    app.after(0, on_all_done)
                bot.quit()
                return

            if on_task_finished:
                app.after(0, on_task_finished)

            for _ in range(6 * 60 * 60): 
                if status == 'stopped':
                    if on_all_done:
                        status = 'idle'
                        bot.quit()
                        app.after(0, on_all_done)
                    return
                status = 'idle'                
                time.sleep(1)


    # 스레드로 반복 작업 시작
    threading.Thread(target=periodic_task, daemon=True).start()
    return error.Error_Type.NONE
