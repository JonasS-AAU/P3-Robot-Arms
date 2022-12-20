from socket import *
import pickle
import time
from threading import Thread
class Client:
    def __init__(self,server_ip, server_port, Buffer_size):
        self.server_ip =server_ip
        self.server_port = server_port
        self.buffer_size = Buffer_size
        self.c = socket(AF_INET,SOCK_STREAM)
        
    def send_image(self,img):
        file = open(img, "rb")
        image_data = file.read(self.buffer_size)
        while image_data:
            self.c.send(image_data)
            image_data = file.read(self.buffer_size)
        stop_msg = "picture_send"
        self.c.send(bytes(stop_msg, encoding="utf-8"))
        print("Data sent.")
        file.close

    def get_msg(self):
        r_msg = ""
        while r_msg == "":
            r_msg = self.c.recv(self.buffer_size)
            d = pickle.loads(r_msg)
            print(d) 
        
    def disconnect(self):
        self.c.send(bytes("Disconnect","utf-8"))

    def connect(self):
        fail = True
        
        while fail == True:
            try:
                self.c.connect((self.server_ip, self.server_port))
                print("connection established")
                fail = False
            except:
                pass


    def server_coms(self,img):
        self.send_image(img)
        self.get_msg()
    
SERVER_IP = "192.168.1.59"
SERVER_PORT = 8888
BUFFER_SIZE = 2048
running = True
full_msg = b""

c = Client(SERVER_IP,SERVER_PORT,BUFFER_SIZE)

time_taken_lis = []
c.connect()
for i in range(1000):
    start = time.time()
    c.server_coms("Test8.jpg")
    time_taken_lis.append(time.time()-start)
    print(i)
c.disconnect()

file = open("time.txt","w")
print(time_taken_lis)
for element in time_taken_lis:
    file.write(str(element) + "\n")
file.close()


