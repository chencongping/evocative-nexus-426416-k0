import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime  # 导入datetime模块


def update_text(text_widget, new_text):
    """动态更新Text控件的内容"""
    text_widget.delete('1.0', tk.END)  # 删除当前所有内容
    text_widget.insert(tk.END, new_text)  # 插入新文本


def create_window():
    root = tk.Tk()
    root.title("底部多行显示框示例")

    # 创建一个滚动文本控件来显示多行文本
    text_widget = scrolledtext.ScrolledText(root, wrap='word', height=10, width=50)
    text_widget.pack(side=tk.BOTTOM, fill=tk.X, expand=False, pady=(0, 10))  # 放置在底部

    # 初始文本内容
    initial_text = "这是初始文本内容，可以很长很长，会自动换行显示。\n这是第二行内容。\n..."
    update_text(text_widget, initial_text)

    # 模拟动态更新文本内容（例如，每隔一段时间）
    def update_content():
        current_time = datetime.fromtimestamp(int(time.time()))  # 使用datetime.fromtimestamp方法获取当前时间
        new_text = "这是新的文本内容，同样可以很长很长。\n时间戳: {}\n...".format(current_time)
        update_text(text_widget, new_text)
        root.after(2000, update_content)  # 每2秒更新一次内容

    # 导入time模块以获取时间戳
    import time

    # 开始定时更新内容
    update_content()

    # 运行Tkinter事件循环
    root.mainloop()


# 调用函数创建窗口
create_window()