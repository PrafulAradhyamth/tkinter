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


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Playlist", menu=subMenu)
subMenu.add_command(label="Open Playlist")
subMenu.add_command(label="Create New")


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

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)



delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=LEFT)


lengthlabel = ttk.Label(root, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(root, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Please check again.')




def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def reverse_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
 
    

playPhoto = PhotoImage(file='play.png')
playBtn = Button(root, image=playPhoto,bg='black', command=play_music)
playBtn.place(relx=0.78,rely=0.63)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = Button(root, image=stopPhoto,bg='black', command=stop_music)
stopBtn.place(relx=0.71,rely=0.628)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = Button(root, image=pausePhoto,bg='black', command=pause_music)
pauseBtn.place(relx=0.46,rely=0.615)

reversePhoto = PhotoImage(file='reverse.png')
reverseBtn = Button(root, image=reversePhoto,bg='black')
reverseBtn.place(relx=0.64,rely=0.629)

recordPhoto = PhotoImage(file='record.png')
recordBtn = Button(root, image=recordPhoto,bg='black')
recordBtn.place(relx=0.38,rely=0.62)

rewindPhoto = PhotoImage(file='rewind.png')
rewindBtn = Button(root, image=rewindPhoto,bg='black')
rewindBtn.place(relx=0.568,rely=0.629)

forwardPhoto = PhotoImage(file='forward.png')
forwardBtn = Button(root, image=forwardPhoto,bg='black')
forwardBtn.place(relx=0.85,rely=0.629)


mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='volume.png')
volumeBtn = Button(root, bg='black',image=volumePhoto, command=mute_music)
volumeBtn.place(relx=0.51,rely=0.07)

scale = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL,length=440)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.place(relx=0.38,rely=0.9)



statusbar = Label(root, text="Bonjour", relief=SUNKEN, anchor=W)
statusbar.place(relx=0.4,rely=0.4)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()