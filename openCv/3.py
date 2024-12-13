import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def process_frame(frame):
    """
    입력된 프레임에서 흰색 차선을 추출하기 위해 그레이스케일 변환 후 이진화를 수행하고,
    모폴로지 연산을 통해 노이즈를 제거합니다.
    """
    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 흰색 차선 검출을 위한 이진화
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 모폴로지 연산으로 작은 노이즈 제거
    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return cleaned

def find_lane_center(cleaned_image):
    """
    이진화된 이미지에서 차선의 중심 좌표를 찾습니다.
    """
    contours, _ = cv2.findContours(cleaned_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # 가장 큰 윤곽선을 차선으로 간주하고, 그 중심을 찾음
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])  # 차선 중심의 x좌표
            cy = int(M['m01'] / M['m00'])  # 차선 중심의 y좌표
            return cx, cy
    return None

def calculate_steering(cx, frame_width):
    """
    차선의 중심 좌표(cx)와 프레임의 중앙을 비교하여 자동차의 회전 방향을 결정합니다.
    """
    # 차량의 중앙과 차선 중심의 차이를 계산하여 방향 결정
    center_offset = cx - frame_width / 2
    if center_offset < -10:
        return "left"
    elif center_offset > 10:
        return "right"
    else:
        return "straight"

# 라즈베리 파이 카메라 초기화
camera = PiCamera()
camera.resolution = (640, 480)  # 해상도 설정
camera.framerate = 32
raw_capture = PiRGBArray(camera, size=(640, 480))

# 카메라 초기화 지연 시간
time.sleep(0.1)

# 카메라로부터 프레임을 실시간으로 받아 처리
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array

    # 이미지 처리 및 차선 검출
    processed_frame = process_frame(image)
    lane_center = find_lane_center(processed_frame)
    
    if lane_center is not None:
        cx, cy = lane_center
        direction = calculate_steering(cx, image.shape[1])
        print(f"Direction: {direction}")

        # 차선 중심 좌표 표시
        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(image, f"Direction: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 원본 프레임에 차선 중심과 방향 표시 후 출력
    cv2.imshow("Real-Time Lane Tracking", image)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 카메라 스트림의 다음 프레임 준비
    raw_capture.truncate(0)

# 모든 창 종료
cv2.destroyAllWindows()
