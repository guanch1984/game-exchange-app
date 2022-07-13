import wx
import wx.grid

class TradeHistoryForm(wx.Dialog):
    def __init__(self, parent):
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
        itemsGrid.SetColSize(8, 10)
        self.formSizer.Add(itemsGrid, 0, wx.ALL, 8)

    
   
