import struct

# Parse reply packet to retrieve the desired records
def deconstruct_packet(packet, qname):
    header = struct.unpack_from('>HHHHHH', packet, 0)               # header
    aa = (header[1] & 0x0400) >> 10                                 # auth
    offset = 12 + len(qname) + 4                                    # initial offset

    answer = []
    for i in range(header[3]):
        (record, offset) = get_answer(packet, offset)
        answer.append(record)
    return answer, aa

def get_answer(packet, offset):
    (name, bytes) = get_label(packet, offset)
    offset += bytes

    aux = struct.unpack_from(">HHIH", packet, offset)
    offset += 10
    type = aux[0]
    clss = aux[1]
    ttl = aux[2]
    length = aux[3]
    data = ''

    if type == 1: # A
        data = struct.unpack_from('>' + 'B' * length, packet, offset)
        ip = ''
        for byte in data:
            ip += str(byte) + '.'
        ip = ip[0:-1]
        data = ip
        offset += length
    elif type == 5: # CName
        (ns, k) = get_name(packet, offset)
        fmt = ''
        for byte in ns:
            fmt += str(byte) + '.'
        fmt = fmt[0:-1]
        data = fmt
        offset += length
    elif type == 2: # NS
        (ns, k) = get_name(packet, offset)
        fmt = ''
        for byte in ns:
            fmt += str(byte) + '.'
        fmt = fmt[0:-1]
        data = fmt 
        offset += length
    elif type == 15: # MX
        pref = struct.unpack_from('>H', packet, offset)
        offset += 2
        (mail, offset) = get_name(packet, offset)
        data = (mail, pref)
        offset += length
    else:
        print(type)
        print("ERROR: Invalid query response.")
        exit(0)
    return [name, type, clss, ttl, length, data], offset

def get_label(packet, offset):
    name = []
    bytes_read = 1
    next = False

    while True:
        byte = struct.unpack_from('>B', packet, offset)[0]
        if byte == 0:
            offset += 1
            break
        elif byte >= 192:
            pointer = struct.unpack_from('>B', packet, offset + 1)[0]
            offset = ((byte << 8) + pointer - 0xc000) - 1
            next = True
        else:
            name.append(byte)
        offset += 1
        if next == False:
            bytes_read += 1

    name.append(0)
    if next == True:
        bytes_read += 1
    return (name, bytes_read)

def get_name(packet, offset):
    chars = []
    while True:
        length, = struct.unpack_from('>B', packet, offset)
        if (length & 0xC0) == 0xC0:
            pointer, = struct.unpack_from('>H', packet, offset)
            offset += 2
            return (list(chars) + list(get_name(packet, pointer & 0x3FFF))), offset
        if (length & 0xC0) != 0x00:
            exit(1)
        offset += 1
        if length == 0:
            return chars, offset
        chars.append(*struct.unpack_from("!%ds" % length, packet, offset))
        offset += length