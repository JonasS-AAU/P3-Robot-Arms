from socket import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
BUFFER_SIZE = 2048

c = socket(AF_INET,SOCK_STREAM)
c.connect((SERVER_IP, SERVER_PORT))

file = open("Test9.jpg", "rb")
image_data = file.read(2048)

while image_data:
    c.send(image_data)
    image_data = file.read(2048)
file.close



print("Data sent.")
c.close()
