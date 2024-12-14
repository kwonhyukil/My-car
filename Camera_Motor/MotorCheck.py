import pygame
from gpiozero import OutputDevice, PWMOutputDevice
import time
import os
from picamera2 import Picamera2
from datetime import datetime
import cv2

# 서보 모터 제어 핀 설정
servo_pin = PWMOutputDevice(21, frequency=50)  # 서보 모터 제어 핀 (GPIO 21번 핀)

# DC 모터 제어 핀 설정
in1 = OutputDevice(23)      # IN1 핀 (모터 방향 제어)
in2 = OutputDevice(24)      # IN2 핀 (모터 반대 방향 제어)
ena = PWMOutputDevice(18)   # ENA 핀 (모터 속도 제어)

# 카메라 초기화
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": "RGB888"}))
camera.start()

# 서보 모터 각도 설정 함수
current_angle = 90
def set_angle(angle):
    duty_cycle = 0.05 + (angle / 180) * 0.05  # 0도(5%) ~ 180도(10%) 사이 값
    servo_pin.value = duty_cycle
    print(f"{angle}도로 설정됨 (듀티 사이클: {duty_cycle:.3f})")

# DC 모터 제어 함수
current_speed = 0.0  # 초기 속도
motor_direction = None  # 전진, 후진 방향 상태를 유지

def motor_forward(speed):
    ena.value = speed
    in1.on()
    in2.off()

def motor_backward(speed):
    ena.value = speed
    in1.off()
    in2.on()

def motor_stop():
    ena.value = 0
    in1.off()
    in2.off()

# 사진 촬영 함수
last_capture_time = 0
def capture_photo():
    global last_capture_time
    now = datetime.now()
    timestamp = time.time()

    # 0.5초 간격으로만 캡처 실행
    if timestamp - last_capture_time >= 0.5:
        date_folder = now.strftime("%Y-%m-%d")
        time_stamp = now.strftime("%H-%M-%S-%f")[:-3]  # 파일명: 시간 및 밀리초
        folder_path = os.path.join("images", date_folder)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = os.path.join(folder_path, f"image_{time_stamp}.jpg")
        camera.capture_file(filename)
        last_capture_time = timestamp
        print(f"사진 저장 완료: {filename}")

# 메인 루프
running = True
try:
    while running:
        # 실시간 카메라 화면 표시
        frame = camera.capture_array()
        cv2.imshow("Live View", frame)

        # 키 입력 이벤트 처리
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 키: 종료
            running = False
        elif key == ord('q'):  # Q 키: 종료
            running = False
        elif key == ord('w'):  # W 키: 전진 속도 증가
            motor_direction = "forward"
            current_speed += 0.1
            if current_speed > 1.0:
                current_speed = 1.0
            print(f"속도 증가: {current_speed * 100:.1f}%")
        elif key == ord('s'):  # S 키: 전진 속도 감소
            motor_direction = "forward"
            current_speed -= 0.1
            if current_speed < 0.0:
                current_speed = 0.0
            print(f"속도 감소: {current_speed * 100:.1f}%")
        elif key == ord('a'):  # A 키: 왼쪽 회전
            if current_angle > 30:
                current_angle -= 30
            set_angle(current_angle)
        elif key == ord('d'):  # D 키: 오른쪽 회전
            if current_angle < 150:
                current_angle += 30
            set_angle(current_angle)

        # DC 모터 상태 유지
        if motor_direction == "forward":
            motor_forward(current_speed)
        elif motor_direction == "backward":
            motor_backward(current_speed)
        else:
            motor_stop()

        # 캡처 실행 (0.5초마다)
        capture_photo()

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    servo_pin.off()
    motor_stop()
    camera.stop()
    cv2.destroyAllWindows()
    print("프로그램 종료")