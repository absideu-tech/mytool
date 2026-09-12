import tkinter as tk
from tkinter import ttk, messagebox

class TimeMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("시간 관리 프로그램")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # ttk 스타일
        self.style = ttk.Style()
        self.style.configure("Home.TButton", font=("Malgun Gothic", 10))

        # 프레임 컨테이너
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
        # 1px 연회색 외곽 테두리
        border_frame = tk.Frame(parent, bg="#d0d0d0", bd=0, cursor="hand2")
        border_frame.pack(pady=12, padx=50, fill="x")

        # 내부 순백색 카드 영역
        inner_frame = tk.Frame(border_frame, bg="#ffffff", bd=0)
        inner_frame.pack(padx=1, pady=1, fill="both", expand=True, ipady=True)

        title_lbl = tk.Label(inner_frame, text=title_text, font=("Malgun Gothic", 13, "bold"), bg="#ffffff", fg="#111111")
        title_lbl.pack(pady=(20, 3))

        sub_lbl = tk.Label(inner_frame, text=sub_text, font=("Malgun Gothic", 10, "normal"), bg="#ffffff", fg="#555555")
        sub_lbl.pack(pady=(0,20))

        widgets = [border_frame, inner_frame, title_lbl, sub_lbl]

        def on_enter(e):
            inner_frame.config(bg="#f4f5f7")
            title_lbl.config(bg="#f4f5f7")
            sub_lbl.config(bg="#f4f5f7")
            border_frame.config(bg="#b0b0b0")

        def on_leave(e):
            inner_frame.config(bg="#ffffff")
            title_lbl.config(bg="#ffffff")
            sub_lbl.config(bg="#ffffff")
            border_frame.config(bg="#d0d0d0")

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
            "(시작~종료 시간)", 
            lambda: self.show_frame(self.calc_frame)
        )
        self.create_custom_button(
            self.main_frame, 
            "시간 체크", 
            "(종료시간 도출)", 
            lambda: self.show_frame(self.check_frame)
        )

    # --- 헬퍼 함수: 입력 필드 세트 ---
    def create_input_set(self, parent, label_text):
        frame = tk.Frame(parent)
        frame.pack(pady=8)

        tk.Label(frame, text=label_text, font=("Malgun Gothic", 11), width=9, anchor="w").pack(side="left")
        
        h_entry = ttk.Entry(frame, width=5, justify='center')
        h_entry.pack(side="left")
        tk.Label(frame, text="시").pack(side="left", padx=2)
        
        m_entry = ttk.Entry(frame, width=5, justify='center')
        m_entry.pack(side="left")
        tk.Label(frame, text="분").pack(side="left", padx=2)
        
        return h_entry, m_entry

    # --- 2. 단순 계산 화면 ---
    def setup_calc_screen(self):
        btn_home = ttk.Button(self.calc_frame, text="🏠 홈으로", style="Home.TButton", 
                              command=lambda: self.show_frame(self.main_frame))
        btn_home.pack(anchor="nw", padx=10, pady=10)

        tk.Label(self.calc_frame, text="단순 시간 계산", font=("Malgun Gothic", 14, "bold")).pack(pady=10)

        self.s1_h, self.s1_m = self.create_input_set(self.calc_frame, "시작 시간")
        self.e1_h, self.e1_m = self.create_input_set(self.calc_frame, "종료 시간")
        self.ex1_h, self.ex1_m = self.create_input_set(self.calc_frame, "제외 시간")

        btn_run = ttk.Button(self.calc_frame, text="계산하기", command=self.calculate_duration)
        btn_run.pack(pady=25)

        self.res1_label = tk.Label(self.calc_frame, text="결과: 0시간 0분", 
                                   font=("Malgun Gothic", 15, "bold"), fg="blue")
        self.res1_label.pack()

    # --- 3. 시간 체크 화면 ---
    def setup_check_screen(self):
        btn_home = ttk.Button(self.check_frame, text="🏠 홈으로", style="Home.TButton", 
                              command=lambda: self.show_frame(self.main_frame))
        btn_home.pack(anchor="nw", padx=10, pady=10)

        tk.Label(self.check_frame, text="시간 체크", font=("Malgun Gothic", 14, "bold")).pack(pady=10)

        self.t2_h, self.t2_m = self.create_input_set(self.check_frame, "목표 시간")
        self.s2_h, self.s2_m = self.create_input_set(self.check_frame, "시작 시간")
        self.ex2_h, self.ex2_m = self.create_input_set(self.check_frame, "제외 시간")

        btn_run = ttk.Button(self.check_frame, text="계산하기", command=self.calculate_end_time)
        btn_run.pack(pady=25)

        self.res2_label = tk.Label(self.check_frame, text="결과: 오전 0시 0분", 
                                   font=("Malgun Gothic", 15, "bold"), fg="green")
        self.res2_label.pack()

    # --- 로직 처리 ---
    def get_val(self, entry):
        val = entry.get().strip()
        return int(val) if val else 0

    def calculate_duration(self):
        try:
            start_min = self.get_val(self.s1_h) * 60 + self.get_val(self.s1_m)
            end_min = self.get_val(self.e1_h) * 60 + self.get_val(self.e1_m)
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
            start_min = self.get_val(self.s2_h) * 60 + self.get_val(self.s2_m)
            target_min = self.get_val(self.t2_h) * 60 + self.get_val(self.t2_m)
            exclude_min = self.get_val(self.ex2_h) * 60 + self.get_val(self.ex2_m)

            final_min = (start_min + target_min + exclude_min) % (24 * 60)
            
            total_h = final_min // 60
            res_m = final_min % 60

            # 결과는 오전/오후 고정 표기
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