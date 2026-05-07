from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.geometry("1290x1920")
window.title("I.S.Y")

Img = Image.open('logo.jpg')
icon = ImageTk.PhotoImage(Img)

window.iconphoto(True, icon)
window.config(background="#EE0943")

photo = ImageTk.PhotoImage(Img)

label = Label(window,
              text="I.S.Y",
              font=('Arial', '60', 'bold'),
              fg='#000000',
              bg='#EE0943',
              image=photo,
              
              compound='bottom')

label.pack()
#label.place(x=50,y=50)

window.mainloop()

