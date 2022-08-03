import paramiko, time, socket


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


def scan_ports(*args):
    sock = socket.socket()
    for port in ports:
        try:
            sock.connect((args[0], port))
            print(f"Порт {port} открыт, его роль: {ports[port]}")
        except:
            if len(args) == 2 and (args[1].lower() == "true" or args[1].lower() == "t"):
                print(f"Порт {port} закрыт")



def scan_network(scan_port=False):
    pass


def __manipulations_with_client(client):
    while True:
        command = input("Введите команду(вы подключены к машине): ")
        if command.lower() == "exit":
            client.close()
            return
        else:
            try:
                stdin, stdout, stderr = client.exec_command(command)
                data = str(stdout.read() + stderr.read())
                data = list(data)
                data.pop(0)
                data.pop(-1)
                data.pop(0)
                data = "".join(data).split("\\n")
                print(*data, sep="\n")
            except:
                print("Произошла ошибка в выполнении команды, закрываю соединение...")
                client.close()
                return


def connect(*args):  # 4 аргумента(ip, name, password, port)
    if len(args) == 0:
        print("Функция не может не принимать параметров")
        return
    cur = None
    if len(args) != 1 and len(args) < 4:
        print("Вы указали не все параметры, выполняю поиск по IP в имеющихся машинах")
    if len(args) < 4:
        for machin in machines:
            if machin["ip"] == args[0]:
                cur = machin
    elif len(args) == 4:
        cur["ip"] = args[0]
        cur["name"] = args[1]
        cur["password"] = args[2]
        cur["port"] = args[3]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=cur["ip"], username=cur["name"], password=cur["password"], port=cur["port"])
    __manipulations_with_client(client)


functions = {
    "connect": connect,
    "scanport": scan_ports,
    "scannetwork": scan_network,
}


def main():
    while True:
        try:
            command = input("Вводите команду:").split()
            if command[0] == "exit":
                print("Завершение работы...")
                return
            func_name = command[0].lower()
            command.pop(0)
            args = command
            if len(args) == 0:
                functions[func_name]()
            else:
                functions[func_name](args)
        except:
            print("Произошла ошибка")


if __name__ == "__main__":
    print("-----    WELCOME TO CONSOLE v0.1    -----")
    time.sleep(1)
    print("\n" * 10)
    main()
