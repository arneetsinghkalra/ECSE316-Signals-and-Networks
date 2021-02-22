import time
import socket
import packet_constructor
import packet_deconstructor

def main():
    # default values
    timeout = 5
    max_retries = 3
    port = 53
    type = 'NS'
    server = '8.8.8.8'          # example query
    name = 'www.google.ca'      # example query

    print("dns_client sending request for {}.".format(name))
    print("Server: {}".format(server))
    print("Request type: {}".format(type))

    # Create socket connection then try to send a packet and receive the reply
    for retries in range(max_retries):
        resp = False
        recvB = ''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        try:
            t1 = time.time()
            sock.sendto(packet_constructor.construct_packet(name, type), (server, port))
            recvB, recvA = sock.recvfrom(512)
            t2 = time.time()
            if recvB:
                resp = True
                sock.close()
                print("Response received after {} seconds and {} retries.".format(t2 - t1, retries))
                break
        except socket.timeout:
            print("ERROR: Request timed out.")

    packet_deconstructor.deconstruct_packet(recvB, packet_constructor.get_qname(name))

if __name__ == "__main__":
    main()