# << Photoshop GUI >>
from ImageRoad import GetImage
from ImageProcessing import PointProcessing

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from functools import partial

#HE test
hetest = ["Fig0316(1)(top_left)","Fig0316(2)(2nd_from_top)","Fig0316(3)(third_from_top)","Fig0316(4)(bottom_left)"]
#실습영상 Gray-Scale
samplecs = ["airplane","baboon","barbara","BoatsColor","boy","goldhill","lenna_color","pepper","sails"]
#실습영상 Color-Scale
samplegs = ["boats","bridge","cameraman","clown","crowd","man","tank","truck","zelda"]

#Initialization
root = Tk()
root.title("Digital Image Processing Photoshop")
root.geometry("1400x1200")
root.resizable(True, True)

### Funtions ###
def get_selected_image():
    global IMAGE, IMAGE_CV, NAME
    NAME = combobox_p1_var.get()
    label1.config(text="\n[ "+NAME+" ] 이미지\n")
    label1.place(x=300, y=5)
    if NAME in hetest:  
        IMAGE_CV = GetImage().get_gray_image_jpg(NAME)
    elif NAME in samplegs:
        IMAGE_CV = GetImage().get_gray_image_bmp(NAME)
    elif NAME in samplecs:
        IMAGE_CV = GetImage().get_color_image_bmp(NAME)
    IMAGE = Image.fromarray(IMAGE_CV)
    IMAGE = ImageTk.PhotoImage(image=IMAGE)
    label2.config(image=IMAGE)
def neg_trans():
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n[ "+NAME+" ] Negative Transformation\n")
        label1.place(x=300, y=5)
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
        label1.place(x=300, y=5)
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
        label1.place(x=300, y=5)
        IMAGE_CV = PointProcessing().histogram_equalization(IMAGE_CV)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
        if(NAME in samplecs):
            label1.config(text="\nColor 사진은 지원되지 않습니다")
### End of Funtions ###

#User Interface
label1 = Label(root, text = "\n편집할 사진을 선택해주세요")
label1.place(x=450, y=300)
label2 = Label(root, text = " ")
label2.place(x=300, y=50)

#Get Image
label3 = Label(root, text = "< IMAGE >")
label3.place(x=15, y=5)

combobox_p1_var = StringVar()
combobox_p1 = ttk.Combobox(root, textvariable=combobox_p1_var)
combobox_p1['value'] = (sum([hetest, samplegs, samplecs], []))
combobox_p1.place(x=10, y=25)

button_select_image = Button(root, text = "선택", command=get_selected_image)
button_select_image.place(x=220, y=20)

#Image Processing
label4 = Label(root, text = "< Processing >")
label4.place(x=15, y=60)
button_p1 = Button(root, text = "Negative Trans.", command=neg_trans)
button_p1.place(x=10, y=90)
button_p2 = Button(root, text = "Power-Law Trans.(γ=0.4)", command=partial(pow_law_trans, 0.4))
button_p2.place(x=10, y=120)
button_p3 = Button(root, text = "Power-Law Trans.(γ=0.67)", command=partial(pow_law_trans, 0.67))
button_p3.place(x=10, y=150)
button_p4 = Button(root, text = "Power-Law Trans.(γ=1.5)", command=partial(pow_law_trans, 1.5))
button_p4.place(x=10, y=180)
button_p5 = Button(root, text = "Power-Law Trans.(γ=2.5)", command=partial(pow_law_trans, 2.5))
button_p5.place(x=10, y=210)
button_p6 = Button(root, text = "Histogram Equal.", command=hist_equal)
button_p6.place(x=10, y=240)


root.mainloop()




