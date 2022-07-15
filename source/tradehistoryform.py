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

        # tmp = wx.StaticText(self, label="My Items")
        # formSizer.Add(tmp, 0, wx.LEFT, 5)
        # tmp = wx.StaticText(self, label="_"*80)
        # tmp.SetForegroundColour('blue')
        # formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)
        
        self.AddDetail()
        self.SetSizerAndFit(formSizer)

    def AddSummary(self):
        # query the database to get trade statistic summary
        countGrid = wx.grid.Grid(self, wx.ID_ANY)
        countGrid.CreateGrid(2, 5)
        countGrid.HideRowLabels()
        countGrid.SetColLabelValue(0, "My role")
        countGrid.SetColLabelValue(1, "Total")
        countGrid.SetColLabelValue(2, "Accepted")
        countGrid.SetColLabelValue(3, "Rejected")
        countGrid.SetColLabelValue(4, "Rejected %")

        countGrid.SetDefaultRowSize(30)
        countGrid.SetDefaultColSize(100)
        self.formSizer.Add(countGrid, 0, wx.ALL, 4)

        # Example code to show how to populate grid with data
        countGrid.SetCellValue(0, 0, "Proposer")
        countGrid.SetCellValue(0, 1, "2")
        countGrid.SetCellValue(0, 2, "1")
        countGrid.SetCellValue(0, 3, "1")
        countGrid.SetCellValue(0, 4, "50.0%")
        countGrid.SetCellBackgroundColour(0, 4, "red")
        countGrid.SetCellValue(1, 0, "Counterparty")
        countGrid.SetCellValue(1, 1, "2")
        countGrid.SetCellValue(1, 2, "2")
        countGrid.SetCellValue(1, 3, "0")
        countGrid.SetCellValue(1, 4, "0.0%")

    def AddDetail(self):
        # query the database to get trade list
        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellClick, itemsGrid)

        itemsGrid.CreateGrid(2, 9)
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

        # Example code tp show how to populate data into grid and fire details event
        itemsGrid.SetCellValue(0, 0, "06/01/21")
        itemsGrid.SetCellValue(0, 1, "06/02/21")
        itemsGrid.SetCellValue(0, 2, "Accepted")
        itemsGrid.SetCellValue(0, 3, "1")
        itemsGrid.SetCellValue(0, 4, "Proposer")
        itemsGrid.SetCellValue(0, 5, "Mastermind")
        itemsGrid.SetCellValue(0, 6, "Skip-Bo")
        itemsGrid.SetCellValue(0, 7, "PrincessZ")
        itemsGrid.SetCellValue(0, 8, "Details")
        underlineFont = wx.Font(8, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        itemsGrid.SetCellFont(0, 8, underlineFont)

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(8, 5)
        self.formSizer.Add(itemsGrid, 0, wx.ALL, 8)

    def OnCellClick(self, event):
        print("row: " + str(event.GetRow()) + " clicked")
        print("col: " + str(event.GetCol()) + " clicked")

    
   
