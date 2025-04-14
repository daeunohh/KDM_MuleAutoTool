import customtkinter as ctk
import webnavigator
import error
import threading

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

def show_popup(str):
    print(str)

def check_if_bot_stopped():
    global running
    if not running:
        set_ui_state(False)
    else:
        app.after(1000, check_if_bot_stopped)  # 1초 후 다시 확인

def on_run_click():
    set_ui_state(True)

    def login_fail_callback():
        show_popup("로그인 실패, 아이디/비밀번호 확인")
        set_ui_state(False)

    def task_finished_callback():
        print("🌀 작업 1회 완료")

    def all_done_callback():
        show_popup("작업 중단됨")
        set_ui_state(False)

    threading.Thread(
        target=lambda: webnavigator.run_task(
            on_login_fail=login_fail_callback,
            on_task_finished=task_finished_callback,
            on_all_done=all_done_callback
        ),
        daemon=True
    ).start()

# def on_run_click():
#     set_ui_state(True)

#     id = id_entry.get()
#     if webnavigator.set_id(id) == error.Error_Type.ID:
#         show_popup('아이디를 확인해주세요.')
#         set_ui_state(False)
#         return
    
#     pw = pw_entry.get()
#     if webnavigator.set_pw(pw) == error.Error_Type.PW:
#         show_popup('비밀번호를 확인해주세요.')
#         set_ui_state(False)
#         return

#     ret = webnavigator.run_task()
#     if ret == error.Error_Type.LOGINFAIL :
#         show_popup('로그인 실패, 아이디와 비밀번호를 확인해주세요.')
#         set_ui_state(False)
#         return

#     # app.after(1000, check_if_bot_stopped)

def on_stop_click():
    webnavigator.stop_task()
    set_ui_state(False)
    return

######################################################################


# 테마 설정 (optional)
ctk.set_appearance_mode("Dark")  # 또는 "Dark", "Light"
ctk.set_default_color_theme("blue")  # 또는 "green", "dark-blue" 등

# 앱 생성
app = ctk.CTk()
app.geometry("400x440")
app.title("Mule posting autotool")

# 위젯 추가
title_label = ctk.CTkLabel(app, text="물 홍보 자동화 프로그램", font=ctk.CTkFont(size=16, weight="bold"))
title_label.pack(pady=(10, 5))

# ID 입력
id_label = ctk.CTkLabel(app, text="아이디")
id_label.pack(anchor="w", padx=20, pady=(20, 0))
id_entry = ctk.CTkEntry(app, placeholder_text="아이디 입력")
id_entry.pack(padx=20, fill="x")

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

# 실행
app.mainloop()
