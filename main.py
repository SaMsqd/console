import paramiko

machines = (
    {
        "ip": "192.168.0.90",
        "name":  "root",
        "password": "123456",
        "port": 22,
    },
)

ip = "192.168.0.90"
name = "root"
password = "123456"
port = 22


def connect(*args):     # 4 аргумента(ip, name, password, port)
    if len(args) == 0:
        print("Функция не может не принимать параметров")

    cur = None
    if len(args) != 1 and len(args) < 4:
        print("Вы указали не все параметры, выполняю поиск по IP в имеющихся машинах")
    if len(args) < 4:
        for machin in machines:
            for ips in machin["ip"]:
                if ips == args[0]:
                    cur = machin
    elif len(args) == 4:
        cur["ip"] = args[0]
        cur["name"] = args[1]
        cur["password"] = args[2]
        cur["port"] = args[3]


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=ip, username=name, password=password, port=port)
stdin, stdout, stderr = client.exec_command('help')
data = stdout.read() + stderr.read()
data = str(data)
client.close()
print(data)
