import wx
import os
from mysql.connector import MySQLConnection, connect, Error
from getpass import getpass
from loginform import LoginForm
from searchform import SearchForm
from newlistingform import NewListingForm
from myitemsform import MyItemsForm
from tradehistoryform import TradeHistoryForm
from acceptrejectform import AcceptRejectForm

#user: admin password: admin
__SETDB = False

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="TradePlaza", size=(300,400))
        self.connection = None
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap(os.getcwd() + r'\source\trade_plaza_icon.png', wx.BITMAP_TYPE_ANY))
        self.SetIcon(self.icon)
        
        self.ConnectToDb()
        self.RenderMainMenu()
        self.DoLogin()
        

    def OnClose(self, event):
        try:
            self.connection.close()
            self.Destroy()
        except:
            pass

    def ConnectToDb(self):
        db_config = {'host': 'localhost', 'user': 'root', 'password': 'admin', 'database':'cs6400_summer2022_team065'}
        try:
            self.connection = MySQLConnection(**db_config)
            self.cursor = self.connection.cursor()
        except Error as e:
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            self.Close()

    def RenderMainMenu(self):
        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)

        self.logout = wx.Button(self, label="logout", style=wx.BORDER_NONE)
        self.logout.SetBackgroundColour('blue')
        self.logout.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoLogout, self.logout)
        formSizer.Add(self.logout, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, 5)   

        boldFont = wx.Font(20, family = wx.FONTFAMILY_MODERN, style = wx.FONTSTYLE_NORMAL, weight = wx.FONTWEIGHT_BOLD)
        tmp = wx.StaticText(self, label="Trade Plaza", size=(-1,25))
        tmp.SetFont(boldFont)
        formSizer.Add(tmp, 0, wx.LEFT, 5)    

        tmp = wx.StaticText(self, label="_"*50)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT, 5)

        self.welcomeMsg = wx.StaticText(self, label="" )
        formSizer.Add(self.welcomeMsg, 0, wx.ALL, 5)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        statsSizer = wx.BoxSizer(wx.VERTICAL)
        # add user stats
        statBox1 = wx.StaticBox(self, wx.ID_ANY, "Unaccepted trades", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox1Sizer = wx.StaticBoxSizer(statBox1, wx.VERTICAL)
        self.button_unacceptedTrades = wx.Button(self, label="", size=(100,30))
        self.button_unacceptedTrades .SetBackgroundColour('white')
        self.button_unacceptedTrades .SetForegroundColour('black')
        statbox1Sizer.Add(self.button_unacceptedTrades, 0)
        statsSizer.Add(statbox1Sizer , 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

        statBox1 = wx.StaticBox(self, wx.ID_ANY, "Response time", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox1Sizer = wx.StaticBoxSizer(statBox1, wx.VERTICAL)
        self.text_responseTime = wx.StaticText(self, label="" + ' days', size=(120,30), style=wx.ALIGN_CENTER)
        statbox1Sizer.Add(self.text_responseTime, 0, wx.EXPAND)
        statsSizer.Add(statbox1Sizer, 0, wx.ALL, 10)

        statBox2 = wx.StaticBox(self, wx.ID_ANY, "My rank", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox2Sizer = wx.StaticBoxSizer(statBox2, wx.VERTICAL)
        self.text_myRank = wx.StaticText(self, label="", size=(120,30), style=wx.ALIGN_CENTER)
        statbox2Sizer.Add(self.text_myRank, 0, wx.EXPAND)
        statsSizer.Add(statbox2Sizer, 0, wx.ALL, 10)

        hSizer.Add(statsSizer, 0)
        ctrlSizer = wx.BoxSizer(wx.VERTICAL)

        self.listItem = wx.Button(self, label="list item", style=wx.BORDER_NONE, size=(100,50))
        self.listItem.SetBackgroundColour('blue')
        self.listItem.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoListItem, self.listItem)
        ctrlSizer.Add(self.listItem, 0,wx.ALL, 5)

        self.myItems = wx.Button(self, label="my items", style=wx.BORDER_NONE, size=(100,50))
        self.myItems.SetBackgroundColour('blue')
        self.myItems.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoMyItems, self.myItems)
        ctrlSizer.Add(self.myItems, 0,wx.ALL, 5)

        self.searchItems = wx.Button(self, label="search items", style=wx.BORDER_NONE, size=(100,50))
        self.searchItems.SetBackgroundColour('blue')
        self.searchItems.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoSearchItem, self.searchItems)
        ctrlSizer.Add(self.searchItems, 0,wx.ALL, 5)

        self.tradeHistory = wx.Button(self, label="Trade History", style=wx.BORDER_NONE, size=(100,50))
        self.tradeHistory.SetBackgroundColour('blue')
        self.tradeHistory.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.DoTradeHistory, self.tradeHistory)
        ctrlSizer.Add(self.tradeHistory, 0,wx.ALL, 5)

        hSizer.Add(ctrlSizer, 0)

        formSizer.Add(hSizer, 0, wx.EXPAND)
        self.SetSizer(formSizer)
        self.Layout()
        self.Update()

    def PopulateUserData(self, user_id):
        self.SetWelcomeMsg(user_id)
        self.SetUnacceptedTrades(user_id)
        self.SetMyRank(user_id)
        self.SetResponseTime(user_id)

    def SetWelcomeMsg(self, msg):
        user_email_query = 'select email, first_name, last_name, nickname from TradePlazaUser where email = %(user_id)s or nickname = %(user_id)s'
        query_dict = {'user_id':self.logged_user}
        cursor = self.connection.cursor()
        cursor.execute(user_email_query, query_dict)
        self.result = cursor.fetchall()
        self.logged_user = self.result[0][0]
        self.welcomeMsg.SetLabel("Welcome, " + self.result[0][1] + ' ' + self.result[0][2] + '(' + self.result[0][3] + ')!')

    def SetUnacceptedTrades(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT COUNT(*)
                FROM (SELECT item_number, email FROM BoardGame WHERE email = "{email}" UNION
                        SELECT item_number, email FROM CollectibleCardGame WHERE email = "{email}" UNION
                        SELECT item_number, email FROM ComputerGame WHERE email = "{email}" UNION
                        SELECT item_number, email FROM PlayingCardGame WHERE email = "{email}" UNION
                        SELECT item_number, email FROM VideoGame WHERE email = "{email}"
                    ) as all_items INNER JOIN Trade ON counter_party_item_number = item_number
                WHERE trade_status = "PENDING"
            """.format(email=user_id)

            cursor.execute(query)
            res = cursor.fetchall()
            num = len(res)
            if num == 0:
                self.button_unacceptedTrades.SetLabel('0')
            else:
                self.button_unacceptedTrades.SetLabel(str(res[-1][-1]))

            if num == 1:
                self.Bind(wx.EVT_BUTTON, self.DoAcceptRejectTrade, self.button_unacceptedTrades )
            elif num >=2 :
                self.Bind(wx.EVT_BUTTON, self.DoAcceptRejectTrade, self.button_unacceptedTrades )
                self.button_unacceptedTrades .SetForegroundColour('Red')

        except Error as e:
            self.unacceptedTrades = "Error"
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)

    def SetResponseTime(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = """Select ROUND(avg(TIMESTAMPDIFF(DAY,proposed_date, accept_reject_date)),1) from Trade Inner Join
                    (Select Item.item_number, ItemJoin.email from Item 
                    NATURAL JOIN 
                    (Select BoardGame.item_number, BoardGame.email from BoardGame 
                    UNION 
                    Select PlayingCardGame.item_number, PlayingCardGame.email from PlayingCardGame 
                    UNION 
                    Select CollectibleCardGame.item_number, CollectibleCardGame.email from CollectibleCardGame 
                    UNION 
                    Select ComputerGame.item_number, ComputerGame.email from ComputerGame 
                    UNION 
                    Select VideoGame.item_number, VideoGame.email from VideoGame) 
                    AS ItemJoin where "{email}" = ItemJoin.email) 
                    AS TradeJoin ON Trade.counter_party_item_number= TradeJoin.item_number 
                    where Trade.trade_status='ACCEPT' or Trade.trade_status='REJECT' 
                    GROUP BY TradeJoin.email;""".format(email=user_id)
            cursor.execute(query)
            res = cursor.fetchall()
            
            if len(res) == 0:
                self.text_responseTime.SetForegroundColour("Black")
                self.text_responseTime.SetLabel("N/A")
                self.responseTime = "N/A"
            elif res[-1][-1] <= 7.0:
                self.text_responseTime.SetForegroundColour("Green")
                self.text_responseTime.SetLabel(str(res[-1][-1]))
                self.responseTime = str(res[-1][-1])
            elif res[-1][-1] <= 14.0:
                self.text_responseTime.SetForegroundColour("Yellow")
                self.text_responseTime.SetLabel(str(res[-1][-1]))
                self.responseTime = str(res[-1][-1])
            elif res[-1][-1] <= 20.9:
                self.text_responseTime.SetForegroundColour("Orange")
                self.text_responseTime.SetLabel(str(res[-1][-1]))
                self.responseTime = str(res[-1][-1])
            elif res[-1][-1] <= 27.9:
                self.text_responseTime.SetForegroundColour("Red")
                self.text_responseTime.SetLabel(str(res[-1][-1]))
                self.responseTime = str(res[-1][-1])
            else:
                self.text_responseTime.SetForegroundColour("Red")
                self.text_responseTime.SetLabel(str(res[-1][-1]))
                self.responseTime = str(res[-1][-1])
                boldFont = wx.Font(20, family = wx.FONTFAMILY_MODERN, style = wx.FONTSTYLE_NORMAL, weight = wx.FONTWEIGHT_BOLD)
                self.text_responseTime.SetFont(boldFont)

        except Error as e:
            self.responseTime="Error"
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)

    def SetMyRank(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = """Select count(*) from Trade Inner Join
                    (Select Item.item_number, ItemJoin.email from Item 
                    NATURAL JOIN 
                    (Select BoardGame.item_number, BoardGame.email from BoardGame 
                    UNION 
                    Select PlayingCardGame.item_number, PlayingCardGame.email from PlayingCardGame 
                    UNION 
                    Select CollectibleCardGame.item_number, CollectibleCardGame.email from CollectibleCardGame 
                    UNION 
                    Select ComputerGame.item_number, ComputerGame.email from ComputerGame 
                    UNION 
                    Select VideoGame.item_number, VideoGame.email from VideoGame) AS ItemJoin 
                    where "{email}" = ItemJoin.email) AS TradeJoin 
                    ON Trade.counter_party_item_number= TradeJoin.item_number 
                    OR Trade.proposer_item_number= TradeJoin.item_number 
                    where Trade.trade_status='ACCEPT' 
                    GROUP BY TradeJoin.email;""".format(email=user_id)
            cursor.execute(query)
            res = cursor.fetchall()
            
            if len(res) == 0:
                self.text_myRank.SetLabel("None")
                self.myRank = "None"
            elif res[-1][-1] <=2:
                self.text_myRank.SetLabel('Aluminium')
                self.myRank = "Aluminium"
            elif res[-1][-1] <=3:
                self.text_myRank.SetLabel('Bronze')
                self.myRank = "Bronze"
            elif res[-1][-1] <=5:
                self.text_myRank.SetLabel('Silver')
                self.myRank = "Silver"
            elif res[-1][-1] <=7:
                self.text_myRank.SetLabel('Gold')
                self.myRank = "Gold"
            elif res[-1][-1] <=9:
                self.text_myRank.SetLabel('Platinum')
                self.myRank = "Platinum"
            else:
                self.text_myRank.SetLabel('Alexandinium')
                self.myRank = "Alexandinium"
        except Error as e:
            self.myRank="Error"
            wx.MessageBox("Error connecting to DB: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)

    def DoListItem(self, event):
        dl = NewListingForm(self, connection=self.connection, user_id=self.logged_user)
        dl.ShowModal()

    def DoAcceptRejectTrade(self, event):
        dar = AcceptRejectForm(self, connection=self.connection, user_id = self.logged_user)
        dar.ShowModal()
        
    def DoMyItems(self, event):
        self.user_status = [self.responseTime, self.myRank]
        mi = MyItemsForm(self, connection=self.connection, user_id = self.logged_user, user_status = self.user_status)
        mi.ShowModal()

    def DoSearchItem(self, event):
        sf = SearchForm(self, connection=self.connection)
        sf.ShowModal()
        self.PopulateUserData(self.logged_user)

    def DoTradeHistory(self,event):
        th = TradeHistoryForm(self, connection=self.connection, user_id = self.logged_user)
        th.ShowModal()

    def DoLogin(self):
        lf = LoginForm(self, connection=self.connection)
        
        res = lf.ShowModal()
        # check if login is succesfull
        if res == wx.ID_OK:
            self.logged_user = lf._logged_user
            self.PopulateUserData(self.logged_user)
            self.Show(True)
        else:
            self.Close()

    def DoLogout(self, event):
        self.logged_user == None
        self.Hide()
        self.ClearForm()
        self.DoLogin()

    def ClearForm(self):
        self.welcomeMsg.SetLabel("")
        self.text_responseTime.SetLabel("")
        self.text_myRank.SetLabel("")

def SetupDB(db_config):
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        # with MySQLConnection(
        #     host="localhost",
        #     user=input("Enter username: "),
        #     password=getpass("Enter password: "),
        # ) as connection:
        cursor = conn.cursor()
        schema_file = open(os.getcwd() + r'\Phase_2\team065_p2_schema.sql', "r")
        querries = schema_file.read().split(";")
        for querry in querries:
            if querry.strip() == "":
                continue
            cursor.execute(querry.replace(r'"', "'"))
    except Error as e:
        print(e)

def PopulateDB(db_config, db_name):
    db_config['database'] = db_name
    conn = None
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        schema_file = open(os.getcwd() + r'\source\sample_data.sql', "r")
        querries = schema_file.read().split(";")
        
        for querry in querries:
            if querry.strip() == "":
                continue
            if "'" in querry:
                continue
            querry = querry.replace(r'"', "'")
            cursor.execute(querry)
        conn.commit()
        print('Successfully populated database!')
        cursor.execute("SELECT * FROM Address LIMIT 10")
        result = cursor.fetchall()
        for row in result:
            print(row) 

    except Error as e:
        print(e)

if __name__ == '__main__':
    # Test env
    if __SETDB:
    # if 1:
        db_config = {'host': 'localhost', 'user': 'root', 'password': 'admin'}    
        db_name = 'cs6400_summer2022_team065'
        SetupDB(db_config)
        PopulateDB(db_config, db_name)
    app = wx.App(False)
    frame = MainWindow()
    app.MainLoop()