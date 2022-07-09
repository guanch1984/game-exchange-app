import wx

class TradeHistoryForm(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="main")
        self.SetIcon(parent.icon)
        self._new_user = None

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        tmp = wx.StaticText(self, label="Trade History")
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*125)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT, 5)

        self.tryBack = wx.Button(self, label="Back", style=wx.BORDER_NONE)
        self.tryBack.SetBackgroundColour('blue')
        self.tryBack.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoBack, self.tryBack)
        formSizer.Add(self.tryBack, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)

        self.SetSizerAndFit(formSizer)

    def TradeSummary(self, event):
        pass

    def TradeDetail(self, event):
        pass

    def DoBack(self, parent, e=None):
        from main import MainWindow
        self.Hide()
        lf = MainWindow(parent)
        lf.ShowModal()
        lf.Destroy()
