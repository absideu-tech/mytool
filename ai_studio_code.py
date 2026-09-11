import tkinter as tk
from tkinter import messagebox

def calculate_time():
    try:
        # 입력값 가져오기
        start_str = entry_start.get().replace(":", "")
        end_str = entry_end.get().replace(":", "")
        exclude_str = entry_exclude.get()

        if len(start_str) != 4 or len(end_str) != 4:
            raise ValueError("시간 형식을 HH:mm 또는 HHmm으로 입력해주세요. (예: 09:00)")

        # 시/분 분리
        start_hour, start_min = int(start_str[:2]), int(start_str[2:])
        end_hour, end_min = int(end_str[:2]), int(end_str[2:])
        
        # 제외 시간 처리 (숫자만 입력하면 분으로 처리, HH:mm 형식이면 변환)
        if ":" in exclude_str:
            ex_h, ex_m = map(int, exclude_str.split(":"))
            exclude_total_min = ex_h * 60 + ex_m
        else:
            exclude_total_min = int(exclude_str) if exclude_str else 0

        # 분 단위로 변환하여 계산
        start_total = start_hour * 60 + start_min
        end_total = end_hour * 60 + end_min

        # 종료 시간이 시작 시간보다 빠른 경우 (다음날로 넘어감) 처리
        if end_total < start_total:
            end_total += 24 * 60

        total_diff_min = end_total - start_total - exclude_total_min

        if total_diff_min < 0:
            messagebox.showwarning("경고", "제외 시간이 전체 시간보다 깁니다.")
            return

        # 결과 출력
        res_hour = total_diff_min // 60
        res_min = total_diff_min % 60
        
        label_result.config(text=f"결과: {res_hour}시간 {res_min}분", fg="blue")

    except ValueError as e:
        messagebox.showerror("오류", "올바른 시간 형식을 입력하세요.\n(예: 시작 09:00, 종료 18:00, 제외 60)")

# GUI 설정
root = tk.Tk()
root.title("시간 계산기")
root.geometry("300x350")
root.resizable(False, False)

# 폰트 설정
font_style = ("Malgun Gothic", 10)

# 입력 레이아웃
tk.Label(root, text="시작 시간 (예: 09:00)", font=font_style).pack(pady=5)
entry_start = tk.Entry(root, font=font_style, justify='center')
entry_start.pack()

tk.Label(root, text="종료 시간 (예: 18:00)", font=font_style).pack(pady=5)
entry_end = tk.Entry(root, font=font_style, justify='center')
entry_end.pack()

tk.Label(root, text="제외 시간 (분 단위 혹은 HH:mm)", font=font_style).pack(pady=5)
entry_exclude = tk.Entry(root, font=font_style, justify='center')
entry_exclude.insert(0, "0")  # 기본값 0
entry_exclude.pack()

# 계산 버튼
btn_calc = tk.Button(root, text="계산하기", font=("Malgun Gothic", 11, "bold"), 
                     command=calculate_time, bg="#4CAF50", fg="white", width=20)
btn_calc.pack(pady=20)

# 결과 표시
label_result = tk.Label(root, text="결과: 0시간 0분", font=("Malgun Gothic", 14, "bold"))
label_result.pack()

root.mainloop()