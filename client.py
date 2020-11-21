
import socket
import threading

HOST = 'localhost' 
PORT = 20000
destiny = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

conectado = True
nome = ''

def entradaDados(conectado):
    while conectado:
        entrada = input()
        entradaList = entrada.split()

        if entradaList[0] == '/bye':
            udp.sendto('BYE'.encode(), destiny)
            conectado = False
            udp.close()
            return

        elif entradaList[0] == '/list':
            udp.sendto('LIST'.encode(), destiny)
            
        elif entradaList[0] == '/file':     
            dados = open(entradaList[1], 'r')
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(destiny)
            fileMsg = 'FILE:' + entradaList[1] 
            tcp.send(fileMsg.encode())
            tcp.recv(1024)
            tcp.send(nome.encode())
            tcp.recv(1024)
            for line in dados.readlines():
                tcp.send(line.encode())
            tcp.close()

        elif entradaList[0] == '/get':
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(destiny)
            getMsg = 'GET:' + entradaList[1]
            tcp.send(getMsg.encode())
            tcp.recv(1024).decode()
            ack = tcp.recv(1024).decode()
            
            nomeArquivo = 'client' + entradaList[1]
            if ack != 'error':
                arquivo = open(nomeArquivo, 'w')
                while True:
                    dados = tcp.recv(1024).decode()
                    if not dados:
                        break
                    arquivo.write(dados)
                tcp.close()
            else:
                print('Arquivo não disponível!')
                tcp.close()

        else:
            info1 = 'MSG:' + entrada 
            udp.sendto(info1.encode(), destiny)


def escutaServer(conectado):
    while conectado:
        msg, host = udp.recvfrom(1024) 
        
        if msg.decode() == 'INFO:desconectado':
            break

        msg = msg.decode()
        msgList = msg.split(':')

        if msgList[0] == 'INFO':
        
            if msgList[1] == 'Clientes conectados':
                print(msgList[1] + ':\n' + msgList[2])
            else:
                print(msgList[1])

        elif msgList[0] == 'MSG':
            print(msgList[1] + ' disse: ' + msgList[2])
            

nome = input("Nome de usuario:")

usuario = 'USER:' + nome
udp.sendto(usuario.encode(), destiny)

t1 = threading.Thread(target=entradaDados, args=(conectado,))
t1.start()
t2 = threading.Thread(target=escutaServer, args=(conectado,))
t2.start()






