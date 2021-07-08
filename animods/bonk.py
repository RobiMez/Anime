# from tkinter import *
# from PIL import ImageTk,Image
# root = Tk()
# root.title('Anicons | Stay Degenerate ✨')
# root.geometry('800x800')



# poster_frame       = LabelFrame(root, text="Poster",padx =5 ,pady=5)
# poster_frame       .grid(row=0,column=0,padx =10 ,pady=10,sticky="NESW")
        
# data = StringVar()
# data.set("No data yet .. select a folder to view its state.")
# data_label = Label(poster_frame,textvar=data,wraplength=300, justify="center")
# data_label.grid(row=0 ,column=0)  


# # create a canvas to show image on
# canvas_for_image = Canvas(poster_frame, borderwidth=0, highlightthickness=0)
# canvas_for_image.grid(row=0, column=2, sticky='nesw', padx=0, pady=0)

# # create image from image location resize it to 200X200 and put in on canvas
# image = Image.open('def.png')
# canvas_for_image.image = ImageTk.PhotoImage(image)
# canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='n')


# bg = PhotoImage(file='def.png')
# labb = Label(root,image=bg)
# labb.place(x=0,y=0,relwidth=1,relheight=1)
# root.mainloop()


class culs:
    HEADER = '\033[96m'
    OKBLUE = '\033[90m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
print(f"{culs.BOLD}│▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ lorem ipsum ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒│{culs.ENDC}")