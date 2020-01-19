#!/usr/bin/python3

import socket
import threading
from itertools import cycle
import json
import random

address = ("localhost", 7000)


letter = ''
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
    global letter
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

        letter = response

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

discovered_letters = []
number_of_errors = 0

# Gets word from json file
categories = json.load(open('categories.json'))

category = list(categories)[random.randint(0, len(categories)-1)]

secret_word = categories[category][random.randrange(
    0, len(categories[category])-1)]
secret_word = secret_word.upper()

print('A palavra é:', secret_word)

message = 'A categoria é: ' + category.upper() + '\nA palavra contém ' + \
    str(len(secret_word)) + ' letras\n'
broadcast_message(message=message, send_to_all=True)

for j in range(0, len(secret_word)):
    discovered_letters.append("_")

text = " ".join(discovered_letters)
broadcast_message(message=text, send_to_all=True)

wrong_letters = []
right_letter = False

for client in cycle(clients):

    text = 'Agora é a vez do ' + str(client['address']) + ' jogar'
    broadcast_message(current_socket=client['server_input'], message=text)

    is_correct = False

    current_client_address = client['address']
    typed = False

    while typed == False:
        continue

    text = 'Letra digitada pelo cliente ' + \
        str(client['address']) + ': ' + letter
    broadcast_message(message=text, send_to_all=True)

    for i in range(0, len(secret_word)):
        if letter == secret_word[i]:
            discovered_letters[i] = letter
            right_letter = True

    if right_letter == False:
        wrong_letters.append(letter)

        text = 'O cliente ' + \
            str(client['address']) + \
            ' digitou uma letra errada! Letras erradas até agora: ' + \
            ", ".join(wrong_letters)
        broadcast_message(message=text, send_to_all=True)

        number_of_errors += 1
        hangman = ''

        if number_of_errors == 1:
            hangman = '+----+\n|    |\n|    0\n'
        if number_of_errors == 2:
            hangman = '+----+\n|    |\n|    0\n|    |  \n|    |\n|    |\n'
        if number_of_errors == 3:
            hangman = '+----+\n|    |\n|    0\n|   /|  \n'
        if number_of_errors == 4:
            hangman = '+----+\n|    |\n|    0\n|   /|\ \n'
        if number_of_errors == 5:
            hangman = '+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   /   \n'
        if number_of_errors == 6:
            hangman = '+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   / \ \n|\n=========\n'

        broadcast_message(message=hangman, send_to_all=True)

        if number_of_errors != 6:
            text = (" ".join(discovered_letters)) + '\n' + str(number_of_errors) + ' letra(s) errada(s). Ainda há ' + \
                str(6-number_of_errors) + ' tentativas!'

            broadcast_message(message=text, send_to_all=True)
        else:
            text = '6 letras erradas. Fim de jogo! A palavra era: ' + secret_word

            broadcast_message(message=text, send_to_all=True)
            broadcast_message(message='endgame', send_to_all=True)

            server_socket.close()

    else:
        text = " ".join(discovered_letters)
        broadcast_message(message=text, send_to_all=True)

    is_correct = True
    letter = ''
    right_letter = False

    for x in range(0, len(discovered_letters)):
        if discovered_letters[x] == "_":
            is_correct = False

    if is_correct == True:
        text = 'O ' + str(client['address']) + ' ganhou o jogo, parabéns!'
        broadcast_message(message=text, send_to_all=True)

        broadcast_message(message='endgame', send_to_all=True)
        break


server_socket.close()
