from mysql.connector import Error
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
        self.gamePlatforms = []
        self.videoGameMedia = ['Optical Disk', 'Game Card', 'Cartridge']
        self.gameConditions = ['Like New', 'Lightly Used', 'Moderately Used', 'Heavily Used', 'Damaged/Missing']
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
        self.gtype = wx.ComboBox(self, id=wx.ID_ANY, choices = ["Board game", "Playing card game", "Collectible card game", "Computer game", "Video game"], 
        size=(180,-1), style=wx.CB_READONLY)
        self.gtype.SetSelection(4)
        self.Bind(wx.EVT_COMBOBOX, self.OnUpdateGameType, self.gtype)
        formSizer.Add(self.gtype, 0, wx.ALL, 5)

        tmp = wx.StaticText(self, label="Tile", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.titleTxt = wx.TextCtrl(self, id=wx.ID_ANY, value="", size=(180,-1))
        formSizer.Add(self.titleTxt, 0, wx.ALL, 5)

        fgs = wx.FlexGridSizer(8, 2, 5, 5)

        tmp = wx.StaticText(self, label="Condition", style=wx.ALIGN_BOTTOM)
        fgs.Add(tmp, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        tmp = wx.StaticText(self, label="No of cards", style=wx.ALIGN_BOTTOM)
        fgs.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)

        self.gCond = wx.ComboBox(self, id=wx.ID_ANY, choices = self.gameConditions, size=(100,-1), style=wx.CB_READONLY)
        self.gCond.SetSelection(0)
        fgs.Add(self.gCond, 0, wx.ALL, 5)
        self.nCards = wx.TextCtrl(self, id=wx.ID_ANY, value="", size=(100,-1))
        self.nCards.Enable(False)
        fgs.Add(self.nCards, 0, wx.ALL, 5)

        fgs.Add(wx.StaticText(self, label="Platform", style=wx.ALIGN_BOTTOM, size=(85,-1)), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        fgs.Add(wx.StaticText(self, label="Media", style=wx.ALIGN_BOTTOM, size=(85,-1)), 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.gamePlatforms = self.GetVideoGamePlatforms()
        self.gPlatform = wx.ComboBox(self, id=wx.ID_ANY, choices = self.gamePlatforms, size=(100,-1), style=wx.CB_READONLY)
        self.gPlatform.SetSelection(0)
        fgs.Add(self.gPlatform, 0, wx.ALL|wx.EXPAND, 5)   
        self.gMedia = wx.ComboBox(self, id=wx.ID_ANY, choices = self.videoGameMedia, size=(100,-1), style=wx.CB_READONLY)
        self.gMedia.SetSelection(0)
        fgs.Add(self.gMedia, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 5) 
        formSizer.Add(fgs, 0, wx.EXPAND)

        tmp = wx.StaticText(self, label="Description", style=wx.ALIGN_BOTTOM)
        formSizer.Add(tmp, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.gDescription = wx.TextCtrl(self, id=wx.ID_ANY, value="", style=wx.TE_MULTILINE, size=(200,150))
        formSizer.Add(self.gDescription, 0, wx.ALL, 5)

        self.listBtn = wx.Button(self, label="List Item", style=wx.BORDER_NONE)
        self.listBtn.SetBackgroundColour('blue')
        self.listBtn.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoListItem, self.listBtn)

        if self.GetPendingTrades() > 2:
            self.listBtn.Enable(False)

        formSizer.Add(self.listBtn, 0, wx.ALL, 5)
        self.SetSizerAndFit(formSizer)
   
    def GetPendingTrades(self):
        try:
            cursor = self.connection.cursor()
            query = """SELECT COUNT(item_number) FROM (SELECT item_number FROM (
                    SELECT item_number FROM BoardGame WHERE email=%(user_email)s
                    UNION 
                    SELECT item_number FROM PlayingCardGame WHERE email=%(user_email)s
                    UNION 
                    SELECT item_number FROM CollectibleCardGame WHERE email=%(user_email)s
                    UNION 
                    SELECT item_number FROM ComputerGame WHERE email=%(user_email)s
                    UNION 
                    SELECT item_number FROM VideoGame WHERE email= %(user_email)s) AS UserItems
                    INNER JOIN (SELECT counter_party_item_number FROM Trade WHERE trade_status = "PENDING") AS 
                    PendingTrades) AS PendingUserTrades""" 

            cursor.execute(query, {'user_email':self.user_id})
            res = cursor.fetchall()
            return res[0][0]
        except Error as e:
            wx.MessageBox("Error querying the DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return []

    def GetVideoGamePlatforms(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT name from platform" 
            cursor.execute(query)
            res = cursor.fetchall()
            return [x[0] for x in res]
        except Error as e:
            wx.MessageBox("Error querying the DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return []

    def OnUpdateGameType(self, event):
        selStr = event.GetEventObject().GetStringSelection()

        if selStr == "Board game" or selStr == "Playing card game":
            self.gPlatform.Enable(False)
            self.gMedia.Enable(False)
            self.nCards.Enable(False)
        if selStr == "Collectible card game":
            self.gPlatform.Enable(False)
            self.gMedia.Enable(False)
            self.nCards.Enable(True)
        elif selStr == "Computer game":
            self.gPlatform.Enable(True)
            self.gamePlatforms = ['Linux', 'MacOS', 'Windows']
            self.gPlatform.Set(self.gamePlatforms)
            self.gPlatform.SetSelection(0)
            self.gMedia.Enable(False)
            self.nCards.Enable(False)
        elif selStr == "Video game":
            self.gPlatform.Enable(True)
            self.gamePlatforms = self.GetVideoGamePlatforms()
            self.gPlatform.Set(self.gamePlatforms)
            self.gPlatform.SetSelection(0)
            self.gMedia.Enable(True)
            self.nCards.Enable(False)
        pass

    def DoListItem(self, event):
        selStr = self.gtype.GetStringSelection()
        title = self.titleTxt.GetValue()
        description = self.gDescription.GetValue()
        condition = self.gCond.GetStringSelection()
        query_dict = {'user_email':self.user_id, 'game_title':title, 'game_description':description, 'game_condition':condition}
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Item () VALUES ();" 
            cursor.execute(query)

            if selStr == "Board game":
                query =     """INSERT INTO BoardGame (item_number, title, description, game_condition, email)
                            SELECT NewItemNum.item_no, %(game_title)s , %(game_description)s, %(game_condition)s,%(user_email)s 
                            FROM (SELECT MAX(item_number) AS item_no FROM Item) AS NewItemNum"""
            elif selStr == "Playing card game":
                query =     """INSERT INTO PlayingCardGame (item_number, title, description, game_condition, email)
                            SELECT NewItemNum.item_no, %(game_title)s , %(game_description)s, %(game_condition)s,%(user_email)s 
                            FROM (SELECT MAX(item_number) AS item_no FROM Item) AS NewItemNum"""   
            elif selStr == "Collectible card game":
                query_dict['no_cards'] = self.nCards.GetValue() 
                query =     """INSERT INTO CollectibleCardGame (item_number, title, description, game_condition, number_of_Cards, email)
                            SELECT NewItemNum.item_no, %(game_title)s , %(game_description)s, %(game_condition)s, %(no_cards)s, %(user_email)s 
                            FROM (SELECT MAX(item_number) AS item_no FROM Item) AS NewItemNum"""
            elif selStr == "Computer game":
                query_dict['game_platform'] = self.gPlatform.GetStringSelection()
                query =     """INSERT INTO ComputerGame (item_number, title, description, game_condition, platform, email)
                            SELECT NewItemNum.item_no, %(game_title)s , %(game_description)s, %(game_condition)s, %(game_platform)s, %(user_email)s 
                            FROM (SELECT MAX(item_number) AS item_no FROM Item) AS NewItemNum"""
            elif selStr == "Video game":
                query_dict['game_platform_id'] = self.gPlatform.GetSelection() + 1
                print(self.gPlatform.GetSelection())
                query_dict['game_media'] = self.gMedia.GetStringSelection()
                query =     """INSERT INTO VideoGame (item_number, title, description, game_condition, media, platform_id, email)
                            SELECT NewItemNum.item_no, %(game_title)s , %(game_description)s, %(game_condition)s, %(game_media)s, %(game_platform_id)s, %(user_email)s 
                            FROM (SELECT MAX(item_number) AS item_no FROM Item) AS NewItemNum"""                      
            cursor.execute(query, query_dict)
            self.connection.commit()

            # Get the item number of the newly added item
            query = """SELECT MAX(item_number) AS item_no FROM Item"""
            cursor.execute(query)
            item_number = cursor.fetchall()[-1][-1]
            wx.MessageBox(message="Your item has been listed!\nYour item number is {}".format(item_number), caption="Success", style=wx.OK)
            self.EndModal(wx.OK)
        except Error as e:
            wx.MessageBox("Error querying the DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return []

            

