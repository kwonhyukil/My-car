import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# 1️⃣ 각도별 사진 개수 확인
data_path = "data/"
angles = ["30", "60", "90", "120", "150"]
photo_counts = {}

for angle in angles:
    folder_path = os.path.join(data_path, angle)
    if os.path.exists(folder_path):
        photo_counts[angle] = len(os.listdir(folder_path))
    else:
        photo_counts[angle] = 0

# 결과 출력
print("각도별 사진 개수:", photo_counts)

# 2️⃣ 데이터 분포 시각화
plt.bar(photo_counts.keys(), photo_counts.values())
plt.xlabel("각도 (degrees)")
plt.ylabel("사진 수")
plt.title("각도별 사진 데이터 분포")
plt.show()

# 3️⃣ CNN 모델 학습 준비
# 데이터 증강 및 전처리
data_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2)  # 학습/검증 분리

train_data = data_gen.flow_from_directory(
    data_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    subset='training'  # 학습 데이터
)

val_data = data_gen.flow_from_directory(
    data_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    subset='validation'  # 검증 데이터
)

# CNN 모델 생성
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(angles), activation='softmax')  # 클래스 수 == 각도 수
])

# 모델 컴파일
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 학습
print("모델 학습 시작!")
history = model.fit(train_data, validation_data=val_data, epochs=10)

# 4️⃣ 학습된 모델 저장
model.save("cnn_angle_model.h5")
print("모델이 cnn_angle_model.h5로 저장되었습니다!")
