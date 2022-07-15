import wx
import wx.grid

class TradeHistoryForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-Trade History")
        self.SetIcon(parent.icon)
        self._new_user = None
        self.user_email = kwargs.pop("user_email")

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = formSizer
        tmp = wx.StaticText(self, label="Trade History")
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*80)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        self.AddSummary()
        self.AddDetail()
        self.SetSizerAndFit(formSizer)

    def AddSummary(self):
        # query the database to get trade statistic summary
        trade_summary_query = '''
        SELECT my_role, COUNT(*) AS Total, 
                SUM( IF (trade_status="ACCEPT", 1, 0)) AS Accepted,
                SUM( IF (trade_status ="REJECT", 1, 0)) AS Rejected,
                FORMAT( SUM( IF (trade_status ="REJECT", 1, 0)) / COUNT(*) , 'P1') AS "Rejected %”"
        FROM (
            SELECT trade_status, IF(T.proposer_item_number=I.item_number, "Proposer", "Counterparty") AS my_role
            FROM Trade AS T INNER JOIN (
                SELECT item_number, email from BoardGame where email = %(user_email)s
                UNION
                SELECT item_number, email from PlayingCardGame where email = %(user_email)s
                UNION
                SELECT item_number, email from CollectibleCardGame where email = %(user_email)s
                UNION
                SELECT item_number, email from ComputerGame where email = %(user_email)s
                UNION
                SELECT item_number, email from VideoGame where email = %(user_email)s
                ) AS I ON T.proposer_item_number = I.item_number OR T.counter_party_item_number=I.item_number
            ) AS TD
        GROUP BY my_role
        '''
        query_dict = {'user_email':self.user_email}
        cursor = self.connection.cursor()
        iterator = cursor.execute(trade_summary_query, query_dict)
        result = cursor.fetchall()
        if result:
            for row in result:
                print(row)
        else:
            print('no result found!')       

        countGrid = wx.grid.Grid(self, wx.ID_ANY)
        countGrid.CreateGrid(1, 5)
        countGrid.HideRowLabels()
        countGrid.SetColLabelValue(0, "My role")
        countGrid.SetColLabelValue(1, "Total")
        countGrid.SetColLabelValue(2, "Accepted")
        countGrid.SetColLabelValue(3, "Rejected")
        countGrid.SetColLabelValue(4, "Rejected %")

        countGrid.SetDefaultRowSize(30)
        countGrid.SetDefaultColSize(100)
        self.formSizer.Add(countGrid, 0, wx.ALL, 4)

    def AddDetail(self):
        # query the database to get trade list
        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        itemsGrid.CreateGrid(1, 9)
        itemsGrid.HideRowLabels()
        itemsGrid.SetColLabelValue(0, "Proposed\nDate")
        itemsGrid.SetColLabelValue(1, "Accepted/\nRejected Date")
        itemsGrid.SetColLabelValue(2, "Trade status")
        itemsGrid.SetColLabelValue(3, "Response\ntime (days)")
        itemsGrid.SetColLabelValue(4, "My role")
        itemsGrid.SetColLabelValue(5, "Proposed item")
        itemsGrid.SetColLabelValue(6, "Desired item")
        itemsGrid.SetColLabelValue(7, "Other User")
        itemsGrid.SetColLabelValue(8, "")

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(8, 5)
        self.formSizer.Add(itemsGrid, 0, wx.ALL, 8)

    
   
