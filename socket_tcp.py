import socket
import numpy as np

# the first three characters are used to encode the amount of data to send.
# this lets us send arbitrarily large or small data. 2^24  = max size

def read_img(socket):

    conn, addr = socket.accept()
    print 'Connection address:', addr

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
        send_data = 'done'
        conn.send(send_data)  # echo response
        conn.close()
        break
    return tmpdata

def send_img(socket,img):
    conn, addr = socket.accept( )
    print 'Connection address:', addr

    # reshape data that gets sent out such that it matches what matlab expects
    # the data is "fortran-like"
    data = np.reshape(img, (1,-1),order='F').astype(np.uint8)

    size = img.size

    # initialize array
    sz_uint8 = [0] * 3
    sz_uint8[0] = (size >> 16) & 0xff
    sz_uint8[1] = (size >>  8) & 0xff
    sz_uint8[2] = (size >>  0) & 0xff
    sz_uint8 = np.reshape(sz_uint8, (1, -1)).astype(np.uint8)

    data2send = np.concatenate((sz_uint8, data), axis=1)

    conn.send(data2send)
    conn.close()

#def tcp_data(socket):


    #data = listen2data(conn)
    #return data