from cProfile import label
import wx
import os
from loginform import LoginForm


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="TradePlaza", size=(400,400))
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(wx.Bitmap(os.getcwd() + r'\Phase II\trade_plaza_icon.png', wx.BITMAP_TYPE_ANY))
        self.RunLogin()

    def RunLogin(self):
        LoginForm(self)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow()
    app.MainLoop()