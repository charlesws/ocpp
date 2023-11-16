import tkinter
import tkinter.messagebox


def hello_callback():
    tkinter.messagebox.showinfo("Hello Python", "Hello Runoob")


async def task_ui():
    root = tkinter.Tk()
    b = tkinter.Button(root, text="点我", command=hello_callback)
    b.pack()

    #  窗口标题
    root.title("我的个性签名设计")
    # 窗口大小
    root.geometry("600x450+374+182")

    root.mainloop()
