import pygame
import math

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("화살표 각도 제한 (0° ~ 180°)")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 255)

# 화살표 그리기 함수
def draw_stylish_arrow(surface, color, position, angle):
    x, y = position
    body_length = 70  # 화살표 몸통 길이
    body_width = 10   # 화살표 몸통 너비
    head_length = 30  # 화살표 머리 길이
    head_width = 30   # 화살표 머리 너비
    angle_rad = math.radians(angle)

    # 몸통 사각형 좌표 계산
    body_x1 = x + body_length * math.cos(angle_rad)
    body_y1 = y - body_length * math.sin(angle_rad)
    body_points = [
        (x - body_width / 2 * math.sin(angle_rad), y - body_width / 2 * math.cos(angle_rad)),
        (x + body_width / 2 * math.sin(angle_rad), y + body_width / 2 * math.cos(angle_rad)),
        (body_x1 + body_width / 2 * math.sin(angle_rad), body_y1 + body_width / 2 * math.cos(angle_rad)),
        (body_x1 - body_width / 2 * math.sin(angle_rad), body_y1 - body_width / 2 * math.cos(angle_rad)),
    ]

    # 머리 삼각형 좌표 계산
    head_x = body_x1 + head_length * math.cos(angle_rad)
    head_y = body_y1 - head_length * math.sin(angle_rad)
    head_points = [
        (body_x1 + head_width / 2 * math.sin(angle_rad), body_y1 + head_width / 2 * math.cos(angle_rad)),
        (body_x1 - head_width / 2 * math.sin(angle_rad), body_y1 - head_width / 2 * math.cos(angle_rad)),
        (head_x, head_y),
    ]

    # 몸통과 머리 그리기
    pygame.draw.polygon(surface, color, body_points)
    pygame.draw.polygon(surface, color, head_points)

# 초기 각도 설정
angle = 90  # 기본 각도는 90° (화살표가 정중앙을 가리킴)

# 메인 루프
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)  # 배경색 채우기
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += 2  # 왼쪽 화살표 키로 각도 증가
    if keys[pygame.K_RIGHT]:
        angle -= 2  # 오른쪽 화살표 키로 각도 감소

    # 각도 제한 (0° ~ 180°)
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    # 화면 중앙에 화살표 그리기
    draw_stylish_arrow(screen, BLUE, (WIDTH // 2, HEIGHT // 2), angle)
    
    # 화면 갱신
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
