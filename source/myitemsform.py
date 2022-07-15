import wx
import wx.grid
from mysql.connector import Error

class MyItemsForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-My Items")
        self.SetIcon(parent.icon)
        self._new_user = None

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
            query = "SELECT COUNT(item_number) AS GameCount FROM BoardGame WHERE email = \"" + self.Parent.logged_user + "\""
            cursor.execute(query)
            res = cursor.fetchall()
            num_board = res[0][0]
            countGrid.SetCellValue(0, 0, str(num_board))
            query = "SELECT COUNT(item_number) AS GameCount FROM PlayingCardGame WHERE email = \"" + self.Parent.logged_user + "\""
            cursor.execute(query)
            res = cursor.fetchall()
            num_card = res[0][0]
            countGrid.SetCellValue(0, 1, str(num_card))
            query = "SELECT COUNT(item_number) AS GameCount FROM ComputerGame WHERE email = \"" + self.Parent.logged_user + "\""
            cursor.execute(query)
            res = cursor.fetchall()
            num_computer = res[0][0]
            countGrid.SetCellValue(0, 2, str(num_computer))
            query = "SELECT COUNT(item_number) AS GameCount FROM CollectibleCardGame WHERE email = \"" + self.Parent.logged_user + "\""
            cursor.execute(query)
            res = cursor.fetchall()
            num_collectible = res[0][0]
            countGrid.SetCellValue(0, 3, str(num_collectible))
            query = "SELECT COUNT(item_number) AS GameCount FROM VideoGame WHERE email = \"" + self.Parent.logged_user + "\""
            cursor.execute(query)
            res = cursor.fetchall()
            num_video = res[0][0]
            countGrid.SetCellValue(0, 4, str(num_video))
            countGrid.SetCellValue(0, 5, str(num_board + num_card + num_computer + num_collectible + num_video))

        except Error as e:
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return False

    def AddItems(self):
        # query the database to get item list
        my_items_query = '''select item_number, "Board Game" as game_type, title, game_condition, description from BoardGame where email = %(user_email)s
            union select item_number, "PlayingCardGame" as game_type,title, game_condition, description from PlayingCardGame where email = %(user_email)s
            union select item_number, "ComputerGame" as game_type,title, game_condition, description from ComputerGame where email = %(user_email)s
            union select item_number, "CollectibleCardGame" as game_type,title, game_condition, description from CollectibleCardGame where email = %(user_email)s
            union select item_number, "VideoGame" as game_type, title, game_condition, description from VideoGame where email = %(user_email)s
            '''
        query_dict = {'user_email':self.user_id}
        cursor = self.connection.cursor()
        iterator = cursor.execute(my_items_query, query_dict)
        result = cursor.fetchall()
        n = len(result)
        
        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        itemsGrid.CreateGrid(n, 6)
        itemsGrid.HideRowLabels()
        itemsGrid.SetColLabelValue(0, "Item #")
        itemsGrid.SetColLabelValue(1, "Game Type")
        itemsGrid.SetColLabelValue(2, "Title")
        itemsGrid.SetColLabelValue(3, "Condition")
        itemsGrid.SetColLabelValue(4, "Description")
        itemsGrid.SetColLabelValue(5, "")
        underlineFont = wx.Font(8, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        if result:
            for i in range(n):
                for j in range(6):
                    if j ==5 :
                        itemsGrid.SetCellValue(i,j, "Detail")
                        itemsGrid.SetCellTextColour(i,j, "blue")
                        itemsGrid.SetCellFont(i,j, underlineFont)
                    else:
                        itemsGrid.SetCellValue(i,j, str(result[i][j]))
        else:
            print('no result found!')   

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(4, 300)
        itemsGrid.SetColSize(5, 60)



        self.formSizer.Add(itemsGrid, 0, wx.ALL, 5)

    
   
