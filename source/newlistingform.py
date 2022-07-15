import wx

class NewListingForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza-New Item Listing")
        self.SetIcon(parent.icon)
        self._logged_user = None

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        tmp = wx.StaticText(self, label="New Item Listing", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        tmp = wx.StaticText(self, label="_"*40)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        tmp = wx.StaticText(self, label="Game Type", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.gtype = wx.ComboBox(self, id=wx.ID_ANY, choices = ["Board game", "Playing card game", "Collectible card game", "Computer game", "Video game"], size=(180,-1))
        self.gtype.SetSelection(4)
        self.Bind(wx.EVT_COMBOBOX, self.OnUpdateGameType, self.gtype)
        formSizer.Add(self.gtype, 0, wx.ALL, 5)

        tmp = wx.StaticText(self, label="Tile", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.titleTxt = wx.TextCtrl(self, id=wx.ID_ANY, value="", size=(180,-1))
        formSizer.Add(self.titleTxt, 0, wx.ALL, 5)

        tmp = wx.StaticText(self, label="Condition", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.gCond = wx.ComboBox(self, id=wx.ID_ANY, choices = ["Like new"], size=(85,-1))
        self.gCond.SetSelection(0)
        formSizer.Add(self.gCond, 0, wx.ALL, 5)

        hsizer0 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer0.Add(wx.StaticText(self, label="Platform", style=wx.ALIGN_BOTTOM, size=(85,-1)), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        hsizer0.Add(wx.StaticText(self, label="Media", style=wx.ALIGN_BOTTOM, size=(85,-1)), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        formSizer.Add(hsizer0, 0, wx.EXPAND)

        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.gPlatform = wx.ComboBox(self, id=wx.ID_ANY, choices = ["Nintendo"], size=(85,-1))
        self.gPlatform.SetSelection(0)
        hsizer1.Add(self.gPlatform, 0, wx.ALL|wx.EXPAND, 5)        
        self.gMedia = wx.ComboBox(self, id=wx.ID_ANY, choices = ["Game card"], size=(85,-1))
        self.gMedia.SetSelection(0)
        hsizer1.Add(self.gMedia, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 5) 
        formSizer.Add(hsizer1, 0, wx.EXPAND)

        tmp = wx.StaticText(self, label="Description", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.gDescription = wx.TextCtrl(self, id=wx.ID_ANY, value="", style=wx.TE_MULTILINE, size=(200,150))
        formSizer.Add(self.gDescription, 0, wx.ALL, 5)

        self.listBtn = wx.Button(self, label="List Item", style=wx.BORDER_NONE)
        self.listBtn.SetBackgroundColour('blue')
        self.listBtn.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoListItem, self.listBtn)
        formSizer.Add(self.listBtn, 0, wx.ALL, 5)
        self.SetSizerAndFit(formSizer)
   
    def OnUpdateGameType(self):
        pass

    def DoListItem(self, event):
        wx.MessageBox(message="Your item has been listed!\nYour item number is 1.", caption="Success", style=wx.OK)

