import os
import random
import tkinter as tk
from tkinter import filedialog
from pygame import mixer


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("音乐播放器")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # 初始化pygame混音器
        mixer.init()

        # 播放列表
        self.playlist = []
        self.current_index = 0

        # 播放模式
        self.mode = tk.StringVar()
        self.mode.set("顺序播放")

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 添加菜单
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="打开目录", command=self.load_directory)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.root.quit)

        # 播放控制按钮
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        self.play_button = tk.Button(control_frame, text="播放", command=self.play)
        self.play_button.grid(row=0, column=0, padx=10)

        pause_button = tk.Button(control_frame, text="暂停", command=self.pause)
        pause_button.grid(row=0, column=1, padx=10)

        next_button = tk.Button(control_frame, text="下一首", command=self.next)
        next_button.grid(row=0, column=2, padx=10)

        prev_button = tk.Button(control_frame, text="上一首", command=self.prev)
        prev_button.grid(row=0, column=3, padx=10)

        stop_button = tk.Button(control_frame, text="停止", command=self.stop)
        stop_button.grid(row=0, column=4, padx=10)

        # 播放模式选择
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=20)

        tk.Radiobutton(mode_frame, text="顺序播放", variable=self.mode, value="顺序播放").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="循环播放", variable=self.mode, value="循环播放").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="单曲播放", variable=self.mode, value="单曲播放").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="随机播放", variable=self.mode, value="随机播放").pack(side=tk.LEFT, padx=10)

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.playlist = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
            self.current_index = 0
            self.play()

    def play(self):
        if not self.playlist:
            return
        mixer.music.load(self.playlist[self.current_index])
        mixer.music.play()
        self.update_title()
        self.play_button.config(text="重播", command=self.replay)
        mixer.music.set_endevent()
        self.root.after(100, self.check_end)

    def replay(self):
        mixer.music.play()

    def pause(self):
        mixer.music.pause()

    def stop(self):
        mixer.music.stop()
        self.play_button.config(text="播放", command=self.play)

    def next(self):
        if self.mode.get() == "顺序播放" or self.mode.get() == "循环播放":
            self.current_index = (self.current_index + 1) % len(self.playlist)
        elif self.mode.get() == "随机播放":
            self.current_index = random.randint(0, len(self.playlist) - 1)
        self.play()

    def prev(self):
        if self.mode.get() == "顺序播放" or self.mode.get() == "循环播放":
            self.current_index = (self.current_index - 1) % len(self.playlist)
        elif self.mode.get() == "随机播放":
            self.current_index = random.randint(0, len(self.playlist) - 1)
        self.play()

    def check_end(self):
        if not mixer.music.get_busy():
            if self.mode.get() == "单曲播放":
                self.replay()
            else:
                self.next()
        else:
            self.root.after(100, self.check_end)

    def update_title(self):
        self.root.title(f"音乐播放器 - {os.path.basename(self.playlist[self.current_index])}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
