from __future__ import print_function, unicode_literals
import os
import os.path
from os import path
import glob
import time
import io
import tempfile
import re
import asyncio

import requests  # import requests to download urls
from tkinter import Tk, filedialog, Frame, LabelFrame, Entry, StringVar, Radiobutton,W,E,N,S, NSEW, Label, Listbox, CENTER, NO, END, OptionMenu, PhotoImage, Button, Scrollbar,HORIZONTAL,VERTICAL
from tkinter import ttk
from tkinter.messagebox import showinfo

from jikanpy import Jikan  # import jikan for anime poster urls
from PIL import Image,ImageTk  # import pil for image conversions
from pprint import pprint

class anicon():
    def __init__(self):
        print("----------------------\n\n\n\nInitiation")
        self.ji = Jikan()
        self.root = Tk()
        app_width = 1080
        app_height = 720
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width/2)
        y = (screen_height / 2) - (app_height/2)
        # window size and positioning
        self.root.geometry(f'{app_width}x{app_height}+{int(x/2)}+{int(y/2)}')
        self.root.title('Anicons | Stay a Degenerate ✨')
        

    def initialize_display(self):


        self.tree_frame       = LabelFrame(self.root, text="Tree Structure",padx =5 ,pady=5)
        self.tree_frame       .grid(row=0,column=0,padx =10 ,pady=10,sticky="NESW")
        
        self.data_frame       = LabelFrame(self.root, text="Selected data",padx =5 ,pady=5 )
        self.data_frame       .grid(row=0,column=20,padx =10 ,pady=10,sticky="NESW")
        
        self.data = StringVar()
        self.data.set("No data yet .. select a folder to view its state. ")
        self.data_label = Label(self.data_frame,textvar=self.data,wraplength=300, justify="center")
        self.data_label.grid(row=0 ,column=0)  
        
        
        
        
        
        


        
        bg = PhotoImage(file='def.png')
        
        labb = Label(self.data_frame,image=bg)
        labb.place(x=0,y=0,relwidth=1,relheight=1)
        
        
        
        
        # self.tree = ttk.Treeview(self.tree_frame)
        
        self.tree_scrollbar  = Scrollbar(self.tree_frame)
        self.tree_scrollbar.grid(row=0,column=6,rowspan=100,sticky=NSEW)
        
        self.tree = ttk.Treeview(self.tree_frame,height=30,yscrollcommand=self.tree_scrollbar.set)
        self.tree['columns'] = ("data",)
        self.tree_scrollbar.config(command= self.tree.yview)
        
        self.tree.column('#0'         ,width=280 ,anchor=CENTER,stretch=NO)
        self.tree.column('data'        ,width=80,anchor=CENTER)
        
        self.tree.heading('#0'            ,text='Directory')
        self.tree.heading('data'           ,text='Icons')
        
        self.tree.grid(row=0,column=0,rowspan=100,columnspan=100)
        self.tree.bind('<<TreeviewSelect>>', self.selection_logic)
        
        
    def render_tree(self,path):
        # Treeview 
        self.tree_styles = ttk.Style()
        self.tree_styles.theme_use('clam')
        self.tree_styles.configure(
            "Treeview",
            background='#fdfdff',
            rowheight=20,
        )
        self.tree_styles.map('Treeview',
                background = [('selected','steelblue')])
        
        abspath = os.path.abspath(path)

        root_node = self.tree.insert('', 'end',text=abspath,values=('Root',), open=True)
        self.process_directory(root_node, abspath)
        
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            
            # print(os.path.exists(os.path.join(abspath,'an.ico')))
            if os.path.exists(os.path.join(abspath,'an.ico')):
                # print(os.path.join(abspath,'an.ico'))
                oid = self.tree.insert(parent, 'end', text=p,values=('yay',abspath), open=False)
            else :
                oid = self.tree.insert(parent, 'end', text=p,values=('-',), open=False)
            
            if isdir:
                self.process_directory(oid, abspath)
    
    def selection_logic(self,event):

        for selected_item in self.tree.selection():
            # dictionary
            self.selected_item = self.tree.item(selected_item)
            print(self.selected_item)
            print(self.selected_item['values'])
            if self.selected_item['values'][0] == 'yay':
                # poster_img = Image.open(self.selected_item['values'][1]+'\\an.ico')
                # poster_img_tk = ImageTk.PhotoImage(poster_img)
                # print(poster_img)
                # poster_img.save()
                pass
                # self.image_label.config(image=poster_img)
            self.data.set(self.selected_item)


    def get_names(self,aname,lim):
        try:
            anime_data = ji.search(search_type='anime', query=aname,parameters={'limit' :lim})
        except requests.exceptions.ConnectionError:
            anime_data = None
            print('[ >~< ] No internet connection detected ')
            print('\n Sorry but this program requires access to the internet\n in order to download the cover arts for the folders.\n')
        if anime_data != None:

            return anime_data['results']
        else :
            return None


    def download_poster(self,image_url,out_dir):
        print("[ ^>^ ] Downloading cover art :")
        buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            downloaded = 0
            filesize = int(r.headers['content-length'])
            for chunk in r.iter_content(chunk_size=1024):
                downloaded += len(chunk)
                buffer.write(chunk)
            buffer.seek(0)
            print()
            i = Image.open(io.BytesIO(buffer.read()))
            i.save(os.path.join(out_dir, 'image.jpg'), quality=100)
        buffer.close()

    def iconify_directory(self,dir):
        print(f'iconify dir : {dir}')
        pass


ani = anicon()
# ani.update_check()
ani.initialize_display()
ani.render_tree('./')
ani.root.mainloop()
print('Execution Finish\n\n\n\n----------------------')