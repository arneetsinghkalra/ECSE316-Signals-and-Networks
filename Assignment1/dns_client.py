#!/usr/bin/env python

import time
import socket
import argparse
import packet_constructor
import packet_deconstructor
import argparse


def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description="python dns_client.py [-t timeout] [-r max-retries] [-p port] ["
                                                 "-mx|-ns] @server name")
    # Adding optional arguments
    parser.add_argument("-t", "--timeout", type=int, dest='timeout', default=5,
                        help="timeout (optional) gives how long to wait, in seconds, before retransmitting an "
                             "unanswered query. Default value: 5."
                        )
    parser.add_argument("-r", "--maxretries", type=int, dest='maxretries', default=3,
                        help="max-retries(optional) is the maximum number of times to retransmit an "
                             "unanswered query before giving up. Default value: 3."
                        )
    parser.add_argument("-p", "--port", type=int, dest='port', default=53,
                        help="port (optional) is the UDP port number of the DNS server. Default value: 53."
                        )
    # Adding mutually exclusive optional parameters
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-mx", action='store_true',
                       help='mx/ns flags (optional) indicate whether to send a MX (mail server) or \
                                NS (name server) query. At most one of these can be given, and if neither \
                                is given then the client should send a type A (IP address) query')
    group.add_argument("-ns", action='store_true')

    parser.add_argument("server", type=str,
                        help="server (required) is the IPv4 address of the DNS server, in a.b.c.d. format")
    parser.add_argument("name", type=str,
                        help="name (required) is the domain name to query for")

    args = parser.parse_args()

    # Store Values
    timeout = args.timeout
    max_retries = args.maxretries
    port = args.port
    if args.mx:
        type = 'MX'
    elif args.ns:
        type = 'NS'
    else:
        type = 'A'
    server = args.server
    name = args.name.strip()

    print("dns_client sending request for {}.".format(name))
    print("Server: {}".format(server))
    print("Request type: {}".format(type))
    print("Timeout: {}".format(timeout))
    print("Max Retries: {}".format(max_retries))
    print("Port: {}".format(port))

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
                print("Response received after {} seconds ({} retries)".format(t2 - t1, retries))
                break
        except socket.timeout:
            print("ERROR: Request timed out.")

    (answer, aa) = packet_deconstructor.deconstruct_packet(recvB, packet_constructor.get_qname(name))

    if aa:
        auth = 'auth'
    else:
        auth = 'nonauth'

    print("*** Answer Section ({} records) ***".format(len(answer)))
    for entry in answer:
        if entry[1] == 1:
            print("IP    {}    {}   {}".format(entry[5], entry[3], auth))
        elif entry[1] == 2:
            print("NS    {}    {}   {}".format(entry[5], entry[3], auth))
        elif entry[1] == 5:
            print("CNAME    {}    {}    {}".format(entry[5], entry[3], auth))
        elif entry[1] == 15:
            pref = entry[5][1][0]
            alias = ''
            for i in entry[5][0]:
                if i != entry[5][0][0]:
                    alias += '.'
                    alias += i
                else:
                    alias += i
            print("MX    {}    {}   {}   {}".format(alias, pref, entry[3], auth))


if __name__ == "__main__":
    main()
