import cv2
import numpy as np

#Color recognition class
class clr_rec:
    def __init__(self,center_arm):
        self.center_arm = center_arm        #Value of where the arm is placed in picture
        self.start_px = 0                   #Where conveyor starts


    #Defining algorithm to sort two arrays keeping same index values
    def sort_index(self, A, B):
        #Creates empty array as copy of A
        tmp = np.zeros_like(A)
        #Sorts array A with index positions as output
        index = np.argsort(A)
        #Sorts A from lowest to highest value
        A = np.sort(A)
        #Loop runs through all indexes in A
        for i in range(len(A)):
            #Saves B index i value in tmp index i
            tmp[i] = B[i]
            #Check if tmp has a saved value in position
            if tmp[index[i]] == 0:
                # if tmp emptry it moves B value to new position
                B[i] = B[index[i]]
            else:
                # if tmp not empty, uses saved value instead
                B[i] = tmp[index[i]]
        #Returns sorted arrays
        return A, B

    #Finding highest value white pixel under the middle of the y-axis
    def find_start_px(self,img,img_len):
        '''
        Finds start pixel of conveyor

        :params img: An image used to find start pixel, must be path in string format
        :params img_len: The resolution value representing the y-axis of picture
        '''
        #Reads image and returns numpy array of BGR values
        image = cv2.imread(img)
        #Finds all white pixels
        Y, X = np.where(np.all((image <= (255,255,255)) & (image >= (240,240,240)), axis = 2))
        #Find pixels that are below midway in the picture
        white_px = np.where(Y < img_len/2, Y, Y*0)

        #Sets object start_px value as highest white pixel below the middle of the picture
        self.start_px = max(white_px)
        print(self.start_px)
        return self.start_px

    #Function to find specific color cubes centre in image
    def find_clr(self, img, upper, lower, dist):
        '''
        Finds BGR values in image for all pixels

        :params img: An image used to find the colors, must be path in string format.
        :params upper: The BGR upper boundary for the color found, must be tuple of BGR values [B,G,R] with max of 255 each.
        :params lower: The BGR lower boundary for the color found, must be a tuple of BGR values [B, G, R] with min of 1 each.
        '''
        correct = False
        # Load image
        image = cv2.imread(img)
        #Finds all pixels within boundary
        Y, X = np.where(np.all((image<=upper) & (image>=lower), axis = 2))
        #Runs find_coordinates function to find center pixels
        center = self.find_coordinates(Y,X,dist)
        
        #Removes first value if it is not present on the conveyor belt, or too far for the conveyor to get
        while correct == False:
            correct = True
            if center[0][1]<self.start_px:
                center.pop(0)
                correct = False
            if center[0][0]<self.center_arm:
                center.pop(0)
                correct = False
        return center

    #Finds centre of all other colors than the one set to ignore
    def find_outlier(self, img, color_index, boundary, dist):
        '''
        Finds BGR values in image for all pixels, returns X and Y as lists with coordinates of colored cubes found.

        :params img: An image used to find the colors, must be in string format.
        :params Boundary: The BGR lower and upper boundary for the color found, must be a list of tuples of BGR values [B,G,R] with max of 255 each and min of 1 each.
        :params color_index: The list index of the color that should not be scanned.
        '''
        correct = False
        center = []
        tmp = boundary[:]
        #Removes color boundary that is set to be ignored
        del tmp[color_index]
        #Goes for each color in the list
        for (lower, upper) in tmp:
            #reads image
            image = cv2.imread(img)
            #Finds pixels within color boundary
            Y, X = np.where(np.all((image<=upper) & (image>=lower), axis = 2))
            #If there are any cubes present, find centers and add them to list, else go to next color
            try:
                center.extend(self.find_coordinates(Y,X,dist))
            except:
                pass
        
        #When all center found, sort them from lowest to highest x-value
        center = sorted(center,reverse=False)
        
        #Removes first value if it is not present on the conveyor belt, or too far for the conveyor to get
        while correct == False:
            correct = True
            if center[0][1]<self.start_px:
                center.pop(0)
                correct = False
            if center[0][0]<self.center_arm-30:
                center.pop(0)
                correct = False
        return center
    
    #Finds coordinates of centre from array of color coordinates
    def find_coordinates(self, X, Y,dist):
        search = True
        center = []
        #While searching for cubes
        while search == True:
            #Checks if X range is larger than Y range, or they are equal
            if (max(Y)-min(Y)) <= (max(X) - min(X)):
                #Sorts arrays with X array as main array
                X, Y = self.sort_index(X,Y)
                X2 = []
                Y2 = []
                j = len(X)
                i = 1   
                #Checks until large enough distance between two pixels are found to be labeled as different cubes
                while i <= j-1:
                    if (X[i] - X[i-1]) > dist:
                        t = i
                        #Splits array so one cube stays in first array, and all others, if any, are sent to second array
                        while j > 0:
                            X2.append(X[t])
                            Y2.append(Y[t])
                            Y = np.delete(Y,t)
                            X = np.delete(X,t)
                            j = len(X) - t
                    i  = i + 1
            #Checks if Y range is greater than X range
            elif ((max(Y)-min(Y)) > (max(X) - min(X))):
                #Sorts arrays with Y array as main array
                Y, X = self.sort_index(Y,X)
                X2 = []
                Y2 = []
                j = len(X)
                i = 1   
                #Checks until large enough distance between two pixels are found to be labeled as different cubes
                while i <= j-1:
                    if (Y[i] - Y[i-1]) > dist:
                        t = i
                        #Splits array so one cube stays in first array, and all others, if any, are sent to second array
                        while j > 0:
                            X2.append(X[t])
                            Y2.append(Y[t])
                            Y = np.delete(Y,t)
                            X = np.delete(X,t)
                            j = len(X) - t
                    i  = i + 1
            #Finds center of cube in first array and appends it to list
            center.append([min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2)])

            #Sets first array values to second array
            X = X2
            Y = Y2
            
            #If any other cubes present, stop while loop
            if len(X2) == 0:
                search = False
        #Return list of centers
        return center

#Example values for distances
Distance = {"Very small" : 5, "Small" : 50, "Medium" : 100, "Large" : 150}

#Boundary colors
boundaries = [
	([17, 15, 100], [50, 56, 200]),     #Red
	([86, 31, 4], [220, 88, 50]),       #Blue
	([25, 146, 190], [62, 174, 250])    #Yellow
]

#Blue boundary
upper = np.array([220, 88, 50])
lower = np.array([86, 31, 4])
