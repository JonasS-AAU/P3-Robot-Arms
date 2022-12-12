import socket, threading, pickle
from Colour_check import clr_rec

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 2048  # Receive Buffer size (power of 2)

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, rec, boundary, dist):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.rec = rec
        self.boundary = boundary
        self.dist = dist

    def run(self):
        i = 0
        file = open("server_img.jpg", "wb")
        img_chunk = self.csocket.recv(BUFFER_SIZE)
        while img_chunk:
            file.write(img_chunk)
            img_chunk = self.csocket.recv(BUFFER_SIZE)

        file.close()
        print("Aquired image")

        center = self.rec.find_outlier("server_img.jpg", 0, self.boundary, self.dist)
        try:
            msg = pickle.dumps(center)
            self.csocket.send(msg)
            self.csocket.close()
            print('    connection closed') 
        except:
            print("failed to send back")

boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250])
]

rec = clr_rec()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, rec,boundaries, 100)
    newthread.start()
    
