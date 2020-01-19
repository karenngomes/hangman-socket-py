#!/usr/bin/python3

import socket
import threading
from itertools import cycle
import json
import random

address = ("localhost", 7000)


letra = ''
current_client_address = ''
typed = False


# Send message to all clients
def broadcast_message(message, current_socket=None, send_to_all=False):
    if message != 'endgame':
        print(message)

    for client in clients:
        c = client['server_input']
        if send_to_all:
            c.sendall(message.encode(encoding='UTF-8'))
        else:
            if c != current_socket:
                c.sendall(message.encode(encoding='UTF-8'))
            else:
                c.sendall('Agora é a sua vez de jogar!'.encode(
                    encoding='UTF-8'))


# Function that gets called instead of run() method
def connect(server_input, address):
    print('Conectado por', address)
    global letra
    global current_client_address
    global typed

    while True:
        response = server_input.recv(1024)
        if (len(response) == 0):
            print('Falha na conexao com', address)
            break
        response = response.decode()

        if (response == "endgame"):
            break

        if current_client_address == address:
            typed = True

        letra = response

    server_input.close()


# Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect sockets
server_socket.bind(address)
server_socket.listen(1)

print('Esperando clientes se conectarem\n')

num_threads = 3

clients = []

for i in range(num_threads):
    server_input, address = server_socket.accept()

    client = {}
    client['address'] = address
    client['server_input'] = server_input
    clients.append(client)

    # Create and start a new thread
    new_thread = threading.Thread(
        target=connect, args=(server_input, address), daemon=True)
    new_thread.start()

# Start the game
message = 'Iniciou o jogo!'
broadcast_message(message=message, send_to_all=True)

letras_descobertas = []
qtd_erros = 0
dados = json.load(open('dados.json'))

categoria = list(dados)[random.randint(0, len(dados)-1)]

palavra_secreta = dados[categoria][random.randrange(
    0, len(dados[categoria])-1)]

palavra_secreta = palavra_secreta.upper()

print('A palavra é:', palavra_secreta)

message = 'A categoria é: ' + categoria.upper() + '\nA palavra contém ' + \
    str(len(palavra_secreta)) + ' letras\n'
broadcast_message(message=message, send_to_all=True)

for j in range(0, len(palavra_secreta)):
    letras_descobertas.append("_")

text = " ".join(letras_descobertas)
broadcast_message(message=text, send_to_all=True)

letras_erradas = []
letra_certa = False

for client in cycle(clients):

    text = 'Agora é a vez do ' + str(client['address']) + ' jogar'
    broadcast_message(current_socket=client['server_input'], message=text)

    acertou = False

    current_client_address = client['address']
    typed = False

    while typed == False:
        continue

    # print('Letra digitada:', letra)
    text = 'Letra digitada pelo cliente ' + \
        str(client['address']) + ': ' + letra
    broadcast_message(message=text, send_to_all=True)

    for i in range(0, len(palavra_secreta)):
        if letra == palavra_secreta[i]:
            letras_descobertas[i] = letra
            letra_certa = True

    if letra_certa == False:
        letras_erradas.append(letra)

        text = 'O cliente ' + \
            str(client['address']) + \
            ' digitou uma letra errada! Letras erradas até agora: ' + \
            ", ".join(letras_erradas)
        broadcast_message(message=text, send_to_all=True)

        qtd_erros += 1
        hangman = ''

        if qtd_erros == 1:
            hangman = '+----+\n|    |\n|    0\n'
        if qtd_erros == 2:
            hangman = '+----+\n|    |\n|    0\n|    |  \n|    |\n|    |\n'
        if qtd_erros == 3:
            hangman = '+----+\n|    |\n|    0\n|   /|  \n'
        if qtd_erros == 4:
            hangman = '+----+\n|    |\n|    0\n|   /|\ \n'
        if qtd_erros == 5:
            hangman = '+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   /   \n'
        if qtd_erros == 6:
            hangman = '+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   / \ \n|\n=========\n'

        broadcast_message(message=hangman, send_to_all=True)

        if qtd_erros != 6:
            text = (" ".join(letras_descobertas)) + '\n' + str(qtd_erros) + ' letra(s) errada(s). Ainda há ' + \
                str(6-qtd_erros) + ' tentativas!'

            broadcast_message(message=text, send_to_all=True)
        else:
            text = '6 letras erradas. Fim de jogo! A palavra era: ' + palavra_secreta

            broadcast_message(message=text, send_to_all=True)
            broadcast_message(message='endgame', send_to_all=True)

            server_socket.close()

    else:
        text = " ".join(letras_descobertas)
        broadcast_message(message=text, send_to_all=True)

    acertou = True
    letra = ''
    letra_certa = False

    for x in range(0, len(letras_descobertas)):
        if letras_descobertas[x] == "_":
            acertou = False

    if acertou == True:
        text = 'O ' + str(client['address']) + ' ganhou o jogo, parabéns!'
        broadcast_message(message=text, send_to_all=True)

        broadcast_message(message='endgame', send_to_all=True)
        break


server_socket.close()
