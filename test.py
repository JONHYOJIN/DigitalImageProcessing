import numpy as np
import pandas as pd
import cv2
from tkinter import *

#객체 생성
root  = Tk()
#타이틀 설정
root.title("GUI Test")
#가로x세로 크기 설정
root.geometry("1000x700")

# #기본 버튼
# btn1 = Button(root, text="버튼1")
# btn1.pack()
# #여백 생성
# btn2 = Button(root, padx=10, pady=10, text="버튼2")
# btn2.pack()
# #버튼 크기 설정
# btn3 = Button(root, width=10, height=10, text="버튼3")
# btn3.pack()
# #버튼 색상 설정
# btn4 = Button(root, fg="green", bg="yellow", text="버튼4")
# btn4.pack()
# #동작하는 버튼
# def btncmd():
#     print("Button Clicked...!!")
# btn5 = Button(root, text="Button5", command = btncmd)
# btn5.pack()

#기본 레이블
# label1 = Label(root, text="버튼을 누르시면 'sample.png'가 나타납니다.")
# label1.pack()
#레이블에 이미지 넣기
# photo = PhotoImage(file="/Users/hyojin/DigitalImageProcessing/sample.png")
# label2 = Label(root, image = photo)
# label2.pack()

#샘플 프로그램
label1 = Label(root, text="버튼을 누르시면 'sample.png'가 나타납니다.")
label1.pack()
label2 = Label(root, text=" ")
label2.pack()

def get_sample_img():
    #레이블 변경
    label1.config(text="'sample.png'입니다.")

    global sample_png
    sample_png = PhotoImage(file="/Users/hyojin/DigitalImageProcessing/sample.png")
    label2.config(image=sample_png)

btn = Button(root, text="Button", command=get_sample_img)
btn.pack()

root.mainloop()

# src = cv2.imread("/Users/hyojin/DigitalImageProcessing/sample.jpg", cv2.IMREAD_COLOR)

# cv2.imshow("source", src)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
