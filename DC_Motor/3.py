from gpiozero import OutputDevice, PWMOutputDevice
import time

# 제어 핀 설정
in1 = OutputDevice(23)      # IN1 핀 (모터 방향 제어)
in2 = OutputDevice(24)      # IN2 핀 (모터 반대 방향 제어)
ena = PWMOutputDevice(18)   # ENA 핀 (모터 속도 제어)

# 모터 제어 함수
def motor_forward(speed=0.5):
    ena.value = speed    # 속도 설정 (0.0 ~ 1.0)
    in1.on()
    in2.off()
    print("모터 정방향 회전")

def motor_backward(speed=0.5):
    ena.value = speed    # 속도 설정 (0.0 ~ 1.0)
    in1.off()
    in2.on()
    print("모터 반대 방향 회전")

def motor_stop():
    ena.value = 0        # 속도를 0으로 설정하여 정지
    in1.off()
    in2.off()
    print("모터 정지")

# 모터 실행 예시
while True:
    try:
        motor_forward(0.8)  # 80% 속도로 전진
        time.sleep(2)       # 2초간 유지
        motor_backward(0.8) # 80% 속도로 후진
        time.sleep(2)       # 2초간 유지
        motor_stop()        # 모터 정지
    finally:
        print("프로그램 종료")