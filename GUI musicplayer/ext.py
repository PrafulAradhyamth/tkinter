import math
import sys
import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("equilux")         # Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike.


menubar = Menu(root)
root.config(menu=menubar)



# Create the submenu


subMenu = Menu(menubar, tearoff=0)

playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    f=open('Playlist.txt',"w+")
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    f.write(filename)
    f.close()
    index += 1


menubar.add_cascade(label="Musique", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)


def New_playlist():
    tasktabs=ttk.Notebook(root)
    NewWorkLab=Label(root,text="Name: ")
    NewWorkLab.grid(row=0,column=2, sticky="W", padx=5,pady=5)
    NewWorkEntry=Entry(root)
    NewWorkEntry.grid(row=0,column=3,sticky="W", padx=5,pady=5)
    def AddNewWork():
        TabName=ttk.Frame(tasktabs)
        tasktabs.add(TabName,text=NewWorkEntry.get())
        NewTree= ttk.Treeview(TabName,height=40)
        NewTree['show'] = 'headings'
        NewTree["columns"]=("1")
        NewTree.column("1", width=200)
        NewTree.heading("1", text="Playlist")
        NewTree.grid(row=2,column=0,pady=10,padx=0)

    AddWorkButton=Button(root,text=' Add ', command=AddNewWork)
    AddWorkButton.grid(row=0,column=4, sticky="W", padx=5, pady=5)
    tasktabs.grid(row=1,column=0,columnspan=4,padx=5)

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    f=open('Playlist.txt',"w+")
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    f.write(filename)
    f.close()
    index += 1

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Playlist", menu=subMenu)
subMenu.add_command(label="Open Playlist",command=New_playlist)
subMenu.add_command(label="Create New",command=browse_file)


def about_us():
    tkinter.messagebox.showinfo('About le musique', 'Absofuckinlutly awesome')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us",command=about_us)



mixer.init()

root.geometry('809x408')
root.title("la musique")
root.iconbitmap('icon.ico')
background_image = PhotoImage(file='wall.png')
background_label = Label(root,image=background_image)
background_label.place(relwidth=1, relheight=1)






root.mainloop()
