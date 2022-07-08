from cProfile import label
from tkinter.ttk import Style
import wx
import os
from loginform import LoginForm



class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="TradePlaza", size=(300,400))
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap(os.getcwd() + r'\source\trade_plaza_icon.png', wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.icon)
        self.RenderMainMenu()
        self.DoLogin()

    def RenderMainMenu(self):
        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)

        self.logout = wx.Button(self, label="logout", style=wx.BORDER_NONE)
        self.logout.SetBackgroundColour('blue')
        self.logout.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoLogout, self.logout)
        formSizer.Add(self.logout, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, 5)   

        boldFont = wx.Font(20, family = wx.FONTFAMILY_MODERN, style = wx.FONTSTYLE_NORMAL, weight = wx.FONTWEIGHT_BOLD)
        tmp = wx.StaticText(self, label="Trade Plaza", size=(-1,25))
        tmp.SetFont(boldFont)
        formSizer.Add(tmp, 0, wx.LEFT, 5)    

        tmp = wx.StaticText(self, label="_"*50)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT, 5)

        self.welcomeMsg = wx.StaticText(self, label="")
        formSizer.Add(self.welcomeMsg, 0, wx.ALL, 5)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        statsSizer = wx.BoxSizer(wx.VERTICAL)
        # add user stats
        statBox0 = wx.StaticBox(self, wx.ID_ANY, "Unaccepted trades", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox0Sizer = wx.StaticBoxSizer(statBox0, wx.VERTICAL)
        self.unacceptedTrades = wx.StaticText(self, label=" ", size=(120,-1), style=wx.ALIGN_CENTER)
        statbox0Sizer.Add(self.unacceptedTrades, 0, wx.EXPAND)
        statsSizer.Add(statbox0Sizer, 0, wx.ALL, 20)

        statBox1 = wx.StaticBox(self, wx.ID_ANY, "Response time", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox1Sizer = wx.StaticBoxSizer(statBox1, wx.VERTICAL)
        self.responseTime = wx.StaticText(self, label=" ", size=(120,-1), style=wx.ALIGN_CENTER)
        statbox1Sizer.Add(self.responseTime, 0, wx.EXPAND)
        statsSizer.Add(statbox1Sizer, 0, wx.ALL, 20)

        statBox2 = wx.StaticBox(self, wx.ID_ANY, "My rank", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox2Sizer = wx.StaticBoxSizer(statBox2, wx.VERTICAL)
        self.myRank = wx.StaticText(self, label=" ", size=(120,-1), style=wx.ALIGN_CENTER)
        statbox2Sizer.Add(self.myRank, 0, wx.EXPAND)
        statsSizer.Add(statbox2Sizer, 0, wx.ALL, 20)

        hSizer.Add(statsSizer, 0)
        ctrlSizer = wx.BoxSizer(wx.VERTICAL)

        self.listItem = wx.Button(self, label="list item", style=wx.BORDER_NONE, size=(100,50))
        self.listItem.SetBackgroundColour('blue')
        self.listItem.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoListItem, self.listItem)
        ctrlSizer.Add(self.listItem, 0,wx.ALL, 5)

        self.myItems = wx.Button(self, label="my items", style=wx.BORDER_NONE, size=(100,50))
        self.myItems.SetBackgroundColour('blue')
        self.myItems.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoMyItems, self.myItems)
        ctrlSizer.Add(self.myItems, 0,wx.ALL, 5)

        self.searchItems = wx.Button(self, label="search items", style=wx.BORDER_NONE, size=(100,50))
        self.searchItems.SetBackgroundColour('blue')
        self.searchItems.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoSearchItem, self.searchItems)
        ctrlSizer.Add(self.searchItems, 0,wx.ALL, 5)

        self.tradeHistory = wx.Button(self, label="Trade History", style=wx.BORDER_NONE, size=(100,50))
        self.tradeHistory.SetBackgroundColour('blue')
        self.tradeHistory.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoTradeHistory, self.tradeHistory)
        ctrlSizer.Add(self.tradeHistory, 0,wx.ALL, 5)

        hSizer.Add(ctrlSizer, 0)

        formSizer.Add(hSizer, 0, wx.EXPAND)
        self.SetSizer(formSizer)

    def SetWelcomeMsg(self, msg):
        self.welcomeMsg.SetLabel(msg)

    def SetUnacceptedTrades(self, msg):
        self.unacceptedTrades.SetLabel(msg)

    def SetResponseTime(self, msg):
        self.responseTime.SetLabel(msg)

    def SetMyRank(self, msg):
        self.myRank.SetLabel(msg)

    def DoListItem(self, event):
        pass

    def DoMyItems(self, event):
        pass

    def DoSearchItem(self, event):
        pass

    def DoTradeHistory(self, event):
        pass

    def DoLogin(self):
        lf = LoginForm(self)
        lf.ShowModal()
        
        # check if login is succesfull
        if lf._logged_user != None:
            self.Show(True)
        else:
            wx.MessageBox("Login failed", style=wx.OK) 
            self.DoLogin()

    def DoLogout(self, event):
        self.Hide()
        self.ClearForm()
        self.DoLogin()

    def ClearForm(self):
        pass

    def FillForm(self):
        pass

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow()
    app.MainLoop()