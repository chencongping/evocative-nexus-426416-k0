import os
import random
import tkinter as tk
from tkinter import ttk
from pygame import mixer

# 初始化pygame的混音器
mixer.init()

class AudioPlayer(tk.Tk):
    def __init__(self, audio_directory):
        super().__init__()
        self.title("音频播放器")
        self.geometry("400x400")

        self.audio_directory = audio_directory
        self.audio_files = self.load_audio_files(audio_directory)
        self.current_index = 0
        self.play_mode = "顺序播放"

        self.create_widgets()

    def load_audio_files(self, directory):
        audio_files = [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav'))]
        return audio_files

    def create_widgets(self):
        self.play_button = tk.Button(self, text="播放", command=self.play_audio)
        self.play_button.pack()

        self.pause_button = tk.Button(self, text="暂停", command=self.pause_audio)
        self.pause_button.pack()

        self.stop_button = tk.Button(self, text="停止", command=self.stop_audio)
        self.stop_button.pack()

        self.play_mode_label = tk.Label(self, text="播放模式")
        self.play_mode_label.pack()

        self.play_mode_combobox = ttk.Combobox(self, values=["顺序播放", "循环播放", "单曲播放", "随机播放"])
        self.play_mode_combobox.current(0)
        self.play_mode_combobox.bind("<<ComboboxSelected>>", self.change_play_mode)
        self.play_mode_combobox.pack()

        self.audio_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        for audio_file in self.audio_files:
            self.audio_listbox.insert(tk.END, os.path.splitext(audio_file)[0])
        self.audio_listbox.pack(fill=tk.BOTH, expand=True)

        self.select_all_button = tk.Button(self, text="全选", command=self.select_all)
        self.select_all_button.pack()

    def play_audio(self):
        if self.audio_listbox.curselection():
            self.current_index = self.audio_listbox.curselection()[0]
        audio_file = os.path.join(self.audio_directory, self.audio_files[self.current_index])
        mixer.music.load(audio_file)
        mixer.music.play()
        self.after(1000, self.check_playback)

    def pause_audio(self):
        mixer.music.pause()

    def stop_audio(self):
        mixer.music.stop()

    def change_play_mode(self, event):
        self.play_mode = self.play_mode_combobox.get()

    def select_all(self):
        if self.audio_listbox.select_includes(0):
            self.audio_listbox.selection_clear(0, tk.END)
        else:
            self.audio_listbox.selection_set(0, tk.END)

    def check_playback(self):
        if not mixer.music.get_busy():
            if self.play_mode == "顺序播放":
                self.current_index += 1
                if self.current_index >= len(self.audio_files):
                    self.current_index = 0
                self.play_audio()
            elif self.play_mode == "循环播放":
                self.play_audio()
            elif self.play_mode == "单曲播放":
                self.play_audio()
            elif self.play_mode == "随机播放":
                self.current_index = random.randint(0, len(self.audio_files) - 1)
                self.play_audio()

if __name__ == "__main__":
    audio_directory = r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\en-US-Journey-D'  # 请替换为你的音频文件夹路径
    app = AudioPlayer(audio_directory)
    app.mainloop()
