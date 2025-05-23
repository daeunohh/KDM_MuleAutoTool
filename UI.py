import customtkinter as ctk
import webnavigator
import error
import threading
import sys
import tkinter.messagebox as msgbox
from datetime import datetime, timedelta
import time

version_string = "1.08"
n = 0
inter_minutes = 60* 60

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
        elif any(x in line for x in ["❌", "🚨","🛑","⚠"]):
            return "error"
        elif any(x in line for x in ["🔄", "⏳", "🚀"]):
            return "status"
        return "info"

    def flush(self):
        pass

def set_ui_state(running: bool):
    for id_entry, pw_entry in id_pw_entries:
        id_entry.configure(state="disabled" if running else "normal")
        pw_entry.configure(state="disabled" if running else "normal")
    # toggle_button.configure(state="disabled" if running else "normal")
    run_button.configure(state="disabled" if running else "normal")
    stop_button.configure(state="normal" if running else "disabled")

def on_run_click():
    set_ui_state(True)
    webnavigator.set_app(app)
    webnavigator.status = 'idle'

    id_pw_list = []
    all_empty = True
    invalid_rows = []

    for idx, (id_entry, pw_entry) in enumerate(id_pw_entries):
        uid = id_entry.get().strip()
        pw = pw_entry.get().strip()

        if uid or pw:
            all_empty = False

        if uid and pw:
            id_pw_list.append((uid, pw))
        elif uid or pw:
            invalid_rows.append(idx + 1)  # 사용자에게 보여주기 위해 1-based 인덱스 사용

    if all_empty:
        print("❌ ID/PW가 모두 비어 있습니다. 최소 한 쌍 이상 입력해 주세요.")
        set_ui_state(False)
        return

    if invalid_rows:
        print(f"❌ 다음 입력칸에 ID 또는 PW가 누락되었습니다: {', '.join(map(str, invalid_rows))}번째")
        print("⚠️ 모든 ID/PW 쌍이 정확히 입력되어야 작업이 시작됩니다.")
        set_ui_state(False)
        return
    

    def run_all():
        global n
        now = datetime.now()

        # 각 ID의 다음 실행 예약 시간 초기화
        next_run_time_map = {}
        for i, (uid, pw) in enumerate(id_pw_list):
            next_run_time_map[(uid, pw)] = now + timedelta(seconds=i * inter_minutes)  # ID 간 1시간 간격 예약

        while True:
            if webnavigator.status == 'stopped':
                break

            for idx, (uid, pw) in enumerate(id_pw_list):
                # 중지 체크
                if webnavigator.status == 'stopped':
                    break

                now = datetime.now()
                next_time = next_run_time_map[(uid, pw)]

                # 아직 실행 시간이 안 됐으면 대기
                remaining = (next_time - now).total_seconds()
                if remaining > 0:
                    mins_left = int(remaining // 60)
                    print(f"⏳ ID {idx+1} 실행까지 약 {mins_left}분 대기...")
                    for _ in range(int(remaining)):
                        if webnavigator.status == 'stopped':
                            break
                        time.sleep(1)

                # 다시 한 번 중지 체크
                if webnavigator.status == 'stopped':
                    break
                
                print(f"🚀 [{idx+1}번째 ID] {uid} 작업 시작")

                # ID 작업 실행
                if webnavigator.set_id(uid) == error.Error_Type.ID:
                    print(f"❌ 아이디 오류: {uid}")
                    continue

                if webnavigator.set_pw(pw) == error.Error_Type.PW:
                    print(f"❌ 비밀번호 오류: {uid}")
                    continue

                done_event = threading.Event()

                def login_fail_callback():
                    print(f"❌ 로그인 실패, 아이디/비밀번호 확인: {uid}")
                    done_event.set()

                def task_finished_callback():
                    global n
                    n += 1
                    print("✅ 작업 1회 완료")
                    done_event.set()

                def all_done_callback():
                    global n
                    print("✅ 작업 중단됨")
                    n = 0
                    app.after(0, lambda: set_ui_state(False))

                webnavigator.status = 'running'
                webnavigator.run_task(
                    on_login_fail=login_fail_callback,
                    on_task_finished=task_finished_callback,
                    on_all_done=all_done_callback
                )
                done_event.wait()
                webnavigator.status = 'idle'

                # 다음 실행 시간 갱신: 현재 시간 + 6시간
                next_run_time_map[(uid, pw)] = datetime.now() + timedelta(hours=6)

            else:
                print("🔄 모든 ID 순회 완료, 다음 라운드 준비 중...")
        
        try:
            print("✅ 작업 중단됨")
        except Exception as e:
            print("❌ print 실패:", e)
        

    threading.Thread(target=run_all, daemon=True).start()

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

id_pw_entries = []  # [(id_entry, pw_entry)] 리스트
pw_entries = []  # 모든 PW entry들을 담기

entry_frame = ctk.CTkFrame(app, fg_color="transparent")
entry_frame.pack(padx=10, pady=5, fill="x")

for i in range(4):  # 고정된 4쌍
    row_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
    row_frame.pack(fill="x", pady=2)  # 간격 좁게

    id_entry = ctk.CTkEntry(row_frame, placeholder_text=f"ID {i+1}")
    id_entry.pack(side="left", expand=True, fill="x", padx=(0, 4))

    pw_entry = ctk.CTkEntry(row_frame, placeholder_text=f"PW {i+1}") #, show="*")
    pw_entry.pack(side="left", expand=True, fill="x", padx=(4, 0))

    id_pw_entries.append((id_entry, pw_entry))

button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(padx=20, pady=10, fill="x")

stop_button = ctk.CTkButton(button_frame, text="중지", fg_color="#2a2a2a", 
                            hover_color="#444", width=180, height=40,
                            command=on_stop_click)
stop_button.pack(side="left", padx=(0, 10))

run_button = ctk.CTkButton(button_frame, text="실행", fg_color="#3B82F6",  
                           height=40,width=180,
                           command=on_run_click)
run_button.pack(side="right", padx=(10, 0))

log_box = ctk.CTkTextbox(app)
log_box.pack(padx=20, pady=10, fill="both", expand=True)

sys.stdout = TextRedirector(log_box)
sys.stderr = TextRedirector(log_box)

print("✅ 봇 시작됨")

app.mainloop()
