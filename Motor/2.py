import pygame
from gpiozero import PWMOutputDevice
import time

# Pygame 초기화
pygame.init()

# 제어 핀 설정
pin = PWMOutputDevice(21, frequency=50)  # 서보 모터 제어 핀 (GPIO 17번 핀)

# 각도를 설정하는 함수
def set_angle(angle):
    duty_cycle = 0.05 + (angle / 180) * 0.05  # 0도(5%) ~ 180도(10%) 사이 값
    pin.value = duty_cycle
    print(f"{angle}도로 설정됨 (듀티 사이클: {duty_cycle:.3f})")

# 초기 각도 설정 (중앙)a
current_angle = 90
set_angle(current_angle)

# 창 크기 설정 (Pygame용, 창은 필요 없으므로 최소 크기로 설정)
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("서보 모터 제어")

# 메인 루프
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # A 키: 왼쪽 회전
                    if current_angle > 30:   # 최소 각도 0도
                        current_angle -= 30  # 10도씩 이동
                        set_angle(current_angle)
                        time.sleep(0.05)
                elif event.key == pygame.K_d:  # D 키: 오른쪽 회전
                    if current_angle < 135:  # 최대 각도 180도
                        current_angle += 30  # 10도씩 이동
                        set_angle(current_angle)
                        time.sleep(0.05)
                        
except KeyboardInterrupt:
    pass

finally:
    # 종료 시 PWM 중지 및 Pygame 종료
    pin.off()
    pygame.quit()
    print("프로그램 종료")