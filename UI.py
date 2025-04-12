import customtkinter as ctk

# 테마 설정 (optional)
ctk.set_appearance_mode("Dark")  # 또는 "Dark", "Light"
ctk.set_default_color_theme("blue")  # 또는 "green", "dark-blue" 등

# 앱 생성
app = ctk.CTk()
app.geometry("400x300")
app.title("Mule Automation Tool")

# 위젯 추가
label = ctk.CTkLabel(app, text="뮬 홍보 자동화 프로그램")
label.pack(pady=10)

label = ctk.CTkLabel(app, text="글 제목")
label.pack(pady=10)
entry = ctk.CTkEntry(app, placeholder_text="Contents Title")
entry.pack(pady=10)

button = ctk.CTkButton(app, text="클릭", command=lambda: print(entry.get()))
button.pack(pady=10)

# 실행
app.mainloop()
