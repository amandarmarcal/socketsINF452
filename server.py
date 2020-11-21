import socket
import threading

HOST = ''
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

origin = (HOST, PORT)
udp.bind(origin)

tcp.bind(origin)
tcp.listen(1)

usuariosPorNome = {}
usuariosPorEndereco = {} 
arquivo = None
nomeArquivo = ''

def conexaoUDP():
    while True:
        msg, cliente = udp.recvfrom(1024)

        msg = msg.decode()
        msgList = msg.split(':')


        if msgList[0] == 'USER':
            info1 = 'INFO:' + msgList[1] + ' entrou'
            for user in usuariosPorNome:
                udp.sendto(info1.encode(), usuariosPorNome[user])
            usuariosPorNome[msgList[1]] = cliente 
            usuariosPorEndereco[cliente] = msgList[1] 

            
        elif msgList[0] == 'MSG':
            info2 = 'MSG:' + usuariosPorEndereco[cliente] + ':' + msgList[1]
            for user in usuariosPorEndereco:
                if(user != cliente):
                    udp.sendto(info2.encode(), user)


        elif msgList[0] == 'LIST':  
            s = ', '
            listC = []
            for user in usuariosPorNome:
                listC.append(user)
            listM = s.join(listC)
            
            info3 = 'INFO:' + 'Clientes conectados:' + listM
            udp.sendto(info3.encode(), cliente)
            
        elif msgList[0] == 'GET':
            print('GET')    

        elif msgList[0] == 'BYE':
            nome2 = usuariosPorEndereco.pop(cliente)
            usuariosPorNome.pop(nome2)

            info4 = 'INFO:' + nome2 + ' saiu'

            udp.sendto('INFO:desconectado'.encode(), cliente)

            for user in usuariosPorNome:
                udp.sendto(info4.encode(), usuariosPorNome[user])

def conexaoTCP():
    while True:
        try:
            con, clienteTCP = tcp.accept()       
            msgTCP = con.recv(1024).decode()
            con.send('ok'.encode())
            msgListTCP = msgTCP.split(':')

            if msgListTCP[0] == 'FILE':
                nomeCliente = con.recv(1024).decode()
                con.send('ok'.encode())
                #nomeCliente = nomeCliente[:-1]
                nomeArquivo = msgListTCP[1]

                nomeCache = 'cache' + nomeArquivo
                arquivo = open(nomeCache, 'w')
                while True:
                    dados = con.recv(1024).decode()
                    if not dados:
                        break
                    arquivo.write(dados)
                arquivo.close()
                con.close()

                info5 = 'INFO:' + nomeCliente + ' enviou ' + msgListTCP[1]
                for user in usuariosPorNome:
                    if(user != nomeCliente):
                        udp.sendto(info5.encode(), usuariosPorNome[user])

            elif msgListTCP[0] == 'GET':
                con.send(''.encode())

                print(msgTCP)
                print(nomeArquivo)
                
                if msgListTCP[1] == nomeArquivo:
                    con.send('ok'.encode())
                    nomeCache = 'cache' + nomeArquivo
                    print(nomeCache)
                    arquivo = open(nomeCache, 'r')
                    for line in arquivo.readlines():
                        con.send(line.encode())
                    con.close()
                else:    
                    con.send('error'.encode())
                    con.close()
        except Exception as ex:
                print (ex)


t1 = threading.Thread(target= conexaoUDP)
t1.start()
t2 = threading.Thread(target= conexaoTCP)
t2.start()

