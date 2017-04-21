
import socket

def tcp_data(ip_addr,sock):

    TCP_IP = ip_addr
    TCP_PORT = sock
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connection address:', addr

    while 1:
        data = ''
        while len(data) < 2:
            rcv = conn.recv(2 - len(data))
            data = data + rcv
            if rcv == '':
                break
        if rcv == '':
            break
        frame_len = (ord(data[0])<<8) + ord(data[1])


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
        print "received data:", tmpdata
        conn.send(data)  # echo
    conn.close()
    return data