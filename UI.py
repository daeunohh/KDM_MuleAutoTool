import customtkinter as ctk
import webnavigator
import error
import threading
import sys
import tkinter.messagebox as msgbox
from datetime import datetime
version_string = "1.052"
n = 0

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
        self._buffer = ""
        self._line_count = 0  # 줄 번호 추적

        # 태그 색상 설정
        self.widget.tag_config("info", foreground="lightgray")
        self.widget.tag_config("success", foreground="lightgreen")
        self.widget.tag_config("error", foreground="tomato")
        self.widget.tag_config("status", foreground="skyblue")

        # ✅ 로그 파일 이름 생성 (실행 시간 기준)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_filename = f"error_log_{timestamp}.txt"

    def write(self, text):
        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._insert_line(line)

    def _insert_line(self, line: str):
        if not line.strip():
            return

        timestamp = datetime.now().strftime("[%H:%M:%S]")
        full_line = f"{timestamp} {line.strip()}\n"

        tag = self._get_tag_for_line(line)

        start_index = self.widget.index("end-1c")
        self.widget.insert("end", full_line)
        end_index = self.widget.index("end-1c")
        self.widget.tag_add(tag, start_index, end_index)
        self.widget.see("end")

        try:
            with open(self.log_filename, "a", encoding="utf-8") as f:
                f.write(full_line)
        except Exception:
            pass  # 파일 오류는 조용히 무시

    def _get_tag_for_line(self, line: str):
        if any(x in line for x in ["✅"]):
            return "success"
        elif any(x in line for x in ["❌", "🚨","🛑"]):
            return "error"
        elif any(x in line for x in ["🔄"]):
            return "status"
        return "info"

def set_ui_state(running: bool):
    if running:
        id_entry.configure(state="disabled")
        pw_entry.configure(state="disabled")
        toggle_button.configure(state="disabled")
        run_button.configure(state="disabled")
        stop_button.configure(state="normal")
    else:
        id_entry.configure(state="normal")
        pw_entry.configure(state="normal")
        toggle_button.configure(state="normal")
        run_button.configure(state="normal")
        stop_button.configure(state="disabled")

def on_run_click():
    set_ui_state(True)
    webnavigator.set_app(app)

    id = id_entry.get()
    if webnavigator.set_id(id) == error.Error_Type.ID:
        print("❌ 아이디를 확인해주세요.")
        set_ui_state(False)
        return
    
    pw = pw_entry.get()
    if webnavigator.set_pw(pw) == error.Error_Type.PW:
        print("❌ 비밀번호를 확인해주세요.")
        set_ui_state(False)
        return

    def login_fail_callback():
        print("❌ 로그인 실패, 아이디/비밀번호 확인")
        set_ui_state(False)

    def task_finished_callback():
        global n
        n += 1
        print("✅ 작업 " + str(n) + "회 완료")

    def all_done_callback():
        global n
        print("✅ 작업 중단됨")
        n = 0
        set_ui_state(False)

    threading.Thread(
        target=lambda: webnavigator.run_task(
            on_login_fail=login_fail_callback,
            on_task_finished=task_finished_callback,
            on_all_done=all_done_callback
        ),
        daemon=True
    ).start()

def on_stop_click():
    is_running = webnavigator.stop_task()
    if not is_running:
        set_ui_state(False)
    return

def on_close():
    if webnavigator.status == 'running':
        if msgbox.askokcancel("종료 확인", "작업이 실행 중입니다. 정말 종료하시겠습니까?"):
            app.destroy()
    else:
        app.destroy()

######################################################################


# 테마 설정 (optional)
ctk.set_appearance_mode("Dark")  # 또는 "Dark", "Light"
ctk.set_default_color_theme("blue")  # 또는 "green", "dark-blue" 등

# 앱 생성
app = ctk.CTk()
app.geometry("400x440")
app.resizable(False, False)
app.title("Mule posting autotool")
app.protocol("WM_DELETE_WINDOW", on_close)

# 위젯 추가
title_label = ctk.CTkLabel(app, text="물 홍보 자동화 프로그램 ver" + version_string, font=ctk.CTkFont(size=16, weight="bold"))
title_label.pack(pady=(10, 5))

# ID 입력
id_label = ctk.CTkLabel(app, text="아이디")
id_label.pack(anchor="w", padx=20, pady=(20, 0))
id_entry = ctk.CTkEntry(app, placeholder_text="아이디 입력")
id_entry.pack(padx=20, fill="x")
id_entry.insert(0, "Libera2")

# PW 입력
pw_label = ctk.CTkLabel(app, text="비밀번호")
pw_label.pack(anchor="w", padx=20, pady=(10, 0))
# 비밀번호 프레임 (입력칸 + 토글 버튼)
pw_frame = ctk.CTkFrame(app, fg_color="transparent")
pw_frame.pack(padx=20, fill="x")
# 토글 버튼
def toggle_pw_visibility():
    if pw_entry.cget("show") == "*":
        pw_entry.configure(show="")
        toggle_button.configure(text="숨기기")
    else:
        pw_entry.configure(show="*")
        toggle_button.configure(text="보기")

toggle_button = ctk.CTkButton(pw_frame, text="보기", fg_color="#2a2a2a", 
                            hover_color="#444", width=60, command=toggle_pw_visibility)
toggle_button.pack(side="right", padx=(5, 0))

pw_entry = ctk.CTkEntry(pw_frame, placeholder_text="비밀번호 입력", show="*")
pw_entry.pack(side="left", expand=True, fill="x")

button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(padx=20, pady=20, fill="x")

stop_button = ctk.CTkButton(button_frame, text="중지", fg_color="#2a2a2a", 
                            hover_color="#444", width=180, height=40,
                            command=on_stop_click)
stop_button.pack(side="left", padx=(0, 10))

run_button = ctk.CTkButton(button_frame, text="실행", fg_color="#3B82F6",  
                           height=40,width=180,
                           command=on_run_click)

run_button.pack(side="right", padx=(10, 0))

log_box = ctk.CTkTextbox(app, width=380, height=200)
log_box.pack(padx=20, pady=10)

sys.stdout = TextRedirector(log_box)
sys.stderr = TextRedirector(log_box)

print("✅ 봇 시작됨")

# 실행
app.mainloop()
