import socket, threading, pickle
from Colour_check import clr_rec

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 2048  # Receive Buffer size (power of 2)

#Create thread class
class ClientThread(threading.Thread):
    def __init__(self, clientsocket, rec, boundary, dist):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.rec = rec
        self.boundary = boundary
        self.dist = dist

    #When thread is started
    def run(self):
        #create empty message to recieve
        msg = ""
        full_msg = b''

        #While not told to disconnect
        while msg != "Disconnect":

            #Tries to recieve message
            try:
                #Recieves message
                img_chunk = self.csocket.recv(BUFFER_SIZE)
                #Try to decode text message
                try:
                    msg = img_chunk.decode("utf-8")
                    if msg == "Disconnect":
                            break
                #If not it is an image
                except:
                    #While still recieving image
                    while img_chunk:
                        #Checking if the entire picture has been sent
                        if  "picture_send" not in str(img_chunk):
                            #Extends full_msg with bytes recieved of picture
                            full_msg = full_msg + img_chunk
                            img_chunk = self.csocket.recv(BUFFER_SIZE)
                        else:
                            #if picture send is in recieved message, stop recieving
                            print("recieved image")
                            break 
                    #A file is opened and the recieved image is written to the file
                    file = open("server_img.jpg", "wb")
                    file.write(full_msg)
                    file.close()
                    #Full_msg is made to an empty byte string again to not stack images
                    full_msg = b''
                    
                    try:
                        #Tries to find center of colored cubes present on image
                        center = self.rec.find_outlier("server_img.jpg", 0, self.boundary, self.dist)
                        print(center)
                        #Pickles center object and sends it back to the client
                        s_msg = pickle.dumps(center)
                        self.csocket.send(s_msg)
                        print("send message")
                    except Exception as ex:
                        print("Finding center Error" + str(ex))
                        
            except:
                pass

        #Disconnects from client
        self.csocket.close()
        print("Disconnected from client")

#Color boundaries
boundaries = [
	([17, 15, 100], [50, 56, 200]),         #Red
	([86, 31, 4], [220, 88, 50]),           #Blue
	([25, 146, 190], [62, 174, 250])        #Yellow
]

#Creating color recognition object
rec = clr_rec()

#Defining server values
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server started")
print("Waiting for client request..")
#Runs while loop to listen for client to connect
while True:
    server.listen(1)
    #If client connects starts a thread
    clientsock, _ = server.accept()
    newthread = ClientThread(clientsock, rec,boundaries, 10)
    newthread.start()
    
