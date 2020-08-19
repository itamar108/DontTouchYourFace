import tkinter as tk

DisappearingFactor = 50


# text="Change Label",
#                       , c

# background = 'black', foreground = "white"

class Example(tk.Frame):

    def __init__(self, parent):
        self.fading = False
        tk.Frame.__init__(self, parent, bg= "yellow")
        b = tk.Button(parent, text="Click to fade away", command=self.quit,
                      height= 40, width = 100, background= "blue",
                      foreground="black")
        b.pack(side = tk.BOTTOM)
        self.parent = parent
        self.parent.wm_attributes('-alpha', 0)

        self.build()

    def quit(self):
        self.fade_away()

    def build(self):
        self.fade_in()

    def fade_in(self):

        if self.fading:
            return
        alpha = self.parent.attributes("-alpha")

        # if recongized touche  ==== > return


        if alpha < 1:
            alpha += .01
            self.parent.attributes("-alpha", alpha)
            self.parent.after(DisappearingFactor, self.fade_in)

        else:
            return


    def fade_away(self):
        self.fading = True
        alpha = self.parent.attributes("-alpha")

        if alpha > 0:
            alpha -= .1
            self.parent.attributes("-alpha", alpha)
            self.parent.after(100, self.fade_away)
        else:
            self.fading = False
            self.parent.destroy()



def creating_transparent_window():
    root = tk.Tk()
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.09)
    root.mainloop()


def creating_disappearing_button():
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":

    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
