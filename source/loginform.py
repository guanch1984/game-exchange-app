import wx

class LoginForm(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="TradePlaza-Login")
        self.SetIcon(parent.icon)

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        formSizer.Add(wx.StaticText(self, label="Sign In"), 0, wx.ALL, 5)
        tmp = wx.StaticText(self, label="_"*50)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        formSizer.Add(wx.StaticText(self, label="Email/nickname"), 0, wx.ALL, 5)
        self.userEmail = wx.TextCtrl(self, value = "", size=(250,-1))
        formSizer.Add(self.userEmail, 0, wx.ALL, 5)
        formSizer.Add(wx.StaticText(self, label="Password"), 0, wx.ALL, 5)
        self.userPassword = wx.TextCtrl(self, value = "", size=(250,-1))
        formSizer.Add(self.userPassword, 0, wx.ALL, 5)
        self.tryLogin = wx.Button(self, label="Login", style=wx.BORDER_NONE)
        self.tryLogin.SetBackgroundColour('blue')
        self.tryLogin.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.LoginUser, self.tryLogin)
        formSizer.Add(self.tryLogin, 0, wx.ALL, 5)
        tmp = wx.StaticText(self, label="_"*50)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        formSizer.Add(wx.StaticText(self, label="New User"), 0, wx.ALL, 5)
        self.tryReg = wx.Button(self, label="Register", style=wx.BORDER_NONE)
        self.tryReg.SetBackgroundColour('blue')
        self.tryReg.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.RegNewUser, self.tryReg)
        formSizer.Add(self.tryReg, 0, wx.ALL, 5)
        self.SetSizerAndFit(formSizer)
        self.Show(True)
   
    def LoginUser(self, event):
        pass

    def RegNewUser(self, event):
        pass