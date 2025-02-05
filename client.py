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

        if ('endgame' in response):
            client_socket.send(response.encode(encoding='UTF-8'))
            client_socket.close()
            break
        else:
            print(response)

        if ('Agora é a sua vez de jogar!' in response):
            text = input(
                "Digite uma letra (se for digitada mais de uma, só a primeira será considerada): ")[0]
            text = text.upper()

            client_socket.send(text.encode(encoding='UTF-8'))
