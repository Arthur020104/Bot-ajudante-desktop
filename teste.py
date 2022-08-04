import speech_recognition as sr
import itertools
import os
import pyttsx3
import ctypes
from playsound import playsound
import subprocess
from datetime import datetime
from cs50 import SQL
import random
# configurando sql database
try:
    db = SQL(f"sqlite:///C:/Users/{os.getlogin()}/Documents/Db_userinfo_R2ajudante/r2ajudanteusersinfo.db")
except RuntimeError:
    print("Nao existe")
    os.mkdir(f"C:/Users/{os.getlogin()}/Documents/Db_userinfo_R2ajudante")
    arquivo = open(f"C:/Users/{os.getlogin()}/Documents/Db_userinfo_R2ajudante/r2ajudanteusersinfo.db", 'w+')
    arquivo.close()
    db = SQL(f"sqlite:///C:/Users/{os.getlogin()}/Documents/Db_userinfo_R2ajudante/r2ajudanteusersinfo.db")
    db.execute("CREATE TABLE modos_de_jogo(id INTEGER PRIMARY KEY,nome TEXT, imgs_list TEXT, app_list TEXT)")
    #Seria melhor criar uma tabela para as imgs e uma para os apps e dps estabelecer relaçao one-to-many, mas vou deixar mais simples agr
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
            name = retornarpesquisa(frase, 'modo de jogo').lower()
            if name == "criar":
                nome_mododejogo = input("Nome do modo de jogo a ser criado.\n-").lower().strip()
                if nome_mododejogo == "criar":
                    print('Você nao pode criar um modo de jogo com a palavra criar')
                    escutar_audio_mic_reconhecer_falar()
                quant_imgs = int(input("Quantas imagens você deseja adicionar nesse modo de jogo.\n-"))
                list_imgs = os.listdir(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers")
                list_imgs.pop(list_imgs.index("Ler.txt"))
                [print(f"{i} - {list_imgs[i]}") for i in range(len(list_imgs))]
                imgs = []
                for imgs_n in range(quant_imgs):
                    num = int(input("Qual img vc deseja selecionar.\n-"))
                    imgs.append(list_imgs[num])
                string_das_imgs = "".join([f'{imgs[i]}\n' if not i+1 == len(imgs) else f'{imgs[i]}' for i in range(len(imgs))])
                quant_apps = int(input(f"{'*'*55}\nQuantos apps você deseja abrir nesse modo de jogo.\n{'*'*55}\n-"))
                #list - f"C:/Users/{os.getlogin()}/Desktop/"
                #list - C:/Users/Public/Desktop/
                list_desktop_apps = os.listdir(f"C:/Users/{os.getlogin()}/Desktop/")
                list_desktop_apps_public = os.listdir("C:/Users/Public/Desktop/")
                list_all_desktop_apps = list_desktop_apps + list_desktop_apps_public
                [print(f"{i} - {list_all_desktop_apps[i]}") for i in range(len(list_all_desktop_apps))]
                apps = []
                for i in range(quant_apps):
                    num = int(input("Qual apps vc deseja selecionar.\n-"))
                    apps.append(list_all_desktop_apps[num])
                string_dos_apps = "".join([f'{apps[i]}\n' if not i+1 == len(apps) else f'{apps[i]}' for i in range(len(apps))])
                db.execute("INSERT INTO modos_de_jogo(nome,imgs_list,app_list) VALUES(?, ?, ?)",nome_mododejogo, string_das_imgs,string_dos_apps)
               #listar apps nas areas de trabalho e numerar igual acima
            modos_de_jogo = db.execute("SELECT nome FROM modos_de_jogo")
            if not modos_de_jogo:
                print('Você ainda nao adicionou nenhum modo de jogo.')
                escutar_audio_mic_reconhecer_falar()
            if name in modos_de_jogo[0]['nome']:
                dados_modo = db.execute("SELECT * FROM modos_de_jogo WHERE nome == ?",name.lower())[0]
                imgs_list = dados_modo['imgs_list'].split("\n")
                img = imgs_list[random.randrange(0, len(imgs_list))]
                apps_list = dados_modo['app_list'].split("\n")
                alterar_desktop_img(img)
                for app in apps_list:
                    open_app(app)
            if 'deletar' in name:
                namedel = retornarpesquisa(frase, 'modo de jogo deletar').lower()
                if not namedel in modos_de_jogo[0]['nome']:
                    return
                db.execute('DELETE FROM modos_de_jogo WHERE nome == ?',namedel)

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
            motor.say("Olá")
            motor.runAndWait()
        if 'esconder barra' in frase.lower():
            run(hideBar)
        if 'mostrar barra' in frase.lower():
            run(showbar)
        if 'mudar' in frase.lower():
            name = retornarpesquisa(frase, 'mudar')
            print(f"Mudando para {name.lower()}")
            alterar_desktop_img(name)
        if "abrir" in frase.lower():
            app = retornarpesquisa(frase, "abrir")
            open_app(app)
            
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
    return name.lstrip()
def criar_pastawallpapers_senaoexite():
    if not os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers"):
        os.mkdir(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers")
    if not os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/Ler.txt"):
        arquivo = open(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/Ler.txt", 'w+')
        arquivo.writelines("Adicionar os wallpapers nessa pasta e todos os nomes dos arquivos devem ser com letras minúsculas.")
        arquivo.close()
def alterar_desktop_img(name):
    if '.' in name:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}" , 2)
    elif os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.png"):
        print(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.png")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.png" , 2)
    elif os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.jpg"):
        print(f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.jpg")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, f"C:/Users/{os.getlogin()}/Desktop/Wallpapers/{name.lower().lstrip()}.jpg" , 2)
    else:
        motor.say(f"Falha em localizar {name.lower().lstrip()}.")
        motor.runAndWait()
def open_app(app):
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
    if os.path.exists(f"C:/Users/Arthur/Downloads/{name.lower()c}.mp4"):
        p = Process(target=animation, args=(name,))
        p.daemon = True
        p.start()"""
