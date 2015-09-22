import socket
import times

UDP_IP = "xxx.xxx.xxx.xxx" # IP of the running test_server.py server
UDP_PORT = 5005
MESSAGE = "Hello, World!"
MAX_SIZE = 16384

print "UDP target IP: '%s'" % UDP_IP
print "UDP target port: '%s'" % UDP_PORT



def test_set_generator(in_sequence):
    seqence_ctr = in_sequence + 32
    if seqence_ctr >= 0 and seqence_ctr <= 2048:
        return seqence_ctr
    if seqence_ctr > 2048 and seqence_ctr < MAX_SIZE:
        return 2048 + ((seqence_ctr - 2048) * 3)

def send_raw_packet(sock, payload):
    sock.sendto(payload, (UDP_IP, UDP_PORT))

def send_packet(sock, sequence, payload):
    pre_seq  = ("%i" % sequence).rjust(16, "0")
    size = len(payload) + 32
    pre_size = ("%i" % size).rjust(16, "0")
    send_raw_packet(sock, pre_seq + pre_size + payload)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send_packet(sock, 1, "C0001XXXX") # 0001 : Debug Trace Current State
# send_packet(sock, 2, "C0002XXXX") # 0002 : Reset Dialogue (Reset sequence and Stack)
# send_packet(sock, 4, "C0003XXXX") # 0003 : Server Quit


send_packet(sock, 0, "C0002XXXX") # 0002 : Reset Dialogue (Reset sequence and Stack)
time.sleep(3)

for sequence in range(1, 4096):
    size     = test_set_generator(sequence)

    pre_seq  = ("%i" % sequence).rjust(16, "0")
    pre_size = ("%i" % size).rjust(16, "0")

    payload = (pre_seq + pre_size).ljust(size, "X")

    # print payload
    try:
        send_raw_packet(sock, payload)
    except socket.error:
        time.sleep(0.05)
        send_raw_packet(sock, payload)

    time.sleep(0.0005)

send_packet(sock, 1, "C0001XXXX") # 0001 : Debug Trace Current State

print "Done."


