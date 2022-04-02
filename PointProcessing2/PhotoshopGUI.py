# << Photoshop GUI >>
from ImageRoad import GetImage
from ImageProcessing import PointProcessing, AreaProcessing

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from functools import partial

#HE test
hetest = ["Fig0316(1)(top_left).jpg","Fig0316(2)(2nd_from_top).jpg","Fig0316(3)(third_from_top).jpg","Fig0316(4)(bottom_left).jpg"]
#실습영상 Gray-Scale
samplecs = ["airplane.bmp","baboon.bmp","barbara.bmp","BoatsColor.bmp","boy.bmp","goldhill.bmp","lenna_color.bmp","pepper.bmp","sails.bmp"]
#실습영상 Color-Scale
samplegs = ["boats.bmp","bridge.bmp","cameraman.bmp","clown.bmp","crowd.bmp","man.bmp","tank.bmp","truck.bmp","zelda.bmp"]

#Initialization
root = Tk()
root.title("Digital Image Processing Photoshop")
root.geometry("1400x1200")
root.resizable(True, True)

### Funtions ###
def get_selected_image(scale):
    global IMAGE, IMAGE_CV, NAME
    NAME = combobox_p1_var.get()
    label1.config(text="\n[ "+NAME+" ] 이미지\n")
    label1.place(x=350, y=5)
    if scale=="gray":
        IMAGE_CV = GetImage().get_gray_image(NAME)
    elif scale=="color":
        IMAGE_CV = GetImage().get_color_image(NAME)
    IMAGE = Image.fromarray(IMAGE_CV)
    IMAGE = ImageTk.PhotoImage(image=IMAGE)
    label2.config(image=IMAGE)
def neg_trans():
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n[ "+NAME+" ] Negative Transformation\n")
        label1.place(x=350, y=5)
        IMAGE_CV = PointProcessing().negative_transformation(IMAGE_CV)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def pow_law_trans(gamma):
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n[ "+NAME+" ] Power-Law Transformation γ="+str(gamma)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = PointProcessing().power_law_transformation(IMAGE_CV, gamma)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def hist_equal():
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n[ "+NAME+" ] Histogram Equalization\n")
        label1.place(x=350, y=5)
        IMAGE_CV = PointProcessing().histogram_equalization(IMAGE_CV)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
        if(NAME):
            label1.config(text="\nColor 사진은 지원되지 않습니다")
def mean_ft(size):
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n[ "+NAME+" ] Mean Filter size="+str(size)+"x"+str(size)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().mean_filter(IMAGE_CV, size)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def med_ft(size):
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n[ "+NAME+" ] Median Filter size="+str(size)+"x"+str(size)+"\n")
        label1.place(x=350, y=5)
        IMAGE_CV = AreaProcessing().median_filter(IMAGE_CV, size)
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
combobox_p1['value'] = (sum([hetest, samplegs, samplecs], []))
combobox_p1.place(x=10, y=25)

button_select_image_gray = Button(root, text = "흑백 선택", command=partial(get_selected_image, "gray"))
button_select_image_gray.place(x=220, y=20)
button_select_image_color = Button(root, text = "컬러 선택", command=partial(get_selected_image, "color"))
button_select_image_color.place(x=220, y=45)

#Image Processing
label4 = Label(root, text = "< Processing >")
label4.place(x=15, y=90)
button_p1 = Button(root, text = "Negative Trans.", command=neg_trans)
button_p1.place(x=10, y=120)
button_p2 = Button(root, text = "Power-Law Trans.(γ=0.4)", command=partial(pow_law_trans, 0.4))
button_p2.place(x=10, y=150)
button_p3 = Button(root, text = "Power-Law Trans.(γ=0.67)", command=partial(pow_law_trans, 0.67))
button_p3.place(x=10, y=180)
button_p4 = Button(root, text = "Power-Law Trans.(γ=1.5)", command=partial(pow_law_trans, 1.5))
button_p4.place(x=10, y=210)
button_p5 = Button(root, text = "Power-Law Trans.(γ=2.5)", command=partial(pow_law_trans, 2.5))
button_p5.place(x=10, y=240)
button_p6 = Button(root, text = "Histogram Equal.", command=hist_equal)
button_p6.place(x=10, y=270)
button_p7 = Button(root, text = "Mean Filter 3x3", command=partial(mean_ft, 3))
button_p7.place(x=10, y=300)
button_p8 = Button(root, text = "Mean Filter 5x5", command=partial(mean_ft, 5))
button_p8.place(x=10, y=330)
button_p9 = Button(root, text = "Median Filter 3x3", command=partial(med_ft, 3))
button_p9.place(x=10, y=360)
button_p10 = Button(root, text = "Median Filter 5x5", command=partial(med_ft, 5))
button_p10.place(x=10, y=390)


root.mainloop()




