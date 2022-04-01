import cv2
import pandas as pd
import numpy as np
from math import pow, acos, pi, sqrt

class Photoshop():
    # def __init__():

    #Negative Transformation
    def negative_transformation(self, image):
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            max = np.max(image)
            result = np.ones((width, height))
            result = result*max
            result = result-image
        elif(len(image.shape)==3):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            max0 = np.max(image[0])
            max1 = np.max(image[1])
            max2 = np.max(image[2])
            result = np.ones((width, height, channel))
            result[0] = result[0]*max0
            result[1] = result[1]*max1
            result[2] = result[2]*max2
            result = result-image

        return np.array(result, dtype='uint8')
    #Power Law Transformation
    def power_law_transformation(self, image, gamma):
        result = np.array(255*(image/255)**gamma, dtype='uint8')
        
        return result
    #Histogram Equalization using openCV
    def histogram_equalization_cv(self, image):
        result = cv2.equalizeHist(image)

        return result
    #Histogram Equalization
    def histogram_equalization(self, image):
        width, height = image.shape[0], image.shape[1]
        max = np.max(image) + 1
        min = np.min(image)
        num_pixel = width*height

        #scale histogram
        hist = np.zeros(max)
        #cdf of scale histogram
        sum_hist = np.zeros(max)
        #normalized sum
        norm_hist = np.zeros(max)

        result = np.zeros((width, height))
        sum = 0
        for i in range(width):
            for j in range(height):
                hist[image[i][j]] += 1
        min = sum_hist[min]
        for i in range(max):
            sum+=hist[i]
            sum_hist[i] = sum
            norm_hist[i] = np.around((max-1)*(sum_hist[i]-min)/(num_pixel-min))
        for i in range(width):
            for j in range(height):
                result[i][j] = norm_hist[image[i][j]]
        return np.array(result, dtype='uint8')
        
