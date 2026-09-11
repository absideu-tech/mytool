import tkinter as tk
from tkinter import ttk, messagebox

class TimeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("시간 관리 프로")
        self.root.geometry("400x450")
        
        # 탭 메뉴 생성 (단순 계산 / 시간 체크)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # 1. 단순 계산 탭
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="단순 계산")
        self.setup_tab1()

        # 2. 시간 체크 탭
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="시간 체크")
        self.setup_tab2()

    def create_time_input(self, parent, label_text):
        """시/분 입력 필드 세트를 만드는 헬퍼 함수"""
        frame = ttk.Frame(parent)
        frame.pack(pady=5)
        
        ttk.Label(frame, text=label_text, width=10).pack(side="left")
        
        h_entry = ttk.Entry(frame, width=5, justify='center')
        h_entry.pack(side="left")
        ttk.Label(frame, text="시").pack(side="left", padx=2)
        
        m_entry = ttk.Entry(frame, width=5, justify='center')
        m_entry.pack(side="left")
        ttk.Label(frame, text="분").pack(side="left", padx=2)
        
        return h_entry, m_entry

    def setup_tab1(self):
        """단순 계산 모드 UI: 시작~종료 사이 시간 계산"""
        container = ttk.Frame(self.tab1, padding="20")
        container.pack(fill="both")

        self.s1_h, self.s1_m = self.create_time_input(container, "시작 시간")
        self.e1_h, self.e1_m = self.create_time_input(container, "종료 시간")
        self.ex1_h, self.ex1_m = self.create_time_input(container, "제외 시간")

        ttk.Button(container, text="소요 시간 계산", command=self.calculate_duration).pack(pady=20)
        
        self.res1_label = ttk.Label(container, text="결과: 0시간 0분", font=("Malgun Gothic", 12, "bold"), foreground="blue")
        self.res1_label.pack()

    def setup_tab2(self):
        """시간 체크 모드 UI: 목표 달성을 위한 종료 시간 도출"""
        container = ttk.Frame(self.tab2, padding="20")
        container.pack(fill="both")

        self.t2_h, self.t2_m = self.create_time_input(container, "목표 시간")
        self.s2_h, self.s2_m = self.create_time_input(container, "시작 시간")
        self.ex2_h, self.ex2_m = self.create_time_input(container, "제외 시간")

        ttk.Button(container, text="필요 종료 시간 계산", command=self.calculate_end_time).pack(pady=20)
        
        self.res2_label = ttk.Label(container, text="결과: 00시 00분", font=("Malgun Gothic", 12, "bold"), foreground="green")
        self.res2_label.pack()

    def get_val(self, entry):
        """입력값이 비어있으면 0을 반환"""
        val = entry.get().strip()
        return int(val) if val else 0

    def calculate_duration(self):
        """단순 계산 로직"""
        try:
            start_min = self.get_val(self.s1_h) * 60 + self.get_val(self.s1_m)
            end_min = self.get_val(self.e1_h) * 60 + self.get_val(self.e1_m)
            exclude_min = self.get_val(self.ex1_h) * 60 + self.get_val(self.ex1_m)

            if end_min < start_min: end_min += 24 * 60  # 자정 넘김 처리
            
            diff = end_min - start_min - exclude_min
            
            if diff < 0:
                messagebox.showwarning("경고", "제외 시간이 전체 시간보다 큽니다.")
                return

            self.res1_label.config(text=f"결과: {diff // 60}시간 {diff % 60}분")
        except ValueError:
            messagebox.showerror("오류", "숫자만 입력해주세요.")

    def calculate_end_time(self):
        """시간 체크 로직 (종료 시간 도출)"""
        try:
            target_min = self.get_val(self.t2_h) * 60 + self.get_val(self.t2_m)
            start_min = self.get_val(self.s2_h) * 60 + self.get_val(self.s2_m)
            exclude_min = self.get_val(self.ex2_h) * 60 + self.get_val(self.ex2_m)

            final_min = start_min + target_min + exclude_min
            
            # 24시간 형식으로 표시 (하루를 넘어가면 0시부터 시작하도록)
            res_h = (final_min // 60) % 24
            res_m = final_min % 60

            self.res2_label.config(text=f"권장 종료 시간: {res_h:02d}시 {res_m:02d}분")
        except ValueError:
            messagebox.showerror("오류", "숫자만 입력해주세요.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeCalculator(root)
    root.mainloop()