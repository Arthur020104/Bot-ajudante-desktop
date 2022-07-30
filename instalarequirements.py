from time import sleep
import subprocess
requirements = ["opencv-python","google","playsound", "pyttsx3", "SpeechRecognition","datetime","pipwin"]
#playsound ctypes
def run(cmd):
    subprocess.run(["powershell", "-Command", cmd])
def principal():
    for requirement in requirements:
        run(f"pip install {requirement}")
    run(f"pipwin install pyaudio")
    for i in range(3, -1,-1):
        if i == 0:
            print("Limpando...")
            run("cls")
        if i in range(1,4):
            if i == 3:
                print("Limpando o terminal em.")
            print(i)
        sleep(1)
if __name__ == "__main__":
    principal()