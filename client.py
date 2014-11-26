#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

if len(sys.argv) != 3:
    print "Usage: python client.py method receiver@IP:SIPport"
    sys.exit()

# Dirección IP del servidor.
METODO = ['INVITE', 'ACK', 'BYE']
METODO = sys.argv[1]
arg1 = sys.argv[2].split("@")
LOGIN = arg1[0]
arg2 = arg1[1].split(":")
IP = arg2[0]
PORT = int(arg2[1])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

LINE = ""
#creamos LINE segun el tipo del metodo que pasamos como argumento
if METODO == "INVITE":
    LINE = "INVITE sip:" + LOGIN + "@" + IP + " SIP/2.0" + '\r\n'
elif METODO == "BYE":
    LINE = "BYE sip:" + LOGIN + "@" + IP + " SIP/2.0" + '\r\n'

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')

try:
    data = my_socket.recv(1024)
    print 'Recibido -- ', data
except socket.error:
    sys.exit("Error: No server listening at " + IP + " port " + str(PORT))

if METODO == "INVITE":
    #Cambio comprobación del mensaje recibido del servidor por una mejor
    processed_data = data.split('\r\n\r\n')
    if processed_data[0] == "SIP/2.0 100 Trying" and\
    processed_data[1] == "SIP/2.0 180 Ringing" and\
    processed_data[2] == "SIP/2.0 200 OK":
        LINE = "ACK sip:" + LOGIN + "@" + IP + " SIP/2.0"
        print "Enviando: " + LINE
        my_socket.send(LINE + '\r\n\r\n')
        data = my_socket.recv(1024)
        print 'Recibido -- ', data

print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
