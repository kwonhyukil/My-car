import os
import tkinter as tk
from PIL import Image, ImageTk

# 이미지 작업용 폴더 설정
base_folder_path = r"C:\Traning_Data\arrows\2024-12-15"

# 폴더 내부의 모든 이미지 파일 가져오기
def get_all_images(base_folder):
    image_paths = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith(".jpg"):  # JPG 파일만 가져오기
                image_paths.append(os.path.join(root, file))
    return image_paths

# 모든 이미지 파일 가져오기
image_files = get_all_images(base_folder_path)

# 현재 이미지 인덱스
current_image_idx = 0

# 이미지 업데이트 함수
def update_image():
    global current_image_idx
    if image_files:
        img_path = image_files[current_image_idx]
        print(f"현재 이미지: {img_path}")  # 디버깅: 현재 이미지 경로 출력
        image = Image.open(img_path)
        image = image.resize((800, 600))  # 이미지를 창 크기에 맞게 조정
        img = ImageTk.PhotoImage(image)
        canvas.itemconfig(image_on_canvas, image=img)
        canvas.image = img
        label.config(text=f"{current_image_idx + 1}/{len(image_files)} - {img_path}")
    else:
        canvas.delete("all")
        canvas.create_text(400, 300, text="이미지가 없습니다!", font=("Arial", 20))
        label.config(text="이미지가 없습니다!")

# 다음 이미지 함수
def next_image():
    global current_image_idx
    if image_files:
        current_image_idx = (current_image_idx + 1) % len(image_files)
        update_image()

# 이전 이미지 함수
def prev_image():
    global current_image_idx
    if image_files:
        current_image_idx = (current_image_idx - 1) % len(image_files)
        update_image()

# 이미지 삭제 함수
def delete_image():
    global current_image_idx
    if image_files:
        img_path = image_files[current_image_idx]
        os.remove(img_path)  # 이미지 파일 삭제
        print(f"삭제됨: {img_path}")
        del image_files[current_image_idx]  # 리스트에서 제거
        current_image_idx = max(0, current_image_idx - 1)  # 인덱스 조정
        update_image()

# 프로그램 종료 함수
def close_program(event=None):
    print("프로그램 종료")
    root.destroy()

# 단축키 설정 함수
def setup_shortcuts():
    root.bind("<Left>", lambda event: prev_image())  # 왼쪽 화살표: 이전 이미지
    root.bind("<Right>", lambda event: next_image())  # 오른쪽 화살표: 다음 이미지
    root.bind("<Delete>", lambda event: delete_image())  # Delete 키: 이미지 삭제
    root.bind("<Escape>", close_program)  # ESC 키: 프로그램 종료

# tkinter GUI 초기화
root = tk.Tk()
root.title("Image Viewer - 우주 최강 귀요미 작업 중!")

# 캔버스 생성
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()
image_on_canvas = canvas.create_image(0, 0, anchor="nw")

# 현재 이미지 경로 및 상태 표시 라벨
label = tk.Label(root, text="")
label.pack()

# 버튼 생성
btn_prev = tk.Button(root, text="이전 이미지", command=prev_image)
btn_prev.pack(side="left")
btn_delete = tk.Button(root, text="삭제", command=delete_image)
btn_delete.pack(side="left")
btn_next = tk.Button(root, text="다음 이미지", command=next_image)
btn_next.pack(side="left")

# 단축키 설정
setup_shortcuts()

# 초기 이미지 설정
update_image()

# tkinter 실행
root.mainloop()
