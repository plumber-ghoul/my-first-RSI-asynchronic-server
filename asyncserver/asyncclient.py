import socket
import json
import random
from sympy import isprime
import math
import asyncio
import aioconsole

while True:
    while True:
        qc = random.randint(100, 1000)
        if isprime(qc):
            break

    while True:
        pc = random.randint(100, 1000)
        if isprime(pc) and qc != pc :
            break

    nc = pc * qc

    while True:
        ec = random.randint(100, 1000)
        if isprime(ec) and math.gcd(ec, (pc - 1) * (qc - 1)) == 1:
            break

    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    _, dc, _ = extended_gcd(ec, (pc - 1) * (qc - 1))
    dc = dc % ((pc - 1) * (qc - 1))  # Обеспечиваем, чтобы d было положительным

    if dc > 60000:
        continue
    else:
        break

publickey = [dc, nc]

def syfr(string):
    string = list(string)
    for i in range(0, len(string)):
        string[i] = ord(string[i])
        string[i] = (string[i] ** ec) % nc
    return string

def desyfr(string, ds, ns):
    string = list(string)
    for i in range(0, len(string)):
        string[i] = (string[i] ** ds) % ns
        string[i] = chr(string[i])
    string = ''.join(num for num in string)
    return string

async def send(sock):
    while True:
        try:
            # Отправка данных
            mess = await asyncio.to_thread(input, 'Вы: ')
            if(mess == '/STOP'):
                break
            mess = syfr(mess)
            sock.sendall(json.dumps(publickey).encode('utf-8'))
            sock.sendall(json.dumps(mess).encode('utf-8'))
        except Exception as e:
            print(f'ошибка: {e}')
            break

async def recieve(sock):
    while True:
        try:
            mykey = await asyncio.to_thread(sock.recv, 128)
            mykey = json.loads(mykey.decode('utf-8'))
            if mykey:
                raw_data = await asyncio.to_thread(sock.recv, 1024)
                data = json.loads(raw_data.decode('utf-8'))
                data = desyfr(data, mykey[0], mykey[1])
                print(f'Сервер: {data}')
        finally:
            a = 0



# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаем сокет к порту, через который прослушивается сервер
server_address = ('127.0.0.1', 10006)
print('Подключено к {} порт {}'.format(*server_address))
sock.connect(server_address)



async def main():
    await asyncio.gather(
        send(sock),
        recieve(sock)
    )


asyncio.run(main())

sock.close()
end = input('program ended')