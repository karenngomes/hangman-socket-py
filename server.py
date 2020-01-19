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
# receber mais uma flag pra saber o tipo de mensagem pra enviar
def broadcast_message(current_socket, message):
    # renomear clients pra colocar socket do servidor tbm
    for client in clients:
        c = client['server_input']
        if c != current_socket:
            c.sendall(message.encode(encoding='UTF-8'))
        else:
            c.sendall('Agora é a sua vez de jogar!'.encode(encoding='UTF-8'))


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

        if current_client_address == address:
            typed = True

        if (response == "sair"):
            print('Cliente', address, 'se desconectou')
            break
        # print("Mensagem do cliente %s: %s" % (address, response))

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
print('Iniciou o jogo!') # mandar isso para todos

letras_descobertas = []
qtd_erros = 0
dados = json.load(open('dados.json'))

categoria = list(dados)[random.randint(0, len(dados)-1)]

palavra_secreta = dados[categoria][random.randrange(
    0, len(dados[categoria])-1)]

palavra_secreta = palavra_secreta.upper()

print(palavra_secreta)  # tirar isso depois

# mandar isso para todos
print('A categoria é:', categoria.upper(),
      "\nA palavra contém", len(palavra_secreta), "letras")

for j in range(0, len(palavra_secreta)):
    letras_descobertas.append("_")

# mandar isso para todos
print(" ".join(letras_descobertas))

letras_erradas = []
letra_certa = False

for client in cycle(clients):

    text = 'Agora é a vez do ' + str(client['address']) + ' jogar'
    broadcast_message(client['server_input'], text) # mandar de acordo com a flag( ver nome da flag)

    acertou = False

    current_client_address = client['address']
    typed = False

    while typed == False:
        continue

    print('Letra digitada:', letra)
    for i in range(0, len(palavra_secreta)):
        if letra == palavra_secreta[i]:
            letras_descobertas[i] = letra
            letra_certa = True

    if letra_certa == False:
        letras_erradas.append(letra)

        # mandar isso para todos | mudar msg para: "o [client] digitou uma letra errada! Letras erradas.."
        print('Letra errada!\nLetras erradas até agora:',
              ", ".join(letras_erradas))
        qtd_erros += 1

        if qtd_erros == 1:
            print('+----+\n|    |\n|    0\n')
        if qtd_erros == 2:
            print('+----+\n|    |\n|    0\n|    |  \n|    |\n|    |\n')
        if qtd_erros == 3:
            print('+----+\n|    |\n|    0\n|   /|  \n')
        if qtd_erros == 4:
            print('+----+\n|    |\n|    0\n|   /|\ \n')
        if qtd_erros == 5:
            print('+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   /   \n')

        if qtd_erros != 6:
            # mandar isso para todos e mudar mensagem (tirar o você)
            print(qtd_erros, 'letra(s) errada(s). Você tem mais',
                  str(6-qtd_erros), 'tentativas!')
            print(" ".join(letras_descobertas))
        else:
            # mandar isso para todos; personalizar mensagem (?) | flag que diz que jogo acabou
            print(
                '+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   / \ \n|\n=========\n')
            print('6 letras erradas. Fim de jogo! A palavra era:', palavra_secreta)

    else:
        # mandar isso para todos
        print(" ".join(letras_descobertas))

    acertou = True
    letra = ''
    letra_certa = False

    for x in range(0, len(letras_descobertas)):
        if letras_descobertas[x] == "_":
            acertou = False

    if acertou == True:
        text = 'O ' + str(client['address']) + ' ganhou o jogo, parabéns!'
        # flag que diz que jogo acabou
        broadcast_message(client['server_input'], text)
        break


server_socket.close()
