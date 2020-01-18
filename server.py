#!/usr/bin/python3

import socket
import threading
from itertools import cycle

address = ("localhost", 7000)


letra = ''
current_client_address = ''
typed = False

# Send message to all clients
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
print('Iniciou o jogo!!!')

palavra_secreta = ""
categoria = ""
letras_descobertas = []
qts_erros = 0
dados = json.load(open('dados.json'))
categoria = data[item][random.randrange(0, len(data[item]))] #REVISAR

print('A categoria é:' ,categoria)
palavra_secreta = dados[categoria][random.randrange(0, len(dados[categoria]))]

print(letras_descobertas, "\nA palavra contém,", len(palavra_secreta),"letras")
for j in range(0, len(palavraEscolhida)): 
        letras_descobertas.append("_")
        print(letras_descobertas)


for client in cycle(clients):

    text = 'Agora é a vez do ' + str(client['address']) + ' jogar'
    broadcast_message(client['server_input'], text)

    acertou = False

    current_client_address = client['address']
    typed = False

    print('Digite a letra: ')
    while typed == False:
        continue

    for i in range(0, len(palavra_secreta)):
        if letra == palavra_secreta[i]:
            letras_descobertas[i] = letra

        print(letras_descobertas[i])
        
        else
        print('Letra errada!')
        letras_erradas = letra
        qtd_erros += 1
        if qtd_erros == 1
            print('+----+\n|    |\n|    0\n') 
            print(qtd_erros 'letra(s) errada(s). Você tem mais', 6-qtd_erros, 'tentativas!')
        if qtd_erros == 2
            print('+----+\n|    |\n|    0\n|    |  \n|    |\n|    |\n')
            print(qtd_erros 'letra(s) errada(s). Você tem mais', 6-qtd_erros, 'tentativas!')
        if qtd_erros == 3
            print('+----+\n|    |\n|    0\n|   /|  \n')
            print(qtd_erros 'letra(s) errada(s). Você tem mais', 6-qtd_erros, 'tentativas!')
        if qtd_erros == 4
            print('+----+\n|    |\n|    0\n|   /|\ \n')
            print(qtd_erros 'letra(s) errada(s). Você tem mais', 6-qtd_erros, 'tentativas!')
        if qtd_erros == 5
            print('+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   /   \n')
            print(qtd_erros 'letra(s) errada(s). Você tem mais', 6-qtd_erros, 'tentativas!')
        if qtd_erros == 6
            print('+----+\n|    |\n|    0\n|   /|\ \n|    |\n|    |\n|   / \ \n|\n=========\n')
            print(qtd_erros 'letra(s) errada(s). Fim de jogo! A palavra era:', palavra_secreta)

    acertou = True
    letra = ''

    for x in range(0, len(letras_descobertas)):
        if letras_descobertas[x] == "-":
            acertou = False

    if acertou == True:
        text = 'O ' + str(client['address']) + ' ganhou o jogo, parabéns!'
        broadcast_message(client['server_input'], text)
        break


server_socket.close()
