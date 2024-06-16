import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import random


class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("青蛙雷神音乐播放器")
        self.playlist = []
        self.current_index = 0
        self.mode = "顺序播放"
        self.is_playing = False

        # 初始化pygame的mixer模块
        pygame.mixer.init()
        self.music = pygame.mixer.Sound(r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\en-US-Journey-D\absolute.mp3')

        # 创建按钮和标签
        self.play_button = tk.Button(self.root, text="播放", command=self.play_or_pause)
        self.play_button.pack()

        self.mode_button = tk.Button(self.root, text="播放模式", command=self.change_mode)
        self.mode_button.pack()

        self.browse_button = tk.Button(self.root, text="浏览目录", command=self.browse_directory)
        self.browse_button.pack()

        self.label = tk.Label(self.root, text="")
        self.label.pack()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.playlist = [os.path.join(directory, f) for f in os.listdir(directory) if
                             f.endswith((".mp3", ".wav", ".ogg"))]
            self.current_index = 0
            self.label.config(text=f"当前播放: {self.playlist[self.current_index]}")

    def play_or_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.config(text="播放")
        else:
            if self.playlist:
                filename = self.playlist[self.current_index]
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_button.config(text="暂停")

    def change_mode(self):
        modes = ["顺序播放", "循环播放", "单曲播放", "随机播放"]
        index = modes.index(self.mode)
        index = (index + 1) % len(modes)
        self.mode = modes[index]
        messagebox.showinfo("播放模式", self.mode)

        # 这里可以添加逻辑来根据模式改变播放行为

    def update_playlist(self):
        # 这个函数可以根据你的播放模式来更新播放列表或索引
        pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    player = AudioPlayer(root)
    player.run()