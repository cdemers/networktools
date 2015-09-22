import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

packet_stack = {}
sequence_pointer = 1
peak_stack_size = 0

print "Listening on IP %s, Port: %s" % (UDP_IP, UDP_PORT)

def decode_packet(packet):
    seq  = int(packet[0:16])
    size = int(packet[16:32])
    pl   = packet[32:]

    return (seq, size, pl)

def dump_state(peak_stack_size, packet_stack):
    print "------ Report ------"
    print "Peak Stack Size: %i" % peak_stack_size
    stack_size = len(packet_stack)
    print "Curent Stack Size: %i" % stack_size

    if stack_size == 0:
        print "Stack is clean."
        return
    highest_packet_seq = 0
    lowest_packet_seq = 999999
    for packet in packet_stack:
        if packet > highest_packet_seq:
            highest_packet_seq = packet
        if packet < lowest_packet_seq:
            lowest_packet_seq = packet
    print "Lowest: %i Highest: %i" % (lowest_packet_seq, highest_packet_seq)

    missing_packets = 0
    for i in range(lowest_packet_seq, highest_packet_seq):
        if i not in packet_stack:
            missing_packets += 1
    print "Missing packet between %i and %i is %i" % (lowest_packet_seq, highest_packet_seq, missing_packets)


try:
    while True:
        data, addr = sock.recvfrom(64536) # 64K Buffer Size

        (seq, size, pl) = decode_packet(data)

        print "Sequence Number: %i Size: %i" % ( seq, size)
        print "Src IP: %s Src Port: %s" % addr
        # print "Payload: '%s'" % pl
        print "Data: '%s'" % data

        # Payload starting with C is for Control commands
        print "L2 Preamble: '%s'" % pl[0:1]
        if pl[0:1] == "C":
            command = int(pl[1:5])
            print "Command: '%s'" % command

            if command == 1:
                print "Command 1: Display the debug trace."
                dump_state(peak_stack_size, packet_stack)
            elif command == 2:
                print "Command 2: Clear the stack and reset the sequence_pointer."
                sequence_pointer = 1
                peak_stack_size = 0
                packet_stack.clear()
                print "\n"
                continue
            elif command == 3:
                print "Command 3: Exit."
                exit(0)


        if len(data) == size:
            print "Packet size validation confirmed."
        else:
            print "Packet size error! %i != %i" % (len(data), size)
            raise Exception("Packet Size Error.")

        if(seq == sequence_pointer):
            print "Received packet (%i) in sequence, passing over." % sequence_pointer
            sequence_pointer += 1

            while sequence_pointer in packet_stack:
                print "Next packet (%i) found in stack, poping out of stack." % sequence_pointer
                packet_stack.pop(sequence_pointer, None)
                sequence_pointer += 1
        else:
            print "Received packet seq %i out of order, pushing onto stack." % seq
            packet_stack[seq] = data

        stack_size = len(packet_stack)
        print "Current Stack Size: %i" % stack_size
        if stack_size > peak_stack_size:
            peak_stack_size = stack_size
        print "\n"

except KeyboardInterrupt:
    dump_state(peak_stack_size, packet_stack)

except:
    print "ERROR!"
    print "Data: '%s'" % data
    print addr
    print "Sequence Index: %i" % sequence_pointer
    print "Peak Stack Size: %i" % peak_stack_size
    stack_size = len(packet_stack)
    print "Curent Stack Size: %i" % stack_size

    raise

