import wx
import os
# import mysql.connector
from mysql.connector import MySQLConnection, connect, Error
from getpass import getpass
from loginform import LoginForm
from searchform import SearchForm
from newlistingform import NewListingForm
from myitemsform import MyItemsForm
from tradehistoryform import TradeHistoryForm

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
        self.RenderMainMenu()
        self.ConnectToDb()
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
            # need to request put in 
            self.connection = MySQLConnection(**db_config)
            self.cursor = self.connection.cursor()

            self.cursor.execute("SELECT * FROM TradePlazaUser LIMIT 10")
            result = self.cursor.fetchall()
            for row in result:
                print(row) 

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

        self.welcomeMsg = wx.StaticText(self, label="")
        formSizer.Add(self.welcomeMsg, 0, wx.ALL, 5)

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        statsSizer = wx.BoxSizer(wx.VERTICAL)
        # add user stats
        statBox0 = wx.StaticBox(self, wx.ID_ANY, "Unaccepted trades", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox0Sizer = wx.StaticBoxSizer(statBox0, wx.VERTICAL)
        self.unacceptedTrades = wx.StaticText(self, label=" ", size=(120,-1), style=wx.ALIGN_CENTER)
        statbox0Sizer.Add(self.unacceptedTrades, 0, wx.EXPAND)
        statsSizer.Add(statbox0Sizer, 0, wx.ALL, 20)

        statBox1 = wx.StaticBox(self, wx.ID_ANY, "Response time", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox1Sizer = wx.StaticBoxSizer(statBox1, wx.VERTICAL)
        self.responseTime = wx.StaticText(self, label=" ", size=(120,-1), style=wx.ALIGN_CENTER)
        statbox1Sizer.Add(self.responseTime, 0, wx.EXPAND)
        statsSizer.Add(statbox1Sizer, 0, wx.ALL, 20)

        statBox2 = wx.StaticBox(self, wx.ID_ANY, "My rank", style=wx.ALIGN_CENTER_HORIZONTAL)
        statbox2Sizer = wx.StaticBoxSizer(statBox2, wx.VERTICAL)
        self.myRank = wx.StaticText(self, label=" ", size=(120,-1), style=wx.ALIGN_CENTER)
        statbox2Sizer.Add(self.myRank, 0, wx.EXPAND)
        statsSizer.Add(statbox2Sizer, 0, wx.ALL, 20)

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

    def PopulateUserData(self, user_id):
        pass

    def SetWelcomeMsg(self, msg):
        self.welcomeMsg.SetLabel(msg)

    def SetUnacceptedTrades(self, msg):
        self.unacceptedTrades.SetLabel(msg)

    def SetResponseTime(self, msg):
        self.responseTime.SetLabel(msg)

    def SetMyRank(self, msg):
        self.myRank.SetLabel(msg)

    def DoListItem(self, event):
        dl = NewListingForm(self)
        dl.ShowModal()

    def DoMyItems(self, event):
        mi = MyItemsForm(self, connection=self.connection, user_email = self.user_email)
        mi.ShowModal()

    def DoSearchItem(self, event):
        sf = SearchForm(self)
        sf.ShowModal()

    def DoTradeHistory(self,event):
        th = TradeHistoryForm(self, connection=self.connection, user_email = self.user_email)
        th.ShowModal()

    def DoLogin(self):
        lf = LoginForm(self, connection=self.connection)
        
        res = lf.ShowModal()
        # check if login is succesfull
        if res == wx.ID_OK:
            self.PopulateUserData(lf._logged_user)
            print(lf._logged_user)
            self.Show(True)
        else:
            self.Close()
        user_email_query = 'select email from TradePlazaUser where email = %s or nickname = %s '
        query_tuple = (lf._logged_user, lf._logged_user)
        self.cursor.execute(user_email_query, query_tuple)
        result = self.cursor.fetchall()
        self.user_email = result[0][0]
        # print(self.user_email)

    def DoLogout(self, event):
        self.Hide()
        self.ClearForm()
        self.DoLogin()

    def ClearForm(self):
        pass

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
        print('Successfully setup database!')
        cursor.execute("SHOW DATABASES")
        for db in cursor:
            print(db)

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


