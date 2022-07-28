import speech_recognition as sr
import itertools
import os
import pyttsx3
import ctypes
from playsound import playsound
import subprocess
from datetime import datetime
now = datetime.now()
"""import time
import shutil
import sys"""
#from multiprocessing import Process
#sys.path.insert(1, 'C:/Users/Arthur/Desktop/Code/SpeeachTest/')

#from animacao import animation



hideBar = "&{$p='HKCU:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3';$v=(Get-ItemProperty -Path $p).Settings;$v[8]=3;&Set-ItemProperty -Path $p -Name Settings -Value $v;&Stop-Process -f -ProcessName explorer}"
showbar = "&{$p='HKCU:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3';$v=(Get-ItemProperty -Path $p).Settings;$v[8]=2;&Set-ItemProperty -Path $p -Name Settings -Value $v;&Stop-Process -f -ProcessName explorer}"
def run(cmd):
    subprocess.run(["powershell", "-Command", cmd])

motor = pyttsx3.init()
motor.say(f"{'Bom dia' if now.hour < 12 and now.hour > 4  else 'Boa tarde' if now.hour >= 12 and now.hour < 18 else 'Boa noite'} {os.getlogin()}.")
motor.runAndWait()
#Função para ouvir e reconhecer a fala
def ouvir_microfone(question = 0, resposta = ''):
    #Habilita o microfone do usuário
    microfone = sr.Recognizer()
    #usando o microfone
    with sr.Microphone() as source:
        #Chama um algoritmo de reducao de ruidos no som
        microfone.adjust_for_ambient_noise(source)
        
        #Frase para o usuario dizer algo
        print("Diga alguma coisa: ")
        
        #Armazena o que foi dito numa variavel
        try:
            audio = microfone.listen(source,timeout=3)
        except sr.WaitTimeoutError:
            print("Não entendi")
            ouvir_microfone()
        
    try:
        #Passa a variável para o algoritmo reconhecedor de padroes
        frase = microfone.recognize_google(audio,language='pt-BR')
        """microfone = None
        audio = None
        source = None"""
        if 'modo de jogo' in frase.lower():
            location = frase.find('modo de jogo')
            location += 12
            name = ''
            name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
            
        #frase = frase['alternative'][0]['transcript']
        print(frase)
        if 'pesquisar' in frase.lower():
            location = frase.find('pesquisar')
            location += 9
            name = ''
            name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
            #os.startfile(f"C:/Users/Public/Desktop/Google Chrome")
            motor.say(f"Pesquisando {name}.")
            motor.runAndWait()
            
            try:
                from googlesearch import search
            except ImportError:
                print("Módulo chamado 'google' nao encontrado.")

            
            for j in search(name, tld="co.in", num=1, stop=1, pause=2):
                import webbrowser
                url = j
                webbrowser.open(url)
        if question == 1 and 'sim' in frase.lower():
            if resposta['taskkill']:
                os.system(f'TASKKILL /F /IM {resposta["taskkill"]} /T')
        if 'r2'in frase.lower():
            playsound("C:/Users/Arthur/Downloads/r2.mp3")
        if 'esconder barra' in frase.lower():
            run(hideBar)
        if 'mostrar barra' in frase.lower():
            run(showbar)
        if 'mudar' in frase.lower():
            location = frase.find('mudar')
            location += 5
            name = ''
            name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
            print(f"Mudando para {name.lower()}")
            if os.path.exists(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.png"):
                print(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.png" , 2)
            elif os.path.exists(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.jpg"):
                print(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.jpg")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.jpg" , 2)
            else:
                motor.say(f"Falha em localizar {name.lower().lstrip()}.")
                motor.runAndWait()
        """ if 'animação' in frase.lower():
            location = frase.find('animação')
            location += 8
            name = ''
            name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
            print(name)
            if os.path.exists('C:/Users/Arthur/Desktop/Code/SpeeachTest/pasta_imagens/'):
                shutil.rmtree('C:/Users/Arthur/Desktop/Code/SpeeachTest/pasta_imagens')
            if os.path.exists(f"C:/Users/Arthur/Downloads/{name.lower().lstrip()}.mp4"):
                p = Process(target=animation, args=(name,))
                p.daemon = True
                p.start()"""

        if "abrir" in frase.lower():
            location = frase.find('abrir')
            location += 6
            app = ''
            app = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
            try:
                s = app
                map(''.join,    itertools.product(*zip(s.upper(), s.lower())))
                os.startfile(f"C:/Users/Arthur/Desktop/{app.lstrip()}")
                motor.say(f"Abrindo {app.lstrip()}.")
                motor.runAndWait()
            except FileNotFoundError:
                try:
                    os.startfile(f"C:/Users/Public/Desktop/{app.lstrip()}")
                    motor.say(f"Abrindo {app.lstrip()}.")
                    motor.runAndWait()
                except FileNotFoundError:
                    motor.say(f"Arquivo {app.lstrip()} não encontado.")
                    motor.runAndWait()
                    print(f"Arquivo {app.lstrip()} não encontado.")
                    #print(f"C:/Users/Arthur/Desktop/{app.lstrip()}")
                    ouvir_microfone()
        if "fechar" in frase.lower():
            location = frase.find('fechar')
            location += 7
            app = ''
            app = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
            try :
                x = os.system(f'TASKKILL /F /IM {app.lstrip()}.exe /T')
                if x == 128:
                    raise Exception("Arquivo não encontrado")
                if x == 1:
                    appp = app.title()
                    appjunto = ''.join(appp.split())
                    #app = ''.join(app.split())
                    x = os.system(f'TASKKILL /F /IM {appjunto.lstrip()}.exe /T')
                    if x == 128:
                        os.system(f'taskkill /F /FI "WINDOWTITLE eq {appp.lstrip()}" ')
                        raise Exception("Arquivo não encontrado")
                    #else:
            except Exception:
                appp = app.title()
                output = os.popen('wmic process get description, processid').read()
                #"""print("2y")
                #print(y)
                appp = ''.join(appp.split())
                appp = app.lower() if app.lower() in output.lower() else appp.lower()
                if appp in output.lower():
                    location = output.lower().find(appp)
                    point = 0
                    palavra = ''
                    for i in range(100):
                        palavra += output[location+i]
                        if location + i >= len(output):
                            palavra = ''
                            break
                        if (output[location+i] and output[location+i-2]  == 'e') and output[location+i-3] == '.' and output[location+i-1] == 'x':
                            point += 4
                        if output[location+i] == "" or output[location+i] == "\n":
                            palavra = ''
                            point = 0
                        if point == 4:
                            print(f"Você quis dizer {palavra[0:len(palavra)-4]}?")
                            motor.say(f"Você quis dizer {palavra[0:len(palavra)-4]}?")
                            motor.runAndWait()
                            resposta = { 'taskkill':palavra}
                            ouvir_microfone(1,resposta)
                    #print()
                motor.say(f"Arquivo {app.lstrip()} não encontado.")
                motor.runAndWait()
                ouvir_microfone()
        
        #Retorna a frase pronunciada
        print("Você disse: " + frase)
        ouvir_microfone()
    
    #Se nao reconheceu o padrao de fala, exibe a mensagem
    except sr.UnknownValueError:
        print("Não entendi")
        ouvir_microfone()
        
    return frase


if __name__ == "__main__":
    ouvir_microfone()