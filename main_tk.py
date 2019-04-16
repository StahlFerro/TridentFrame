from tkinter import *


class Window(Frame):

    def __init__(self, master: Tk = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        m = self.master
        self.master.title("TridentFrame")
        self.pack(fill=BOTH, expand=1)
        exit_button = Button(self, text='Exit', command=self.exit_client)
        exit_button.place(x=275, y=350)

    def exit_client(self):
        exit()

root = Tk()
root.geometry("600x400")
app = Window(root)
root.mainloop()
