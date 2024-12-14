import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy

# 1️⃣ 데이터 생성 (예제 데이터)
X = np.random.rand(1000, 10)  # 1000개의 샘플, 각 샘플에 10개의 특성
y = np.random.randint(0, 5, (1000,))  # 다중 클래스 분류 (0, 1, 2, 3, 4)

# 2️⃣ 모델 생성
model = Sequential([
    Dense(64, activation='relu', input_shape=(10,)),  # 첫 번째 은닉층
    BatchNormalization(),                             # Batch Normalization 추가
    Dropout(0.3),                                     # Dropout 증가
    Dense(128, activation='relu'),                    # 두 번째 은닉층
    BatchNormalization(),
    Dropout(0.4),
    Dense(64, activation='relu'),                     # 세 번째 은닉층
    BatchNormalization(),
    Dropout(0.4),
    Dense(32, activation='relu'),                     # 네 번째 은닉층
    BatchNormalization(),
    Dropout(0.3),
    Dense(16, activation='relu'),                     # 다섯 번째 은닉층
    BatchNormalization(),
    Dropout(0.3),
    Dense(5, activation='softmax')                    # 출력층 (다중 클래스 분류)
])

# 3️⃣ 모델 컴파일
model.compile(
    optimizer=Adam(learning_rate=0.0005),             # 학습률 감소
    loss=SparseCategoricalCrossentropy(),            # 다중 클래스 분류 손실 함수
    metrics=['accuracy']                             # 정확도 평가
)

# 4️⃣ 모델 학습
history = model.fit(
    X, y,                                            # 전체 데이터
    validation_split=0.3,                            # 검증 데이터 비율 30%
    epochs=3000,                                       # Epoch 수 감소
    batch_size=32,                                   # Batch 크기
    verbose=1                                        # 학습 로그 출력
)

# 5️⃣ 학습 결과 확인
train_loss, train_accuracy = model.evaluate(X, y, verbose=0)
print(f"\n학습 손실: {train_loss:.4f}, 학습 정확도: {train_accuracy:.4f}")

# 6️⃣ 테스트 데이터 예측
X_test = np.random.rand(5, 10)  # 5개의 테스트 샘플
predictions = model.predict(X_test)

print("\n테스트 데이터 예측:")
for i, pred in enumerate(predictions):
    predicted_class = np.argmax(pred)  # 가장 높은 확률을 가지는 클래스
    print(f"샘플 {i + 1}: 클래스 {predicted_class} (확률: {pred[predicted_class]:.4f})")

# 7️⃣ 모델 저장
model.save('improved_model.h5')
print("\n모델이 'improved_model.h5'로 저장되었습니다.")
