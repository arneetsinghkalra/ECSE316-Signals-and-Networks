import time
import socket


def main():
    # Default values
    timeout = 5
    max_retries = 3
    port = 53
    type = 'A'
    server = '132.206.85.18'    # Example query
    name = 'www.mcgill.ca'      # Example query

    


    for retries in range(max_retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        t1 = time.time()
        sock.sendto(packet, (server, port))

        try:
            recv = sock.recvfrom(1024)
            t2 = time.time()
            rqst_time = t2 - t1
            print(rqst_time)
        except socket.timeout:
            print("REQUEST TIMEOUT")


if __name__ == "__main__":
    main()