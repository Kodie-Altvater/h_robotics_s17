# Echo server program

#def setup_socket():
import socket
import image_training

HOST = '10.0.0.101'      # Symbolic name meaning all available interfaces
PORT = 50007             # Arbitrary non-privileged port

get_image()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()
