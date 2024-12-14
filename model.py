import os
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# 1️⃣ 데이터 준비
base_folder_path = r"C:\Traning_Data\arrows\2024-12-15"
labels_map = {"30_degrees": 0, "60_degrees": 1, "90_degrees": 2, "120_degrees": 3, "150_degrees": 4}

def load_data(base_folder):
    images = []
    labels = []
    for folder_name, label in labels_map.items():
        folder_path = os.path.join(base_folder, folder_name)
        for file in os.listdir(folder_path):
            if file.endswith(".jpg"):
                img_path = os.path.join(folder_path, file)
                img = load_img(img_path, target_size=(64, 64))
                img_array = img_to_array(img) / 255.0
                images.append(img_array)
                labels.append(label)
    return np.array(images), np.array(labels)

images, labels = load_data(base_folder_path)
labels = to_categorical(labels, num_classes=5)
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# 2️⃣ 모델 정의
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(5, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = create_model()

# 3️⃣ 모델 학습
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=1000, batch_size=32)

# 4️⃣ 모델 저장
model.save("motor_control_model.h5")
print("모델 저장 완료: motor_control_model.h5")
