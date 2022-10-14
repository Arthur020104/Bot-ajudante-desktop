import os
import cv2
import ctypes,win32con

def sliptframes(location):
    os.mkdir('C:/Users/Arthur/Desktop/teste_animation')
    vidcap = cv2.VideoCapture(location)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("C:/Users/Arthur/Desktop/teste_animation/frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
    return count
def animation(name):
    count = sliptframes(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.mp4")
    while True:
        for i in range(0,count):
            changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
            ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER,0,f"C:/Users/Arthur/Desktop/teste_animation/frame{i}.jpg",changed)