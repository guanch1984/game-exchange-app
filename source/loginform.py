import wx
import mysql
from registrationform import RegistrationForm

class LoginForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza-Login")
        self.SetIcon(parent.icon)
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

        self.tryLogin = wx.Button(self, id=wx.ID_EXECUTE, label="Login", style=wx.BORDER_NONE)
        self.tryLogin.SetBackgroundColour('blue')
        self.tryLogin.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.LoginUser, self.tryLogin)
        formSizer.Add(self.tryLogin, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        tmp = wx.StaticText(self, label="_"*35)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)
        formSizer.Add(wx.StaticText(self, label="New User"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.tryReg = wx.Button(self, id=wx.ID_NEW, label="Register", style=wx.BORDER_NONE)
        self.tryReg.SetBackgroundColour('blue')
        self.tryReg.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.RegNewUser, self.tryReg)

        formSizer.Add(self.tryReg, 0, wx.ALL, 5)
        self.SetSizerAndFit(formSizer)
   
    def ValidateUser(self, user_id, user_password):
        try:
            cursor = self.connection.cursor()
            query = "SELECT email from TradePlazaUser where (TradePlazaUser.email=" + "\"" + user_id  + \
            "\"" + " or TradePlazaUser.nickname=" + "\"" + user_id  + "\"" + ") and TradePlazaUser.password=" + "\"" + user_password  + "\""
            cursor.execute(query)
            res = cursor.fetchall()
            if len(res) == 1:
                return True
            else:
                return False
        except mysql.connector.Error as e:
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return False


    def LoginUser(self, event):
        user_id = self.userEmail.GetValue()
        user_password = self.userPassword.GetValue()
        if user_id == "" or user_password == "":
            return
        validated = self.ValidateUser(user_id, user_password)

        if validated:
            self._logged_user = user_id
            self.EndModal(wx.ID_OK)
        else:
            res = wx.MessageBox("Invalid user credentials. Retry?", 'Error', wx.OK|wx.CANCEL|wx.ICON_ERROR )
            if res != wx.OK:
                self.EndModal(wx.ID_EXIT)

    def RegNewUser(self, event):
        self.Hide()
        rf = RegistrationForm(self.Parent)
        res = rf.ShowModal()
        if res == wx.ID_OK:
            self._logged_user = rf._new_user
            self.EndModal(wx.ID_OK)