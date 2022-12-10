from socket import *

SERVER_IP = "192.168.1.200"
SERVER_PORT = 8888
BUFFER_SIZE = 1024

c = socket(AF_INET,SOCK_STREAM)
c.connect((SERVER_IP, SERVER_PORT))

file = open("Test9.jpg", "rb")
image_data = file.read(2048)

while image_data:
    c.send(image_data)
    image_data = file.read(2048)
    print("sending")

file.close
c.send(bytes("Hello there. My name is Ignacio",'utf-8'))
print("Data sent.")
data = c.recv(BUFFER_SIZE)
print('Received data: {}'.format(data))
