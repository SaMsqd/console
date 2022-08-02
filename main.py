import paramiko, time

machines = (
    {
        "ip": "192.168.0.90",
        "name": "root",
        "password": "123456",
        "port": 22,
    },
)


def __manipulations_with_client(client):
    while True:
        command = input("Введите команду(вы подключены к машине): ")
        if command.lower() == "exit":
            client.close()
            return None
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
                return None


def connect(*args):  # 4 аргумента(ip, name, password, port)
    if len(args) == 0:
        print("Функция не может не принимать параметров")
        return None
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
}


def main():
    while True:
        try:
            command = input("Вводите команду:").split()
            if command[0] == "exit":
                print("Завершение работы...")
                return None
            func_name = command[0].lower()
            command.pop(0)
            args = " ".join(command)
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
