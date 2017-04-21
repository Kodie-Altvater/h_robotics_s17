import socket

# the first three characters are used to encode the amount of data to send.
# this lets us send arbitrarily large or small data. 2^24  = max size

def listen2data(conn):
    while 1:
        data = ''
        while len(data) < 3:
            rcv = conn.recv(3 - len(data))
            data = data + rcv
            if rcv == '':
                break
        if rcv == '':
            break
        frame_len = (ord(data[0]) << 16) + (ord(data[1]) << 8) + ord(data[0])

        data = ''
        while len(data) < frame_len:
            rcv = conn.recv(frame_len - len(data))
            data = data + rcv
            if rcv == '':
                break
        if rcv == '':
            break

        #tmpdata = []
        #for i in data:
        #    tmpdata.append(ord(i))
        #print "received data:", tmpdata
        conn.send(data)  # echo
        conn.close()
        break
    return data

def tcp_data(socket):

    conn, addr = socket.accept()
    #print 'Connection address:', addr

    data = listen2data(conn)
    return data