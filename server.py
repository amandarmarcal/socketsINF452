import socket

HOST = 'localhost'
PORT = 20000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
origin = (HOST, PORT)
udp.bind(origin)
usuariosPorNome = {}
usuariosPorEndereco = {} 

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
        info3 = 'INFO:' + listM
        udp.sendto(info3.encode(), cliente)

    elif msgList[0] == 'FILE':
        print('FILE')

    elif msgList[0] == 'GET':
        print('GET')    

    elif msgList[0] == 'BYE':
        nome2 = usuariosPorEndereco.pop(cliente)
        usuariosPorNome.pop(nome2)

        info4 = 'INFO:' + nome2 + ' saiu'

        udp.sendto('INFO:desconectado'.encode(), cliente)

        for user in usuariosPorNome:
            udp.sendto(info4.encode(), usuariosPorNome[user])


udp.close()