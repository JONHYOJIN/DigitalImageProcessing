# cv2.IMREAD_UNCHANGED : 이미지 그대로 출력(원본)
# cv2.IMREAD_GRAYSCALE : 1 채널, 회색조 이미지로 변환
# cv2.IMREAD_COLOR : 3채널, BGR 이미지로 변환
# cv2.IMREAD_ANYDEPTH : 이미지에 따라 16,32bit 또는 8비트로 변환
# cv2.IMREAD_ANYCOLOR : 이미지 모든 색상 형식으로 읽기

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

class GetImage():
    # def __init__(self):

    #Read Gray-Scale Image
    def get_gray_image(self, filename):
        # address = "/Users/hyojin/DigitalImageProcessing/실습영상/" + filename
        address = "./실습영상/" + filename
        image = cv2.imread(address, cv2.IMREAD_GRAYSCALE)
        return image
    #Read BGR(RGB) Image
    def get_color_image_rgb(self, filename):
        # address = "/Users/hyojin/DigitalImageProcessing/실습영상/" + filename
        address = "./실습영상/" + filename
        image = cv2.imread(address, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    def get_color_image_hsi(self, filename):
        # address = "/Users/hyojin/DigitalImageProcessing/실습영상/" + filename
        address = "./실습영상/" + filename
        image = cv2.imread(address, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image
    #Show the imaage(Only one at onece)
    def show_image(self, image):
        cv2.imshow("Sample", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    #Show the histogram result of Histrogram Equalization
    def show_histogram(self, image, result):
        plt.hist(np.concatenate(image).tolist(), bins=100, alpha=0.4, color='red')
        plt.hist(np.concatenate(result).tolist(), bins=100, alpha=0.4, color='dodgerblue')
        plt.title("Histogram Equalization")
        plt.ylabel("The number of pixels")
        plt.xlabel("Scale")
        plt.show()
class GetVideo():
    def get_video_frames(self, filename):
        address = "./실습동영상/" + filename
        capture = cv2.VideoCapture(address)
        frames = []
        while capture.isOpened():
            run, frame = capture.read()
            if not run:
                break
            img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
            frames.append(img)
        capture.release()
        return np.array(frames, dtype='uint8')


if __name__=='__main__':
    frames = GetVideo().get_video_frames("예시1.avi")
    for frame in frames:
        cv2.imshow("Video1", frame)
        if cv2.waitKey(30)&0xFF == ord('q'):
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    
        
        