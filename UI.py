import customtkinter as ctk
import webnavigator
import error

def show_popup(str):
    print(str)

def on_run_click():
    id = id_entry.get()
    if webnavigator.set_id(id) == error.Error_Type.ID:
        show_popup('아이디를 확인해주세요.')
        return
    
    pw = pw_entry.get()
    if webnavigator.set_pw(pw) == error.Error_Type.PW:
        show_popup('비밀번호를 확인해주세요.')
        return

    ret = webnavigator.run_task()
    if ret == error.Error_Type.LOGINFAIL :
        show_popup('로그인 실패, 아이디와 비밀번호를 확인해주세요.')

    return

def on_stop_click():
    webnavigator.stop_task()
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

# # 글 제목 입력
# subject_label = ctk.CTkLabel(app, text="글 제목")
# subject_label.pack(anchor="w", padx=20)
# subject_entry = ctk.CTkEntry(app, placeholder_text="합주실 홍보합니다.")
# subject_entry.pack(padx=20, pady=(0, 10), fill="x")
# # 글 내용 라벨
# content_label = ctk.CTkLabel(app, text="글 내용")
# content_label.pack(anchor="w", padx=20)
# # 첫 번째 텍스트박스
# text1 = ctk.CTkTextbox(app, height=100, )
# text1.insert("1.0", "홍보글_1 내용 입력")
# text1.pack(padx=20, pady=5, fill="both")
# # 두 번째 텍스트박스
# text2 = ctk.CTkTextbox(app, height=100)
# text2.insert("1.0", "홍보글_2 내용 입력")
# text2.pack(padx=20, pady=5, fill="both")

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
