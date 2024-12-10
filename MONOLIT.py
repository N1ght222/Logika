import sys

def clear():
    sys.stdout.write('\033[H\033[J')
    sys.stdout.flush()

try:
    from colorama import init, Fore
    import time
    import os
    import socket
    import requests
    from rich.console import Console
    from rich.table import Table
except ImportError as e:
    print("Скачай библиотеки pip install colorama rich requests")

init() 
        
c = Console()
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
yellow = Fore.YELLOW
purpl = Fore.MAGENTA

reset = Fore.RESET

menu_text = f"""{purpl}|{reset}{green}1.пробив по IP(Полная инфа)                 2.пробив IP(Рашифровка){reset}{purpl}   |{reset}
{purpl}|{reset}{red}Для вихода - exit                           Для фикса меню - fix{reset}{purpl}      |{reset}
{purpl}|{reset}{blue}Калькутор - calc                      Проверка дисплея - display test{reset}{purpl} |{reset}
{purpl}|{reset}{blue}Мой IP адресс - myip                        Информация - info {reset}{purpl}        |{reset}
{purpl}|{reset}{yellow}О создателе - creator                       О проекте - project{reset}{purpl}       |{reset}
{purpl}|{reset}{purpl}                          servers - sv                                 |{reset}"""
   
def ip_1(ip):
    def get_hostname_by_ip(ip_address):
        try:
            hostname, alias, ip = socket.gethostbyaddr(ip_address)
            return hostname
        except socket.herror as e:
            return f"Не удалось определить имя хоста для IP-адреса {ip_address}: {e}"

    def get_whois_info(ip_address):
        try:
            response = requests.get(f"https://rdap.arin.net/registry/ip/{ip_address}")
            return response.json()
        except Exception as e:
            return f"Не удалось получить информацию WHOIS для IP-адреса {ip_address}: {e}"

    def get_geoip_info(ip_address):
        try:
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            return response.json()
        except Exception as e:
            return f"Не удалось получить информацию GeoIP для IP-адреса {ip_address}: {e}"

    def ip_info(ip):
        try:
            response = requests.get(f"http://ipinfo.io/{ip}/json")
            if response.status_code == 200:
                data = response.json()
                print(data)
                return data
            else:
                return f"Не удалось получить информацию об IP: {ip}"
        except requests.exceptions.RequestException as e:
            return f"Произошла ошибка при запросе: {e}"
        
    hostname = get_hostname_by_ip(ip)
    whois_info = get_whois_info(ip)
    geoip_info = get_geoip_info(ip)
    print(f"Имя устройства для IP-адреса {ip}: {hostname}")
    print(f"Информация WHOIS для IP-адреса {ip}: {whois_info}")
    print(f"Информация GeoIP для IP-адреса {ip}: {geoip_info}")

def ip_2(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    data = response.json()
    c = Console()
    table = Table(title="Информация о IP-адресе")

    table.add_column("Параметр", style="cyan", no_wrap=True)
    table.add_column("Значение", style="magenta")

    for key, value in data.items():
        table.add_row(key, str(value))
    c.print(table)
    

def public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data['ip']

def local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def color(text, color):
    print(color + text + reset)
def rich(text, color):
    c.print(text, style=color)

    
def start():
    def logo():
        logo = """
    ███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ ██╗     ██╗████████╗
    ████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗██║     ██║╚══██╔══╝
    ██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║██║     ██║   ██║   
    ██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║██║     ██║   ██║   
    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝███████╗██║   ██║   
    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   
    """
        rich(logo, "#205670")
        color("    CODE BY TIMONO", yellow)
        color("""    Github: https://github.com/TimonoTV
    """, red)
        
    def menu():
        color("⌈" + "¯" * 70 + "⌉", purpl)
        print(menu_text)
        color("⌊" + "_" * 70 + "⌋", purpl)
        print("")
    
    clear()
    logo()
    menu()
    
start()

def q():
    q = input(blue + "Для вихода в меню нажмите Enter..." + reset)
    start()
    
def creator():
    m = """
Слава Монолиту!
Во славу Монолита!
Монолит зовет нас!
Мы едины с Монолитом!
Монолит, направь нас!
Монолит, защити нас!
Во имя Монолита!
Смерть врагам Монолита!
Монолит ведет нас к победе!
Монолит — наша вера и сила!

я Timono пишу MONOLIT на amd fx6300 6cores, gigabyte gtx750

Моя старая видуха умерла(
------|=======================|
      |                       |
    ==|       ⌈¯¯¯¯¯¯⌉        |
     =|       |gs8000|        |
    ==|       ⌊______⌋        |
      |                       |
      |=======================|
       #################
       
не забудем
"""
    rich(m, "#fa8d07")
    
def project():
    project = """О проекте:
проект создан как инструмент для Termux
написан на язике Python
использовать моожно как хотите
"""
    rich(project, "#9907fa")
    color("Удачи вам)", purpl)




def cr_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, int(port)))
    server_socket.listen(5)
    print(f"Server started on IP {ip} and port {port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключен клиент: {client_address}")
        data = client_socket.recv(1024)
        print(f"Получено: {data.decode('utf-8')}")
        client_socket.close()

def client(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        print(f"Подключено к серверу {ip}:{port}")
        message = input(red + "message: " + reset)
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        print(f"Ответ от сервера: {response.decode()}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

def DOS_client(ip, port, sms, r):
    for i in range(r):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        message = sms
        print(sms)
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        client_socket.close()

def servers():
    clear()
    rich("beta obcidian.on", "#790987")
    menu = """
server 
  |_ 1.server create
      |_ 1.system
      |_ 2.local

client 
  |_ 1.client connect
  |_ 2.DOS connect"""
    rich(menu, "#019880")
    op = input(purpl + "Вибрать опцию: " + reset)
    if op == "menu":
        q()
    if op == "server":
        server = input(blue + "Действие с сервером: " + reset)
        if server == "1":
            type_server = input(yellow + "Тип сервера: " + reset)
            if type_server == "1":
                port = int(input(green + "server port: "))
                print(reset)
                cr_server("127.0.0.1", port)
            if type_server == "2":
                ip = input(green + "server ip: ")
                port = input("server port: ")
                print(reset)
                cr_server(ip, port)
    if op == "client":
        type_client = input(yellow + "Тип клиента: " + reset)
        if type_client == "1":
            ip = input(green + "server ip: ")
            port = int(input("server port: "))
            print(reset)
            client(ip, port)
        if type_client == "2":
            ip = input(green + "server ip: ")
            port = int(input("server port: "))
            sms = input("Передай серверу привет): ")
            print(reset)
            r = int(input(red + "сколько DOS сообшений: " + reset))
            DOS_client(ip, port, sms, r)
        
    q()

wind = True
while wind:
    vod = input(green + "MONOLIT: " + reset)
    if vod == "1":
        clear()
        ip = input(yellow + "Веддите IP: " + reset)
        print(green + "Пробив..." + reset)
        time.sleep(0.5)
        if ip == "":
            print(red + "Пустой IP" + reset)
            q()
        else:
            ip_1(ip)
            q()
    elif vod == "2":
        clear()
        ip = input(yellow + "Веддите IP: " + reset)
        print(green + "Пробив..." + reset)
        time.sleep(0.5)
        if ip == "":
            print(red + "Пустой IP" + reset)
            q()
        else:
            ip_2(ip)
            q()
    elif vod == "exit":
        wind = False
        clear()
    elif vod == "calc":
        clear()
        calc = input(yellow + "Пример: " + reset)
        print(eval(calc))
        q()
    elif vod == "fix":
        start()
    elif vod == "creator":
        creator()
        q()
    elif vod == "project":
        project()
        q()
    elif vod == "display test":
        col = 100000
        for i in range(1152):
            col = col + i
            rich("■" * 80, f"#{col}")
            time.sleep(0.01)
        q()
    elif vod == "myip":
        rich("Локальний: " + local_ip(), "#300456")
        rich("Публичний: " + public_ip(), "#406900")
        q()
    elif vod == "info":
        rich("Названия системи: " + os.name, "#205670")
    elif vod == "sv":
        servers()
    else:
        print(red + "Команда не найдена" + reset)
