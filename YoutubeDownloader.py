from pytube import YouTube
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from urllib.request import urlopen
import sys, os, ffmpeg, threading, pyperclip
from random import randint
from playsound import playsound
import tkinter.ttk as ttk
from tkinter import filedialog

root = Tk()
root.geometry("650x400")
root.iconbitmap("icon.ico")
root.title("YoutubeDownloader")

# Zdjecie
default_image = ImageTk.PhotoImage(Image.open("GGYD.png"))

# KoniecPobierania
Finish1 = "Finish.mp3"

global selected
selected = pyperclip.paste()

# Menu PPM
m = Menu(root, tearoff=0)
m.add_command(label="Wytnij", command=lambda: cut_text(False))
m.add_command(label="Kopiuj", command=lambda: copy_text(False))
m.add_separator()
m.add_command(label="Wklej", command=lambda: paste_text(False))

# Default Directory
my_dir = "Pobrane"

# Popup Methods
def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def cut_text(e):
    global selected
    if TextBox.selection_get():
        # Grab selected text
        selected = pyperclip.copy(TextBox.selection_get())
        # Delete selected text
        TextBox.delete("sel.first", "sel.last")


def copy_text(e):
    global selected
    if TextBox.selection_get():
        # Grab selected text
        selected = pyperclip.copy(TextBox.selection_get())

def paste_text(e):
    selected = pyperclip.paste()
    position = TextBox.index(INSERT)
    TextBox.insert(position, selected)



# Main Methods

def download(link):

    # MainFunction
    global Pobieranie
    Pobieranie = YouTube(str(link), on_progress_callback=progress, on_complete_callback=complete)

    global LabelFrameImg
    global LabelFrameOpt
    global LabelFR
    global LabelProgress
    global LabelDirectory
    global DirectoryCheck

    LabelFrameImg.place_forget()
    LabelFrameOpt.place_forget()
    LabelFR.place_forget()

    # Sound
    global sound
    sound = True

    global var
    var = StringVar()

    def soundmethod():
        global sound
        if var.get() == "On":
            sound = True
            #print(var.get())
        else:
            sound = False
            #print(var.get())


    # Menu PPM
    m = Menu(root, tearoff=0)
    m.add_command(label="Wytnij", state=DISABLED, command=lambda: cut_text(False))
    m.add_command(label="Kopiuj", state=DISABLED, command=lambda: copy_text(False))
    m.add_separator()
    m.add_command(label="Wklej", state=DISABLED, command=lambda: paste_text(False))

    def do_popup(event):
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    # Miniatura
    mf = YouTube(link)
    imageurl = mf.thumbnail_url
    u = urlopen(imageurl)
    img = Image.open(u).resize((178,100))
    photo = ImageTk.PhotoImage(img)


    # Pierwszy rząd
    LabelFR = Label(root)
    LabelFR.place(x=0, y=20)

    # Miniaturka
    LabelFrameImg = LabelFrame(root)
    LabelFrameImg.place(x=35, y=70)

    # Opcje Pobierania
    LabelFrameOpt = LabelFrame(root, padx=10)
    LabelFrameOpt.place(x=230, y=70)

    # Information
    LabelInfo = LabelFrame(root, padx=10, pady=13)
    LabelInfo.place(x=35, y=180)

    # Restart
    LabelRestart = LabelFrame(root, padx=10, pady=13)
    LabelRestart.place(x=35, y=255)

    # Age_Restrict
    LabelAge = LabelFrame(root, padx=10, pady=16)
    LabelAge.place(x=174, y=255)

    # Filesize
    LabelFilesize = LabelFrame(root, padx=10)
    LabelFilesize.place(x=450, y=70)

    # LabelProgress
    LabelProgress = LabelFrame(root, padx=10)
    LabelProgress.place(x=35, y=314)

    # LabelDirectory
    LabelDirectory = LabelFrame(root, padx=10)
    LabelDirectory.place(x=35, y=350)

    TextInfo = Label(LabelFR, text="Tutaj dawaj LINK! -->")
    TextInfo.grid(row=0, column=0, padx=10)

    TextBox = Entry(LabelFR, width=50)
    TextBox.insert(0, link)
    TextBox.grid(row=0, column=1, padx=10)

    TextBox.bind("<Button-3>", do_popup)

    TextSubmit = Button(LabelFR, text="ENTER!!!", width=10, state=DISABLED)
    TextSubmit.grid(row=0, column=2, padx=10)

    # VideoPhoto
    Label_Min = Label(LabelFrameImg, image=photo)
    Label_Min.image = photo
    Label_Min.grid()

    # HighRes
    TextHighRes = Label(LabelFrameOpt, text="MP4 1080p (VERY SLOW)")
    TextHighRes.grid(row=0, column=0)

    ButtonHighRes = Button(LabelFrameOpt, text="Pobierz", cursor="hand2", command=lambda:download2(0))
    ButtonHighRes.grid(row=0, column=1)

    # 720p Res
    TextHigRes = Label(LabelFrameOpt, text="MP4 720p")
    TextHigRes.grid(row=1, column=0)

    ButtonHigRes = Button(LabelFrameOpt, text="Pobierz", cursor="hand2", command=lambda:download2(1))
    ButtonHigRes.grid(row=1, column=1)

    # LowRes
    TextLowRes = Label(LabelFrameOpt, text="MP4 360p")
    TextLowRes.grid(row=2, column=0)

    ButtonLowRes = Button(LabelFrameOpt, text="Pobierz", cursor="hand2", command=lambda:download2(2))
    ButtonLowRes.grid(row=2, column=1)

    # Audio
    TextAudio = Label(LabelFrameOpt, text="MP3 160kbps")
    TextAudio.grid(row=3, column=0)

    ButtonAudio = Button(LabelFrameOpt, text="Pobierz", cursor="hand2", command=lambda:download2(3))
    ButtonAudio.grid(row=3, column=1)

    # Informacje
    Title = Label(LabelInfo, text=Pobieranie.title)
    Title.grid(row=0, column=0)

    Length = Label(LabelInfo, text=f"Długość: {round(Pobieranie.length / 60,2)} minut")
    Length.grid(row=1, column=0)

    # Restart
    ButtonRestart = Button(LabelRestart, text="Pobierz inny filmik!", cursor="hand2", command=RestartProgram, state=DISABLED)
    ButtonRestart.grid(row=0, column=0)

    # Sound
    SoundCheck = Checkbutton(root, text="Powiadomienie", command=soundmethod, variable=var, onvalue="On", offvalue="Off")
    SoundCheck.place(x=425, y=272)

    # Directory
    DirectoryChange = Button(LabelDirectory, text="Zmień lokalizację", command=lambda:Directory())
    DirectoryChange.grid(row=0, column=0)
    DirectoryCheck = Label(LabelDirectory, text=my_dir)
    DirectoryCheck.grid(row=0, column=1)

    # Age Restricted
    if Pobieranie.age_restricted:
        AgeLabel = Label(LabelAge, text="FILMIK Z OGRANICZENIEM WIEKOWYM", fg="red")
        AgeLabel.grid(row=0, column=0)
    else:
        AgeLabel = Label(LabelAge, text="FILMIK BEZ OGRANICZENIA WIEKOWEGO", fg="green")
        AgeLabel.grid(row=0, column=0)

    # Resolution Availability ////

    bool1080p = bool(Pobieranie.streams.filter(res="1080p", progressive=False))
    bool720p = bool(Pobieranie.streams.get_by_resolution("720p"))
    bool360p = bool(Pobieranie.streams.get_by_resolution("360p"))
    boolMP3 = bool(Pobieranie.streams.filter(abr="160kbps", progressive=False))

    if bool1080p:
        Ava1080p = Label(LabelFilesize, text="Dostępny", fg="green", pady=5)
        Ava1080p.grid(row=0, column=0)
    else:
        Ava1080p = Label(LabelFilesize, text="Nie Dostępny", fg="red", pady=5)
        Ava1080p.grid(row=0, column=0)

    if bool720p:
        Ava720p = Label(LabelFilesize, text="Dostępny", fg="green")
        Ava720p.grid(row=1, column=0)

        Filesize720p = Label(LabelFilesize, text=f"{round(Pobieranie.streams.get_highest_resolution().filesize / 1000000,2)} MB")
        Filesize720p.grid(row=1, column=1)
    else:
        Ava720p = Label(LabelFilesize, text="Nie Dostępny", fg="red")
        Ava720p.grid(row=1, column=0)

    if bool360p:
        Ava360p = Label(LabelFilesize, text="Dostępny", fg="green", pady=5)
        Ava360p.grid(row=2, column=0)

        Filesize360p = Label(LabelFilesize, text=f"{round(Pobieranie.streams.get_lowest_resolution().filesize / 1000000,2)} MB")
        Filesize360p.grid(row=2, column=1)
    else:
        Ava360p = Label(LabelFilesize, text="Nie Dostępny", fg="red", pady=5)
        Ava360p.grid(row=2, column=0)

    if boolMP3:
        AvaMP3 = Label(LabelFilesize, text="Dostępny", fg="green", pady=3)
        AvaMP3.grid(row=3, column=0)

        FilesizeMP3 = Label(LabelFilesize, text=f"{round(Pobieranie.streams.filter(abr='160kbps', progressive=False).first().filesize / 1000000,2)} MB")
        FilesizeMP3.grid(row=3, column=1)
    else:
        AvaMP3 = Label(LabelFilesize, text="Nie Dostępny", fg="red")
        AvaMP3.grid(row=3, column=0)

def download2(index):
    try:
        match index:
            case 0:
                threading.Thread(target=HD).start()
            case 1:
                threading.Thread(target=TheHighest).start()
            case 2:
                threading.Thread(target=TheLowest).start()
            case 3:
                threading.Thread(target=MP3).start()
    except:
        messagebox.showerror("Błąd Pobierania!", "Upewni się że film który pobierasz: \n"
                                                 "- Jest w tej jakości jaką chcesz pobrać \n"
                                                 "- Nie ma ograniczeń wiekowych")

def progress(stream, chunk, bytes_remaining):
    print(100 - (bytes_remaining / stream.filesize * 100))

    global LabelDownload
    LabelDownload = Label(LabelProgress, text="POBIERANIE", fg="green", pady=5)
    LabelDownload.grid(row=0, column=0)

    bar = ttk.Progressbar(LabelProgress, orient=HORIZONTAL, length=150)
    bar.grid(row=0, column=1)

    while bytes_remaining>stream.filesize:
        bar["value"] = 100 - (bytes_remaining / stream.filesize * 100)
        LabelProgress.update_idletasks()

    bar["value"] = 100 - (bytes_remaining / stream.filesize * 100)

def complete(stream, file_path):
    print(stream)
    print(file_path)

    for widget in LabelProgress.winfo_children():
        widget.destroy()

    LabelDownload = Label(LabelProgress, text="POBRANO", fg="green", pady=5)
    LabelDownload.grid(row=0, column=0)

    # Play sound
    if sound:
        playsound(Finish1, block=False)

def RestartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def Directory():
    global my_dir
    my_dir = filedialog.askdirectory()
    DirectoryCheck.config(text=my_dir)



def HD():
    Pobieranie.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3",
                                                                                 output_path=my_dir)
    Pobieranie.streams.filter(res="1080p", progressive=False).first().download(filename="video.mp4",
                                                                               output_path=my_dir)

    audio = ffmpeg.input(f"{my_dir}/audio.mp3")
    video = ffmpeg.input(f"{my_dir}/video.mp4")

    ffmpeg.concat(video, audio, v=1, a=1).output(f"{my_dir}/{randint(100, 1000)}.mp4").run(overwrite_output=True)

    os.remove(f"{my_dir}/audio.mp3")
    os.remove(f"{my_dir}/video.mp4")

def TheHighest():
    Pobieranie.streams.get_highest_resolution().download(output_path=my_dir)

def TheLowest():
    Pobieranie.streams.get_lowest_resolution().download(output_path=my_dir)

def MP3():
    Pobieranie.streams.filter(abr="160kbps", progressive=False).first().download(output_path=my_dir,
                                                                                 filename=f"{randint(0, 100)}.mp3")

# Wizualne

# Pierwszy rząd
LabelFR = Label(root)
LabelFR.place(x=0, y=20)

# Miniaturka
LabelFrameImg = LabelFrame(root)
LabelFrameImg.place(x=35, y=70)

# Opcje Pobierania
LabelFrameOpt = LabelFrame(root, padx=10)
LabelFrameOpt.place(x=230, y=70)



# Funkcjonalne

# Pierwszy rząd
TextInfo = Label(LabelFR, text="Tutaj dawaj LINK! -->")
TextInfo.grid(row=0, column=0, padx=10)

TextBox = Entry(LabelFR, width=50)
TextBox.grid(row=0, column=1, padx=10)

TextBox.bind("<Button-3>", do_popup)

TextSubmit = Button(LabelFR, text="ENTER!!!", width=10, cursor="hand2", command=lambda: download(TextBox.get()))
TextSubmit.grid(row=0, column=2, padx=10)

# Drugi rząd

# Miniaturka
Label_Min = Label(LabelFrameImg, image=default_image)
Label_Min.grid()

# HighRes
TextHighRes = Label(LabelFrameOpt, text="MP4 1080p (VERY SLOW)")
TextHighRes.grid(row=0, column=0)

ButtonHighRes = Button(LabelFrameOpt, text="Pobierz", state=DISABLED)
ButtonHighRes.grid(row=0, column=1)

#LowRes
TextHigRes = Label(LabelFrameOpt, text="MP4 720p")
TextHigRes.grid(row=1, column=0)

ButtonHigRes = Button(LabelFrameOpt, text="Pobierz", state=DISABLED)
ButtonHigRes.grid(row=1, column=1)

TextLowRes = Label(LabelFrameOpt, text="MP4 360p")
TextLowRes.grid(row=2, column=0)

ButtonLowRes = Button(LabelFrameOpt, text="Pobierz", state=DISABLED)
ButtonLowRes.grid(row=2, column=1)

TextAudio = Label(LabelFrameOpt, text="MP3 160kbps")
TextAudio.grid(row=3, column=0)

ButtonAudio = Button(LabelFrameOpt, text="Pobierz", state=DISABLED)
ButtonAudio.grid(row=3, column=1)


# Stopka
FlexLabel = Label(root, text="Programmed by Sebastian")
FlexLabel.place(x=500, y=375)


root.mainloop()