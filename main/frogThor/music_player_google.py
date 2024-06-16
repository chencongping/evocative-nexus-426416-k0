import tkinter as tk
from tkinter import ttk
import os
import pygame
import re


class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("音乐播放器")

        self.music_dir = r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\en-US-Journey-D'  # 替换成你的音乐目录
        self.music_files = [f for f in os.listdir(self.music_dir) if f.endswith((".mp3", ".wav"))]
        self.current_track = 0
        self.playing = False
        self.shuffle = False
        self.search_term = ""

        # 初始化 Pygame
        pygame.mixer.init()

        # 创建主框架
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # 创建搜索框框架
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(side="top", fill="x")

        # 创建搜索框
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.search)

        # 创建播放列表框架
        self.playlist_frame = tk.Frame(self.main_frame)
        self.playlist_frame.pack(side="left", fill="both", expand=True)

        # 创建播放控制框架
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side="right")

        # 创建播放列表
        self.playlist = tk.Listbox(self.playlist_frame, selectmode="extended", font=("Arial", 12))
        self.update_playlist()
        self.playlist.pack(fill="both", expand=True)

        # 创建滚动条
        self.scrollbar = tk.Scrollbar(self.playlist_frame, orient="vertical", command=self.playlist.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.playlist.config(yscrollcommand=self.scrollbar.set)

        # 创建播放按钮
        self.play_button = tk.Button(self.control_frame, text="播放", command=self.play)
        self.play_button.pack(pady=10)

        # 创建暂停按钮
        self.pause_button = tk.Button(self.control_frame, text="暂停", command=self.pause, state=tk.DISABLED)
        self.pause_button.pack(pady=10)

        # 创建停止按钮
        self.stop_button = tk.Button(self.control_frame, text="停止", command=self.stop)
        self.stop_button.pack(pady=10)

        # 创建循环播放按钮
        self.loop_button = tk.Button(self.control_frame, text="循环", command=self.toggle_loop)
        self.loop_button.pack(pady=10)

        # 创建随机播放按钮
        self.shuffle_button = tk.Button(self.control_frame, text="随机", command=self.toggle_shuffle)
        self.shuffle_button.pack(pady=10)

        # 创建全选按钮
        self.select_all_button = tk.Button(self.control_frame, text="全选", command=self.select_all)
        self.select_all_button.pack(pady=10)

        # 绑定事件
        self.playlist.bind("<<ListboxSelect>>", self.handle_selection)

        # 初始化播放状态
        self.update_controls()

    # 搜索歌曲
    def search(self, event=None):
        self.search_term = self.search_entry.get()
        self.update_playlist()

    # 更新播放列表
    def update_playlist(self):
        self.playlist.delete(0, tk.END)
        if self.search_term:
            for file in self.music_files:
                if re.search(self.search_term, os.path.splitext(file)[0]):
                    self.playlist.insert(tk.END, os.path.splitext(file)[0])
        else:
            for file in self.music_files:
                self.playlist.insert(tk.END, os.path.splitext(file)[0])

    # 播放音频
    def play(self):
        self.playing = True
        self.update_controls()

        if self.shuffle:
            self.current_track = self.random_track()

        selected_indices = self.playlist.curselection()
        if selected_indices:
            self.current_track = selected_indices[0]

        track = self.playlist.get(self.current_track)
        file_path = os.path.join(self.music_dir, track + ".mp3")  # 假设文件后缀为 mp3
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    # 暂停音频
    def pause(self):
        self.playing = False
        self.update_controls()
        pygame.mixer.music.pause()

    # 停止音频
    def stop(self):
        self.playing = False
        self.update_controls()
        pygame.mixer.music.stop()

    # 切换循环播放模式
    def toggle_loop(self):
        self.loop_button.config(text="循环" if not self.loop else "单曲")
        self.loop = not self.loop

    # 切换随机播放模式
    def toggle_shuffle(self):
        self.shuffle_button.config(text="随机" if not self.shuffle else "顺序")
        self.shuffle = not self.shuffle

    # 全选/取消全选
    def select_all(self):
        if self.playlist.curselection() == ():
            for i in range(self.playlist.size()):
                self.playlist.selection_set(i)
        else:
            self.playlist.selection_clear(0, tk.END)

    # 处理列表选择事件
    def handle_selection(self, event):
        selected_indices = self.playlist.curselection()
        if selected_indices:
            self.current_track = selected_indices[0]  # 获取第一个选中的索引
            self.play()

    # 更新控制按钮状态
    def update_controls(self):
        if self.playing:
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

    # 获取随机的歌曲索引
    def random_track(self):
        import random
        return random.randint(0, len(self.playlist.get(0, tk.END)) - 1)


# 创建主窗口
root = tk.Tk()
player = MusicPlayer(root)
root.mainloop()