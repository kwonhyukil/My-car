import pygame
from gpiozero import OutputDevice, PWMOutputDevice
import time

# Pygame 초기화
pygame.init()

# 서보 모터 제어 핀 설정
servo_pin = PWMOutputDevice(21, frequency=50)  # 서보 모터 제어 핀 (GPIO 21번 핀)

# DC 모터 제어 핀 설정
in1 = OutputDevice(23)      # IN1 핀 (모터 방향 제어)
in2 = OutputDevice(24)      # IN2 핀 (모터 반대 방향 제어)
ena = PWMOutputDevice(18)   # ENA 핀 (모터 속도 제어)

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
    print(f"모터 전진, 속도: {speed * 100:.1f}%")

def motor_backward(speed):
    ena.value = speed
    in1.off()
    in2.on()
    print(f"모터 후진, 속도: {speed * 100:.1f}%")

def motor_stop():
    ena.value = 0
    in1.off()
    in2.off()
    print("모터 정지")

# 초기 서보 각도 설정 (중앙) 및 DC 모터 정지
set_angle(current_angle)
motor_stop()

# Pygame 창 설정
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("모터 제어")

# 메인 루프
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Q 키: 프로그램 종료
                    running = False
                elif event.key == pygame.K_w:  # W 키: 전진
                    motor_direction = "forward"
                    current_speed += 0.1
                    if current_speed > 1:  # 최대 속도 제한
                        current_speed = 1
                elif event.key == pygame.K_s:  # S 키: 후진
                    motor_direction = "backward"
                    current_speed += 0.1
                    if current_speed > 1:  # 최대 속도 제한
                        current_speed = 1
                elif event.key == pygame.K_a:  # A 키: 왼쪽 회전
                    if current_angle > 30:  # 최소 각도 제한
                        current_angle -= 30
                    set_angle(current_angle)
                elif event.key == pygame.K_d:  # D 키: 오른쪽 회전
                    if current_angle < 150:  # 최대 각도 제한
                        current_angle += 30
                    set_angle(current_angle)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    motor_direction = motor_direction  # 속도 유지

        # DC 모터 상태 유지
        if motor_direction == "forward":
            motor_forward(current_speed)
        elif motor_direction == "backward":
            motor_backward(current_speed)
        elif motor_direction is None:
            motor_stop()

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    servo_pin.off()
    motor_stop()
    pygame.quit()
    print("프로그램 종료")
