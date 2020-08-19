import tkinter as tk
root = tk.Tk()


img = tk.PhotoImage("/Users/itamar/Desktop/mygui/myface.png")
print(img)

label_img = tk.Label(root, image=img)
label_img.image = img
label_img.pack(side=tk.TOP)
b = tk.Button(root, text = "click here", font= ("Helvetica", 20))
b.pack(side=tk.BOTTOM)
root.mainloop()