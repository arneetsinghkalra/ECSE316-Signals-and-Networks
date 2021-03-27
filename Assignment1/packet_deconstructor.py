import struct

# Parse reply packet to retrieve the desired records
def deconstruct_packet(packet, qname):
    header = struct.unpack_from('>HHHHHH', packet, 0)   # header
    aa = (header[1] & 0x0400) >> 10 # auth
    rcode = (header[1] & 0x000f) # error code
    if rcode != 0:
        output_error(rcode)
    offset = 13 + len(qname) + 4    # initial offset

    answer = []
    for i in range(header[3]):
        (record, offset) = get_answer(packet, offset)
        answer.append(record)
    return answer, aa

def get_answer(packet, offset):
    (name, offset) = get_name(packet, offset)
    fields = struct.unpack_from('>HHIH', packet, offset)    # fields from answer section
    offset += 10    # skip to data section
    type = fields[0]
    ttl = fields[2]
    length = fields[3]
    data = ''

    if type == 1: # A
        data = struct.unpack_from('>' + 'B' * length, packet, offset)
        data = format_data(data)
        offset += length
    elif type == 5: # CName
        (name, k) = get_name(packet, offset)
        data = format_data(name)
        offset += length
    elif type == 2: # NS
        (name, k) = get_name(packet, offset)
        data = format_data(name)
        offset += length
    elif type == 15: # MX
        pref = struct.unpack_from('>H', packet, offset)
        offset += 2
        (mail, offset) = get_name(packet, offset)
        data = (format_data(mail), pref)
        offset += length
    else:
        print("ERROR: Invalid query response.")
        exit(0)
    return [type, ttl, length, data], offset

def format_data(data):
    fname = ''
    for i in data:
        fname += str(i) + '.'
    return fname[0:-1]

def get_name(packet, offset):
    chars = []
    while True:
        length, = struct.unpack_from('>B', packet, offset)
        if (length & 0xC0) == 0xC0:
            ptr, = struct.unpack_from('>H', packet, offset)
            offset += 2
            return (list(chars) + list(get_name(packet, ptr & 0x3FFF))), offset
        if (length & 0xC0) != 0x00:
            exit(1)
        offset += 1
        if length == 0:
            return chars, offset
        chars.append(*struct.unpack_from('!%ds' % length, packet, offset))
        offset += length

def output_error(rcode):
    if rcode == 1:
        print("ERROR    Format error: the name server was unable to interpret the query.")
        exit(0)
    elif rcode == 2:
        print("ERROR    Server failure: the name server was unable to process this query due to a problem with the name server")
        exit(0)
    elif rcode == 3:
        print("NOTFOUND")
        exit(0)
    elif rcode == 4:
        print("ERROR    Not implemented: the name server does not support the requested kind of query.")
        exit(0)
    elif rcode == 5:
        print("ERROR    Refused: the name server refuses to perform the requested operation for policy reasons.")
        exit(0)