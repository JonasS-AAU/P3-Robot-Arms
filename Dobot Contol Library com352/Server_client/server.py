import socket, threading, pickle
from Colour_check import clr_rec

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 2048  # Receive Buffer size (power of 2)

class ClientThread(threading.Thread):
    def __init__(self, clientsocket, rec, boundary, dist):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.rec = rec
        self.boundary = boundary
        self.dist = dist

    def run(self):
        i = 0
        msg = ""
        full_msg = b''
        while msg != "Disconnect":
            try:
                img_chunk = self.csocket.recv(BUFFER_SIZE)
                try:
                    msg = img_chunk.decode("utf-8")
                    if msg == "Disconnect":
                            break
                except:
                    while img_chunk:
                        if  "picture_send" not in str(img_chunk):
                            full_msg = full_msg + img_chunk
                            img_chunk = self.csocket.recv(BUFFER_SIZE)
                        else:
                            print("recieved image")
                            break 
                        
                    file = open("server_img.jpg", "wb")
                    file.write(full_msg)
                    file.close()
                    full_msg = b''
                        
                    try:
                        center = self.rec.find_outlier("server_img.jpg", 0, self.boundary, self.dist)
                        print(center)
                        s_msg = pickle.dumps(center)
                        self.csocket.send(s_msg)
                        print("send message")
                    except Exception as ex:
                        print("Finding center Error" + str(ex))
                        
            except:
                pass

        
        self.csocket.close()
        print("Disconnected from client")

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
    clientsock, _ = server.accept()
    newthread = ClientThread(clientsock, rec,boundaries, 10)
    newthread.start()
    
