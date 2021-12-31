import socket, threading

import time
from selenium.webdriver.firefox.options import Options


options = Options()
options.headless = False

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.first_pocket = self.csocket.recv(4096).decode()
        self.username = self.first_pocket[5::]
        print ("Новое подключение: ", clientAddress)

    userslist = {'karriiiii': ['xxx.xxx.xxx.xxx', 'xxx.xxx.xxx.xxx', 'xxx.xxx.xxx.xxx'], 'second_user': ['xxx.xxx.xxx.xxx']}

    def checker(self):
        if self.first_pocket[0:5] == 'check':

            if self.first_pocket[5::] not in self.userslist.keys():
                self.csocket.sendall(bytes('Connection closed! Wrong username!', "UTF-8"))
                print('Попытка подключения с IP: {0} на несуществующий ник({1})'.format(clientAddress, self.first_pocket))
                return False

            elif self.first_pocket[5::] in self.userslist.keys() and clientAddress[0] not in self.userslist.get(self.first_pocket[5::]):
                self.csocket.sendall(bytes('Connection closed! Unknown IP address!', 'UTF-8'))
                print('Попытка подключения с IP: {0} на ник: {1}'.format(clientAddress, self.first_pocket[5::]))
                return False

            else:
                self.csocket.sendall(bytes('Connection successufully done!', "UTF-8"))
                print ("Подключение с IP: ", clientAddress, "Юзер: ", self.first_pocket[5::])
                return True

        else:
            return False

    def run(self):
        msg = ''

        try:
            while True:
                data = self.csocket.recv(4096)
                msg = data.decode()
                print(self.username, ':', msg)

                if msg == 'leave session':
                    print("Отключение", self.username)
                    break

        except ConnectionResetError:
            print('Соединение с {0}{1} было разорвано.'.format(self.username, clientAddress))   

        print ("Клиент ", clientAddress, self.username, " покинул нас...")


LOCALHOST = "xxx.xxx.xxx.xxx"
PORT = 1337

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((LOCALHOST, PORT))
print("Сервер запущен!")

while True:
    server.listen(3)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    checker = newthread.checker()
    if checker == True:
        newthread.start()
    