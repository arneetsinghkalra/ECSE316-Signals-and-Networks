import struct
import random

# Build packet header before sending to server
def construct_packet(name, type):
    packet = struct.pack('>H', random.getrandbits(16))
    packet += struct.pack('>H', 256)
    packet += struct.pack('>H', 1)
    packet += struct.pack('>H', 0)
    packet += struct.pack('>H', 0)
    packet += struct.pack('>H', 0)
    packet += get_qname(name)
    packet += struct.pack('B', 0)
    packet += struct.pack('>H', get_code(type))
    packet += struct.pack('>H', 1)
    return packet

# Get the qname of the url to insert into packet
def get_qname(name):
    qname = ''
    slices = name.split('.')
    for i in slices:
        qname += struct.pack('>B', len(i))
        for j in bytes(i):
            qname += j    
    return qname

# Get the code corresponding to the query type to insert into packet
def get_code(type):
    code = 0
    if type == 'A':
        code = 1
    elif type == 'CNAME':
        code = 5
    elif type == 'NS':
        code = 2
    elif type == 'MX':
        code = 15
    else:
        print("ERROR: Invalid query type.")
        exit(1)
    return code