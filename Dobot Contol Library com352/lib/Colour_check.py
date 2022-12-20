import cv2
import numpy as np

class clr_rec:
    def __init__(self,center_arm):
        self.center_arm = center_arm
        self.start_px = 0

    def sort_index(self, A, B):
        tmp = np.zeros_like(A)
        index = np.argsort(A)
        A = np.sort(A)
        for i in range(len(A)):
            tmp[i] = B[i]
            if tmp[index[i]] == 0:
                B[i] = B[index[i]]
            else:
                B[i] = tmp[index[i]]
        return A, B

    def find_start_px(self,img,img_len):
        '''
        
        '''
        image = cv2.imread(img)
        Y, X = np.where(np.all((image <= (255,255,255)) & (image >= (240,240,240)), axis = 2))
        white_px = np.where(Y < img_len/2, Y, Y*0)
        self.start_px = max(white_px)
        print(self.start_px)
        return self.start_px

    def find_clr(self, img, upper, lower, dist):
        '''
        Finds BGR values in image for all pixels

        :params img: An image used to find the colors, must be in string format.
        :params upper: The BGR upper boundary for the color found, must be tuple of BGR values [B,G,R] with max of 255 each.
        :params lower: The BGR lower boundary for the color found, must be a tuple of BGR values [B, G, R] with min of 1 each.
        '''
        correct = False
        # Load image
        image = cv2.imread(img)
        Y, X = np.where(np.all((image<=upper) & (image>=lower), axis = 2))
        center = self.find_coordinates(Y,X,dist)
        
        while correct == False:
            correct = True
            if center[0][1]<self.start_px:
                center.pop(0)
                correct = False
            if center[0][0]<self.center_arm:
                center.pop(0)
                correct = False
        return center

    def find_outlier(self, img, color_index, boundary, dist):
        '''
        Finds BGR values in image for all pixels, returns X and Y as lists with coordinates of colored cubes found.

        :params img: An image used to find the colors, must be in string format.
        :params Boundary: The BGR lower and upper boundary for the color found, must be a list of tuples of BGR values [B,G,R] with max of 255 each and min of 1 each.
        :params color_index: The list index of the color that should not be scanned.
        '''
        #print(self.boundaries)
        #boundary = self.boundaries
        correct = False
        center = []
        tmp = boundary[:]
        del tmp[color_index]
        X = np.zeros(0,dtype=int)
        Y = np.zeros(0,dtype=int)
        for (lower, upper) in tmp:
            image = cv2.imread(img)
            Y, X = np.where(np.all((image<=upper) & (image>=lower), axis = 2))
            try:
                center.extend(self.find_coordinates(Y,X,dist))
            except:
                pass
        center = sorted(center,reverse=False)
        
        while correct == False:
            correct = True
            if center[0][1]<self.start_px:
                center.pop(0)
                correct = False
            if center[0][0]<self.center_arm-30:
                center.pop(0)
                correct = False
        return center
    

    def find_coordinates(self, X, Y,dist):
        search = True
        center = []
        while search == True:
            if (max(Y)-min(Y)) <= (max(X) - min(X)):
                X, Y = self.sort_index(X,Y)
                X2 = []
                Y2 = []
                j = len(X)
                i = 1   
                while i <= j-1:
                    if (X[i] - X[i-1]) > dist:
                        t = i
                        while j > 0:
                            X2.append(X[t])
                            Y2.append(Y[t])
                            Y = np.delete(Y,t)
                            X = np.delete(X,t)
                            j = len(X) - t
                    i  = i + 1

            elif ((max(Y)-min(Y)) > (max(X) - min(X))):
                Y, X = self.sort_index(Y,X)
                X2 = []
                Y2 = []
                j = len(X)
                i = 1   
                while i <= j-1:
                    if (Y[i] - Y[i-1]) > dist:
                        t = i
                        while j > 0:
                            X2.append(X[t])
                            Y2.append(Y[t])
                            Y = np.delete(Y,t)
                            X = np.delete(X,t)
                            j = len(X) - t
                    i  = i + 1
            
            center.append([min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2)])
            X = X2
            Y = Y2
            
            if len(X2) == 0:
                search = False
        
        return center

Distance = {"Very small" : 5, "Small" : 50, "Medium" : 100, "Large" : 150}

boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250])
]


upper = np.array([220, 88, 50])
lower = np.array([86, 31, 4])
