from socket import *
import pickle
import time

class Client:
    def __init__(self,server_ip, server_port, Buffer_size):
        #Sets valuables for the class
        self.server_ip =server_ip
        self.server_port = server_port
        self.buffer_size = Buffer_size

        #defines TDP connection to server
        self.c = socket(AF_INET,SOCK_STREAM)
        
    # Function for sending images
    def send_image(self,img):
        #Opens file a reads some of it to send
        file = open(img, "rb")
        image_data = file.read(self.buffer_size)
        #Continues to read and send until whole file is sent
        while image_data:
            self.c.send(image_data)
            image_data = file.read(self.buffer_size)
        #Defines the stop message
        stop_msg = "picture_send"

        #Sends stop message to say entire picture has been recieved
        self.c.send(bytes(stop_msg, encoding="utf-8"))
        print("Data sent.")
        file.close

    # Function to recieve message
    def get_msg(self):
        #Empty message
        r_msg = ""

        #While the message is empty, listen for message
        while r_msg == "":
            r_msg = self.c.recv(self.buffer_size)
            #Recieve an object with pickle
            d = pickle.loads(r_msg)

            #Print recieved object
            print(d) 
        
    # Send disconnect message to disconnect from server
    def disconnect(self):
        self.c.send(bytes("Disconnect","utf-8"))

    # Connect function
    def connect(self):
        fail = True
        
        #Loop that continues until connection is established
        while fail == True:
            try:
                self.c.connect((self.server_ip, self.server_port))
                print("connection established")
                fail = False
            except:
                pass

    # Sends image and recieves coordinates
    def server_coms(self,img):
        self.send_image(img)
        self.get_msg()

#Values and variabels used during testing
SERVER_IP = ""
SERVER_PORT = 8888
BUFFER_SIZE = 2048
running = True
full_msg = b""

#Used for testing latency
'''c = Client(SERVER_IP,SERVER_PORT,BUFFER_SIZE)

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
'''

