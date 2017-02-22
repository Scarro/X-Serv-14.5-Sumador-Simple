#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Sergio Carro Albarrán

import socket
import random


# Create a TCP object socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1234))

# Queue a maximun of 5 TCP conection request

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
# (in an almost infinite loop; the loop can be stopped with Ctrl+C)
sumando1 = None
sumando2 = None
start = '<html><body><h1>'
end = '</h1></body></html>\r\n'

def procesarSuma(numero):
    global sumando1
    global sumando2
    if sumando1 is None:
        sumando1 = numero
        html = start + 'Primer numero: ' + str(sumando1)
        html += '</br>Introduce el segundo' + end
    else:
        sumando2 = numero
        suma = sumando1 + sumando2
        html = start + 'Primer numero: ' + str(sumando1)
        html += '<br/>Segundo numero: ' + str(sumando2)
        html += '<br/><em>Suma:</em> ' + str(suma) + end
        sumando1 = None
        sumando2 = None
    return html

while True:
    try:
        print('Waiting for connections...')
        (recvSocket, address) = mySocket.accept()
        print('Request received:')
        dato = recvSocket.recv(1024)
        print(dato)
        query = dato.split()[1][1:];
        if query.decode('UTF-8') == 'favicon.ico':
            # No pongo icono al sumador
            recvSocket.send(bytes('HTTP/1.1 404 Not Found\r\n\r\n','utf-8'))
            recvSocket.close()
            continue
        else:
            try:
                numero = int(query)            
            except ValueError:
                html = start + 'Introduce un número correcto'
                html += end
                recvSocket.send(bytes('HTTP/1.1 400 Bad Request\r\n\r\n' +
                    html, 'utf-8'))
                recvSocket.close()
                continue

            html = procesarSuma(numero)
            print(html)
            recvSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n' + 
                html, 'utf-8'))
            recvSocket.close()

    except KeyboardInterrupt:
        break;

mySocket.close()
print("Closed binded socket")
