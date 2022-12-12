from socket import *
import pickle
class Client:
    def __init__(self,server_ip, server_port, Buffer_size):
        self.server_ip =server_ip
        self.server_port = server_port
        self.buffer_size = Buffer_size
        
    def connect_send(self,img):
        fail = True
        c = socket(AF_INET,SOCK_STREAM)
        while fail == True:
            try:
                c.connect((self.server_ip, self.server_port))
                fail = False
                self.send_image(img,c)
                print("connection established")
                c.close()
            except:
                pass

    def send_image(img,c):
        file = open("Test9.jpg", "rb")
        image_data = file.read(2048)

        while image_data:
            c.send(image_data)
            image_data = file.read(2048)
        print("Data sent.")
        file.close
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
BUFFER_SIZE = 2048
running = True
full_msg = b""



    


