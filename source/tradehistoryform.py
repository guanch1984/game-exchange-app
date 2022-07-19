import wx
import wx.grid
from tradehistorydetailform import TradeHistoryDetailForm

class TradeHistoryForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_email = kwargs.pop("user_id")
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
                cast(100 * SUM( IF (trade_status ="REJECT", 1, 0)) / COUNT(*) as decimal(18,2)) AS "Rejected %”"
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
        query_dict = {'user_email':self.user_email}
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
                for j in range(5):
                    if j==4 and float(result[i][j])>=50:
                        countGrid.SetCellValue(i,j, str(result[i][j]))
                        countGrid.SetCellBackgroundColour(i, j, 'red')
                    countGrid.SetCellValue(i,j, str(result[i][j]))
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
            PI.title AS proposed_item,
            CI.title AS desired_item,
            IF(PI.email=%(user_email)s, CU.nickname, PU.nickname) AS other_user,
            PI.item_number,
            CI.item_number,
            PI.game_type,
            CI.game_type,
            PI.game_condition,
            CI.game_condition,
            PI.description,
            PA.longitude,
            PA.latitude,
            CA.longitude,
            CA.latitude
        FROM Trade AS T left JOIN (
            SELECT item_number, email, title, "Board Game" as game_type, game_condition, description from BoardGame
            UNION
            SELECT item_number, email, title, "Playing Card Game" as game_type, game_condition, description from PlayingCardGame
            UNION
            SELECT item_number, email, title, "Collectible Card Game" as game_type, game_condition, description from CollectibleCardGame
            UNION
            SELECT item_number, email, title, "Computer Game" as game_type, game_condition, description from ComputerGame
            UNION
            SELECT item_number, email, title, "Video Game" as game_type, game_condition, description from VideoGame
            ) AS PI ON T.proposer_item_number = PI.item_number 
            left JOIN (
            SELECT item_number, email, title, "Board Game" as game_type, game_condition, description from BoardGame
            UNION
            SELECT item_number, email, title, "Playing Card Game" as game_type, game_condition, description from PlayingCardGame
            UNION
            SELECT item_number, email, title, "Collectible Card Game" as game_type, game_condition, description from CollectibleCardGame
            UNION
            SELECT item_number, email, title, "Computer Game" as game_type, game_condition, description from ComputerGame
            UNION
            SELECT item_number, email, title, "Video Game" as game_type, game_condition, description from VideoGame
            ) as CI on T.counter_party_item_number=CI.item_number
            left join TradePlazaUser as PU on PI.email=PU.email
            left join TradePlazaUser as CU on CI.email=CU.email
            left join Address as PA on PU.postal_code=PA.postal_code
            left join Address as CA on CU.postal_code=CA.postal_code
        WHERE PI.email= %(user_email)s or CI.email= %(user_email)s
        ORDER BY proposed_date DESC, response_time DESC;
        '''
        query_dict = {'user_email':self.user_email}
        cursor = self.connection.cursor()
        iterator = cursor.execute(trade_detail_query, query_dict)
        self.detailresult = cursor.fetchall()
        n = len(self.detailresult)

        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        itemsGrid.CreateGrid(n, 9)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellClick, itemsGrid)

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
        if self.detailresult:
            for i in range(n):
                for j in range(9):
                    if j ==8 :
                        itemsGrid.SetCellValue(i,j, "Detail")
                        itemsGrid.SetCellTextColour(i,j, "blue")
                        itemsGrid.SetCellFont(i,j, underlineFont)
                    else:
                        itemsGrid.SetCellValue(i,j, str(self.detailresult[i][j]))
        else:
            print('no result found!')  

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(8, 5)
        self.formSizer.Add(itemsGrid, 0, wx.ALL, 8)

    def OnCellClick(self, event):
        if event.GetCol() == 8:
            self.DoTradeHistorDetail(event)

    def DoTradeHistorDetail(self, event):
        thd = TradeHistoryDetailForm(self, connection=self.connection, user_id = self.user_email, result=self.detailresult[event.GetRow()])
        thd.ShowModal()