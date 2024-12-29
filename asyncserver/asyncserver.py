import socket
import json
import random
import sympy
from sympy import isprime
import math
import sys
import asyncio
import aioconsole

#подбор ключей шифрования
while True:
    while True:
        qs = random.randint(100, 1000)
        if isprime(qs):
            break

    while True:
        ps = random.randint(100, 1000)
        if isprime(ps) and qs != ps :
            break

    ns = ps * qs

    while True:
        es = random.randint(100, 1000)
        if isprime(es) and math.gcd(es, (ps - 1) * (qs - 1)) == 1:
            break

    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    _, ds, _ = extended_gcd(es, (ps - 1) * (qs - 1))
    ds = ds % ((ps - 1) * (qs - 1))  # Обеспечиваем, чтобы d было положительным

    if ds > 60000:
        continue
    else:
        break

publickey = [ds, ns]


def syfr(string):
    string = list(string)
    for i in range(0, len(string)):
        string[i] = ord(string[i])
        string[i] = (string[i] ** es) % ns
    return string


def desyfr(string, dc, nc):
    for i in range(0, len(string)):
        string[i] = (string[i] ** dc) % nc
        string[i] = chr(string[i])
    string = ''.join(num for num in string)
    return string


def clear_input():
    # Перемещаем курсор в начало строки и очищаем её
    sys.stdout.write("\033[F\033[K")  # Перемещение вверх и очистка
    sys.stdout.flush()


# создаем TCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ('0.0.0.0', 10006)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen(1)

async def send(connection, client_address, sock):
    while True:
        try:
            while True:
                #servdata = await aioconsole.ainput('Вы: ')
                #servdata = input('Вы: ')
                servdata = await asyncio.to_thread(input, 'Вы: ')
                servdata = syfr(servdata)
                servdata = json.dumps(servdata).encode('utf-8')
                connection.sendall(json.dumps(publickey).encode('utf-8'))
                connection.sendall(servdata)
        except Exception as e:
            if str(e) == '[WinError 10054] Удаленный хост принудительно разорвал существующее подключение':
                print('Клиент отключился')
            else:
                print(f'Ой! возникла ошибка: {e}')
                break
        finally:
            print('Закрытие соединения...')
            connection.close()
            break


async def recieve(connection, client_address, sock):
    while True:
        try:
            mykey = await asyncio.to_thread(connection.recv, 128)
            mykey = json.loads(mykey.decode('utf-8'))
            if mykey:
                data = json.loads(connection.recv(1024).decode('utf-8'))
                data = desyfr(data, mykey[0], mykey[1])
                print('Клиент:', data)
        finally:
            a = 0

    

async def main():
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    print('Подключено к:', client_address)

    await asyncio.gather(
        send(connection, client_address, sock),
        recieve(connection, client_address, sock)
    )
asyncio.run(main())
