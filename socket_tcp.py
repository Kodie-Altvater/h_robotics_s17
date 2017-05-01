# Kodie Altvater
# Socket accept and read/write
# April 22nd, 2017
# Designed for Human Robotics Course project, JHU

import numpy as np

# LIMITATIONS: This code currently only supports sending and receiving 640 x 480 x 3 sized images
# It is very much possible to make this scaleable to larger/smaller images; however, for the
# purpose of this project it wasn't needed.

# the first three bytes are used to encode the amount of data to send/receive
# this lets us send arbitrarily large or small data. 2^24 (16777216 bytes)  = max size


# Reads data from socket and interprets as image
def read_data(conn):

    while 1:
        data = ''
        tmpdata = ''
        while len(data) < 3:
            rcv = conn.recv(3 - len(data))
            data = data + rcv
            if rcv == '':
                break
        if rcv == '':
            break
        frame_len = (ord(data[0]) << 16) + (ord(data[1]) << 8) + ord(data[2])
        data = ''
        while len(data) < frame_len:
            rcv = conn.recv(frame_len - len(data))
            data = data + rcv
            if rcv == '':
                break
        if rcv == '':
            break

        tmpdata = []
        for i in data:
            tmpdata.append(ord(i))
        # tell client that you're finished
        send_data = 'done'
        conn.sendall(send_data)  # echo response
        break
    return tmpdata


# which function do you wish to complete?
# detect, read gray, read color
def feature2do(conn):
    data = ''
    while len(data) < 4:
        rcv = conn.recv(4 - len(data))
        data = data + rcv
        if rcv == '':
            break
    # determine which type is requested
    if (data == 'gray'):
        type = 1
    elif (data == 'colr'):
        type = 2
    elif (data == 'detc'):
        type = 3
    elif(data == 'exit'):
        type = 4
    elif(data == 'save'):
        type = 5
    else:
        # there was an error so make type something it doesn't use
        type = 6
    return type

# Function that reshapes data according to column-wise (fortran)
# Sends over to client and the client can decode image/data if wanted.
def send_data(conn,data):

    # captures the length so it can be made a 3 byte value
    length = data.size

    # Size of data to send (packet header in a sense)
    sz_uint8 = [0] * 3
    sz_uint8[0] = (length >> 16) & 0xff
    sz_uint8[1] = (length >>  8) & 0xff
    sz_uint8[2] = (length >>  0) & 0xff

    sz_uint8 = np.reshape(sz_uint8, (1, -1)).astype(np.uint8)
    data = np.reshape(data,(1,-1),order='F').astype(np.uint8)

    # concatenate along single row
    data2send = np.concatenate((sz_uint8, data), axis=1)

    #return data2send
    # send data issue with conn.send where it wouldn't always send the data...
    conn.sendall(data2send)