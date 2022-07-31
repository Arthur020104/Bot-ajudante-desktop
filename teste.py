import speech_recognition as sr
import itertools
import os
import pyttsx3
import ctypes
from playsound import playsound
import subprocess
from datetime import datetime
now = datetime.now()

hideBar = "&{$p='HKCU:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3';$v=(Get-ItemProperty -Path $p).Settings;$v[8]=3;&Set-ItemProperty -Path $p -Name Settings -Value $v;&Stop-Process -f -ProcessName explorer}"
showbar = "&{$p='HKCU:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3';$v=(Get-ItemProperty -Path $p).Settings;$v[8]=2;&Set-ItemProperty -Path $p -Name Settings -Value $v;&Stop-Process -f -ProcessName explorer}"
def run(cmd):
    subprocess.run(["powershell", "-Command", cmd])

motor = pyttsx3.init()
motor.say(f"{'Bom dia' if now.hour < 12 and now.hour > 4  else 'Boa tarde' if now.hour >= 12 and now.hour < 18 else 'Boa noite'} {os.getlogin()}.")
motor.runAndWait()
def escutar_audio_mic_reconhecer_falar(question = 0, resposta = ''):
    microfone = sr.Recognizer()
    #^
    #|Habilitando mic/|usando o microfone
    #                 ˘
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Diga alguma coisa: ")
        #Tenta armazenar o que foi dito numa variavel, se nao for possivel avisa que nao entedeu e chama a msm funcao dnv
        try:
            audio = microfone.listen(source,timeout=4)
        except sr.WaitTimeoutError:
            print("Não entendi")
            escutar_audio_mic_reconhecer_falar()
    try:
        #passa a variavel de audio para o reconhecedor de padroes do google
        frase = microfone.recognize_google(audio,language='pt-BR')
        if 'modo de jogo' in frase.lower():
            name = retornarpesquisa(frase, 'modo de jogo')
            #fazer o modo de jogo ser cofigurado com o terminal abrir novo terminal e listar imagens na pasta,perguntar se deseja modificar algum modo,
            #perguntar quantas imagens deseja nesse modo, listar as imagens com numeros e perguntar pela quantidade que ele escolheu uma de cada vez
            #perguntar nome do modo, pergutar se deseja abrir algum app com esse modo se 0 nao se qualquer outro quantidade que deseja e printar no final "modo configurado".
        print(frase)
        if 'pesquisar' in frase.lower():
            name = retornarpesquisa(frase, "pesquisar")
            motor.say(f"Pesquisando {name}.")
            motor.runAndWait()
            try:
                from googlesearch import search
            except ImportError:
                print("Módulo chamado 'google' nao encontrado.")
            for urls in search(name, tld="co.in", num=1, stop=1, pause=2):
                import webbrowser
                url = urls
                webbrowser.open(url)
        if question == 1 and 'sim' in frase.lower():
            if resposta['taskkill']:
                os.system(f'TASKKILL /F /IM {resposta["taskkill"]} /T')
        if 'r2'in frase.lower():
            playsound(f"C:/Users/{os.getlogin()}/Downloads/r2.mp3")
        if 'esconder barra' in frase.lower():
            run(hideBar)
        if 'mostrar barra' in frase.lower():
            run(showbar)
        if 'mudar' in frase.lower():
            name = retornarpesquisa(frase, 'mudar')
            print(f"Mudando para {name.lower()}")
            if os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.png"):
                print(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.png" , 2)
            elif os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.jpg"):
                print(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.jpg")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.jpg" , 2)
            else:
                motor.say(f"Falha em localizar {name.lower().lstrip()}.")
                motor.runAndWait()
        if "abrir" in frase.lower():
            app = retornarpesquisa(frase, "abrir")
            try:
                s = app
                map(''.join,    itertools.product(*zip(s.upper(), s.lower())))
                os.startfile(f"C:/Users/{os.getlogin()}/Desktop/{app.lstrip()}")
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
                    escutar_audio_mic_reconhecer_falar()
        if "fechar" in frase.lower():
            app = retornarpesquisa(frase, "fechar")
            try :
                retorno = os.system(f'TASKKILL /F /IM {app.lstrip()}.exe /T')
                if retorno == 128:
                    raise Exception("Arquivo não encontrado")
                if retorno == 1:
                    nomedoapp_title = app.title()
                    nomedoapp_sem_espaco = ''.join(nomedoapp_title.split())
                    retorno = os.system(f'TASKKILL /F /IM {nomedoapp_sem_espaco.lstrip()}.exe /T')
                    if retorno == 128:
                        os.system(f'taskkill /F /FI "WINDOWTITLE eq {nomedoapp_title.lstrip()}" ')
                        raise Exception("Arquivo não encontrado")
            except Exception:
                nomedoapp_title = app.title()
                todos_processos_pc = os.popen('wmic process get description, processid').read()
                nomedoapp_title = ''.join(nomedoapp_title.split())
                nome_app_parabusca = app.lower() if app.lower() in todos_processos_pc.lower() else nomedoapp_title.lower()
                #se o nome do app tiver em algum processo rodando no pc, procura o processo e pergunta se era esse que queria fechar
                if nome_app_parabusca in todos_processos_pc.lower():
                    location = todos_processos_pc.lower().find(nome_app_parabusca)
                    point = 0
                    palavra = ''
                    for i in range(100):
                        palavra += todos_processos_pc[location+i]
                        if location + i >= len(todos_processos_pc):
                            palavra = ''
                            break
                        if (todos_processos_pc[location+i] and todos_processos_pc[location+i-2]  == 'e') and todos_processos_pc[location+i-3] == '.' and todos_processos_pc[location+i-1] == 'x':
                            point += 4
                        if todos_processos_pc[location+i] == "" or todos_processos_pc[location+i] == "\n":
                            palavra = ''
                            point = 0
                        if point == 4:
                            print(f"Você quis dizer {palavra[0:len(palavra)-4]}?")
                            motor.say(f"Você quis dizer {palavra[0:len(palavra)-4]}?")
                            motor.runAndWait()
                            resposta = { 'taskkill':palavra}
                            escutar_audio_mic_reconhecer_falar(1,resposta)
                motor.say(f"Arquivo {app.lstrip()} não encontado.")
                motor.runAndWait()
                escutar_audio_mic_reconhecer_falar()
        
        print("Você disse: " + frase)
        #Retorno da frase
        escutar_audio_mic_reconhecer_falar()

    except sr.UnknownValueError:
        #Exibir mensagem se nao reconhecer padrao de fala
        print("Não entendi")
        escutar_audio_mic_reconhecer_falar()
        
    return frase
def retornarpesquisa(frase, acao):
    location = frase.find(acao)
    location += len(acao)
    name = ''
    name = "".join([i if i != "/n" and i != ""else "" for i in frase[location:len(frase)]])
    return name
def criar_pastawallpapers_senaoexite():
    if not os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers"):
        os.mkdir(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers")
    if not os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/Ler.txt"):
        arquivo = open(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/Ler.txt", 'w+')
        arquivo.writelines("Adicionar os wallpapers nessa pasta e todos os nomes dos arquivos devem ser com letras minúsculas.")
        arquivo.close()


if __name__ == "__main__":
    criar_pastawallpapers_senaoexite()
    escutar_audio_mic_reconhecer_falar()
#codigo de animacao que talvez vou usar
"""import time
import shutil
import sys"""
#from multiprocessing import Process
#sys.path.insert(1, 'C:/Users/Arthur/Desktop/Code/SpeeachTest/')

#from animacao import animation
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
