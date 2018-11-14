from tkinter import *
import pyperclip

class guiController(object):
    #Initialize
    def __init__(self, parent, colorDic=None):
        #Class variables
        self.colorDic = colorDic
        self.parent = parent
    #Center window on screen method
    def center(self):
        #Geomotry and screen calculations to center our window
        #Taken from https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        self.parent.update_idletasks()
        width = self.parent.winfo_width()
        frm_width = self.parent.winfo_rootx() - self.parent.winfo_x()
        win_width = width + 2 * frm_width
        height = self.parent.winfo_height()
        titlebar_height = self.parent.winfo_rooty() - self.parent.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.parent.winfo_screenwidth() // 2 - win_width // 2
        y = self.parent.winfo_screenheight() // 2 - win_height // 2
        self.parent.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.parent.deiconify()
    #Copy label's text method
    def copy_label_text(self, label):
        #Copy code to clipboard
        pyperclip.copy(label["text"])
    #Canvas on configure method
    def on_configure(self, event):
        #Set scroll region to everything in canvas
        event.widget.configure(scrollregion=event.widget.bbox('all'))
    #Special button highlight method
    def special_button_hover(self, event):
        #Update button color when mouse enters
        event.widget.configure(bg=self.colorDic["specialButtonBackgroundHover"])

        for item in event.widget.children.values():
            item.configure(bg=self.colorDic["specialButtonBackgroundHover"])
    #Special button highlight remove method
    def special_button_leave(self, event):
        #Update button color when mouse leaves
        event.widget.configure(bg=self.colorDic["specialButtonBackground"])

        for item in event.widget.children.values():
            item.configure(bg=self.colorDic["specialButtonBackground"])
