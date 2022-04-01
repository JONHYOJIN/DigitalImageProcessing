# Point Processing 2
from ImageRoad import GetImage
from ImageProcessing import PointProcessing

import cv2
import numpy as np

ImageGetter = GetImage()
Ptshop = PointProcessing()

# Fig1 = ImageGetter.get_gray_image("Fig0316(1)(top_left)")
# Fig1_hist = Ptshop.histogram_equalization(Fig1)

# Fig2 = ImageGetter.get_gray_image("Fig0316(2)(2nd_from_top)")
# Fig2_hist = Ptshop.histogram_equalization(Fig2)

# Fig3 = ImageGetter.get_gray_image("Fig0316(3)(third_from_top)")
# Fig3_hist = Ptshop.histogram_equalization(Fig3)

# Fig4 = ImageGetter.get_gray_image("Fig0316(4)(bottom_left)")
# Fig4_hist = Ptshop.histogram_equalization(Fig4)

# ImageGetter.show_histogram(Fig1, Fig1_hist)
# ImageGetter.show_histogram(Fig2, Fig2_hist)
# ImageGetter.show_histogram(Fig3, Fig3_hist)
# ImageGetter.show_histogram(Fig4, Fig4_hist)

sample1 = GetImage().get_color_image("airplane")
# sample1 = cv2.imread("/Users/hyojin/DigitalImageProcessing/실습영상/airplane.bmp", cv2.IMREAD_COLOR)
print(sample1.dtype)
sample2 = cv2.cvtColor(sample1, cv2.COLOR_BGR2RGB)


GetImage().show_image(sample2)
# cv2.imshow("airplane", sample1)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)