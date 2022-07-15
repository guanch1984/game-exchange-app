import wx
import wx.grid

class TradeHistoryForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-Trade History")
        self.SetIcon(parent.icon)
        self._new_user = None

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
            SELECT trade_status, IF(PI.email= %(user_email)s, "Proposer", "Counterparty") AS my_role
            FROM Trade AS T left JOIN (
                SELECT item_number, email from BoardGame
                UNION
                SELECT item_number, email from PlayingCardGame
                UNION
                SELECT item_number, email from CollectibleCardGame
                UNION
                SELECT item_number, email from ComputerGame
                UNION
                SELECT item_number, email from VideoGame
                ) AS PI ON T.proposer_item_number = PI.item_number 
                left JOIN (
                SELECT item_number, email from BoardGame
                UNION
                SELECT item_number, email from PlayingCardGame
                UNION
                SELECT item_number, email from CollectibleCardGame
                UNION
                SELECT item_number, email from ComputerGame
                UNION
                SELECT item_number, email from VideoGame
                ) as CI on T.counter_party_item_number=CI.item_number
            where PI.email= %(user_email)s or CI.email= %(user_email)s
            ) AS TD
        GROUP BY my_role
        '''
        query_dict = {'user_email':self.user_id}
        cursor = self.connection.cursor()
        iterator = cursor.execute(trade_summary_query, query_dict)
        result = cursor.fetchall()
        n = len(result)
        
        countGrid = wx.grid.Grid(self, wx.ID_ANY)
        countGrid.CreateGrid(n, 5)

        countGrid.HideRowLabels()
        countGrid.SetColLabelValue(0, "My role")
        countGrid.SetColLabelValue(1, "Total")
        countGrid.SetColLabelValue(2, "Accepted")
        countGrid.SetColLabelValue(3, "Rejected")
        countGrid.SetColLabelValue(4, "Rejected %")

        if result:
            for i in range(n):
                print(result[i])
                for j in range(5):
                    countGrid.SetCellValue(i,j, str(result[i][j]))
                    if j==4 and float(result[i][j])>=0.5:
                        countGrid.SetBackgroundColour(i,j,"red")
        else:
            print('no result found!')      

        countGrid.SetDefaultRowSize(30)
        countGrid.SetDefaultColSize(100)
        self.formSizer.Add(countGrid, 0, wx.ALL, 4)

    def AddDetail(self):
        # query the database to get trade list
        trade_detail_query = '''
        SELECT date_format(proposed_date, '%m/%d/%Y'), 
            date_format(accept_reject_date, '%m/%d/%Y'),
            trade_status,
            IF(accept_reject_date is NULL, timestampdiff(DAY, proposed_date, current_date()),
                timestampdiff(DAY,proposed_date,accept_reject_date)) AS response_time,
            IF(PI.email=%(user_email)s, "Proposer", "Counterparty") AS my_role,
            PI.title AS propsed_item,
            CI.title AS desired_item,
            IF(PI.email=%(user_email)s, CU.nickname, PU.nickname) AS other_user
        FROM Trade AS T left JOIN (
            SELECT item_number, email, title from BoardGame
            UNION
            SELECT item_number, email, title from PlayingCardGame
            UNION
            SELECT item_number, email, title from CollectibleCardGame
            UNION
            SELECT item_number, email, title from ComputerGame
            UNION
            SELECT item_number, email, title from VideoGame
            ) AS PI ON T.proposer_item_number = PI.item_number 
            left JOIN (
            SELECT item_number, email, title from BoardGame
            UNION
            SELECT item_number, email, title from PlayingCardGame
            UNION
            SELECT item_number, email, title from CollectibleCardGame
            UNION
            SELECT item_number, email, title from ComputerGame
            UNION
            SELECT item_number, email, title from VideoGame
            ) as CI on T.counter_party_item_number=CI.item_number
            left join TradePlazaUser as PU on PI.email=PU.email
            left join TradePlazaUser as CU on CI.email=CU.email
        WHERE PI.email= %(user_email)s or CI.email= %(user_email)s
        ORDER BY proposed_date DESC, response_time DESC;
        '''
        query_dict = {'user_email':self.user_id}
        cursor = self.connection.cursor()
        iterator = cursor.execute(trade_detail_query, query_dict)
        result = cursor.fetchall()
        n = len(result)

        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        itemsGrid.CreateGrid(n, 9)

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
        
        underlineFont = wx.Font(8, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        if result:
            for i in range(n):
                for j in range(9):
                    if j ==8 :
                        itemsGrid.SetCellValue(i,j, "Detail")
                        itemsGrid.SetCellTextColour(i,j, "blue")
                        itemsGrid.SetCellFont(i,j, underlineFont)
                    else:
                        itemsGrid.SetCellValue(i,j, str(result[i][j]))
        else:
            print('no result found!')  

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(8, 5)
        self.formSizer.Add(itemsGrid, 0, wx.ALL, 8)

    def OnCellClick(self, event):
        print("row: " + str(event.GetRow()) + " clicked")
        print("col: " + str(event.GetCol()) + " clicked")

    
   
