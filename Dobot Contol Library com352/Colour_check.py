import cv2
import numpy as np

class clr_rec:
    def __init__(self):
        pass

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

    def find_clr(self, img, upper, lower):
        '''
        Finds BGR values in image for all pixels

        :params img: An image used to find the colors, must be in string format.
        :params upper: The BGR upper boundary for the color found, must be tuple of BGR values [B,G,R] with max of 255 each.
        :params lower: The BGR lower boundary for the color found, must be a tuple of BGR values [B, G, R] with min of 1 each.
        '''
        # Load image
        image = cv2.imread(img)
        Y, X = np.where(np.all((image<=upper) & (image>=lower), axis = 2))
        print(X,Y)
        return Y, X

    def find_outlier(self,img,Boundary, color_index):
        '''
        Finds BGR values in image for all pixels, returns X and Y as lists with coordinates of colored cubes found.

        :params img: An image used to find the colors, must be in string format.
        :params Boundary: The BGR lower and upper boundary for the color found, must be a list of tuples of BGR values [B,G,R] with max of 255 each and min of 1 each.
        :params color_index: The list index of the color that should not be scanned.
        '''
        del Boundary[color_index]
        X = np.zeros(0,dtype=int)
        Y = np.zeros(0,dtype=int)
        for (lower, upper) in Boundary:
            image = cv2.imread(img)
            tmpY, tmpX = np.where(np.all((image<=upper) & (image>=lower), axis = 2))
            X = np.concatenate((X,tmpX),axis=None)
            Y = np.concatenate((Y,tmpY),axis=None)
        return Y,X


    def find_coordinates(self, X, Y,dist):
        tmpX = []
        tmpY = []
        search = True
        center = []
        while search == True:
            if (max(Y)-min(Y)) <= (max(X) - min(X)):
                print("X longer")
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
                            X = np.delete(X,t)
                            Y2.append(Y[t])
                            Y = np.delete(Y,t)
                            j = len(X) - t
                    i  = i + 1

            elif ((max(Y)-min(Y)) > (max(X) - min(X))):
                print("Y longer")
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
                            X = np.delete(X,t)
                            Y2.append(Y[t])
                            Y = np.delete(Y,t)
                            j = len(X) - t
                    i  = i + 1
            
            center.append([min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2)])
            print(center)
            '''
            print(max(X),min(X2))
            print(max(Y),min(Y2))
            print(len(X),len(Y))
            print(len(X2),len(Y2))
            

            if len(tmpX) == 0:
                tmpX = X
                tmpY = Y
            if len(tmpX) > len(X2)+1000:
                X = tmpX
                Y = tmpY
            else:
            '''
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

rec = clr_rec()
#X,Y = rec.find_clr("Test9.jpg", upper, lower)
X,Y = rec.find_outlier("Test10.jpg",boundaries,1)
cord = rec.find_coordinates(X,Y,Distance["Very small"])
print(cord)
