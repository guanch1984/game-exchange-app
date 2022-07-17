import wx
import wx.grid
from mysql.connector import Error
from itemdetailform import ItemDetailForm

class MyItemsForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_email = kwargs.pop("user_id")
            self.user_status = kwargs.pop("user_status")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-My Items")
        self.SetIcon(parent.icon)

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

        try:
            cursor = self.connection.cursor()
            query_dict = {'user_email':self.user_email}

            query = "SELECT COUNT(item_number) AS GameCount FROM BoardGame WHERE email = %(user_email)s"
            cursor.execute(query, query_dict)
            res = cursor.fetchall()
            num_board = res[0][0]
            countGrid.SetCellValue(0, 0, str(num_board))
            query = "SELECT COUNT(item_number) AS GameCount FROM PlayingCardGame WHERE email = %(user_email)s"
            cursor.execute(query, query_dict)
            res = cursor.fetchall()
            num_card = res[0][0]
            countGrid.SetCellValue(0, 1, str(num_card))
            query = "SELECT COUNT(item_number) AS GameCount FROM ComputerGame WHERE email = %(user_email)s"
            cursor.execute(query, query_dict)
            res = cursor.fetchall()
            num_computer = res[0][0]
            countGrid.SetCellValue(0, 2, str(num_computer))
            query = "SELECT COUNT(item_number) AS GameCount FROM CollectibleCardGame WHERE email = %(user_email)s"
            cursor.execute(query, query_dict)
            res = cursor.fetchall()
            num_collectible = res[0][0]
            countGrid.SetCellValue(0, 3, str(num_collectible))
            query = "SELECT COUNT(item_number) AS GameCount FROM VideoGame WHERE email = %(user_email)s"
            cursor.execute(query, query_dict)
            res = cursor.fetchall()
            num_video = res[0][0]
            countGrid.SetCellValue(0, 4, str(num_video))
            countGrid.SetCellValue(0, 5, str(num_board + num_card + num_computer + num_collectible + num_video))

        except Error as e:
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return False

    def AddItems(self):
        # query the database to get item list

        
        item_query = '''
            select item_number, game_type, title, game_condition, description, email, platform, media
            from (
            SELECT item_number, "Board Game" as game_type, title, game_condition, description, email, "None" as platform, "None" as media from BoardGame
            UNION
            SELECT item_number, "Playing Card Game" as game_type, title, game_condition, description, email, "None" as platform, "None" as media from PlayingCardGame
            UNION
            SELECT item_number, "Collectible Card Game" as game_type, title, game_condition, description, email, "None" as platform, "None" as media from CollectibleCardGame
            UNION
            SELECT item_number, "Computer Game" as game_type, title, game_condition, description, email, platform, "None" as media from ComputerGame
            UNION
            SELECT item_number, "Video Game" as game_type, title, game_condition, description, email, name as platform, media from VideoGame left join platform on VideoGame.platform_id = platform.platform_id
            ) as ALLI
            where ALLI.email = %(user_email)s
            ORDER BY item_number asc
        '''
        query_dict = {'user_email':self.user_email}
        cursor = self.connection.cursor()
        iterator = cursor.execute(item_query, query_dict)
        self.itemresult = cursor.fetchall()
        n = len(self.itemresult)

        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellClick, itemsGrid)
        itemsGrid.CreateGrid(n, 6)

        itemsGrid.HideRowLabels()
        itemsGrid.SetColLabelValue(0, "Item #")
        itemsGrid.SetColLabelValue(1, "Game Type")
        itemsGrid.SetColLabelValue(2, "Title")
        itemsGrid.SetColLabelValue(3, "Condition")
        itemsGrid.SetColLabelValue(4, "Description")
        itemsGrid.SetColLabelValue(5, "")

        underlineFont = wx.Font(8, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        if self.itemresult:
            for i in range(n):
                for j in range(6):
                    if j ==5 :
                        itemsGrid.SetCellValue(i,j, "Detail")
                        itemsGrid.SetCellTextColour(i,j, "blue")
                        itemsGrid.SetCellFont(i,j, underlineFont)
                    else:
                        itemsGrid.SetCellValue(i,j, str(self.itemresult[i][j]))
        else:
            print('no result found!')  

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(4, 300)
        itemsGrid.SetColSize(5, 60)

        self.formSizer.Add(itemsGrid, 0, wx.ALL, 5)

    def OnCellClick(self, event):
        if event.GetCol() == 5:
            self.DoItemDetail(event)

    def DoItemDetail(self, event):
        thd = ItemDetailForm(self, connection=self.connection, user_id = self.user_email, result=self.itemresult[event.GetRow()], user_status = self.user_status)
        thd.ShowModal()


    
   
