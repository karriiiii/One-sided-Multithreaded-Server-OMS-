import socket
from threading import Thread
import threading

#SERVER = "xxx.xxx.xxx.xxx"
PORT = 1337

SERVER = input('IP address of server: ')
username = str(input('Введите своё имя: '))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes('check{0}'.format(username), 'UTF-8'))
first_answer = client.recv(1024)

print('От сервера: ', first_answer.decode())

def task():
    while True:
        in_data = client.recv(4096)
        print("От сервера :" ,in_data.decode())

def task2():
    while True:
        out_data = input('Я: ')
        client.sendall(bytes(out_data,'UTF-8'))
        print("(Отправлено)")
        if out_data == 'leave_session':
            client.close()

t1 = Thread(target=task2)
t2 = Thread(target=task)

t1.start()
t2.start()

t1.join()
t2.join()