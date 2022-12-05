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
        return Y, X

    def find_coordinates(self, X, Y):
        if (max(Y)-min(Y)) < (max(X) - min(X)):
            X, Y = self.sort_index(self, X,Y)
            X2 = []
            Y2 = []
            j = len(X)
            i = 1   
            while i <= j-1:
                if (X[i] - X[i-1]) > 50:
                    t = i
                    print("works")
                    while j > 0:
                        X2.append(X[t])
                        #print(X[t])
                        X = np.delete(X,t)
                        Y2.append(Y[t])
                        Y = np.delete(Y,t)
                        j = len(X) - t
                i  = i + 1
            if len(X2) > 0:
                return (min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2)), (min(Y2)+((max(Y2)-min(Y2))/2),min(X2)+((max(X2)-min(X2))/2))
            else:  
                return (min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2))

        elif ((max(Y)-min(Y)) > (max(X) - min(X))):
            Y, X = self.sort_index(self, Y,X)
            print("runs")
            X2 = []
            Y2 = []
            j = len(X)
            i = 1   
            while i <= j-1:
                if (Y[i] - Y[i-1]) > 50:
                    t = i
                    print("works")
                    while j > 0:
                        X2.append(X[t])
                        #print(X[t])
                        X = np.delete(X,t)
                        Y2.append(Y[t])
                        Y = np.delete(Y,t)
                        j = len(X) - t
                i  = i + 1
            if len(X2) > 0:
                return (min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2)), (min(Y2)+((max(Y2)-min(Y2))/2),min(X2)+((max(X2)-min(X2))/2))
            else:  
                return (min(Y)+((max(Y)-min(Y))/2),min(X)+((max(X)-min(X))/2))

rec = clr_rec

upper = np.array([50, 56, 200])
lower = np.array([17, 15, 100])

X, Y = rec.find_clr(rec,"Control.jpg", upper, lower)

a,b = rec.find_coordinates(rec, X,Y)
print(a,b)
rec.find_clr()