# << Photoshop GUI >>
# from msilib.schema import ComboBox
from ImageRoad import GetImage
from ImageProcessing import Photoshop

from tkinter import *
from PIL import ImageTk, Image
from functools import partial

#Initialization
root = Tk()
root.title("Digital Image Processing Photoshop")
root.geometry("1500x1200")
root.resizable(True, True)

### Funtions ###
def get_image_g_jpg(name):
    global IMAGE, IMAGE_CV, NAME
    NAME = name
    label1.config(text="\n"+NAME+" 이미지\n")
    label1.place(x=250, y=5)

    IMAGE_CV = GetImage().get_gray_image_jpg(name)
    IMAGE = Image.fromarray(IMAGE_CV)
    IMAGE = ImageTk.PhotoImage(image=IMAGE)
    label2.config(image=IMAGE)
def get_image_g_bmp(name):
    global IMAGE, IMAGE_CV, NAME
    NAME = name
    label1.config(text="\n"+NAME+" 이미지\n")
    label1.place(x=250, y=5)

    IMAGE_CV = GetImage().get_gray_image_bmp(name)
    IMAGE = Image.fromarray(IMAGE_CV)
    IMAGE = ImageTk.PhotoImage(image=IMAGE)
    label2.config(image=IMAGE)
def get_image_c_bmp(name):
    global IMAGE, IMAGE_CV, NAME
    NAME = name
    label1.config(text="\n"+NAME+" 이미지\n")
    label1.place(x=250, y=5)

    IMAGE_CV = GetImage().get_color_image_bmp(name)
    IMAGE = Image.fromarray(IMAGE_CV)
    IMAGE = ImageTk.PhotoImage(image=IMAGE)
    label2.config(image=IMAGE)
def neg_trans():
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n"+NAME+" Negative Transformation\n")
        label1.place(x=250, y=5)
        IMAGE_CV = Photoshop().negative_transformation(IMAGE_CV)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def pow_law_trans(gamma):
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n"+NAME+" Power-Law Transformation γ="+str(gamma)+"\n")
        label1.place(x=250, y=5)
        IMAGE_CV = Photoshop().power_law_transformation(IMAGE_CV, gamma)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
def hist_equal():
    global IMAGE, IMAGE_CV, NAME
    try:
        label1.config(text="\n"+NAME+" Histogram Equalization\n")
        label1.place(x=250, y=5)
        IMAGE_CV = Photoshop().histogram_equalization(IMAGE_CV)
        IMAGE = Image.fromarray(IMAGE_CV)
        IMAGE = ImageTk.PhotoImage(image=IMAGE)
        label2.config(image=IMAGE)
    except:
        label1.config(text="\n선택된 사진이 없습니다")
### End of Funtions ###

label1 = Label(root, text = "\n편집할 사진을 선택해주세요")
label1.place(x=400, y=300)
label2 = Label(root, text = " ")
label2.place(x=250, y=50)

#Get Image
label3 = Label(root, text = "< HE IMAGE >")
label3.place(x=15, y=5)
label5 = Label(root, text="< Sample IMAGE >")
label5.place(x=1305, y=5)

#HE IMAGE
button_g1 = Button(root, text = "Fig0316(1)(top_left)", command=partial(get_image_g_jpg,"Fig0316(1)(top_left)"))
button_g1.place(x=10, y=25)
button_g2 = Button(root, text = "Fig0316(2)(2nd_from_top)", command=partial(get_image_g_jpg,"Fig0316(2)(2nd_from_top)"))
button_g2.place(x=10, y=50)
button_g3 = Button(root, text = "Fig0316(3)(third_from_top)", command=partial(get_image_g_jpg,"Fig0316(3)(third_from_top)"))
button_g3.place(x=10, y=75)
button_g4 = Button(root, text = "Fig0316(4)(bottom_left)", command=partial(get_image_g_jpg,"Fig0316(4)(bottom_left)"))
button_g4.place(x=10, y=100)
#Color IMAGE
button_c1 = Button(root, text = "airplane", command=partial(get_image_c_bmp,"airplane"))
button_c1.place(x=1300, y=25)
button_c2 = Button(root, text = "baboon", command=partial(get_image_c_bmp,"baboon"))
button_c2.place(x=1300, y=50)
button_c3 = Button(root, text = "barbara", command=partial(get_image_c_bmp,"barbara"))
button_c3.place(x=1300, y=75)
button_c4 = Button(root, text = "boats", command=partial(get_image_g_bmp,"boats"))
button_c4.place(x=1300, y=100)
button_c5 = Button(root, text = "BoatsColor", command=partial(get_image_c_bmp,"BoatsColor"))
button_c5.place(x=1300, y=125)
button_c6 = Button(root, text = "boy", command=partial(get_image_c_bmp,"boy"))
button_c6.place(x=1300, y=150)
button_c7 = Button(root, text = "bridge", command=partial(get_image_g_bmp,"bridge"))
button_c7.place(x=1300, y=175)
button_c8 = Button(root, text = "cameraman", command=partial(get_image_g_bmp,"cameraman"))
button_c8.place(x=1300, y=200)
button_c9 = Button(root, text = "clown", command=partial(get_image_g_bmp,"clown"))
button_c9.place(x=1300, y=225)
button_c10 = Button(root, text = "crowd", command=partial(get_image_g_bmp,"crowd"))
button_c10.place(x=1300, y=250)
button_c11 = Button(root, text = "goldhill", command=partial(get_image_c_bmp,"goldhill"))
button_c11.place(x=1300, y=275)
button_c12 = Button(root, text = "lenna_color", command=partial(get_image_c_bmp,"lenna_color"))
button_c12.place(x=1300, y=300)
button_c13 = Button(root, text = "man", command=partial(get_image_g_bmp,"man"))
button_c13.place(x=1300, y=325)
button_c14 = Button(root, text = "pepper", command=partial(get_image_c_bmp,"pepper"))
button_c14.place(x=1300, y=350)
button_c15 = Button(root, text = "sails", command=partial(get_image_c_bmp,"sails"))
button_c15.place(x=1300, y=375)
button_c16 = Button(root, text = "tank", command=partial(get_image_g_bmp,"tank"))
button_c16.place(x=1300, y=400)
button_c17 = Button(root, text = "truck", command=partial(get_image_g_bmp,"truck"))
button_c17.place(x=1300, y=425)
button_c18 = Button(root, text = "zelda", command=partial(get_image_g_bmp,"zelda"))
button_c18.place(x=1300, y=450)

#Image Processing
label4 = Label(root, text = "< Processing >")
label4.place(x=15, y=160)
button_p1 = Button(root, text = "Negative Trans.", command=neg_trans)
button_p1.place(x=10, y=190)
button_p2 = Button(root, text = "Power-Law Trans.(γ=0.4)", command=partial(pow_law_trans, 0.4))
button_p2.place(x=10, y=220)
button_p3 = Button(root, text = "Power-Law Trans.(γ=0.67)", command=partial(pow_law_trans, 0.67))
button_p3.place(x=10, y=250)
button_p4 = Button(root, text = "Power-Law Trans.(γ=1.5)", command=partial(pow_law_trans, 1.5))
button_p4.place(x=10, y=280)
button_p5 = Button(root, text = "Power-Law Trans.(γ=2.5)", command=partial(pow_law_trans, 2.5))
button_p5.place(x=10, y=310)
button_p6 = Button(root, text = "Histogram Equal.", command=hist_equal)
button_p6.place(x=10, y=340)


root.mainloop()




