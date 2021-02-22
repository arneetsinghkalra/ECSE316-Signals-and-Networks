import struct

# Parse reply packet to retrieve the desired records
def deconstruct_packet(packet, qname):
    header = struct.unpack_from('>HHHHHH', packet, 0)               # header
    offset = 12 + len(qname) + 4                                    # initial offset
    records = []                                                    # output

    (answers, offset) = get_section(packet, offset, header[3])      # ancount
    records.append(answers)
    (answers, offset) = get_section(packet, offset, header[4])      # nscount
    records.append(answers)
    (answers, offset) = get_section(packet, offset, header[5])      # arcount
    records.append(answers)
    return records

def get_section(packet, offset, count):
    answers = []
    for i in range(count):
        (answer, offset) = get_answer(packet, offset)
        answers.append(answer)
    return answers, offset

def get_answer(packet, offset):
    (name, bytes) = get_name(packet, offset)
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
        (name, bytes) = get_name(packet, offset)
        offset += bytes
        data = (name, offset)
        offset += length

    elif type == 2: # NS
        (name, bytes) = get_name(packet, offset)
        offset += bytes
        data = (name, offset)
        offset += length

    elif type == 6: # SOA
        (pns, bytes) = get_name(packet, offset)
        offset += bytes
        (amb, bytes) = get_name(packet, offset)
        offset += bytes
        data = (pns, amb, offset)  
        offset += length

    elif type == 15: # MX
        config = struct.unpack_from(">H", packet, offset)
        offset += 2

        data = struct.unpack_from('>' + 'B' * (length - 2), packet, offset)[0]
        mail = ''
        for byte in data:
            mail += chr(byte)
        mail += '\x00'
        data = (config, mail)
        offset += length
    else:
        print(type)
        print("ERROR: Invalid query response.")
        exit(0)
    return data, offset

def get_name(packet, offset):
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
    fname = ''

    for byte in name:
        if byte < 30:
            fname += '.'
        else:
            fname += chr(int(byte))
    fname = name[1:-1]
    return (fname, bytes_read)