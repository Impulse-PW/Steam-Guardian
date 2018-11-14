#This must be first
from gevent import monkey
monkey.patch_all(thread=False)
from lib import *
from tkinter import Tk

#Main function
def main():
    colorDic = colors()
    colorDic = colorDic.colorDic
    root = Tk()
    mainWindow(root, colorDic).pack()
    root.mainloop()
#Start main function
if __name__ == "__main__":
    main()
