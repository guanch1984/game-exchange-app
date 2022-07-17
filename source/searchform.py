import wx,mysql
from query_search import keyword_search,my_postal_search,within_miles_search,in_postal_search
from searchresults import SearchResults

class SearchForm(wx.Dialog):
    def __init__(self, parent,**kwargs):
        try:
            self.connection = kwargs.pop("connection")
        except:
            self.Destroy()
        
        super().__init__(parent, title="TradePlaza-Search")
        self.SetIcon(parent.icon)
        self.user_email = parent.logged_user

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        tmp = wx.StaticText(self, label="Search", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        tmp = wx.StaticText(self, label="_"*50)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        keyWordSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.byKeywordRb = wx.RadioButton(self, wx.ID_ANY, label="By keyword:")
        keyWordSizer.Add(self.byKeywordRb, 0)
        self.byKeywordTxt = wx.TextCtrl(self, value = "", size=(100,-1))
        keyWordSizer.Add(self.byKeywordTxt, 0)
        formSizer.Add(keyWordSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.inMyPostalCodeRb = wx.RadioButton(self, wx.ID_ANY, label="In my postal code")
        formSizer.Add(self.inMyPostalCodeRb, 0, wx.EXPAND|wx.ALL, 5)

        radSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.withinMilesRb = wx.RadioButton(self, wx.ID_ANY, label="Within")
        radSizer.Add(self.withinMilesRb, 0)
        # radSizer.Add(wx.StaticText(self, label="Within"), 0, wx.ALL, 5)
        self.radSpin = wx.SpinCtrl(self, wx.ID_ANY, initial=1, min=1, max=100000, style= wx.SP_ARROW_KEYS)
        radSizer.Add(self.radSpin, 0)
        radSizer.Add(wx.StaticText(self, label="miles of me"), 0, wx.ALL, 5)
        formSizer.Add(radSizer, 0, wx.EXPAND|wx.ALL, 5)

        inPostalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inPostalRb = wx.RadioButton(self, wx.ID_ANY, label="In postal code:")
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
        if not(self.byKeywordRb.GetValue() or self.inMyPostalCodeRb.GetValue() or self.inPostalRb.GetValue() or self.withinMilesRb.GetValue()):
            res=wx.MessageBox("No search option selected", 'Error', wx.OK|wx.CANCEL|wx.ICON_ERROR )
            if res != wx.OK:
                self.EndModal(wx.ID_EXIT)

        # keyword
        if self.byKeywordRb.GetValue():
            if self.byKeywordTxt.GetValue().strip()=="":
                res=wx.MessageBox("Search by Keyword Selected, but no keyword entered", 'Error', wx.OK|wx.CANCEL|wx.ICON_ERROR )
                if res != wx.OK:
                    self.EndModal(wx.ID_EXIT)

            else:
                try:
                    cursor = self.connection.cursor()
                    query = keyword_search(self.user_email, self.byKeywordTxt.GetValue().strip())

                    cursor.execute(query)
                    res = cursor.fetchall()
                    search_type="keyword " + self.byKeywordTxt.GetValue().strip()
                except mysql.connector.Error as e:
                    wx.MessageBox("Error Searching for items: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
                    return False

        # postal code

        if self.inMyPostalCodeRb.GetValue():
            try:
                cursor = self.connection.cursor()
                query = my_postal_search(self.user_email)

                cursor.execute(query)
                res = cursor.fetchall()
                search_type="In my postal code "
            except mysql.connector.Error as e:
                wx.MessageBox("Error Searching for items: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
                return False

        #within miles
        if self.withinMilesRb.GetValue():
            try:
                cursor = self.connection.cursor()
                query = within_miles_search(self.user_email,self.radSpin.GetValue())

                cursor.execute(query)
                res = cursor.fetchall()
                search_type="within" + str(self.radSpin.GetValue()) + " miles "
            except mysql.connector.Error as e:
                wx.MessageBox("Error Searching for items: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
                return False

        
        #In Postal code
        if self.inPostalRb.GetValue():
            if self.inPostalTxt.GetValue().strip()=="":
                res=wx.MessageBox("Search by postal code Selected, but no code entered", 'Error', wx.OK|wx.CANCEL|wx.ICON_ERROR )
                if res != wx.OK:
                    self.EndModal(wx.ID_EXIT)
            try:
                cursor = self.connection.cursor()
                query = in_postal_search(self.user_email,self.inPostalTxt.GetValue().strip())

                cursor.execute(query)
                res = cursor.fetchall()
                search_type="In postal code " + self.inPostalTxt.GetValue()
            except mysql.connector.Error as e:
                wx.MessageBox("Error Searching for items: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
                return False

        self.Hide()
        sr=SearchResults(self.Parent, user_id=self.user_email,res=res,search_type=search_type,connection=self.connection)
        r=sr.ShowModal()
        if r == wx.ID_OK:
            self.EndModal(wx.ID_OK)