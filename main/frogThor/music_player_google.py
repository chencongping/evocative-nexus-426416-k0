import base64
import time
import tkinter as tk
from tkinter import ttk
import os
import pygame
import re
from tkinter import filedialog, messagebox
from tkinter import Menu, messagebox
import pyperclip
from playerUtil import get_mp3_duration
from PIL import Image, ImageTk
import io


class MusicPlayer:
    def __init__(self, master):
        self.save_button = None
        self.example_text = None
        self.bottom_frame = None
        self.image_frame = None
        self.image_label = None
        self.example_frame = None
        self.upload_button = None
        self.master = master
        master.title("单词杀手")

        self.music_dir = (r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words\en-US'
                          r'-Journey-D')  # 替换成你的音乐目录
        self.music_explain_dir = (
            r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words-and-explain')  # 替换成你的例句目录
        self.music_picture_dir = (
            r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words-and-picture')  # 替换成你的图片目录
        self.music_examples_dir = (
            r'C:\Users\10843\OneDrive\文档\GitHub\evocative-nexus-426416-k0\output\5500-words-and-examples')  # 替换成你的例句目录
        if not os.path.exists(self.music_explain_dir):
            os.makedirs(self.music_explain_dir)
        if not os.path.exists(self.music_picture_dir):
            os.makedirs(self.music_picture_dir)
        if not os.path.exists(self.music_examples_dir):
            os.makedirs(self.music_examples_dir)

        self.music_files = []

        self.music_files = [f for f in os.listdir(self.music_dir) if f.endswith((".mp3", ".wav"))]
        self.current_track = 0
        self.playing = False
        self.shuffle = False
        self.search_term = ""
        self.current_index = 10
        self.current_see = 0
        self.text_widget = None
        self.explain_text = ''
        self.current_select_index = 0
        self.selected_indices = []
        self.selected_indices_max_index = 0
        self.auto_save = True  # 自动保存模式

        # 初始化 Pygame
        pygame.mixer.init()

        # 创建主框架
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # 添加菜单
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="打开文件", command=self.load_file)
        filemenu.add_command(label="打开目录", command=self.load_directory)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.master.quit)

        # 创建搜索框框架
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(side="top", fill="x", padx=10, pady=10)

        # 创建搜索框
        self.search_entry = ttk.Entry(self.search_frame, font=("Helvetica", 14))
        self.search_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.search)

        # 创建清除按钮
        self.clear_button = ttk.Button(self.search_frame, text="清除", command=self.clear_search, style='TButton')
        self.clear_button.pack(side="left", padx=5, pady=5)

        # 创建播放列表框架
        self.playlist_frame = ttk.Frame(self.main_frame, borderwidth=2, relief=tk.GROOVE)
        self.playlist_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # 创建文本展示框架
        self.text_display_frame = ttk.Frame(self.main_frame, borderwidth=2, relief=tk.GROOVE)
        self.text_display_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # 创建播放控制框架
        self.control_frame = ttk.Frame(self.main_frame, borderwidth=2, relief=tk.GROOVE)
        self.control_frame.pack(side="right", fill="y", padx=10, pady=10)

        # 创建播放列表
        self.playlist = tk.Listbox(self.playlist_frame, selectmode="extended", font=("Arial", 14))
        self.update_playlist()
        self.playlist.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # 创建滚动条
        self.scrollbar = ttk.Scrollbar(self.playlist_frame, orient="vertical", command=self.playlist.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.playlist.config(yscrollcommand=self.scrollbar.set)

        # 创建文本展示框
        self.text_display = tk.Text(self.text_display_frame, wrap='word', font=("Helvetica", 20), height=4)
        self.text_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_display.bind("<KeyRelease>", self.text_changed)

        # 创建播放按钮
        self.play_button = ttk.Button(self.control_frame, text="播放", command=self.button_play, style='TButton')
        self.play_button.pack(pady=10)

        # 创建暂停按钮
        self.pause_button = ttk.Button(self.control_frame, text="暂停", command=self.pause, state=tk.DISABLED,
                                       style='TButton')
        self.pause_button.pack(pady=10)

        # 创建停止按钮
        self.stop_button = ttk.Button(self.control_frame, text="停止", command=self.stop, style='TButton')
        self.stop_button.pack(pady=10)

        # 创建循环播放按钮
        self.loop_button = ttk.Button(self.control_frame, text="循环", command=self.toggle_loop, style='TButton')
        self.loop_button.pack(pady=10)

        # 创建随机播放按钮
        self.shuffle_button = ttk.Button(self.control_frame, text="随机", command=self.toggle_shuffle, style='TButton')
        self.shuffle_button.pack(pady=10)

        # 创建全选按钮
        self.select_all_button = ttk.Button(self.control_frame, text="全选", command=self.select_all, style='TButton')
        self.select_all_button.pack(pady=10)

        # 绑定事件
        self.playlist.bind("<<ListboxSelect>>", self.handle_selection)

        # 创建右键菜单
        self.popup_menu = Menu(self.playlist, tearoff=0)
        self.popup_menu.add_command(label="复制", command=self.copy_selected)
        # 绑定右键点击事件
        self.playlist.bind("<Button-3>", self.show_popup)

        # 绑定快捷键
        self.playlist.bind("<Control-c>", self.copy_to_clipboard)
        self.search_entry.bind("<Control-v>", self.paste_from_clipboard)
        self.search_entry.bind("<Control-z>", self.undo)
        self.search_entry.bind("<Control-y>", self.redo)

        # 用于撤销/重做功能的变量
        self.undo_stack = []
        self.redo_stack = []

        # 初始化播放状态
        self.update_controls()
        self.create_bottom_panel()

    def copy_to_clipboard(self, event):
        selected_items = self.playlist.curselection()
        selected_texts = [self.playlist.get(index) for index in selected_items]
        text_to_copy = "\n".join(selected_texts)
        pyperclip.copy(text_to_copy)
        print(f'复制{text_to_copy}')

    def paste_from_clipboard(self, event):
        try:
            clipboard_text = self.master.clipboard_get()
            # 判断是否为图片
            if clipboard_text.startswith('data:image/'):
                image_data = clipboard_text.split(',')[1]
                image_bytes = io.BytesIO(base64.b64decode(image_data))
                img = Image.open(image_bytes)
                self.save_pasted_image(img)
            else:
                self.search_entry.insert(tk.INSERT, clipboard_text)
                print(f'粘贴{clipboard_text}')
        except tk.TclError:
            print("Clipboard is empty or invalid content.")
        return "break"

    def save_pasted_image(self, img):
        track = self.playlist.get(self.current_track)
        img_save_path = os.path.join(self.music_picture_dir, f"{track}.png")
        img.save(img_save_path, "PNG")
        self.display_image(track)

    def undo(self, event):
        if self.search_entry.get():
            self.redo_stack.append(self.search_entry.get())
            if self.undo_stack:
                last_state = self.undo_stack.pop()
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, last_state)
            print("撤销")
        return "break"

    def redo(self, event):
        if self.redo_stack:
            last_state = self.redo_stack.pop()
            self.undo_stack.append(last_state)
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, last_state)
            print("重做")
        return "break"

    def show_popup(self, event):
        try:
            # 检查是否有选中的项
            selected_items = self.playlist.curselection()
            if not selected_items:
                return  # 如果没有选中的项，则不显示菜单

            # 显示菜单
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            # 确保菜单在点击其他位置时消失
            self.popup_menu.grab_release()

    def copy_selected(self):
        # 获取选中的项并复制到某个地方（例如剪贴板）
        selected_items = self.playlist.curselection()
        selected_texts = [self.playlist.get(index) for index in selected_items]
        text_to_copy = "\n".join(selected_texts)
        print(f'复制{text_to_copy}')
        # 这里只是简单地将文本打印出来，你可以根据需要修改（例如使用pyperclip库复制到剪贴板）
        pyperclip.copy(text_to_copy)

    def create_bottom_panel(self):
        # 创建底部框架，用于显示图片和例句
        self.bottom_frame = ttk.Frame(self.master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10, expand=True)

        # 图片显示模块
        self.image_frame = ttk.LabelFrame(self.bottom_frame, text="图片", width=400, height=400)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.image_frame.pack_propagate(0)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True)

        self.upload_button = ttk.Button(self.image_frame, text="上传图片", command=self.upload_image)
        self.upload_button.pack(side=tk.BOTTOM, pady=5)

        # 例句模块
        self.example_frame = ttk.LabelFrame(self.bottom_frame, text="例句", width=400, height=400)
        self.example_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.example_frame.pack_propagate(0)

        self.example_text = tk.Text(self.example_frame, wrap='word', font=("Helvetica", 14), height=15)
        self.example_text.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(self.example_frame, text="保存例句", command=self.save_example)
        self.save_button.pack(side=tk.BOTTOM, pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img  # 保存对图像对象的引用

            # 保存图片到指定目录
            track = self.playlist.get(self.current_track)
            img_save_path = os.path.join(self.music_picture_dir, f"{track}.png")
            with open(file_path, 'rb') as f_in, open(img_save_path, 'wb') as f_out:
                f_out.write(f_in.read())

    def save_example(self):
        example_text = self.example_text.get("1.0", tk.END).strip()
        track = self.playlist.get(self.current_track)
        example_file = os.path.join(self.music_examples_dir, f"{track}.txt")
        with open(example_file, 'w', encoding='utf-8') as file:
            file.write(example_text)
        # messagebox.showinfo("保存成功", f"例句已保存到 {example_file}")

    def text_changed(self, event=None):
        if self.auto_save:
            self.save_explanation()

    def save_explanation(self):
        text = self.text_display.get("1.0", tk.END).strip()
        track = self.playlist.get(self.current_track)
        explain_file = os.path.join(self.music_explain_dir, f"{track}.txt")
        with open(explain_file, 'w', encoding='utf-8') as file:
            file.write(text)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.search()

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
        self.explain_text = self.get_explain(track)

        # 显示对应图片
        self.display_image(track)

        # 显示对应例句
        self.display_example(track)
        self.display_explain(track)

    def display_image(self, track):
        img_path = f"{self.music_picture_dir}/{track}.png"
        if os.path.exists(img_path):
            # 获取LabelFrame的内部宽度和高度（去掉边框和填充）
            label_frame_width = self.image_frame.winfo_reqwidth() * 0.6
            label_frame_height = self.image_frame.winfo_reqheight() * 0.4
            img = Image.open(img_path)
            # 计算等比例缩放后的图片大小
            max_size = (label_frame_width, label_frame_height)
            img.thumbnail(max_size, Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img  # 保存对图像对象的引用

        else:
            # 图片不存在，清除图片
            self.image_label.config(image='')  # 清除图片

    def display_example(self, track):
        example_file = os.path.join(self.music_examples_dir, f"{track}.txt")
        if os.path.exists(example_file):
            with open(example_file, 'r', encoding='utf-8') as file:
                content = file.read()
            self.example_text.delete("1.0", tk.END)
            self.example_text.insert(tk.END, content)
        else:
            self.example_text.delete("1.0", tk.END)

    def display_explain(self, track):
        self.text_display.delete('1.0', tk.END)  # 删除当前所有内容
        self.text_display.insert(tk.END, track)  # 插入新文本
        self.text_display.insert(tk.END, "\n")  # 插入新文本
        self.text_display.insert(tk.END, "\n")  # 插入新文本
        self.text_display.insert(tk.END, self.explain_text)  # 插入新文本

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

        if self.selected_indices:
            for current_track in self.selected_indices:
                self.current_track = current_track
                track = self.playlist.get(self.current_track)
                file_path = os.path.join(self.music_dir, track + ".mp3")  # 假设文件后缀为 mp3
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                time.sleep(get_mp3_duration(file_path))

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
