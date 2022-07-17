import wx

class ProposeTradeForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
            self.tradeitem = kwargs.pop("tradeitem")
            self.tradeitemnumber = kwargs.pop("tradeitemnumber")
            self.distance = kwargs.pop("distance")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza")
        # self.SetIcon(parent.icon)

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
        distance = self.distance
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
        """.format(self.user_id, self.user_id)

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
        for row, item in enumerate(cursor.fetchall()):
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
            INSERT INTO Trade (proposer_item_number, counter_party_item_number, trade_status, proposed_date, accept_reject_date) 
            VALUES ({}, {}, "PENDING", NOW(), NULL)
        """.format(myitemnumber, self.tradeitemnumber)

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
        # Confirmation message to bring user back to the main page
        res = wx.MessageBox("Trade proposed. Returning to main menu.", 'Ok', wx.OK )
        self.EndModal(wx.ID_EXIT)