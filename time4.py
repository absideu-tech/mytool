import tkinter as tk
from tkinter import ttk, messagebox

class TimeMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("시간 관리 프로그램")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure("Home.TButton", font=("Malgun Gothic", 10))

        # 메인 컨테이너
        self.main_frame = tk.Frame(self.root)
        self.calc_frame = tk.Frame(self.root)
        self.check_frame = tk.Frame(self.root)

        for frame in (self.main_frame, self.calc_frame, self.check_frame):
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.setup_main_screen()
        self.setup_calc_screen()
        self.setup_check_screen()

        self.show_frame(self.main_frame)

    def show_frame(self, frame):
        """프레임 전환 함수"""
        frame.tkraise()

    # --- 1. 메인 화면 ---
    def create_custom_button(self, parent, title_text, sub_text, command):
        btn_frame = tk.Frame(parent, bg="#f8f9fa", relief="groove", bd=1, cursor="hand2")
        btn_frame.pack(pady=10, padx=50, fill="x", ipady=12)

        title_lbl = tk.Label(btn_frame, text=title_text, font=("Malgun Gothic", 13, "bold"), bg="#f8f9fa")
        title_lbl.pack(pady=(0, 3))

        sub_lbl = tk.Label(btn_frame, text=sub_text, font=("Malgun Gothic", 10, "normal"), fg="#555555", bg="#f8f9fa")
        sub_lbl.pack()

        widgets = [btn_frame, title_lbl, sub_lbl]

        def on_enter(e):
            for w in widgets:
                w.config(bg="#e9ecef")

        def on_leave(e):
            for w in widgets:
                w.config(bg="#f8f9fa")

        for w in widgets:
            w.bind("<Button-1>", lambda e: command())
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

    def setup_main_screen(self):
        label = tk.Label(self.main_frame, text="원하는 기능을 선택하세요", font=("Malgun Gothic", 16, "bold"))
        label.pack(pady=35)

        self.create_custom_button(
            self.main_frame, 
            "단순 계산", 
            "(시작~종료 입력)", 
            lambda: self.show_frame(self.calc_frame)
        )
        self.create_custom_button(
            self.main_frame, 
            "시간 체크", 
            "(종료시간 도출)", 
            lambda: self.show_frame(self.check_frame)
        )

    # --- 헬퍼 함수: 입력 세트 생성 ---
    def create_input_set(self, parent, label_text, is_time_point=False):
        frame = tk.Frame(parent)
        frame.pack(pady=6)

        ampm_cb = None
        if is_time_point:
            ampm_cb = ttk.Combobox(frame, values=["오전", "오후"], width=4, state="readonly")
            ampm_cb.set("오전")
            # 24시 형식이 기본값이므로 초기에 pack하지 않음
        
        tk.Label(frame, text=label_text, font=("Malgun Gothic", 11), width=9, anchor="w").pack(side="left")
        
        h_entry = ttk.Entry(frame, width=5, justify='center')
        h_entry.pack(side="left")
        tk.Label(frame, text="시").pack(side="left", padx=2)
        
        m_entry = ttk.Entry(frame, width=5, justify='center')
        m_entry.pack(side="left")
        tk.Label(frame, text="분").pack(side="left", padx=2)
        
        return h_entry, m_entry, ampm_cb

    def toggle_mode(self, is_24h, widget_list):
        """24시 사용 여부에 따라 오전/오후 콤보박스 표시 여부 전환"""
        for cb in widget_list:
            if cb is not None:
                if is_24h.get():
                    cb.pack_forget()
                else:
                    # 12시 형식으로 전환 시 라벨 앞에 배치
                    cb.pack(side="left", padx=(0, 4), before=cb.master.winfo_children()[0])

    # --- 2. 단순 계산 화면 ---
    def setup_calc_screen(self):
        top_frame = tk.Frame(self.calc_frame)
        top_frame.pack(fill="x", padx=10, pady=10)

        btn_home = ttk.Button(top_frame, text="🏠 홈으로", command=lambda: self.show_frame(self.main_frame))
        btn_home.pack(side="left")

        # 24시 형식을 기본값(True)으로 설정
        self.calc_is_24h = tk.BooleanVar(value=True)
        chk_24h = ttk.Checkbutton(top_frame, text="24시 형식 사용", variable=self.calc_is_24h,
                                  command=lambda: self.toggle_mode(self.calc_is_24h, [self.s1_ampm, self.e1_ampm]))
        chk_24h.pack(side="right", padx=5)

        tk.Label(self.calc_frame, text="단순 시간 계산", font=("Malgun Gothic", 14, "bold")).pack(pady=10)

        self.s1_h, self.s1_m, self.s1_ampm = self.create_input_set(self.calc_frame, "시작 시간", is_time_point=True)
        self.e1_h, self.e1_m, self.e1_ampm = self.create_input_set(self.calc_frame, "종료 시간", is_time_point=True)
        self.ex1_h, self.ex1_m, _ = self.create_input_set(self.calc_frame, "제외 시간", is_time_point=False)

        btn_run = ttk.Button(self.calc_frame, text="계산하기", command=self.calculate_duration)
        btn_run.pack(pady=20)

        self.res1_label = tk.Label(self.calc_frame, text="결과: 0시간 0분", 
                                   font=("Malgun Gothic", 15, "bold"), fg="blue")
        self.res1_label.pack()

    # --- 3. 시간 체크 화면 ---
    def setup_check_screen(self):
        top_frame = tk.Frame(self.check_frame)
        top_frame.pack(fill="x", padx=10, pady=10)

        btn_home = ttk.Button(top_frame, text="🏠 홈으로", command=lambda: self.show_frame(self.main_frame))
        btn_home.pack(side="left")

        # 24시 형식을 기본값(True)으로 설정
        self.check_is_24h = tk.BooleanVar(value=True)
        chk_24h = ttk.Checkbutton(top_frame, text="24시 형식 사용", variable=self.check_is_24h,
                                  command=lambda: self.toggle_mode(self.check_is_24h, [self.s2_ampm]))
        chk_24h.pack(side="right", padx=5)

        tk.Label(self.check_frame, text="시간 달성 체크", font=("Malgun Gothic", 14, "bold")).pack(pady=10)

        self.s2_h, self.s2_m, self.s2_ampm = self.create_input_set(self.check_frame, "시작 시간", is_time_point=True)
        self.t2_h, self.t2_m, _ = self.create_input_set(self.check_frame, "목표 시간", is_time_point=False)
        self.ex2_h, self.ex2_m, _ = self.create_input_set(self.check_frame, "제외 시간", is_time_point=False)

        btn_run = ttk.Button(self.check_frame, text="계산하기", command=self.calculate_end_time)
        btn_run.pack(pady=20)

        self.res2_label = tk.Label(self.check_frame, text="결과: 오전 0시 0분", 
                                   font=("Malgun Gothic", 15, "bold"), fg="green")
        self.res2_label.pack()

    # --- 로직 처리 ---
    def get_val(self, entry):
        val = entry.get().strip()
        return int(val) if val else 0

    def parse_to_minutes(self, h_entry, m_entry, ampm_cb, is_24h):
        h = self.get_val(h_entry)
        m = self.get_val(m_entry)

        if not is_24h.get():
            ampm = ampm_cb.get()
            if ampm == "오후" and h < 12:
                h += 12
            elif ampm == "오전" and h == 12:
                h = 0
        return h * 60 + m

    def calculate_duration(self):
        try:
            start_min = self.parse_to_minutes(self.s1_h, self.s1_m, self.s1_ampm, self.calc_is_24h)
            end_min = self.parse_to_minutes(self.e1_h, self.e1_m, self.e1_ampm, self.calc_is_24h)
            exclude_min = self.get_val(self.ex1_h) * 60 + self.get_val(self.ex1_m)

            if end_min < start_min:
                end_min += 24 * 60
            diff = end_min - start_min - exclude_min
            
            if diff < 0:
                messagebox.showwarning("경고", "제외 시간이 전체 시간보다 깁니다.")
                return

            self.res1_label.config(text=f"결과: {diff // 60}시간 {diff % 60}분")
        except ValueError:
            messagebox.showerror("오류", "숫자만 입력해주세요.")

    def calculate_end_time(self):
        try:
            start_min = self.parse_to_minutes(self.s2_h, self.s2_m, self.s2_ampm, self.check_is_24h)
            target_min = self.get_val(self.t2_h) * 60 + self.get_val(self.t2_m)
            exclude_min = self.get_val(self.ex2_h) * 60 + self.get_val(self.ex2_m)

            final_min = (start_min + target_min + exclude_min) % (24 * 60)
            
            total_h = final_min // 60
            res_m = final_min % 60

            # 24시 형식 체크 여부와 관계없이 오전/오후 고정 표기
            ampm_str = "오전" if total_h < 12 else "오후"
            res_h = total_h % 12
            if res_h == 0:
                res_h = 12

            self.res2_label.config(text=f"결과: {ampm_str} {res_h}시 {res_m}분")
        except ValueError:
            messagebox.showerror("오류", "숫자만 입력해주세요.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeMasterApp(root)
    root.mainloop()