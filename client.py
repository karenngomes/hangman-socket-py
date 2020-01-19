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

        if (response == "endgame"):
            client_socket.send(response.encode(encoding='UTF-8'))
            client_socket.close()
            break
        else:
            print(response)

        if ('Agora é a sua vez de jogar!' in response):
            text = input("Digite uma letra: ")
            # tratar texto para pegar só a 1ª letra e que envie como maiuscula
            client_socket.send(text.encode(encoding='UTF-8'))
