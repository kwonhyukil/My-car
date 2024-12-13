import cv2
import numpy as np

def process_frame(frame):
    """
    이미지에서 흰색 라인만 추출하기 위해 그레이스케일 변환 후 이진화를 수행하고
    모폴로지 연산으로 노이즈를 제거합니다.
    """
    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 흰색 라인 검출을 위한 이진화
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 모폴로지 연산으로 작은 노이즈 제거
    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return cleaned

def find_lane_center(cleaned_image):
    """
    이진화된 이미지에서 라인의 중심 좌표를 찾습니다.
    """
    contours, _ = cv2.findContours(cleaned_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # 가장 큰 윤곽선 찾기 (가장 큰 면적을 가지는 컨투어를 라인으로 가정)
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])  # 라인의 중심 x좌표
            cy = int(M['m01'] / M['m00'])  # 라인의 중심 y좌표
            return cx, cy
    return None

def calculate_steering(cx, frame_width):
    """
    라인의 중심 좌표(cx)와 프레임의 중앙을 비교하여 자동차의 회전 방향을 결정합니다.
    """
    # 차량의 중앙과 라인 중심의 차이를 구하여 방향 결정
    center_offset = cx - frame_width / 2
    if center_offset < -10:
        return "left"
    elif center_offset > 10:
        return "right"
    else:
        return "straight"

# 카메라 초기화
cap = cv2.VideoCapture(0)  # 카메라 번호가 0인 경우 (필요에 따라 1, 2로 변경)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지 처리 및 라인 검출
    processed_frame = process_frame(frame)
    lane_center = find_lane_center(processed_frame)
    
    if lane_center is not None:
        cx, cy = lane_center
        direction = calculate_steering(cx, frame.shape[1])
        print(f"Direction: {direction}")

        # 중심 좌표 표시
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    
    # 처리된 프레임 화면에 표시
    cv2.imshow("Lane Tracking", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라와 모든 창 종료
cap.release()
cv2.destroyAllWindows()
