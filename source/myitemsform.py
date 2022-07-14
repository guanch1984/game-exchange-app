import wx
import wx.grid

class MyItemsForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza-My Items")
        self.SetIcon(parent.icon)
        self.user_email = kwargs.pop("user_email")

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = formSizer
        tmp = wx.StaticText(self, label="Item Counts")
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*80)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        self.AddCounts()

        tmp = wx.StaticText(self, label="My Items")
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*80)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        
        self.AddItems()
        self.SetSizerAndFit(formSizer)

    def AddCounts(self):
        countGrid = wx.grid.Grid(self, wx.ID_ANY)
        countGrid.CreateGrid(1, 6)
        countGrid.HideRowLabels()
        countGrid.SetColLabelValue(0, "Board\ngames")
        countGrid.SetColLabelValue(1, "Playing card\ngames")
        countGrid.SetColLabelValue(2, "Computer\ngames")
        countGrid.SetColLabelValue(3, "Collectible\ncard games")
        countGrid.SetColLabelValue(4, "Video\ngames")
        countGrid.SetColLabelValue(5, "Total")

        countGrid.SetDefaultRowSize(30)
        countGrid.SetDefaultColSize(100)
        self.formSizer.Add(countGrid, 0, wx.ALL, 5)

    def AddItems(self):
        # query the database to get item list
        # my_items_query = '''select title, game_condition, description from BoardGame where email = "%s"
        #     union select title, game_condition, description from PlayingCardGame where email = "%s"
        #     union select title, game_condition, description from ComputerGame where email = "%s"
        #     union select title, game_condition, description from CollectibleCardGame where email = "%s"
        #     union select title, game_condition, description from VideoGame where email = "%s"
        #     '''
        my_items_query = 'select title, game_condition, description from ComputerGame where email = %(user_email)s'
        # query_tuple = (self.user_email,self.user_email,self.user_email,self.user_email,self.user_email)
        query_dict = {'user_email':self.user_email}
        cursor = self.connection.cursor()
        iterator = cursor.execute(my_items_query, query_dict)
        result = cursor.fetchall()
        print(self.user_email)
        if result:
            for row in result:
                print(row)
        else:
            print('no result found!')
        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        itemsGrid.CreateGrid(1, 6)
        itemsGrid.HideRowLabels()
        itemsGrid.SetColLabelValue(0, "Item #")
        itemsGrid.SetColLabelValue(1, "Game Type")
        itemsGrid.SetColLabelValue(2, "Title")
        itemsGrid.SetColLabelValue(3, "Condition")
        itemsGrid.SetColLabelValue(4, "Description")
        itemsGrid.SetColLabelValue(5, "")

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(4, 300)
        itemsGrid.SetColSize(5, 60)



        self.formSizer.Add(itemsGrid, 0, wx.ALL, 5)

    
   
