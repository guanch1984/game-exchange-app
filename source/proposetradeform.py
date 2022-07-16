import wx
from mysql.connector import Error


class ProposeTradeForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_email = kwargs.pop("user_email")
            self.user_id = kwargs.pop("user_id")
            self.tradeitem = kwargs.pop("tradeitem")
            self.tradeitemnumber = kwargs.pop("tradeitemnumber")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza")
        self.SetIcon(parent.icon)
        self._logged_user = None

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        formSizer.Add(wx.StaticText(self, label="Propose Trade"), 0, wx.ALL, 1)
        tmp = wx.StaticText(self, label="_"*120)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 2)


        formSizer.Add(self.CheckDistanceWarning(), wx.CENTER, 3)

        tradeLabel = wx.StaticText(self, label="Proposing Trade for\n{}".format(str(self.tradeitem)))
        self.confirmBtn = wx.Button(self, id=wx.ID_NEW, label="Confirm", style=wx.BORDER_NONE)
        self.confirmBtn.SetBackgroundColour('gray')
        self.confirmBtn.SetForegroundColour('white')
        self.confirmBtn.Disable()
        self.confirmBtn.Bind(wx.EVT_BUTTON, self.onConfirm)

        subFormSizer = wx.BoxSizer(wx.HORIZONTAL)
        subFormSizer.Add(tradeLabel, 0, wx.ALL, 3)
        subFormSizer.Add(wx.StaticText(self, label=" " * 100), 0, wx.ALL, 4)
        subFormSizer.Add(self.confirmBtn, 0, wx.ALL, 4)

        formSizer.Add(subFormSizer, 0, wx.ALL, 3)
        formSizer.Add

        itemGrid = self.PopulateMyTradeItems()
        formSizer.Add(wx.StaticText(self, label="Please choose your proposed item:"), 0, wx.ALL, 4)
        formSizer.Add(itemGrid, 0, wx.ALL, 5)

        self.SetSizerAndFit(formSizer)

    def CheckDistanceWarning(self):
        query = """
            SELECT (3958.75 * 2 * POWER(ATAN(SQRT((POWER(SIN((offered_address.Latitude - my_address.Latitude) / 2), 2) + COS(my_address.Latitude) * COS(offered_address.Latitude) * POWER(SIN((offered_address.Longitude - my_address.Longitude) / 2), 2))), SQRT(1 - (POWER(SIN((offered_address.Latitude - my_address.Latitude) / 2), 2) + COS(my_address.Latitude) * COS(offered_address.Latitude) * POWER(SIN((offered_address.Longitude - my_address.Longitude) / 2), 2)))), 2)) as distance
            FROM (SELECT item_number, email FROM BoardGame WHERE item_number = {item_number} UNION
                        SELECT item_number, email FROM CollectibleCardGame WHERE item_number = {item_number} UNION
                        SELECT item_number, email FROM ComputerGame WHERE item_number = {item_number} UNION
                        SELECT item_number, email FROM PlayingCardGame WHERE item_number = {item_number} UNION
                        SELECT item_number, email FROM VideoGame WHERE item_number = {item_number}
                    ) as offered_item INNER JOIN tradeplazauser as offered_user on offered_user.email = offered_item.email
                    INNER JOIN address as offered_address ON offered_user.postal_code = offered_address.postal_code
                    CROSS JOIN (SELECT * FROM tradeplazauser WHERE email = "{email}" or nickname = "{nickname}") as my_user
                    INNER JOIN address as my_address ON my_user.postal_code = my_address.postal_code
        """.format(item_number="1", email=self.user_email, nickname=self.user_id)
        cursor = self.connection.cursor()
        cursor.execute(query)

        data = cursor.fetchall()
        if (data is not None and len(data) > 0):
            distance = data[0][0]

        distanceLabel = wx.StaticText(self, label="{1}The other user is {0} miles away!{1}".format(str(distance), " " * 30))
        distanceLabel.SetBackgroundColour('blue')
        if distance >= 100:
            distanceLabel.SetBackgroundColour('red')

        return distanceLabel

    def PopulateMyTradeItems(self):
        query = """
            SELECT item_number, game_type, title, game_condition
            FROM (
                    SELECT email, item_number, title, game_condition, 'Board Game' AS game_type FROM BoardGame UNION
                    SELECT email, item_number, title, game_condition, 'Playing Cards' as game_type FROM PlayingCardGame UNION
                    SELECT email, item_number, title, game_condition, 'Collectible Card Game' AS game_type FROM CollectibleCardGame UNION
                    SELECT email, item_number, title, game_condition, 'Video Game' AS game_type FROM VideoGame UNION
                    SELECT email, item_number, title, game_condition, 'Computer Game' AS game_type FROM ComputerGame
                ) as all_games NATURAL JOIN tradeplazauser
            WHERE (email = "{}" OR nickname = "{}") AND
                item_number NOT IN (
                    SELECT proposer_item_number as item_number FROM Trade WHERE trade_status = "ACCEPT" OR trade_status = "REJECT"
                )
            ORDER BY item_number ASC
        """.format(self.user_email, self.user_id)

        # Generate grid to display data in
        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        self.grid_ref = itemsGrid
        itemsGrid.CreateGrid(0, 4)
        itemsGrid.HideRowLabels()
        itemsGrid.SetColLabelValue(0, "Item #")
        itemsGrid.SetColLabelValue(1, "Game Type")
        itemsGrid.SetColLabelValue(2, "Title")
        itemsGrid.SetColLabelValue(3, "Condition")
        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)

        # Grid binding for if a row is selected
        itemsGrid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onGridSelect)

        # Populate the grid with data
        cursor = self.connection.cursor()
        cursor.execute(query)
        for row, item in enumerate(cursor.fetchall() * 2):
            itemsGrid.AppendRows(numRows=1)
            for col, attribute in enumerate(item):
                itemsGrid.SetCellValue(row, col, str(attribute))
                itemsGrid.SetReadOnly(row, col, True)
            
        # Bad code, but I just want this to work, I hate wxPython
        return itemsGrid

    def onGridSelect(self, event):
        self.grid_ref.SelectRow(event.Row, True)
        self.confirmBtn.Enable()
        self.confirmBtn.SetBackgroundColour('blue')

    def onConfirm(self, event):
        pass
        # Confirm the trade
        myitemnumber = self.grid_ref.GetCellValue(self.grid_ref.GetSelectedRows()[0], 0)
        
        query = """
            UPDATE Trade SET counter_party_item_number = {}, proposed_date = NOW() WHERE proposer_item_number = {} AND counter_party_item_number IS NULL
        """.format(myitemnumber, self.tradeitemnumber)

        cursor = self.connection.cursor()
        cursor.execute(query)
        
        # Confirmation message to bring user back to the main page
        res = wx.MessageBox("Trade proposed. Returning to main menu.", 'Ok', wx.OK )
        self.EndModal(wx.ID_EXIT)