import socket
import threading

HOST = 'localhost' 
PORT = 20000
destiny = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

conectado = True

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
            continue

        elif entradaList[0] == '/get':
            continue
        else:
            info1 = 'MSG:' + entrada 
            udp.sendto(info1.encode(), destiny)


def escutaServer(conectado):
    while conectado:
        msg, host = udp.recvfrom(1024)
        if msg.decode() == 'INFO:desconectado':
            break
        print(msg.decode())
        



nome = input("Nome de usuario:")

usuario = 'USER:' + nome
udp.sendto(usuario.encode(), destiny)

t1 = threading.Thread(target=entradaDados, args=(conectado,))
t1.start()
t2 = threading.Thread(target=escutaServer, args=(conectado,))
t2.start()






