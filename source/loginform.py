import wx
from registrationform import RegistrationForm

class LoginForm(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="TradePlaza-Login")
        self.SetIcon(parent.icon)
        self._doExit = False
        self._logged_user = None

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        formSizer.Add(wx.StaticText(self, label="Sign In"), 0, wx.ALL, 5)
        tmp = wx.StaticText(self, label="_"*35)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)
        formSizer.Add(wx.StaticText(self, label="Email/nickname"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.userEmail = wx.TextCtrl(self, value = "", size=(150,-1))
        formSizer.Add(self.userEmail, 0, wx.ALL, 5)
        formSizer.Add(wx.StaticText(self, label="Password"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.userPassword = wx.TextCtrl(self, value = "", size=(150,-1))
        formSizer.Add(self.userPassword, 0, wx.ALL, 5)

        self.tryLogin = wx.Button(self, label="Login", style=wx.BORDER_NONE)
        self.tryLogin.SetBackgroundColour('blue')
        self.tryLogin.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.LoginUser, self.tryLogin)
        formSizer.Add(self.tryLogin, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        tmp = wx.StaticText(self, label="_"*35)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)
        formSizer.Add(wx.StaticText(self, label="New User"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.tryReg = wx.Button(self, label="Register", style=wx.BORDER_NONE)
        self.tryReg.SetBackgroundColour('blue')
        self.tryReg.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.RegNewUser, self.tryReg)

        self.tryExit = wx.Button(self, label="Exit", style=wx.BORDER_NONE)
        self.tryExit.SetBackgroundColour('blue')
        self.tryExit.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.tryExit)

        formSizer.Add(self.tryReg, 0, wx.ALL, 5)
        formSizer.Add(self.tryExit, 0, wx.ALL, 5)
        self.SetSizerAndFit(formSizer)


   
    def LoginUser(self, event):
        self._logged_user = "test_user"
        self.Close()

    def RegNewUser(self, event):
        self.Hide()
        rf = RegistrationForm(self.Parent)
        rf.ShowModal()
        
        if rf._new_user != None:
            self._logged_user = rf._new_user
            self.Close()

    def OnExit(self,e):
        self.Close(True)  # Close the frame.
        self._doExit = True