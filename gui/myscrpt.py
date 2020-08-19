# from tkinter import *
#
#
# class App:
#     def __init__(self, parent):
#         self.frame = Frame(parent)
#         self.frame.pack(fill=BOTH)
#
#         def on_button():
#             print("Called")
#             self.frame.forget()
#             self.newFrame()
#
#         self.printButton = Button(self.frame, text="Make a new button appear",
#                                   command=on_button)
#         self.printButton.pack(side=LEFT)
#
#         self.quitButton = Button(self.frame, text="Quit",
#                                  command=self.frame.quit)
#         self.quitButton.pack(side=LEFT)
#
#
#     def newFrame(self):
#         print("Debug")
#         frame2 = Frame()
#         frame2.pack(fill=BOTH)
#         self.b2 = Button(frame2, text="Yo", command=print())
#         self.b2.pack()
#
#
#     def printMessage(self):
#         print("Third button")
#
#
# root = Tk()
# boats = App(root)
# root.mainloop()


from tkinter import *
from tkinter.filedialog import askopenfilename


def NewFile():
    print("New File!")


def OpenFile():
    name = askopenfilename()
    print(name)


def About():



root = Tk()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="help_key...", command=About)

mainloop()