from tkinter import *
raiz = Tk()
raiz.title("Fisioterapia en casa")
miframe = Frame()
miframe.pack(fill="both",expand=True)
miframe.config(bg="white")
miframe.config(width=1200,height=750)
imagen_logo = PhotoImage(file="logo_final.png")
milabel = Label(miframe,image=imagen_logo)
milabel.place(x=250,y=20)

raiz.mainloop()