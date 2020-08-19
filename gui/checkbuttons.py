import tkinter as tk
class myApp:
    def __init__(self,parent):
        self.parent = tk.Frame(parent)
        self.parent.configure(background="green")
        self.var = tk.BooleanVar()
        self.check_button = tk.Checkbutton(self.parent, text="Sound?",
                                      font=("David",20), variable=
        self.var)
        self.var.trace("w", self.callback)
        self.check_button.pack(side=tk.LEFT)
        self.parent.pack(side=tk.BOTTOM, fill= tk.BOTH)


    def callback(self,*args):
        if self.var.get():
            self.parent.configure(background= "pink")
        else:
            self.parent.configure(background="yellow")




root = tk.Tk()
myApp(root)
root.mainloop()
