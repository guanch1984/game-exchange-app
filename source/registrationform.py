import wx
import mysql

class RegistrationForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza-Registration")
        self.SetIcon(parent.icon)
        self._new_user = None

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        tmp = wx.StaticText(self, label="Registration")
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*60)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        fgs = wx.FlexGridSizer(12, 2, 5, 5)
        fgs.Add(wx.StaticText(self, label="Email"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        fgs.Add(wx.StaticText(self, label="First Name"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.userEmail = wx.TextCtrl(self, value = "", size=(150,-1))
        fgs.Add(self.userEmail, 0, wx.ALL, 5)        
        self.userFirstName = wx.TextCtrl(self, value = "", size=(150,-1))
        fgs.Add(self.userFirstName, 0, wx.ALL, 5)

        fgs.Add(wx.StaticText(self, label="Password"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        fgs.Add(wx.StaticText(self, label="Last Name"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.userPassword = wx.TextCtrl(self, value = "", size=(150,-1))
        fgs.Add(self.userPassword, 0, wx.ALL, 5)
        self.userLastName = wx.TextCtrl(self, value = "", size=(150,-1))
        fgs.Add(self.userLastName, 0, wx.ALL, 5)

        fgs.Add(wx.StaticText(self, label="Nickname"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        fgs.Add(wx.StaticText(self, label="Postal Code"), 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.userNickname = wx.TextCtrl(self, value = "", size=(150,-1))
        fgs.Add(self.userNickname, 0, wx.ALL, 5)
        self.userPostalCode = wx.TextCtrl(self, value = "", size=(150,-1))
        fgs.Add(self.userPostalCode, 0, wx.ALL, 5)

        formSizer.Add(fgs, 0)

        self.tryLogin = wx.Button(self, label="Register", style=wx.BORDER_NONE)
        self.tryLogin.SetBackgroundColour('blue')
        self.tryLogin.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.RegisterUser, self.tryLogin)
        formSizer.Add(self.tryLogin, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 5)

        self.SetSizerAndFit(formSizer)
   
    def RegisterUser(self, event):
        user_id = self.userEmail.GetValue()
        user_password = self.userPassword.GetValue()
        user_nickname = self.userNickname.GetValue()
        user_firstname= self.userFirstName.GetValue()
        user_lastname = self.userLastName.GetValue()
        user_postalcode = self.userPostalCode.GetValue()

        success = False
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO TradePlazaUser (email, password, nickname, first_name, last_name, postal_code) VALUES " + \
                "(\"" + user_id + "\", \"" + user_password + "\", \"" + user_nickname + "\", \"" + user_firstname + "\", \"" + \
                    user_lastname + "\", \"" + user_postalcode + "\")"
            cursor.execute(query)
            self.connection.commit()
            success = True
        except mysql.connector.Error as e:
            wx.MessageBox("Error registering new user to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            success = False

        # query the database to add new user
        if success:
            self._new_user = user_id
            self.EndModal(wx.ID_OK)
