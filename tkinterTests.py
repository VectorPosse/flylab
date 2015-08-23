__author__ = 'Kira'
from tkinter import *
bottom = Tk()

def windowSettings(windowName, height, width):
    windowName.wm_title("Fly Mater")
    h = height
    w = width
    ws = windowName.winfo_screenwidth()
    hs = windowName.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    windowName.geometry('%dx%d+%d+%d' % (w, h, x, y))

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

windowSettings(bottom, 400, 400)
scrollbar = Scrollbar(bottom)
scrollbar.pack(side=RIGHT, fill=Y)

canvas1 = Canvas(bottom, relief = FLAT, width = 400, height = 400, yscrollcommand=scrollbar.set)
canvas1.pack()
#listbox = Listbox(bottom, yscrollcommand=scrollbar.set)
for i in range(100):
    me = Button(canvas1, text=i).pack()
    button_window = canvas1.create_window(0,0,window=me)

scrollbar.config(command=canvas1.yview)

def quitC():
    bottom.destroy()

quit = Button(bottom, text="close", command = quitC)
quit.pack()

bottom.mainloop()

master = Tk()

listbox = Listbox(master)
listbox.pack()

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

master.mainloop()