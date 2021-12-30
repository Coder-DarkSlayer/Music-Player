import tkinter
from tkinter import ttk
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]='hide'
from pygame import mixer
from PIL import ImageTk , Image
from mutagen.id3 import ID3
from audioread import audio_open

mixer.init()

# ENTER PATH WHERE SONGS ARE PRESENT
path = r''

root = tkinter.Tk()
root.title("Music Player")
root.geometry("950x600")
root.minsize(950 , 600)
root.maxsize(950 , 600)

Status = 'NOT PLAYING'
selArtists = 'All'
Index = 0
name = ' '
info = " \n "
imgObj = ImageTk.PhotoImage((Image.open(os.path.join('assets' , 'static' , 'default.png'))).resize((200 , 199) , Image.ANTIALIAS))

playButton = ImageTk.PhotoImage((Image.open(os.path.join('assets' , 'static' , 'play.png'))).resize((40 , 40) , Image.ANTIALIAS))
pauseButton = ImageTk.PhotoImage((Image.open(os.path.join('assets' , 'static' , 'pause.png'))).resize((40 , 40) , Image.ANTIALIAS))
nextButton = ImageTk.PhotoImage((Image.open(os.path.join('assets' , 'static' , 'next.png'))).resize((40 , 40) , Image.ANTIALIAS))
prevButton = ImageTk.PhotoImage((Image.open(os.path.join('assets' , 'static' , 'next.png'))).resize((40 , 40) , Image.ANTIALIAS).rotate(180))

def sorter(Array):
    for i in range(len(Array)-1):
        for j in range(len(Array)-1):
            if Array[j].upper() > Array[j + 1].upper():
                Array[j] , Array[j + 1] = Array[j + 1] , Array[j]
    return Array

song = [os.path.join(path , i) for i in os.listdir(path) if i.endswith('.mp3') or i.endswith('.m4a') or i.endswith('.ogg')]
song = sorter(song)

string = "/".join([str(ID3(i)['TPE1']) for i in song])
dat = []
meta = [dat.append(i) for i in string.split("/") if i not in dat]
dat = sorter(dat)
dat.insert(0 , 'All')

ArtList = {}
ArtList['All'] = song

for i in range(1,len(dat)):
    temp = []
    for j in song:
        if dat[i] in str(ID3(j)['TPE1']):
            temp.append(j)
    ArtList[dat[i]] = temp  

def songBox(nameWithPath):
    global name , album , artist , imgObj , info
    try:
        rawData = ID3(nameWithPath)
        name = str(rawData['TIT2'])
        if len(name) >= 32:
            name = name[:30] + '...'

        album = str(rawData['TALB'])
        if len(album) >= 24:
            album = album[:23] + '...'

        artist = str(rawData['TPE2'])
        if len(artist) >= 26:
            artist = artist[:24] + '...'
        
        info = "by " + str(artist) + "\nfrom " + str(album)

        cover = rawData['APIC:Cover'].data
        imageFile = os.path.join('assets' , 'temp' , f"{nameWithPath.split(os.path.sep)[-1].split('.')[0]}.jpg")
        with open(imageFile ,'wb') as f:
            f.write(cover)
        imgObj = ImageTk.PhotoImage((Image.open(imageFile)).resize((207 , 202) , Image.ANTIALIAS))

    except Exception:
        i = nameWithPath
        
        if i.endswith('.mp3'):
            name = str((i.split(os.path.sep))[-1].replace('.mp3' , ''))
        elif i.endswith('.m4a'):
            name = str((i.split(os.path.sep))[-1].replace('.m4a' , ''))
        elif i.endswith('.ogg'):
            name = str((i.split(os.path.sep))[-1].replace('.ogg' , ''))
    
        if len(name) >= 32:
            name = name[:30] + '...'
        album = 'Unknown'
        artist = 'Unknown'
        info = "by " + str(artist) + "\nfrom " + str(album)
        imgObj = ImageTk.PhotoImage((Image.open(os.path.join('assets' , 'static' , 'default.png'))).resize((200 , 199) , Image.ANTIALIAS))

def playSong(i):
    global Status
    if Status == 'PAUSED':
        mixer.music.pause()
    elif Status == "PLAYING":
        mixer.music.unpause()

def TransitionNext():
    global Index , Status
    if Status == 'PLAYING' or Status == 'PAUSED':
        if Index < len(ArtList[selArtists]) - 1:
            Index += 1
        else:
            Index = 0
        songBox(ArtList[selArtists][Index])
        detail.config(text = name)
        albumArt.config(image = imgObj)
        songArtist.config(text = info)
        Play.config(image = pauseButton)
        buttonPlay(Index)

def TransitionPrev():
    global Index , Status
    if Status == 'PLAYING' or Status == 'PAUSED':
        if Index > -1*len(ArtList[selArtists]):
            Index -= 1
        else:
            Index = 0
        songBox(ArtList[selArtists][Index])
        detail.config(text = name)
        albumArt.config(image = imgObj)
        songArtist.config(text = info)
        Play.config(image = pauseButton)
        buttonPlay(Index)

def PauseDisplay():
    global Status , Index
    if Status == 'PLAYING':
        Play.config(image = playButton)
        Status = 'PAUSED'
        playSong(Index)
    elif Status == 'PAUSED':
        Play.config(image = pauseButton)
        Status = 'PLAYING'
        playSong(Index)
    
def musicChange(event):
    global selArtists
    select = event.widget.curselection()
    if select:
        ArtistIndex = select[0]
        selArtists = dat[ArtistIndex]
        show(selArtists)

def buttonPlay(i):
    playFromTree()

def checkAndPlay():
    global Index
    if mixer.music.get_busy():
        pass
    else:
        Index += 1
        playFromTree()

def playFromTree():
    global Index
    mixer.music.stop()
    songBox(ArtList[selArtists][Index])
    detail.config(text = name)
    albumArt.config(image = imgObj)
    songArtist.config(text = info)
    Play.config(image = pauseButton)

    mixer.music.load(ArtList[selArtists][Index])
    mixer.music.play()
    
    length = (int(audio_open(ArtList[selArtists][Index]).duration) + 1) * 1000
    musicBox.after(length , checkAndPlay)

base = tkinter.Frame(root , width = 950 , height = 600 , bg = 'black')
base.pack(fill = 'both')

musicBox = tkinter.Frame(base , width = 950 , height = 250 , bg = 'black')
musicBox.pack(side = 'bottom')

setMBoxTop = tkinter.Frame(musicBox , width = 950)
setMBoxTop.pack(side = 'top')

setMBoxSide = tkinter.Frame(musicBox , height = 289)
setMBoxSide.pack(side = 'left')

leftWidth = tkinter.Frame(base , width = 625 , height = 350  , bg = 'purple')
leftWidth.pack(side = 'left' , anchor = 'nw')

setLBoxTop = tkinter.Frame(leftWidth , width = 625)
setLBoxTop.pack(side = 'top')

setLBoxSide = tkinter.Frame(leftWidth , height = 309)
setLBoxSide.pack(side = 'left')

rightWidth = tkinter.Frame(base , width = 325 , height = 350 , bg = 'dark blue')
rightWidth.pack(side = 'right' , anchor = 'ne')

setRBoxTop = tkinter.Frame(rightWidth , width = 325)
setRBoxTop.pack(side = 'top')

setRBoxSide = tkinter.Frame(rightWidth , height = 309)
setRBoxSide.pack(side = 'left')

####################################################################################

detail = tkinter.Label(leftWidth , text = str(name) , fg = 'white' , bg = 'purple' , font = 'comicsans 22 bold')
detail.pack(side = 'top' , pady = 10 , anchor = 'center')

cover = tkinter.Frame(leftWidth , width = 215 , height = 215 , highlightbackground = 'black' , highlightthickness = 2.5 )
cover.pack(side = 'left' , padx = 20 , pady = 20)

songArtist = tkinter.Label(leftWidth , text = info , fg = 'white' , bg = 'purple' , font = 'comicsans 16 italic')
songArtist.pack(pady = 25)

albumArt = tkinter.Label(cover , image = imgObj)
albumArt.place(x=0,y=0)
#################################################################
buttonFrame = tkinter.Frame(leftWidth , width = 275 , height = 50 , bg = 'purple')
buttonFrame.pack(pady = 15)

Previous = tkinter.Button(buttonFrame , image = prevButton , bg= 'dark blue' , activebackground = 'yellow' , command = TransitionPrev)
Previous.grid(row = 1 , column = 1)

Play = tkinter.Button(buttonFrame , image = playButton , bg= 'dark blue' , activebackground = 'yellow' , command = PauseDisplay)
Play.grid(row = 1 , column = 2 , padx = 80)

Next = tkinter.Button(buttonFrame , image = nextButton , bg= 'dark blue' , activebackground = 'yellow' , command = TransitionNext)
Next.grid(row = 1 , column = 3)

#################################################################

RightHeader = tkinter.Frame(rightWidth , width = 325 , height = 30)
RightHeader.pack(side = 'top' , pady = 5)

NameHeader = tkinter.Label(RightHeader , bg = 'dark blue' , fg = 'white' , font = 'comicsans 15 bold' , text = '     Artists                                   ')
NameHeader.pack()

scrr = tkinter.Scrollbar(rightWidth , orient='vertical' , background = 'dark blue')
scrr.pack(side='right' , fill = 'y')

ArtBox = tkinter.Listbox(rightWidth , width = 38 , bg = 'purple' , height = 15 , activestyle = 'none' , font = 'comicsans 12' , fg = 'white' , selectmode = 'single' , highlightcolor = 'black' , highlightthickness= 1 , selectbackground= 'yellow' , selectforeground = 'black' , yscrollcommand = scrr.set)

ArtBox.insert('end' , *["   " + str(i) for i in dat])

ArtBox.bind('<Double-1>' , musicChange)
ArtBox.pack()

#################################################################

def selectedSong(item):
    global Index , Status
    Status = 'PLAYING'
    Index = tree.item(tree.focus())['open']
    playFromTree()

scrd = tkinter.Scrollbar(musicBox , orient='vertical' , background = 'dark blue')
scrd.pack(side='right' , fill = 'y')

style = ttk.Style()
style.configure('Treeview' , font = 'comicsans 12' , foreground = 'white' , background = 'purple' , rowheight = 19 , fieldbackground ='purple')
style.map("Treeview" , background = [('selected' , 'yellow')] , foreground = [('selected' , 'black')])
style.configure('Treeview.Heading' , font = 'comicsans 12 bold' , foreground = 'white' , background = 'dark blue' , heigt = 14)
style.map("Treeview.Heading" , background = [('selected' , 'purple')] , foreground = [('selected' , 'white')])

tree = ttk.Treeview(musicBox , columns = ('Title' , 'Artist' , 'Album') , show = 'headings' , height = 14 , yscrollcommand = scrd.set)

tree.column("# 1", anchor = 'w'  , width = 280)
tree.heading("# 1", text = 'Track')
tree.column("# 2", anchor = 'w'  , width = 330)
tree.heading("# 2", text = 'Artist(s)')
tree.column("# 3", anchor = 'w'  , width = 330)
tree.heading("# 3", text = 'Album')

def show(Artist):
    try:
        tree.delete(*tree.get_children())
        root.update()
    except Exception:
        pass

    for k,i in enumerate(ArtList[Artist]):
        if i.endswith('.mp3'):
            tree.insert('', 'end', values= ("   " + str((i.split(os.path.sep))[-1].replace('.mp3' , '')) , "   " + str(ID3(i)['TPE1']) , "   " + str(ID3(i)['TALB'])) , open = k)
        elif i.endswith('.m4a'):
            tree.insert('', 'end', values= ("   " + str((i.split(os.path.sep))[-1].replace('.m4a' , '')) , "   " + str(ID3(i)['TPE1']) , "   " + str(ID3(i)['TALB'])) , open = k)
        elif i.endswith('.ogg'):
            tree.insert('', 'end', values= ("   " + str((i.split(os.path.sep))[-1].replace('.ogg' , '')) , "   " + str(ID3(i)['TPE1']) , "   " + str(ID3(i)['TALB'])) , open = k)
    root.update()

tree.bind('<Double-1>' , selectedSong)
tree.pack()

show(selArtists)

if __name__ == '__main__':
    tkinter.mainloop()