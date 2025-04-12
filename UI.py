import customtkinter as ctk
import webnavigator
import error

def show_popup(str):
    print(str)

def on_run_click():
    title = subject_entry.get()
    if webnavigator.set_title(title) == error.Error_Type.TITLE:
        show_popup('글 제목을 확인해주세요.')
        return
    
    content1 = text1.get("1.0", "end").strip()
    content2 = text2.get("1.0", "end").strip()
    if webnavigator.set_contents(content1, content2) == error.Error_Type.CONTENT:
        show_popup('글 내용을 확인해주세요.')
        return

    ret = webnavigator.run_task()
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

# 글 제목 입력
subject_label = ctk.CTkLabel(app, text="글 제목")
subject_label.pack(anchor="w", padx=20)

subject_entry = ctk.CTkEntry(app, placeholder_text="합주실 홍보합니다.")
# subject_entry.insert(0, "합주실 홍보합니다.")
subject_entry.pack(padx=20, pady=(0, 10), fill="x")

# 글 내용 라벨
content_label = ctk.CTkLabel(app, text="글 내용")
content_label.pack(anchor="w", padx=20)

# 첫 번째 텍스트박스
text1 = ctk.CTkTextbox(app, height=100, )
text1.insert("1.0", "홍보글_1 내용 입력")
text1.pack(padx=20, pady=5, fill="both")
# 두 번째 텍스트박스
text2 = ctk.CTkTextbox(app, height=100)
text2.insert("1.0", "홍보글_2 내용 입력")
text2.pack(padx=20, pady=5, fill="both")

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
