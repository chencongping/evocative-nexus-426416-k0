import tkinter as tk


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Frame Size Example")

        # 创建一个父级框架
        self.playlist_frame = tk.Frame(self, bg='lightblue')  # 添加背景色以便观察
        self.playlist_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 创建一个按钮，点击时打印父级框架的长宽
        self.btn_check_size = tk.Button(self, text="Check Frame Size", command=self.check_frame_size)
        self.btn_check_size.pack(pady=20)

        # 创建播放列表（这里只是示例，没有实际内容）
        self.playlist = tk.Listbox(self.playlist_frame, selectmode="extended", font=("Arial", 14))
        self.playlist.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    def check_frame_size(self):
        # 获取父级框架的宽度和高度
        width = self.playlist_frame.winfo_width()
        height = self.playlist_frame.winfo_height()
        print(f"Frame width: {width} pixels")
        print(f"Frame height: {height} pixels")


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()