from tkinter import *
from PIL import Image, ImageTk
import tkinter.filedialog as fd
import cv2
import math
import numpy as np
import os

window = Tk()
window.title("Обнаружение наклона камер")
window.iconbitmap("icon.ico")
window.geometry('1200x800')
window.resizable(False, False)

img = None

def deffect(image):
    if image == None:
        return 3

    image = np.array(image)
    image = image[:, :, ::-1].copy()

    image = image[20:480, 0:1000]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=100,  # Min number of votes for valid line
        minLineLength=100,  # Min allowed length of line
        maxLineGap=5  # Max allowed gap between line for joining them
    )

    angles = []
    for points in lines:
        x1, y1, x2, y2 = points[0]
        angle = math.degrees(math.atan((y2 - y1) / (x2 - x1)))
        angle = abs(angle)
        angles.append(angle)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    print(angles)
    sred = sum(angles) / len(angles)
    print(sred)
    if sred <= 5:
        return 2
    else:
        return 1


def button_defect():
    res = deffect(img)
    if res == 1:
        lbl_def.config(text="Камера наклонена", fg="#FF0000")
    elif res == 2:
        lbl_def.config(text="Камера стоит ровно", fg="#000000")
    else:
        lbl_def.config(text="Выберите изображение", fg="#000000")


def button_askimage():
    lbl_def.config(text="Выберите изображение", fg="#000000")

    filetypes = (("Изображение", "*.jpg *.gif *.png"),)
    filename = fd.askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)

    global img
    global label

    img = Image.open(filename)
    if img.format != 'PNG':
        filename = filename[:-3]
        filename += 'png'
        img.save(filename)
        os.remove(filename)

    fixed_width = 700
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    img = img.resize((fixed_width, height_size))

    image = ImageTk.PhotoImage(img)
    label.image = image
    label['image'] = label.image


btn_askImage = Button(window, text="Выбрать изображение", command=button_askimage)
btn_askImage.place(x=1000, y=50, width=150, height=50)

btn_def = Button(window, text="Определить дефект", command=button_defect)
btn_def.place(x=1000, y=150, width=150, height=50)

lbl_def = Label(window, text="Определите дефект")
lbl_def.place(x=1000, y=250, width=150, height=50)

canvas = Canvas(window, width=900, height=500, bd=0, highlightthickness=0)
canvas.place(anchor=NW, x=0, y=0)

label = Label(window)
label.place(x=50, y=50)

window.mainloop()
