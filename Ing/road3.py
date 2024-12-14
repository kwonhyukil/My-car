import cv2
import numpy as np
import torch
from gpiozero import OutputDevice, PWMOutputDevice
from picamera2 import Picamera2
from datetime import datetime

# 서보 모터와 DC 모터 설정
servo_pin = PWMOutputDevice(21, frequency=50)
in1 = OutputDevice(23)
in2 = OutputDevice(24)
ena = PWMOutputDevice(18)

def set_servo_angle(angle):
    duty_cycle = 0.05 + (angle / 180) * 0.05
    servo_pin.value = duty_cycle
    print(f"서보 모터 각도: {angle}")

def set_dc_motor_speed(speed, direction="forward"):
    ena.value = abs(speed)
    if direction == "forward":
        in1.on()
        in2.off()
    elif direction == "backward":
        in1.off()
        in2.on()
    print(f"DC 모터 속도: {speed * 100:.1f}%, 방향: {direction}")

# 딥러닝 모델 로드
class SimpleLaneModel(torch.nn.Module):
    def __init__(self):
        super(SimpleLaneModel, self).__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(3, 16, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(16, 1, kernel_size=3, padding=1),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

model = SimpleLaneModel()
model.load_state_dict(torch.load("lane_model.pth", map_location="cpu"))
model.eval()

# 카메라 초기화
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
camera.start()

def detect_lane_with_model(frame):
    input_tensor = torch.tensor(frame).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    with torch.no_grad():
        output = model(input_tensor)
    mask = output.squeeze().cpu().numpy()
    return mask

try:
    while True:
        frame = camera.capture_array()
        lane_mask = detect_lane_with_model(frame)

        # 중심선 계산
        height, width = lane_mask.shape
        left_x = np.argmax(lane_mask[:, :width // 2], axis=1).mean()
        right_x = np.argmax(lane_mask[:, width // 2:], axis=1).mean() + width // 2
        center_x = (left_x + right_x) / 2

        # 차량 방향 제어
        frame_center = width / 2
        if center_x < frame_center - 10:
            set_servo_angle(45)  # 좌회전
            set_dc_motor_speed(0.5, direction="forward")
        elif center_x > frame_center + 10:
            set_servo_angle(135)  # 우회전
            set_dc_motor_speed(0.5, direction="forward")
        else:
            set_servo_angle(90)  # 직진
            set_dc_motor_speed(0.8, direction="forward")

        # 결과 표시
        cv2.imshow("Lane Mask", lane_mask)
        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    camera.stop()
    servo_pin.off()
    ena.value = 0
    in1.off()
    in2.off()
    cv2.destroyAllWindows()
