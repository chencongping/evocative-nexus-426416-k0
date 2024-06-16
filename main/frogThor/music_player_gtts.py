import os
import random
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from gtts import gTTS


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("音乐播放器")
        self.root.geometry("600x400")
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
        filemenu.add_command(label="打开文件", command=self.load_file)
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

        # 音频列表及相关功能
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=20, padx=20)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, width=50, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # 发音按钮
        pronounce_button = tk.Button(self.root, text="发音", command=self.pronounce)
        pronounce_button.pack(pady=10)

        # 全选按钮
        select_button = tk.Button(self.root, text="全选", command=self.select_all)
        select_button.pack(pady=10)

    def load_file(self):
        file = filedialog.askopenfilename(filetypes=[("MP3 文件", "*.mp3")])
        if file:
            self.playlist = [file]
            self.current_index = 0
            self.update_listbox()
            self.play()

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.playlist = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
            self.current_index = 0
            self.update_listbox()
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

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.playlist:
            self.listbox.insert(tk.END, os.path.basename(item).split('.')[0])  # 只显示文件名，不显示后缀

    def pronounce(self):
        selection = self.listbox.curselection()
        if selection:
            selected_items = [self.playlist[index] for index in selection]
            for item in selected_items:
                text = os.path.basename(item).split('.')[0]
                tts = gTTS(text=text, lang='en')
                tts.save("pronounce.mp3")
                mixer.music.load("pronounce.mp3")
                mixer.music.play()
                while mixer.music.get_busy():
                    self.root.update()  # 更新tkinter界面以防止阻塞

    def select_all(self):
        if self.listbox.size() > 0:
            if all(self.listbox.selection_includes(index) for index in range(self.listbox.size())):
                self.listbox.selection_clear(0, tk.END)
            else:
                self.listbox.select_set(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
