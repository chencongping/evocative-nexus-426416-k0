import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class ImageDisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片显示与上传")

        # 图片显示模块
        self.image_frame = ttk.LabelFrame(self, text="图片")
        self.image_frame.pack(padx=10, pady=10)

        # 用于显示图片的Label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # 创建一个透明的Button来接收点击事件
        self.upload_button = tk.Button(self.image_frame, text="点击上传图片", command=self.upload_image)
        self.upload_button.pack()
        # 如果你想让Button看起来是透明的，并且与Label大小一致，需要进行额外的设置
        # 这里简化为一个普通的Button

    def upload_image(self):
        # 弹出文件选择对话框，让用户选择图片
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            # 加载并显示图片
            self.display_image(file_path)

    def display_image(self, image_path):
        # 使用PIL加载并缩放图片
        original_image = Image.open(image_path)
        photo = ImageTk.PhotoImage(original_image)

        # 在Label上显示图片
        self.image_label.config(image=photo)
        self.image_label.image = photo  # 保持对photo的引用


if __name__ == "__main__":
    app = ImageDisplayApp()
    app.mainloop()