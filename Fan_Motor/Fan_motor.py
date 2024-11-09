from gpiozero import OutputDevice
import time

# 팬 모터 제어 핀 설정
fan_in_a = OutputDevice(23)  # IN A 핀 (한쪽 방향 제어)
fan_in_b = OutputDevice(24)  # IN B 핀 (반대 방향 제어)

# 팬 모터 제어 함수
def fan_on():
    fan_in_a.on()
    fan_in_b.off()  # 원래 방향으로 회전
    print("팬 모터 ON - 정방향")

def fan_reverse():
    fan_in_a.off()
    fan_in_b.on()  # 반대 방향으로 회전
    print("팬 모터 ON - 반대 방향")

def fan_off():
    fan_in_a.off()
    fan_in_b.off()  # 팬 정지
    print("팬 모터 OFF")

# 실행 예시
try:
    fan_on()             # 팬 모터 정방향 회전
    time.sleep(2)        # 2초 동안 유지
    fan_reverse()        # 팬 모터 반대 방향 회전
    time.sleep(2)        # 2초 동안 유지
finally:
    fan_off()            # 팬 모터 정지
    print("프로그램 종료")