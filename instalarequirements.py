import subprocess
requirements = ["opencv-python","google","playsound", "pyttsx3", "speech_recognition","datetime"]
#playsound ctypes
def run(cmd):
    subprocess.run(["powershell", "-Command", cmd])
def principal():
    for requirement in requirements:
        run(f"pip install {requirement}")

if __name__ == "__main__":
    principal()