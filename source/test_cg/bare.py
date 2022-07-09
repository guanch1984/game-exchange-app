import wx

class App(wx.App):

   def OnInit(self):
      frame = wx.Frame(parent=None, title='Bare')
      frame.Show()
      return True

app = App()
app.MainLoop()
# if __name__ == '__main__':
#    app = wx.App(False)
#    # frame = MainWindow()
#    app.MainLoop()