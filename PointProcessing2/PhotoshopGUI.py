# << Photoshop GUI >>
from ImageRoad import GetImage
from ImageProcessing import PointProcessing, AreaProcessing, EdgeDetection

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
#도로교통공단 cctv capture images
cctvs = ["대공원IC.png","청담대교북단.png","큰방죽사거리.png","벗말사거리.png","경부선_공세육교.png"]
#오늘의집 책상 Images
desks = ["책상1.png","책상2.png","책상3.png"]


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
#Point Processing
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
def pow_law_trans():
    global IMAGE, IMAGE_CV, NAME, TYPE
    gamma = combobox_plT_var.get()
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
#Area Processing
def mean_ft():
    global IMAGE, IMAGE_CV, NAME, TYPE
    size = combobox_meanft_var.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Mean Filter size="+str(size)+"x"+str(size)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().mean_filter(IMAGE_CV, size, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def med_ft():
    global IMAGE, IMAGE_CV, NAME, TYPE
    size = combobox_medianft_var.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Median Filter size="+str(size)+"x"+str(size)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().median_filter(IMAGE_CV, size, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def gaus_ft():
    global IMAGE, IMAGE_CV, NAME, TYPE
    size = combobox_gausft_var_1.get()
    sigma = combobox_gausft_var_2.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Gaussian Filter size="+str(size)+"x"+str(size)+", σ="+str(sigma)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().gaussian_filter(IMAGE_CV, size, sigma, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def hb_ft():
    global IMAGE, IMAGE_CV, NAME, TYPE
    alpha = combobox_hbft_var_1.get()
    highpass = combobox_hbft_var_2.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" High-Boost Filter size= 3x3, A="+str(alpha)+", HighPass Type:"+str(highpass)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().highboost_filter(IMAGE_CV, alpha, highpass, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
#Edge Detection
def prewitt():
    global IMAGE, IMAGE_CV, NAME, TYPE
    threshold = combobox_prewitt_var_1.get()
    background = combobox_prewitt_var_2.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Prewitt Operator size= 3x3, Threshold= "+str(threshold)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = EdgeDetection().prewitt_operator(IMAGE_CV, threshold, background, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def sobel():
    global IMAGE, IMAGE_CV, NAME, TYPE
    threshold = combobox_sobel_var_1.get()
    background = combobox_sobel_var_2.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Sobel Operator size= 3x3, Threshold= "+str(threshold)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = EdgeDetection().sobel_operator(IMAGE_CV, threshold, background, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def LoG():
    global IMAGE, IMAGE_CV, NAME, TYPE
    size = combobox_log_var_1.get()
    sigma = combobox_log_var_2.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Gaussian Filter size="+str(size)+"x"+str(size)+", σ="+str(sigma)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = EdgeDetection().LoG_operator(IMAGE_CV, size, sigma, TYPE)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def canny():
    global IMAGE, IMAGE_CV, NAME, TYPE
    threshold1 = combobox_canny_var_1.get()
    threshold2 = combobox_canny_var_2.get()
    try:
        label1.config(text="\n[ "+NAME+" ] "+TYPE+" Sobel Operator size= 3x3, Threshold= "+str(threshold1)+", "+str(threshold2)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = EdgeDetection().canny_operator(IMAGE_CV, threshold1, threshold2, TYPE)
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
combobox_p1['value'] = (sum([hetest, samplegs, samplecs, n_images, cctvs, desks], []))
combobox_p1.place(x=10, y=25)

button_select_image_gray = Button(root, text = "흑백 선택", command=partial(get_selected_image, "GRAY"), width=4, fg='grey20')
button_select_image_gray.place(x=220, y=20)
button_select_image_rgb = Button(root, text = "RGB 선택", command=partial(get_selected_image, "RGB"), width=4, fg='brown4')
button_select_image_rgb.place(x=220, y=45)
button_select_image_hsi = Button(root, text = "HSI 선택", command=partial(get_selected_image, "HSI"), width=4, fg='steel blue')
button_select_image_hsi.place(x=220, y=70)

#IMAGE Processing
BX = 10     #Button 가로 위치(x) 기준
PP = 150    #Point Processing 세로 위치 기준
AP = 270    #Area Processing 세로 위치 기준
ED = 420    #Edge Detection 세로 위치 기준
STAIR = 30
XOPTION = 145

#[Point Processing]
label4 = Label(root, text = "< Point Processing >")
label4.place(x=BX+5, y=PP-20)
##Negative Transformation
button_p1 = Button(root, text = "Negative Trans.", command=neg_trans, width=11)
button_p1.place(x=BX, y=PP)
##Power-Law Transformation
label_meanft = Label(root, text ="γ :")
label_meanft.place(x=XOPTION, y=PP+(1*STAIR))
combobox_plT_var = DoubleVar()
combobox_plT = ttk.Combobox(root, textvariable=combobox_plT_var, width=3)
combobox_plT['value'] = ([0.4, 0.67, 1.5, 2.5])
combobox_plT.place(x=XOPTION+22, y=PP+(1*STAIR)+3)
combobox_plT.set(0.4)
button_p2 = Button(root, text = "Power-Law Trans.", command=pow_law_trans, width=11)
button_p2.place(x=BX, y=PP+(1*STAIR))
##Histogram Equalization
button_p3 = Button(root, text = "Histogram Equal.", command=hist_equal, width=11)
button_p3.place(x=BX, y=PP+(2*STAIR))

#[Area Processing]
label5 = Label(root, text = "< Area Processing >")
label5.place(x=BX+5, y=AP-20)
##Mean FILTER
label_meanft = Label(root, text ="Size :")
label_meanft.place(x=XOPTION, y=AP+3)
combobox_meanft_var = IntVar()
combobox_meanft = ttk.Combobox(root, textvariable=combobox_meanft_var, width=2)
combobox_meanft['value'] = ([3, 5, 7, 9, 11, 13, 15, 17, 19])
combobox_meanft.place(x=XOPTION+38, y=AP+3)
combobox_meanft.set(3)
button_p4 = Button(root, text = "Mean Filter", command=mean_ft, width=11)
button_p4.place(x=BX, y=AP)
##Median FILTER
label_medianft = Label(root, text ="Size :")
label_medianft.place(x=XOPTION, y=AP+(1*STAIR)+3)
combobox_medianft_var = IntVar()
combobox_medianft = ttk.Combobox(root, textvariable=combobox_medianft_var, width=2)
combobox_medianft['value'] = ([3, 5, 7, 9, 11, 13, 15, 17, 19])
combobox_medianft.place(x=XOPTION+38, y=AP+(1*STAIR)+3)
combobox_medianft.set(3)
button_p5 = Button(root, text = "Median Filter", command=med_ft, width=11)
button_p5.place(x=BX, y=AP+(1*STAIR))
##Gaussian FILTER
label_gausft_1 = Label(root, text ="Size :")
label_gausft_1.place(x=XOPTION, y=AP+(2*STAIR)+3)
label_gausft_2 = Label(root, text ="σ :")
label_gausft_2.place(x=XOPTION+83, y=AP+(2*STAIR)+3)
combobox_gausft_var_1 = IntVar()
combobox_gausft_1 = ttk.Combobox(root, textvariable=combobox_gausft_var_1, width=2)
combobox_gausft_1['value'] = ([3, 5, 7, 9, 11, 13, 15, 17, 19])
combobox_gausft_1.place(x=XOPTION+38, y=AP+(2*STAIR)+3)
combobox_gausft_1.set(3)
combobox_gausft_var_2 = IntVar()
combobox_gausft_2 = ttk.Combobox(root, textvariable=combobox_gausft_var_2, width=3)
combobox_gausft_2['value'] = ([0.1, 0.5, 1, 5, 10])
combobox_gausft_2.place(x=XOPTION+107, y=AP+(2*STAIR)+3)
combobox_gausft_2.set(1)
button_p6 = Button(root, text = "Gaussian Filter", command=gaus_ft, width=11)
button_p6.place(x=BX, y=AP+(2*STAIR))
##HighBoost FILTER
label_hbft_1 = Label(root, text ="A :")
label_hbft_1.place(x=XOPTION, y=AP+(3*STAIR)+3)
label_hbft_2 = Label(root, text ="HP :")
label_hbft_2.place(x=XOPTION+83, y=AP+(3*STAIR)+3)
combobox_hbft_var_1 = DoubleVar()
combobox_hbft_1 = ttk.Combobox(root, textvariable=combobox_hbft_var_1, width=3)
combobox_hbft_1['value'] = ([0.8, 1.0, 1.2, 1.4])
combobox_hbft_1.place(x=XOPTION+29, y=AP+(3*STAIR)+3)
combobox_hbft_1.set(1.0)
combobox_hbft_var_2 = IntVar()
combobox_hbft_2 = ttk.Combobox(root, textvariable=combobox_hbft_var_2, width=2)
combobox_hbft_2['value'] = ([4, 8])
combobox_hbft_2.place(x=XOPTION+116, y=AP+(3*STAIR)+3)
combobox_hbft_2.set(4)
button_p7 = Button(root, text = "HighBoost Filter", command=hb_ft, width =11)
button_p7.place(x=BX, y=AP+(3*STAIR))

#[Edge Detection]
label6 = Label(root, text = "< Edge Detection >")
label6.place(x=BX+5, y=ED-20)
##Prewitt Operator
label_prewitt_1 = Label(root, text ="Lv :")
label_prewitt_1.place(x=XOPTION, y=ED+3)
label_prewitt_2 = Label(root, text ="BG :")
label_prewitt_2.place(x=XOPTION+75, y=ED+3)
combobox_prewitt_var_1 = IntVar()
combobox_prewitt_1 = ttk.Combobox(root, textvariable=combobox_prewitt_var_1, width=2)
combobox_prewitt_1['value'] = ([1, 2, 3, 4, 5])
combobox_prewitt_1.place(x=XOPTION+30, y=ED+3)
combobox_prewitt_1.set(1)
combobox_prewitt_var_2 = StringVar()
combobox_prewitt_2 = ttk.Combobox(root, textvariable=combobox_prewitt_var_2, width=2)
combobox_prewitt_2['value'] = (['O','X'])
combobox_prewitt_2.place(x=XOPTION+108, y=ED+3)
combobox_prewitt_2.set('O')
button_p8 = Button(root, text = "Prewitt Operator", command=prewitt, width =11)
button_p8.place(x=BX, y=ED)
##Sobel Operator
label_sobel_1 = Label(root, text ="Lv :")
label_sobel_1.place(x=XOPTION, y=ED+(1*STAIR)+3)
label_sobel_2 = Label(root, text ="BG :")
label_sobel_2.place(x=XOPTION+75, y=ED+(1*STAIR)+3)
combobox_sobel_var_1 = IntVar()
combobox_sobel_1 = ttk.Combobox(root, textvariable=combobox_sobel_var_1, width=2)
combobox_sobel_1['value'] = ([1, 2, 3, 4, 5])
combobox_sobel_1.place(x=XOPTION+30, y=ED+(1*STAIR)+3)
combobox_sobel_1.set(1)
combobox_sobel_var_2 = StringVar()
combobox_sobel_2 = ttk.Combobox(root, textvariable=combobox_sobel_var_2, width=2)
combobox_sobel_2['value'] = (['O','X'])
combobox_sobel_2.place(x=XOPTION+108, y=ED+(1*STAIR)+3)
combobox_sobel_2.set('O')
button_p9 = Button(root, text = "Sobel Operator", command=sobel, width =11)
button_p9.place(x=BX, y=ED+(1*STAIR))
##LoG Operator
label_log_1 = Label(root, text ="Size :")
label_log_1.place(x=XOPTION, y=ED+(2*STAIR)+3)
label_log_2 = Label(root, text ="σ :")
label_log_2.place(x=XOPTION+83, y=ED+(2*STAIR)+3)
combobox_log_var_1 = IntVar()
combobox_log_1 = ttk.Combobox(root, textvariable=combobox_log_var_1, width=2)
combobox_log_1['value'] = ([3, 5, 7, 9, 11, 13, 15, 17, 19])
combobox_log_1.place(x=XOPTION+38, y=ED+(2*STAIR)+3)
combobox_log_1.set(3)
combobox_log_var_2 = IntVar()
combobox_log_2 = ttk.Combobox(root, textvariable=combobox_log_var_2, width=3)
combobox_log_2['value'] = ([0.1, 0.5, 1, 5, 10])
combobox_log_2.place(x=XOPTION+107, y=ED+(2*STAIR)+3)
combobox_log_2.set(1)
button_p10 = Button(root, text = "LoG Operator", command=LoG, width =11)
button_p10.place(x=BX, y=ED+(2*STAIR))
##Canny Operator
label_canny_1 = Label(root, text ="L :")
label_canny_1.place(x=XOPTION, y=ED+(3*STAIR)+3)
label_canny_2 = Label(root, text ="H :")
label_canny_2.place(x=XOPTION+75, y=ED+(3*STAIR)+3)
combobox_canny_var_1 = IntVar()
combobox_canny_1 = ttk.Combobox(root, textvariable=combobox_canny_var_1, width=3)
combobox_canny_1['value'] = ([50, 100, 150, 200, 250])
combobox_canny_1.place(x=XOPTION+20, y=ED+(3*STAIR)+3)
combobox_canny_1.set(150)
combobox_canny_var_2 = IntVar()
combobox_canny_2 = ttk.Combobox(root, textvariable=combobox_canny_var_2, width=3)
combobox_canny_2['value'] = ([100, 150, 200, 250, 300])
combobox_canny_2.place(x=XOPTION+98, y=ED+(3*STAIR)+3)
combobox_canny_2.set(250)
button_p11 = Button(root, text = "Canny Operator", command=canny, width =11)
button_p11.place(x=BX, y=ED+(3*STAIR))




root.mainloop()




