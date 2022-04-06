import cv2
import numpy as np
import colorsys

class PointProcessing():
    # def __init__():

    #Negative Transformation
    def negative_transformation(self, image, color_type=None):
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.ones((width, height))*np.max(image)
            result = result-image
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.ones((width, height, channel))
            for i in range(3):
                result[i] = result[i]*np.max(image[i])
            result = result-image
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = image.copy()
            result = np.ones((width, height, channel))
            for i in range(1, 3):
                result[:,:,i] = result[:,:,i]*np.max(image[i])
            result = result-image
            result[:,:,0] = image[:,:,0]
        return np.array(result, dtype='uint8')
    
    #Power Law Transformation
    def power_law_transformation(self, image, gamma, color_type=None):
        if(color_type=="GRAY" or color_type=="RGB"):
            result = np.array(255*(image/255)**gamma, dtype='uint8')
        elif(color_type=="HSI"):
            result = np.array(image, dtype='uint8')
            # result[:,:,0] = np.array(255*(image[:,:,0]/255)**gamma)
            result[:,:,1] = np.array(255*(image[:,:,1]/255)**gamma)
            result[:,:,2] = np.array(255*(image[:,:,2]/255)**gamma, dtype='uint8')
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return result

    #Histogram Equalization using openCV
    def histogram_equalization_cv(self, image, color_type=None):
        result = cv2.equalizeHist(image)
        return result

    #Histogram Equalization
    def histogram_equalization(self, image, color_type=None):
        if(color_type=="GRAY"):
            channel = image
        elif(color_type=="HSI"):
            channel = image[:,:,2]

        width, height = channel.shape[0], channel.shape[1]
        max = np.max(channel) + 1
        min = np.min(channel)
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
                hist[channel[i][j]] += 1
        min = sum_hist[min]
        for i in range(max):
            sum+=hist[i]
            sum_hist[i] = sum
            norm_hist[i] = np.around((max-1)*(sum_hist[i]-min)/(num_pixel-min))
        for i in range(width):
            for j in range(height):
                result[i][j] = norm_hist[channel[i][j]]
        if(color_type=="GRAY"):
            return np.array(result, dtype='uint8')
        elif(color_type=="HSI"):
            result_hsi = image
            result_hsi[:,:,2] = result
            result_hsi = cv2.cvtColor(result_hsi, cv2.COLOR_HSV2RGB)
            return result_hsi

        
class AreaProcessing():
    # def __init__():
        
    #Mean Filter(Average Filter)
    def mean_filter(self, image, size, color_type=None):
        total_size = size**2
        radius = int((size-1)/2)
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.sum(image[i:i+size,j:j+size])/total_size
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.zeros((width-2*radius, height-2*radius, channel))
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.sum(image[i:i+size,j:j+size,ch])/total_size
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :]
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.sum(image[i:i+size,j:j+size,2])/total_size
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')

    #Median Filter
    def median_filter(self, image, size, color_type=None):
        radius = int((size-1)/2)
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.median(image[i:i+size,j:j+size])
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.zeros((width-2*radius, height-2*radius, channel))
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.median(image[i:i+size,j:j+size,ch])
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :]
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.median(image[i:i+size,j:j+size,2])
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')
    
    #Gaussian Filter
    def gaussian_filter(self, image, size, sigma, color_type=None):
        kernel1d = cv2.getGaussianKernel(size, sigma)
        kernel2d = np.outer(kernel1d, kernel1d.transpose())
        radius = int((size-1)/2)
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.sum(np.multiply(image[i:i+size,j:j+size], kernel2d))
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            result = np.zeros((width-2*radius, height-2*radius, channel))
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.sum(np.multiply(image[i:i+size,j:j+size,ch], kernel2d))
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :]
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.sum(np.multiply(image[i:i+size,j:j+size,2], kernel2d))
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')
    
    #High-Boost Filter
    def highboost_filter(self, image, alpha, highpass, color_type=None):
        size = 3
        radius = int((size-1)/2)
        if(highpass==4):
            kernel = np.zeros((size, size))
            kernel[radius-1, radius] = kernel[radius+1, radius] = -1
            kernel[radius, radius-1] = kernel[radius, radius+1] = -1
            kernel[radius, radius] = 4 + alpha
        elif(highpass==8):
            kernel = -np.ones((size, size))
            kernel[radius, radius] = 8 + alpha
        
        if(len(image.shape)==2):
            width, height = image.shape[0], image.shape[1]
            result = np.zeros((width-2*radius, height-2*radius))
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j] = np.sum(np.multiply(image[i:i+size,j:j+size], kernel))
        elif(len(image.shape)==3 and color_type=="RGB"):
            width, height, channel = image.shape[0], image.shape[1], image.shape[2]
            # result = np.zeros((width-2*radius, height-2*radius, channel))
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for ch in range(channel):
                for i in range(width-2*radius):
                    for j in range(height-2*radius):
                        result[i,j,ch] = np.sum(np.multiply(image[i:i+size,j:j+size,ch], kernel))
        elif(len(image.shape)==3 and color_type=="HSI"):
            width, height = image.shape[0], image.shape[1]
            result = image[radius:width-radius+1, radius:height-radius+1, :].copy()
            for i in range(width-2*radius):
                for j in range(height-2*radius):
                    result[i,j,2] = np.sum(np.multiply(image[i:i+size,j:j+size,2], kernel))
            # for ch in range(channel):
            #     for i in range(width-2*radius):
            #         for j in range(height-2*radius):
            #             result[i,j,ch] = np.sum(np.multiply(image[i:i+size,j:j+size,ch], kernel))
            result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        return np.array(result, dtype='uint8')
    