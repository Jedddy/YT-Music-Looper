from tkinter import *
from tkinter import ttk
import pygame
import yt_dlp
import os
import threading


"""Create the Music Directory
Initialize PyGame mixer"""
try:
    os.mkdir("./dl_music/")
except FileExistsError:
    pass

pygame.mixer.init() # Initialize Mixer

class YTMusicPLayer(ttk.Frame):
    def __init__(self, master=Tk()):
        super().__init__(master)
        self.master.title("Youtube Loop Player")
        self.master.minsize(480, 270)
        self.master.maxsize(480, 270)
        self.is_paused = False
        self.is_playing = False
        self.volume = 0.5
        self.playing_label = ttk.Label(text="Insert Youtube link...", font="Times 10 italic bold")
        self.playing_label.place(relx=0.5, rely=0.5, anchor="center")
        self.link_entry = ttk.Entry(width=40)
        self.link_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.play_btn = ttk.Button(text="Play", command=self.play_music)
        self.play_btn.place(relx=0.5, rely=0.6, anchor="center")
        self.pause_btn = ttk.Button(text="Pause", command=self.pause)
        self.pause_btn.place(relx=0.3, rely=0.6, anchor="center")
        self.stop_btn = ttk.Button(text="Stop", command=self.stop)
        self.stop_btn.place(relx=0.7, rely=0.6, anchor="center")
        self.volumeup_btn = ttk.Button(text="Volume +", command=self.volume_up)
        self.volumeup_btn.place(relx=0.4, rely=0.75, anchor="center")
        self.volumedown_btn = ttk.Button(text="Volume -", command=self.volume_down)
        self.volumedown_btn.place(relx=0.6, rely=0.75, anchor="center")
        self.informer = ttk.Label(text="Nothing is playing at the moment.",
                                  font="Times 10 italic bold")
        self.informer.place(relx=0.5, rely=0.3, anchor="center")

        # Create a new Thread
        self.music_thread = threading.Thread(target=self.playing_thread)
        self.music_thread.start()

    def get_song_name(self):
        """Gets song name from directory"""
        song_name = os.listdir("./dl_music/")[0]
        return song_name

    def pygame_player(self):
        """Player Function"""
        song_name = self.get_song_name()

        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        pygame.mixer.music.load(f"./dl_music/{song_name}")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    def download(self):
        """Downloads the Music"""

        """Starting name for the downloaded MP3 file,

        that way os.listdir("./dl_music/")[0] will always return the last downloaded MP3."""

        starting_name = 999
        starting_name -= len(os.listdir("./dl_music/"))

        # YTDL Options
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"./dl_music/{starting_name}%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.link_entry.get()])
        except Exception as e:
            print("Download exception: " + str(e))

    def play_music(self):
        """Play Music"""
        self.download()
        song_name = self.get_song_name()

        if not self.is_playing:
            self.pygame_player()
            self.is_playing = True
        else:
            pygame.mixer.music.stop()
            self.pygame_player()
            self.is_playing = True
        self.informer.config(text=f"Playing: {song_name[3:-4]}")

    def pause(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.pause_btn.config(text="Pause")
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.pause_btn.config(text="Resume")

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.informer.config(text="Nothing is playing at the moment.")
            # Quit the mixer so it doesn't cause issues when deleting the file.
            pygame.mixer.quit()
            # Removes all files inside the music directory
            for i in os.listdir("./dl_music/"):
                os.remove(f"./dl_music/{i}")

    def volume_up(self):
        self.volume += 0.1
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume
        self.volume -= 0.1
        pygame.mixer.music.set_volume(self.volume)

    def playing_thread(self):
        """Thread for the player"""
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# root = Tk()
ytplayer = YTMusicPLayer()
ytplayer.mainloop()