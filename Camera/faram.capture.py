# A 입력시 저장되는 코드 (a 입력 이미지 캡쳐, q 입력시 종료)
import cv2
from picamera2 import Picamera2
import os
import time
# A 입력시 저장되는 코드
# 저장 디렉토리 설정
save_dir = "./captured_images/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)  # 디렉토리가 없으면 생성

# Picamera2 초기화
picam2 = Picamera2()
picam2.start()

print("Press 'A' to capture an image. Press 'Q' to quit.")

try:
    while True:
        # 실시간 카메라 화면
        frame = picam2.capture_array()
        cv2.imshow("Live Feed", frame)

        # 키 입력 대기
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('a'):  # 'A' 키를 눌렀을 때 사진 저장
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{save_dir}image_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captured and saved: {filename}")

        if key == ord('q'):  # 'Q' 키를 눌러 종료
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
