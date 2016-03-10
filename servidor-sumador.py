#!/usr/bin/python
# -*- coding: utf-8 -*-
#Sergio Carro Albarran

import socket
import random


# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)
numero1 = None
numero2 = None

try:
        while True:
                print 'Waiting for connections'
                (recvSocket, address) = mySocket.accept()
                print 'Request received:'
                dato = recvSocket.recv(1024)
                print dato
                html = '<html><body><h1>'
                htmlend = '</h1></body></html>'
                try:
                        numero = int(dato.split()[1][1:])
                except ValueError:
                        print 'Introduce un numero correcto'
                        html += 'Introduce un numero correcto'
                        html += 'un numero correcto'
                        html += htmlend
                        recvSocket.send("HTTP/1.1 400 Bad request\r\n\r\n" +
                                html + "\r\n")
                        recvSocket.close()
                        continue
                if numero1 is None:
                        numero1 = numero
                        html += 'Primer numero: '
                        html += str(numero1)
                        html += '<p>Introduce el segundo</p>'
                        html += htmlend
                        recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                html + "\r\n")
                else:
                        numero2 = numero
                        suma = numero1 + numero2
                        html += 'Primero numero: ' + str(numero1)
                        html += '<br/>Segundo numero: ' + str(numero2)
                        html += '<br/><em>Suma:</em> ' + str(suma)
                        html += htmlend
                        recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
                                html + "\r\n")
                        numero1 = None
                        numero2 = None
                recvSocket.close()

except KeyboardInterrupt:
    print "Servidor cerrado"
    mySocket.close()
