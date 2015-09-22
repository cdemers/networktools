# PING!

import socket
import time
import sys

UDP_IP = "xxx.xxx.xxx.xxx" # IP of the running pong.py server.
UDP_PORT = 5005
TIMEOUT=10
SIZE=1472
SIZE=1500

print "UDP target IP: '%s'" % UDP_IP
print "UDP target port: '%s'" % UDP_PORT


def new_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT) # In seconds
    return sock

def open_server_sock(sock, port):
    sock.bind(('0.0.0.0', port))

def send_raw_packet(sock, ip_port, payload):
    sock.sendto(payload, ip_port )

sock = new_socket()
open_server_sock(sock, UDP_PORT)

exchange_counter = 0

safe_packets = 0
lost_packets = 0
avg_latency = None

btm_latency  = 9999
peak_latency = 0

try:
    while True:

        print "Sending Ping #%i and Waiting for Pong." % exchange_counter
        send_raw_packet(sock, (UDP_IP, UDP_PORT), "PING".ljust(SIZE, "X"))

        t_start = time.time()
        try:
            data, ip_port = sock.recvfrom(32534)
            t_end = time.time()
            safe_packets += 1
        except socket.timeout:
            print "Time out! Restarting."
            lost_packets += 1
            exchange_counter = 0
            t_end = time.time()

        if data[0:4] == "PONG":
            latency = ((t_end - t_start) * 1000)
            print "Received Pong %i Bytes in %f ms!" % (len(data), latency)

            if avg_latency is None:
                avg_latency = latency
            else:
                avg_latency = (avg_latency + latency)/2

            if latency > peak_latency and latency < (TIMEOUT*1000):
                peak_latency = latency
            if latency < btm_latency:
                btm_latency = latency
        else:
            raise Exception("Uh Oh!")

        exchange_counter += 1
except:
    sock.close()

    if safe_packets == 0:
        print "100% Failure, quitting."
        sys.exit(1)
    print "\n\nSafe Packets: %i Lost Packets: %i Safe to Lost Ratio: %f %%" % (safe_packets, lost_packets, ( 100 / float(safe_packets) * float(lost_packets) ))
    print "Average Latency: %f ms  Peak: %f ms  Bottom: %f ms" % (avg_latency, peak_latency, btm_latency)

    raise