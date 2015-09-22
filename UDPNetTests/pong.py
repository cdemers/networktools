# PONG!

import socket
import time

UDP_PORT = 5005
SIZE = 1500

print "UDP port: '%s'" % UDP_PORT


def new_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def open_server_sock(sock, port):
    sock.bind(('0.0.0.0', port))

def send_raw_packet(sock, ip_port, payload):
    sock.sendto(payload, ip_port )

socket = new_socket()
open_server_sock(socket, UDP_PORT)

exchange_counter = 0

while True:

    print "[%i] Waiting for Ping..." % exchange_counter
    data, ip_port = socket.recvfrom(32534)

    if data[0:4] == "PING":
        print "Received Ping (%i bytes)!" % len(data)
    else:
        raise Exception("Error: '%s'" % data)

    print "Sending Pong!"
    send_raw_packet(socket, ip_port, "PONG".ljust(SIZE, "X"))

    exchange_counter += 1
