import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import tensorflow as tf

# 1️⃣ 데이터 생성 (예제 데이터)
X = np.random.rand(1000, 10)  # 1000개의 샘플, 각 샘플에 10개의 특성
y = np.random.randint(0, 5, (1000,))  # 다중 클래스 분류 (0, 1, 2, 3, 4)

# 2️⃣ 모델 생성
model = Sequential([
    Dense(1024, activation='relu', input_shape=(10,), kernel_regularizer=tf.keras.regularizers.l2(0.05)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.05)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.05)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(5, activation='softmax')
])

# 3️⃣ 모델 컴파일
model.compile(
    optimizer=Adam(learning_rate=0.0005),
    loss=SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

# 4️⃣ EarlyStopping 및 Learning Rate Scheduler 설정
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=100,
    restore_best_weights=True
)
lr_scheduler = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.7,
    patience=15,
    min_lr=1e-6
)

# 5️⃣ 모델 학습
history = model.fit(
    X, y,
    validation_split=0.3,
    epochs=700,
    batch_size=256,  # Batch 크기 증가
    callbacks=[early_stopping, lr_scheduler],
    verbose=1
)

# 6️⃣ 학습 결과 확인
train_loss, train_accuracy = model.evaluate(X, y, verbose=0)
print(f"\n학습 손실: {train_loss:.4f}, 학습 정확도: {train_accuracy:.4f}")

# 7️⃣ 테스트 데이터 예측
X_test = np.random.rand(5, 10)
predictions = model.predict(X_test)

print("\n테스트 데이터 예측:")
for i, pred in enumerate(predictions):
    predicted_class = np.argmax(pred)
    print(f"샘플 {i + 1}: 클래스 {predicted_class} (확률: {pred[predicted_class]:.4f})")

# 8️⃣ 모델 저장
model.save('improved_model_final.h5')
print("\n모델이 'improved_model_final.h5'로 저장되었습니다.")
