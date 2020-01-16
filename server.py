#!/usr/bin/python3

import socket
import threading
import queue
from itertools import cycle

address = ("localhost", 4000)


letra = ''
current_client_address = '' 
digitou = False

def sendMessagesFromServer(server_socket):
    while True:
        msg = input("Msg> ")
        print(msg)
        try:
            server_socket.sendall(msg.encode("utf-8"))
        except socket.error:
            print('deu erro')
            break
        if msg.lower() == "fechar":
            server_socket.close()


# Function that gets called instead of run() method
def connect(server_input, address, clients_queue):
    print('Conectado por', address)
    global letra
    global current_client_address
    global digitou

    while True:
        # print(threading.currentThread().getName())
        response = server_input.recv(1024)
        if (len(response) == 0):
            print('Falha na conexao com', address)
            break
        response = response.decode()

        if current_client_address == address:
            digitou = True 
        # else:
        #     digitou = False

        if (response == "sair"):
            print('Cliente', address, 'se desconectou')
            break
        print("Mensagem do cliente %s: %s" % (address, response))
        letra = response

        print('response', response)
        print('letrah', letra)
    server_input.close()


# Create sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect sockets
server_socket.bind(address)
server_socket.listen(1)

print('Esperando clientes se conectarem\n')

num_threads = 3

clients = []

clients_queue = queue.Queue(maxsize=0)


for i in range(num_threads):
    server_input, address = server_socket.accept()

    client = {}
    client['address'] = address
    client['thread'] = 'Thread-' + str(i+1)
    client['server_input'] = server_input
    clients.append(client)
    # print('clients:', clients)

    # Create and start a new thread
    new_thread = threading.Thread(
        target=connect, args=(server_input, address, clients_queue), daemon=True)
    new_thread.start()

# sendMessages = threading.Thread(
#     target=sendMessagesFromServer, args=(server_socket,))
# sendMessages.start()

# Start the game
print('iniciou o jogo!!!')
your_turn = True

palavra_secreta = ["M", "A", "C", "E", "I", "O"]
letras_descobertas = []

for i in range(0, len(palavra_secreta)):
    letras_descobertas.append("-")

for client in cycle(clients):
    text = 'Agora é a vez do' + \
        str(client['address']) + \
        'jogar. Ele tem 1 minuto para chutar uma letra ou a vez dele irá passar para o próximo'

    your_turn = True
    acertou = False

    current_client_address = client['address']
    digitou = False

    # global digitou
    # global letra
    print('Digite a letra: ')
    while digitou == False:
        # print('letraaa', letra)
        # auxiliar = input('Digite')
        # print(auxiliar)
        # continue
        a = 3
    print(letra)

    # letra = str(input("Digite a letra: "))
    for i in range(0, len(palavra_secreta)):
        if letra == palavra_secreta[i]:
            letras_descobertas[i] = letra

        print(letras_descobertas[i])
    acertou = True
    letra = ''

    for x in range(0, len(letras_descobertas)):
        if letras_descobertas[x] == "-":
            acertou = False

    if acertou == True:
        print('O %s ganhou o jogo, parabéns!', client['address'])
        break


server_socket.close()
