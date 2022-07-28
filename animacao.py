import os
import ctypes
import cv2
import time

def sliptframes(location):
    os.mkdir("pasta_imagens")
    vidcap = cv2.VideoCapture(location)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("pasta_imagens/frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
    return count
def animation(name):
    count = sliptframes(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.mp4")
    countt = 0
    while True:
        if countt > 8:
            return
        countt +=1
        #time.sleep(10)
        step = 1
        """if count > 500:
            step = 5
            naodel = [i for i in range(0,count,step)]
            for i in range(count):
                if i in naodel:
                    continue
                else:
                    os.remove(f"C:/Users/Arthur/Desktop/Code/SpeeachTest/pasta_imagens/frame{i}.jpg")"""
        for i in range(0,count,step):
            #if i > 250:
            #    return
            ctypes.windll.user32.SystemParametersInfoW.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
            ctypes.windll.user32.SystemParametersInfoW.restype = ctypes.wintypes.BOOL
            print(f"C:/Users/Arthur/Desktop/Code/SpeeachTest/pasta_imagens/frame{i}.jpg")
            ctypes.windll.user32.SystemParametersInfoW(20, 0,f"C:/Users/Arthur/Desktop/Code/SpeeachTest/pasta_imagens/frame{i}.jpg" , 2)
            time.sleep(0.3)