import wx

class SearchForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza-Search")
        self.SetIcon(parent.icon)
        self._logged_user = None

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        tmp = wx.StaticText(self, label="Search", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        tmp = wx.StaticText(self, label="_"*50)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        keyWordSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.byKeywordRb = wx.RadioButton(self, wx.ID_ANY, label="By Keyword:")
        keyWordSizer.Add(self.byKeywordRb, 0)
        self.byKeywordTxt = wx.TextCtrl(self, value = "", size=(100,-1))
        keyWordSizer.Add(self.byKeywordTxt, 0)
        formSizer.Add(keyWordSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.inMyPostalCodeRb = wx.RadioButton(self, wx.ID_ANY, label="In my postal code")
        formSizer.Add(self.inMyPostalCodeRb, 0, wx.EXPAND|wx.ALL, 5)

        radSizer = wx.BoxSizer(wx.HORIZONTAL)
        radSizer.Add(wx.StaticText(self, label="Within"), 0, wx.ALL, 5)
        self.radSpin = wx.SpinCtrl(self, wx.ID_ANY, initial=1, min=1, max=300, style= wx.SP_ARROW_KEYS)
        radSizer.Add(self.radSpin, 0)
        radSizer.Add(wx.StaticText(self, label="miles of me"), 0, wx.ALL, 5)
        formSizer.Add(radSizer, 0, wx.EXPAND|wx.ALL, 5)

        inPostalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inPostalRb = wx.RadioButton(self, wx.ID_ANY, label="By Keyword:")
        inPostalSizer.Add(self.inPostalRb, 0)
        self.inPostalTxt = wx.TextCtrl(self, value = "", size=(100,-1))
        inPostalSizer.Add(self.inPostalTxt, 0)
        formSizer.Add(inPostalSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.searchBtn = wx.Button(self, label="Search", style=wx.BORDER_NONE)
        self.searchBtn.SetBackgroundColour('blue')
        self.searchBtn.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoSearch, self.searchBtn)
        formSizer.Add(self.searchBtn, 0, wx.ALL, 5)
        self.SetSizerAndFit(formSizer)
   
    def DoSearch(self, event):
        pass

