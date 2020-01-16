#!/usr/bin/python3

import socket

address = ("localhost", 7000)

# Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

# Echo
while True:
    response = client_socket.recv(1024)

    if (len(response) != 0):
        response = response.decode()
        print(response)

        if(response == 'Agora é a sua vez de jogar!'):
            text = input("Digite uma letra: ")

            client_socket.send(text.encode(encoding='UTF-8'))
            if (text == "sair"):
                client_socket.close()
                break
