import tkinter
import tkinter.messagebox


def hello_callback():
    tkinter.messagebox.showinfo("Hello Python", "Hello Runoob")


async def task_ui():
    root_window = tkinter.Tk()
    b = tkinter.Button(root_window, text="关闭", command=hello_callback)
    b.pack(side="bottom")

    root_window.iconbitmap()
    #  窗口标题
    root_window.title("SETEC POWER OCPP2.0.1 报文测试工具")
    # 窗口大小
    root_window.geometry("400x250")

    # root_window.title('GUI图形用户界面')
    # # 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
    # root_window.geometry('450x300')
    # # 更改左上角窗口的的icon图标
    # # root_window.iconbitmap('C:/Users/Administrator/Desktop/favicon.ico')
    # # 设置主窗口的背景颜色,颜色值可以是英文单词，或者颜色值的16进制数,除此之外还可以使用Tk内置的颜色常量
    # root_window["background"] = "#C9C9C9"
    # # 添加文本内,设置字体的前景色和背景色，和字体类型、大小
    # text = tkinter.Label(root_window, text="tkinter欢迎您", bg="yellow", fg="red", font=('Times', 20, 'bold italic'))
    # # 将文本内容放置在主窗口内
    # text.pack()
    # # 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
    # button = tkinter.Button(root_window, text="关闭", command=root_window.quit)
    # # 将按钮放置在主窗口内
    # button.pack(side="bottom")

    root_window.mainloop()
