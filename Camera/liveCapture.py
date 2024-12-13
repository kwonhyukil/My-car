import cv2
from picamera2 import Picamera2
import os
import time
import threading

# 기본 설정
base_dir = "./captured_images/"  # 저장 폴더의 기본 경로
capture_running = False  # 캡처 상태를 제어하는 변수
capture_interval = 0.5  # 초당 2번 캡처

# Picamera2 초기화
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))

# 저장 디렉토리 생성 함수
def create_directory(base_dir):
    current_time = time.strftime("%Y-%m-%d/%H-%M-%S")  # 날짜 및 시간별 폴더
    directory = os.path.join(base_dir, current_time)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# 캡처 함수 (별도 스레드에서 실행)
def capture_images():
    global capture_running
    save_directory = create_directory(base_dir)
    while capture_running:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_directory, f"image_{timestamp}.jpg")
        frame = picam2.capture_array()
        cv2.imwrite(filename, frame)  # 이미지 저장
        print(f"Captured and saved: {filename}")
        time.sleep(capture_interval)  # 초당 2번 캡처 (0.5초 간격)

# 메인 프로그램
print("Press 'A' to start capturing. Press 'Q' to quit.")
picam2.start()

try:
    while True:
        # 카메라 실시간 화면 표시
        frame = picam2.capture_array()
        cv2.imshow("Live Feed", frame)

        # 키 입력 대기
        key = cv2.waitKey(1) & 0xFF

        if key == ord('a'):  # 'A' 키를 눌러 캡처 시작
            if not capture_running:
                print("Capture started.")
                capture_running = True
                threading.Thread(target=capture_images).start()

        if key == ord('q'):  # 'Q' 키를 눌러 종료
            if capture_running:
                capture_running = False
                print("Capture stopped.")
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()