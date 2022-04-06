# << Photoshop GUI >>
from ImageRoad import GetImage
from ImageProcessing import PointProcessing, AreaProcessing

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from functools import partial
import cv2

#HE test
hetest = ["Fig0316(1)(top_left).jpg","Fig0316(2)(2nd_from_top).jpg","Fig0316(3)(third_from_top).jpg","Fig0316(4)(bottom_left).jpg"]
#실습영상 Gray-Scale
samplecs = ["airplane.bmp","baboon.bmp","barbara.bmp","BoatsColor.bmp","boy.bmp","goldhill.bmp","lenna_color.bmp","pepper.bmp","sails.bmp"]
#실습영상 Color-Scale
samplegs = ["boats.bmp","bridge.bmp","cameraman.bmp","clown.bmp","crowd.bmp","man.bmp","tank.bmp","truck.bmp","zelda.bmp"]
#Noise Images
n_images = ["Gaussian noise.png","Lena_noise.png","Salt&pepper noise.png","Fig0327(a)(tungsten_original).jpg","Fig0525(a)(aerial_view_no_turb).jpg","Fig0503 (original_pattern).jpg","Fig0504(a)(gaussian-noise).jpg",\
    "Fig0504(i)(salt-pepper-noise).jpg","Fig0507(a)(ckt-board-orig).jpg","Fig0510(a)(ckt-board-saltpep-prob.pt05).jpg","Fig0513(a)(ckt_gaussian_var_1000_mean_0).jpg"]

#Initialization
root = Tk()
root.title("Digital Image Processing Photoshop")
root.geometry("1400x1200")
root.resizable(True, True)

### Funtions ###
def get_selected_image(scale):
    global IMAGE, IMAGE_CV, NAME, TYPE
    NAME = combobox_p1_var.get()
    if scale=="GRAY":
        IMAGE_CV = GetImage().get_gray_image(NAME)
        TYPE = "GRAY"
    elif scale=="RGB":
        IMAGE_CV = GetImage().get_color_image_rgb(NAME)
        TYPE = "RGB"
    elif scale=="HSI":
        IMAGE_CV = GetImage().get_color_image_hsi(NAME)
        TYPE = "HSI"
    label1.config(text="\n[ "+NAME+" ] "+TYPE+" 이미지\n")
    label1.place(x=350, y=5)
    if scale=="HSI":
        IMAGE = cv2.cvtColor(IMAGE_CV, cv2.COLOR_HSV2RGB)
        IMAGE = Image.fromarray(IMAGE)
    else:
        IMAGE = Image.fromarray(IMAGE_CV)
    IMAGE = ImageTk.PhotoImage(image=IMAGE)
    label2.config(image=IMAGE)
def neg_trans():
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Negative Transformation\n")
        label1.place(x=350, y=5)
        IMAGE_CV = PointProcessing().negative_transformation(IMAGE_CV, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def pow_law_trans(gamma):
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Power-Law Transformation γ="+str(gamma)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = PointProcessing().power_law_transformation(IMAGE_CV, gamma, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def hist_equal():
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Histogram Equalization\n")
        label1.place(x=350, y=5)
        IMAGE_CV = PointProcessing().histogram_equalization(IMAGE_CV, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
        if(NAME):
            label1.config(text="\nRGB 사진은 지원되지 않습니다")
def mean_ft(size):
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Mean Filter size="+str(size)+"x"+str(size)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().mean_filter(IMAGE_CV, size, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def med_ft(size):
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Median Filter size="+str(size)+"x"+str(size)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().median_filter(IMAGE_CV, size, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def gaus_ft(size, sigma):
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Gaussian Filter size="+str(size)+"x"+str(size)+", σ="+str(sigma)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().gaussian_filter(IMAGE_CV, size, sigma, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def hb_ft(alpha, highpass):
    global IMAGE, IMAGE_CV, NAME, TYPE
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" High-Boost Filter size= 3x3, A="+str(alpha)+", HighPass Type:"+str(highpass)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().highboost_filter(IMAGE_CV, alpha, highpass, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
### End of Funtions ###

#User Interface
label1 = Label(root, text = "\n편집할 사진을 선택해주세요")
label1.place(x=500, y=300)
label2 = Label(root, text = " ")
label2.place(x=350, y=50)

#Get Image
label3 = Label(root, text = "< IMAGE >")
label3.place(x=15, y=5)

combobox_p1_var = StringVar()
combobox_p1 = ttk.Combobox(root, textvariable=combobox_p1_var)
combobox_p1['value'] = (sum([hetest, samplegs, samplecs, n_images], []))
combobox_p1.place(x=10, y=25)

button_select_image_gray = Button(root, text = "흑백 선택", command=partial(get_selected_image, "GRAY"))
button_select_image_gray.place(x=220, y=20)
button_select_image_rgb = Button(root, text = "RGB 선택", command=partial(get_selected_image, "RGB"))
button_select_image_rgb.place(x=220, y=45)
button_select_image_hsi = Button(root, text = "HSI 선택", command=partial(get_selected_image, "HSI"))
button_select_image_hsi.place(x=220, y=70)

#IMAGE Processing
BX = 10
PP = 120
AP = 330
STAIR = 30
#Point Processing
label4 = Label(root, text = "< Point Processing >")
label4.place(x=BX+5, y=PP-20)
button_p1 = Button(root, text = "Negative Trans.", command=neg_trans)
button_p1.place(x=BX, y=PP)
button_p2 = Button(root, text = "Power-Law Trans.(γ=0.4)", command=partial(pow_law_trans, 0.4))
button_p2.place(x=BX, y=PP+(1*STAIR))
button_p3 = Button(root, text = "Power-Law Trans.(γ=0.67)", command=partial(pow_law_trans, 0.67))
button_p3.place(x=BX, y=PP+(2*STAIR))
button_p4 = Button(root, text = "Power-Law Trans.(γ=1.5)", command=partial(pow_law_trans, 1.5))
button_p4.place(x=BX, y=PP+(3*STAIR))
button_p5 = Button(root, text = "Power-Law Trans.(γ=2.5)", command=partial(pow_law_trans, 2.5))
button_p5.place(x=BX, y=PP+(4*STAIR))
button_p6 = Button(root, text = "Histogram Equal.", command=hist_equal)
button_p6.place(x=BX, y=PP+(5*STAIR))
#Area Processing
label5 = Label(root, text = "< Area Processing >")
label5.place(x=BX+5, y=AP-20)
button_p7 = Button(root, text = "Mean Filter 3x3", command=partial(mean_ft, 3))
button_p7.place(x=BX, y=AP)
button_p8 = Button(root, text = "Mean Filter 5x5", command=partial(mean_ft, 5))
button_p8.place(x=BX, y=AP+(1*STAIR))
button_p9 = Button(root, text = "Median Filter 3x3", command=partial(med_ft, 3))
button_p9.place(x=BX, y=AP+(2*STAIR))
button_p10 = Button(root, text = "Median Filter 5x5", command=partial(med_ft, 5))
button_p10.place(x=BX, y=AP+(3*STAIR))
button_p11 = Button(root, text = "Gaussian Filter 3x3 (σ=1)", command=partial(gaus_ft, 3, 1))
button_p11.place(x=BX, y=AP+(4*STAIR))
button_p12 = Button(root, text = "Gaussian Filter 5x5 (σ=1)", command=partial(gaus_ft, 3, 1))
button_p12.place(x=BX, y=AP+(5*STAIR))
button_p13 = Button(root, text = "High-Boost Filter 3x3 (A=1.0, HP:4)", command=partial(hb_ft, 1, 4))
button_p13.place(x=BX, y=AP+(6*STAIR))
button_p14 = Button(root, text = "High-Boost Filter 3x3 (A=1.2, HP:4)", command=partial(hb_ft, 1.2, 4))
button_p14.place(x=BX, y=AP+(7*STAIR))
button_p15 = Button(root, text = "High-Boost Filter 3x3 (A=1.4, HP:4)", command=partial(hb_ft, 1.4, 4))
button_p15.place(x=BX, y=AP+(8*STAIR))
button_p16 = Button(root, text = "High-Boost Filter 3x3 (A=1.0, HP:8)", command=partial(hb_ft, 1, 8))
button_p16.place(x=BX, y=AP+(9*STAIR))
button_p17 = Button(root, text = "High-Boost Filter 3x3 (A=1.2, HP:8)", command=partial(hb_ft, 1.2, 8))
button_p17.place(x=BX, y=AP+(10*STAIR))
button_p18 = Button(root, text = "High-Boost Filter 3x3 (A=1.4, HP:8)", command=partial(hb_ft, 1.4, 8))
button_p18.place(x=BX, y=AP+(11*STAIR))

root.mainloop()




