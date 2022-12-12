from socket import *
import pickle

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
BUFFER_SIZE = 2048
running = True
full_msg = b""
c = socket(AF_INET,SOCK_STREAM)
c.connect((SERVER_IP, SERVER_PORT))


file = open("Test9.jpg", "rb")
image_data = file.read(2048)

while image_data:
    c.send(image_data)
    image_data = file.read(2048)
print("Data sent.")
file.close
    

msg = c.recv(BUFFER_SIZE)
full_msg += msg
d = pickle.loads(full_msg)
print(d)


