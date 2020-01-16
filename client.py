#!/usr/bin/python3

import socket

address = ("localhost", 7000)

# Create sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

# Echo
while True:
    text = input("Informe texto ou digite 'sair' para desconectar: ")
    client_socket.send(text.encode(encoding='UTF-8'))
    if (text == "sair"):
        client_socket.close()
        break
