import tkinter as tk
from tkinter import Menu, messagebox


class PlayerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 创建播放列表框架（假设你已经有了这个框架）
        self.playlist_frame = tk.Frame(self)
        self.playlist_frame.pack(fill="both", expand=True)

        # 创建播放列表
        self.playlist = tk.Listbox(self.playlist_frame, selectmode="extended", font=("Arial", 12))
        self.update_playlist()  # 假设这个函数用于填充播放列表
        self.playlist.pack(fill="both", expand=True)

        # 创建右键菜单
        self.popup_menu = Menu(self.playlist, tearoff=0)
        self.popup_menu.add_command(label="复制", command=self.copy_selected)

        # 绑定右键点击事件
        self.playlist.bind("<Button-3>", self.show_popup)

    def update_playlist(self):
        # 这里应该填充你的播放列表，例如：
        self.playlist.insert(tk.END, "歌曲1")
        self.playlist.insert(tk.END, "歌曲2")
        self.playlist.insert(tk.END, "歌曲3")

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

        # 这里只是简单地将文本打印出来，你可以根据需要修改（例如使用pyperclip库复制到剪贴板）
        messagebox.showinfo("复制", "已复制：\n" + text_to_copy)

    # 创建并运行应用


app = PlayerApp()
app.mainloop()