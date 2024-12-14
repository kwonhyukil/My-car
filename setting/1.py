import os
import subprocess

# 설치할 라이브러리 목록
libraries = [
    "opencv-python",
    "numpy",
    "torch",
    "gpiozero",
    "picamera2"
]

# 각 라이브러리 설치
for library in libraries:
    try:
        print(f"Installing {library}...")
        subprocess.check_call(["pip", "install", library])
        print(f"{library} installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {library}. Error: {e}")