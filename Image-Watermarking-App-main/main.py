from tkinter import *
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import ImageTk, Image, ImageGrab


def drag_image(file, strip):
    global canvas1, new_img
    if strip:
        file = file.strip('{}')

    btn_frame.destroy()
    btn.destroy()
    img = Image.open(file)
    img_resize = img.resize((700, 500))
    new_img = ImageTk.PhotoImage(img_resize)

    canvas1 = Canvas(root, width=700, height=500)
    canvas1.grid(column=0, row=0)

    img_container = canvas1.create_image(350, 250, image=new_img)
    next_window()
    canvas1.config(img_container)


def open_file(strip):
    f_types = [('All', ('*.jpg', '*.png', '*.svg'))]
    filename = filedialog.askopenfile(filetypes=f_types)
    drag_image(filename.name, strip)


def save():
    x = canvas1.winfo_rootx() + 25
    y = canvas1.winfo_rooty() + 25
    x1 = x + canvas1.winfo_width() + 140
    y1 = y + canvas1.winfo_height() + 120
    snapshot = ImageGrab.grab((x, y, x1, y1))
    snapshot.save('new_img.png')


def water_mark():
    f_types = [('All', ('*.jpg', '*.png', '*.svg'))]
    filename = filedialog.askopenfile(filetypes=f_types)
    img = Image.open(filename.name)
    img1 = img.resize((40, 40))
    wm_img = ImageTk.PhotoImage(img1)

    img_container = canvas1.create_image(350, 250, image=new_img)
    img_container1 = canvas1.create_image(645, 460, image=wm_img)
    canvas1.config(img_container)
    canvas1.config(img_container1)


def paste_text():
    global text_container
    txt = entry.get()
    text_container = canvas1.create_text(645, 460, text=txt, font=('Ariel', 12, 'normal'))
    canvas1.itemconfig(text_container)


def color(color):
    if color == 'red':
        canvas1.itemconfig(text_container, fill='red')
    elif color == 'black':
        canvas1.itemconfig(text_container, fill='black')


def location(loc):
    if loc == 'left':
        canvas1.moveto(text_container, x=10, y=460)
    elif loc == 'right':
        canvas1.moveto(text_container, x=645, y=460)


def next_window():
    global entry
    frame = Frame(root)
    frame.grid(column=0, row=1, pady=10, sticky=W)

    btn1 = Button(frame, text='Watermark Image', font=('Ariel', 11, 'normal'), fg='white', bg='blue', command=water_mark)
    btn1.grid(column=0, row=0, columnspan=2, sticky=W)

    lb = Label(frame, text='Write Text:', font=('Ariel', 12, 'normal'))
    lb.grid(column=0, row=1, pady=10)

    entry = Entry(frame)
    entry.grid(column=1, row=1, padx=10)

    btn2 = Button(frame, text='Add', font=('Ariel', 11, 'normal'), fg='white', bg='blue', command=paste_text)
    btn2.grid(column=2, row=1)

    lb1 = Label(frame, text='Change Watermark Color:', font=('Ariel', 12, 'normal'))
    lb1.grid(column=0, row=2, sticky=W, columnspan=2)

    btn3 = Button(frame, text='Red', font=('Ariel', 11, 'normal'), fg='white', bg='red', command=lambda: color('red'))
    btn3.grid(column=2, row=2)

    btn4 = Button(frame, text='Black', font=('Ariel', 11, 'normal'), fg='white', bg='black', command=lambda: color('black'))
    btn4.grid(column=3, row=2, padx=10)

    lb2 = Label(frame, text='Change Watermark Position:', font=('Ariel', 12, 'normal'))
    lb2.grid(column=0, row=3, sticky=W, columnspan=2, pady=10)

    btn5 = Button(frame, text='Bottom Left', font=('Ariel', 11, 'normal'), fg='white', bg='blue', command=lambda: location('left'))
    btn5.grid(column=2, row=3)

    btn6 = Button(frame, text='Bottom Right', font=('Ariel', 11, 'normal'), fg='white', bg='blue', command=lambda: location('right'))
    btn6.grid(column=3, row=3, padx=10)

    btn7 = Button(frame, text='Save', font=('Ariel', 11, 'normal'), fg='white', bg='green', command=save)
    btn7.grid(column=1, row=4)
    

root = TkinterDnD.Tk()
root.title('Watermark App')
root.config(padx=20, pady=20)

canvas = Canvas(root, width=400, height=400)
canvas.create_rectangle(10,10,390,390, dash=(5, 1), outline='blue')
canvas.create_text(200, 200, text='Drag and drop image', fill='blue', font=('Ariel', 16, 'bold'))
canvas.grid(column=0, row=0)

btn_frame = Frame(root, bd=2, bg='blue', relief='flat')
btn_frame.place(x=150, y=220)

btn = Button(btn_frame, text='Upload Image', font=('Ariel', 12, 'normal'), fg='white', bg='blue', border=0, command=lambda: open_file(False))
btn.grid()

# Drop file
canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', lambda i: drag_image(i.data, True))


root.mainloop()
