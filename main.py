# TODO: сделать нормальное управление каталогами удалённой машины(paramiko, разобраться)
import paramiko, time, socket, os, subprocess, threading

ports = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    66: "SQL-NET",
    69: "TFTP",
    80: "HTTP",
    81: "HTTP",
    115: "SFTP",
    118: "SQL-services",
    143: "IMAP",
    150: "SQL-NET",
    8888: "Web-interface"
}

machines = (
    {
        "ip": "192.168.0.90",
        "name": "root",
        "password": "123456",
        "port": 22,
    },
)


def ping(*args):  # ip, times
    try:
        if len(args) == 2:
            arg = "ping " + "-n " + args[1] + " " + args[0]
            con_out = subprocess.check_output(arg, shell=True).decode('cp866')
            print(str(con_out))
        elif len(args) != 0:
            arg = "ping " + "-n 1 " + args[0]
            con_out = str(subprocess.check_output(arg, shell=True).decode('cp866'))
            if "недоступен" not in con_out and "превышен" not in con_out:
                if len(args) == 3:
                    return 1
                print(f"{args[0]} доступен")
            else:
                if len(args) == 3:
                    return 0
                print(f"{args[0]} недоступен")
        else:
            print("Не указано достаточно аргументов")
    except:
        if len(args) == 3:
            return 0
        print(f"Машина не в сети/указан не правильный ip")


def scan_ports(*args):  # IP, True/False(показывать ли состояние всех портов)
    sock = socket.socket()
    for port in ports:
        try:
            sock.connect((args[0], port))
            print(f"Порт {port} открыт, его роль: {ports[port]}")
        except:
            if len(args) == 2 and (args[1].lower() == "true" or args[1].lower() == "t"):
                print(f"Порт {port} закрыт")


def __scan_ip(first, second, ip, show=False):
    for i in range(first, second + 1):
        cur = ".".join(ip)+"." + str(i)
        response = bool(ping(cur, 1, True))
        if response and show:
            print(f"Машина {ip} в сети\nПроверка её портов:\n\n")
            scan_ports(cur)
        elif response:
            print(f"Машина {cur} в сети")


def scan_network(*args): # Example: 192.168.0.1-255 True        (ip, провести сканирование портов?)
    threads = []
    ip = args[0].split(".")
    lenght = ip.pop(-1).split("-")
    ran = (int(lenght[1]) - int(lenght[0])) // 4
    first = int(lenght[0])
    for i in range(4):
        threads.append(threading.Thread(target=__scan_ip, args=(first + ran * i, first + ran * (i+1)+2, ip)))
        threads[i].start()
    for i in range(4):
        threads[i].join()
    print("\nСканирование закончено")


def __client_exec(client, command):
    try:
        if command == "cd":
            stdin, stdout, stderr = client.exec_command("cd ..")
        else:
            stdin, stdout, stderr = client.exec_command(command)
        data = str(stdout.read() + stderr.read())
        data = list(data)
        data.pop(0)
        data.pop(-1)
        data.pop(0)
        data = "".join(data).split("\\n")
        if command == "pwd":
            return "".join(data)
        else:
            if data != None:
                print(*data, sep="\n")
            else:
                print("\n")
    except:
        print("Произошла ошибка в выполнении команды, закрываю соединение...")
        client.close()
        return


def __manipulations_with_client(client):
    while True:
        dir = __client_exec(client, "pwd")
        command = input(f"{dir}: ")
        if command.lower() == "exit":
            client.close()
            return
        else:
            print(__client_exec(client, command))


def connect(*args):  # 4 аргумента(ip, name, password, port)
    if len(args) == 0:
        print("Функция не может не принимать параметров")
        return
    cur = None
    if len(args) < 4:
        print("Вы указали не все параметры, выполняю поиск по IP в имеющихся машинах")
        for machin in machines:
            if machin["ip"] == args[0]:
                cur = machin
                break
    elif len(args) == 4:
        cur["ip"] = args[0]
        cur["name"] = args[1]
        cur["password"] = args[2]
        cur["port"] = args[3]
    if cur != None:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=cur["ip"], username=cur["name"], password=cur["password"], port=cur["port"])
        __manipulations_with_client(client)


def help(func_name=None):
    if func_name == None:
        for func in functions:
            if funcs_info.get(func) != None:
                print(func, ": ", funcs_info[func], sep="")
        print("\n" * 3)
        return
    print(funcs_info[func_name])


funcs_info = {
    "connect": "Функция для подключения к удалённой машине, аргументы:\n!ip, name, password, port",
    "scanport": "Функция для сканирования активных портов, аргументы:\n!ip, (показывать все порты?)",
    "ping": "Функция для проверки активности конкретной виртуальной машины, аргументы:\n!ip, times",
    "scan": "Функция для сканирования активных машин, аргументы:\n!ip(192.168.0.1-255), (провести сканирование портов?)",
}
functions = {
    "connect": connect,
    "scanport": scan_ports,
    "scannetwork": scan_network,
    "ping": ping,
    "scan": scan_network,
    "help": help,
}


def main():
    while True:
        try:
            command = input("Вводите команду:").split()
            if command[0] == "exit":
                print("Завершение работы...")
                os.system("color 7")
                return
            elif command[0] == "clear":
                os.system("cls")
            else:
                func_name = command[0].lower()
                command.pop(0)
                args = command
                if len(args) == 0:
                    functions[func_name]()
                else:
                    functions[func_name](*args)
        except:
            print("Произошла ошибка")


if __name__ == "__main__":
    os.system("cls")
    os.system("color 2")
    print("""
 __          __  _                            _           _____                      _               ___   _____ 
 \ \        / / | |                          | |         / ____|                    | |             / _ \ | ____|
  \ \  /\  / ___| | ___ ___  _ __ ___   ___  | |_ ___   | |     ___  _ __  ___  ___ | | ___  __   _| | | || |__  
   \ \/  \/ / _ | |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | |    / _ \| '_ \/ __|/ _ \| |/ _ \ \ \ / | | | ||___ \ 
    \  /\  |  __| | (_| (_) | | | | | |  __/ | || (_) | | |___| (_) | | | \__ | (_) | |  __/  \ V /| |_| _ ___) |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \_____\___/|_| |_|___/\___/|_|\___|   \_/  \___(_|____/ 
     \n\n\t\t\t\t\t\t Creator: SaM
    """)
    time.sleep(1.5)
    os.system("cls")
    main()
