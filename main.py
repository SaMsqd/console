# TODO: сделать нормальное управление каталогами удалённой машины(paramiko, разобраться)
import paramiko, time, socket, os, subprocess


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
def ping(host="8.8.8.8"):
    args = "ping " + "-n 1 " + host
    con_out = subprocess.check_output(args, shell=True).decode('cp866')
    print(str(con_out))


def scan_ports(*args):  # IP
    os.system("cls")
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


functions = {
    "connect": connect,
    "scanport": scan_ports,
    "scannetwork": scan_network,
    "ping": ping,
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
    os.system("color 2")
    print("-----    WELCOME TO CONSOLE v0.1    -----")
    time.sleep(1)
    os.system("cls")
    main()
