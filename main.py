from tkinter import *
from tkinter import ttk
import pygame
import yt_dlp
import os
import threading


is_paused = False
is_playing = False
VOLUME = 0.5


"""Create the Music Directory
Initialize PyGame mixer"""
try:
    os.mkdir("./dl_music/")
except FileExistsError:
    pass

# Initialize Mixer
pygame.mixer.init()


"""Functions"""
def get_song_name():
    """Gets song name from directory"""
    song_name = os.listdir("./dl_music/")[0]
    return song_name


def pygame_player():
    """Player Function"""
    song_name = get_song_name()

    pygame.mixer.music.load(f"./dl_music/{song_name}")
        
    pygame.mixer.music.set_volume(VOLUME)
        
    pygame.mixer.music.play(-1)

        
def download():
    """Downloads the Music"""
    
    """Starting name for the downloaded MP3 file,

    that way os.listdir("./dl_music/")[0] will always return the last downloaded MP3."""

    starting_name = 999
    starting_name -= len(os.listdir("./dl_music/"))


    # YTDL Options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'./dl_music/{starting_name}%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
                ydl.download([link_entry.get()])
                
    except Exception as e:
        print("Download exception: " + str(e))


def play_music():
    """Play Music"""
    global is_playing

    download()

    song_name = get_song_name()
    
    if not is_playing:
        pygame_player()
        is_playing = True

    else:
        pygame.mixer.music.stop()
        pygame_player()
        is_playing = True
        
    informer.config(text=f"Playing: {song_name[3:-4]}")


def pause():
    global is_paused
    global is_playing

    if not is_playing:
        pass

    else:
        if is_paused:
            pygame.mixer.music.unpause()
            pause_btn.config(mnfrm, text="Pause")
            is_paused = False

        else:
            pygame.mixer.music.pause()
            is_paused = True
            pause_btn.config(mnfrm, text="Resume")

def stop():
    global is_playing


    if not is_playing:
        pass
    else:
        pygame.mixer.music.stop()
        is_playing = False

        informer.config(mnfrm, text="Nothing is playing at the moment.")

        #Quit the mixer so it doesn't cause issues when deleting the file.
        pygame.mixer.quit()
        # Removes all files inside the music directory
        for i in os.listdir("./dl_music/"):
            os.remove(f"./dl_music/{i}")
        

def volume_up():
    global VOLUME
    VOLUME += 0.1
    pygame.mixer.music.set_volume(VOLUME)

def volume_down():
    global VOLUME
    VOLUME -= 0.1
    pygame.mixer.music.set_volume(VOLUME)


def playing_thread():
    """Thread for the player"""
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)   


"""Initialize Window"""
root = Tk()
root.title("Youtube Loop Player")
mnfrm = ttk.Frame(root, padding=10).grid()
root.minsize(480, 270)
root.maxsize(480, 270)
    

playing_label = ttk.Label(mnfrm, text="Insert Youtube link...", font="Times 10 italic bold")
playing_label.place(relx=.5, rely=.5, anchor="center")

link_entry = ttk.Entry(mnfrm, width=40)
link_entry.place(relx=.5, rely=.4, anchor="center")

play_btn = ttk.Button(mnfrm, text="Play", command=play_music)
play_btn.place(relx=.5, rely=.6, anchor="center")

pause_btn = ttk.Button(mnfrm, text="Pause", command=pause)
pause_btn.place(relx=.3, rely=.6, anchor="center")

stop_btn = ttk.Button(mnfrm, text="Stop", command=stop)
stop_btn.place(relx=.7, rely=.6, anchor="center")

volumeup_btn = ttk.Button(mnfrm, text="Volume +", command=volume_up)
volumeup_btn.place(relx=.4, rely=.75, anchor="center")

volumedown_btn = ttk.Button(mnfrm, text="Volume -", command=volume_down)
volumedown_btn.place(relx=.6, rely=.75, anchor="center")

informer = ttk.Label(mnfrm, text="Nothing is playing at the moment.", font="Times 10 italic bold")
informer.place(relx=.5, rely=.3, anchor="center")

#Create a new Thread
music_thread = threading.Thread(target=playing_thread)
music_thread.start()

root.mainloop()
