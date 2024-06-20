import tkinter as tk


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 创建一个父级框架（例如，整个窗口）
        self.playlist_frame = tk.Frame(self)
        self.playlist_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 创建一个内部框架，其宽度将是父级框架宽度的40%
        inner_frame = tk.Frame(self.playlist_frame)
        inner_frame.pack(side="left", fill="y", expand=False)  # 只在垂直方向上填充，不扩展

        # 使用grid布局管理器在内部框架中放置列表框，并设置列宽为内部框架宽度的100%
        self.playlist = tk.Listbox(inner_frame, selectmode="extended", font=("Arial", 14))
        self.playlist.grid(row=0, column=0, sticky="nsew")  # 填充所有可用空间

        # 设置内部框架的宽度为父级框架宽度的40%
        # 需要先知道父级框架的宽度（这里假设已经设置或可以获取），然后设置内部框架的宽度
        # 但Tkinter的窗口大小是动态的，所以你可能需要使用窗口的resize事件或其他机制来动态调整
        # 这里只是示例，假设我们知道父级框架的宽度是400像素
        inner_frame_width = int(400 * 0.4)
        inner_frame.config(width=inner_frame_width)

        # 更新播放列表（这里只是示例）
        self.update_playlist()

    def update_playlist(self):
        # 在这里添加代码来更新播放列表的内容
        for i in range(10):
            self.playlist.insert(tk.END, f"Track {i + 1}")


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()