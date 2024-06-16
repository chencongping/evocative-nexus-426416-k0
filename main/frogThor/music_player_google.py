import time
import tkinter as tk
from tkinter import ttk
import os
import pygame
import re
from tkinter import filedialog, messagebox
from playerUtil import get_mp3_duration
import re
import math


#
# def update_text(text_widget, new_text):
#     """动态更新Text控件的内容"""


class MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("单词杀手")

        self.music_dir = (r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words\en-US'
                          r'-Journey-D')  # 替换成你的音乐目录
        self.music_explain_dir = (
            r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words-and-explain')  # 替换成你的音乐目录
        self.music_files = []

        self.music_files = [f for f in os.listdir(self.music_dir) if f.endswith((".mp3", ".wav"))]
        self.current_track = 0
        self.playing = False
        self.shuffle = False
        self.search_term = ""
        self.current_index = 10
        self.current_see = 0
        self.text_widget = None
        self.long_text = ''
        self.current_select_index = 0
        self.selected_indices = []
        self.selected_indices_max_index = 0

        # 初始化 Pygame
        pygame.mixer.init()

        # 创建主框架
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # 添加菜单
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="打开文件", command=self.load_file)
        filemenu.add_command(label="打开目录", command=self.load_directory)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.master.quit)

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
        self.play_button = tk.Button(self.control_frame, text="播放", command=self.button_play)
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

        # self.button_play_loop()
        # 初始化播放状态
        self.update_controls()
        self.create_window()

    def create_window(self):
        # 创建一个Text控件来显示多行文本
        self.text_widget = tk.Text(self.master, wrap='word', height=10, width=50)  # wrap='word' 表示在单词边界处换行
        self.text_widget.pack(side=tk.BOTTOM, fill=tk.X, expand=False, pady=(0, 10))  # 放置在底部，水平填充，不扩展，并添加一些内边距

        # 插入一些长文本到Text控件中
        self.text_widget.insert(tk.END, '')

        # 如果你想要禁用Text控件的编辑功能，可以设置其state为'disabled'
        # self.text_widget.config(state='disabled')
        self.update_content()
        # 运行Tkinter事件循环
        self.master.mainloop()

    def update_content(self):
        # print(f'{self.long_text}')
        self.text_widget.delete('1.0', tk.END)  # 删除当前所有内容
        self.text_widget.insert(tk.END, self.long_text)  # 插入新文本
        self.master.after(500, self.update_content)  # 每2秒更新一次内容

    # 搜索歌曲
    def search(self, event=None):
        self.search_term = self.search_entry.get()
        self.search_term = re.sub(r'\s+', '', self.search_term)
        print(f'{self.search_term}')
        self.update_playlist()
        if self.search_term == '' or self.search_term is None:
            self.playlist.see(99)
            print(f'go {self.current_see}')

    # 更新播放列表
    def update_playlist(self):
        print(f'更新播放列表')
        self.playlist.delete(0, tk.END)
        if self.search_term:
            for file in self.music_files:
                if re.search(self.search_term, os.path.splitext(file)[0]):
                    self.playlist.insert(tk.END, os.path.splitext(file)[0])
        else:
            for file in self.music_files:
                self.playlist.insert(tk.END, os.path.splitext(file)[0])
        print(f'{self.playlist}')

    # 播放音频
    def play(self):
        self.playing = True
        self.update_controls()

        if self.shuffle:
            self.current_track = self.random_track()

        selected_indices = self.playlist.curselection()
        print(f'{selected_indices}')
        if selected_indices:
            self.current_track = selected_indices[0]

        track = self.playlist.get(self.current_track)
        file_path = os.path.join(self.music_dir, track + ".mp3")  # 假设文件后缀为 mp3
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.current_see = self.current_track
        self.long_text = self.get_explain(track)

    def get_explain(self, word):
        explain_file = f'{self.music_explain_dir}/{word}.txt'
        if os.path.exists(explain_file):
            with open(explain_file, 'r', encoding='utf-8') as file:
                content = file.read()
            print(content)
            return content
        else:
            return ''

    def button_play(self):
        self.selected_indices = self.playlist.curselection()
        print(f'{self.selected_indices}')

        self.selected_indices_max_index
        if self.selected_indices:
            # self.button_play_loop()
            for current_track in self.selected_indices:
                self.current_track = current_track
                track = self.playlist.get(self.current_track)
                file_path = os.path.join(self.music_dir, track + ".mp3")  # 假设文件后缀为 mp3
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                time.sleep(get_mp3_duration(file_path))

    # def button_play_loop(self):
    #     if self.current_select_index < len(self.selected_indices) - 1:
    #         self.current_select_index = self.current_select_index + 1
    #         track = self.playlist.get(self.selected_indices[self.current_select_index])
    #         file_path = os.path.join(self.music_dir, track + ".mp3")  # 假设文件后缀为 mp3
    #         pygame.mixer.music.load(file_path)
    #         pygame.mixer.music.play()
    #         print(f'等待时间： {math.ceil(get_mp3_duration(file_path))}')
    #         self.master.after(math.ceil(get_mp3_duration(file_path)), self.update_content)  # 每2秒更新一次内容

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
        # if self.playing:
        #     self.play_button.config(state=tk.DISABLED)
        #     self.pause_button.config(state=tk.NORMAL)
        #     self.stop_button.config(state=tk.NORMAL)
        # else:
        #     self.play_button.config(state=tk.NORMAL)
        #     self.pause_button.config(state=tk.DISABLED)
        #     self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    # 获取随机的歌曲索引
    def random_track(self):
        import random
        return random.randint(0, len(self.playlist.get(0, tk.END)) - 1)

    def load_file(self):
        file = filedialog.askopenfilename(filetypes=[("MP3 文件", "*.mp3")])
        if file:
            self.music_files = [file]
            self.update_listbox()
            self.current_index = 0
            self.play()

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            # self.music_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
            self.music_files = [f for f in os.listdir(self.music_dir) if f.endswith((".mp3", ".wav"))]
            self.update_listbox()
            self.current_index = 0
            self.play()

    def update_listbox(self):
        self.playlist.delete(0, tk.END)
        for idx, file in enumerate(self.music_files):
            self.playlist.insert(tk.END, os.path.splitext(os.path.basename(file))[0])
            self.playlist.itemconfig(idx, {'bg': 'white'})


# 创建主窗口
root = tk.Tk()
player = MusicPlayer(root)
root.mainloop()
