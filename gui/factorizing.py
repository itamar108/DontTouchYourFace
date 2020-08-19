from tkinter import Tk
from tkinter import ttk

root = Tk()

style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="white")

l1 = ttk.Label(text="This is the best label in the world", style="BW.TLabel")
l1.pack()


root.mainloop()
