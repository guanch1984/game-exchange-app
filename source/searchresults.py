import wx
import wx.grid

class SearchResults(wx.Dialog):
    def __init__(self, parent,**kwargs):
        super().__init__(parent, title="TradePlaza-Search Results")
        self.SetIcon(parent.icon)
        self._new_user = None
        self.res = kwargs.pop("res")

        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        self.formSizer = formSizer

        tmp = wx.StaticText(self, label="Search results: " + kwargs.pop("search_type"))
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*80)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        
        self.AddItems()
        self.SetSizerAndFit(formSizer)

    def AddItems(self):
        # query the database to get item list
        itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        itemsGrid.CreateGrid(1, 9)
        itemsGrid.HideRowLabels()
        itemsGrid.SetColLabelValue(0, "Item #")
        itemsGrid.SetColLabelValue(1, "Game Type")
        itemsGrid.SetColLabelValue(2, "Title")
        itemsGrid.SetColLabelValue(3, "Condition")
        itemsGrid.SetColLabelValue(4, "Description")
        itemsGrid.SetColLabelValue(5, "Response Time (days)")
        itemsGrid.SetColLabelValue(6, "Rank")
        itemsGrid.SetColLabelValue(7, "Distance")
        itemsGrid.SetColLabelValue(8, "")

        itemsGrid.SetDefaultRowSize(30)
        itemsGrid.SetDefaultColSize(150)
        itemsGrid.SetColSize(4, 300)
        itemsGrid.SetColSize(5, 60)
        self.formSizer.Add(itemsGrid, 0, wx.ALL, 5)

        for c,v in enumerate(self.res):
            itemsGrid.SetCellValue(c, 0, str(v[0]))
            itemsGrid.SetCellValue(c, 1, str(v[1]))
            itemsGrid.SetCellValue(c, 2, str(v[2]))
            itemsGrid.SetCellValue(c, 3, str(v[3]))
            itemsGrid.SetCellValue(c, 4, str(v[4]))
            itemsGrid.SetCellValue(c, 5, str(v[5]))
            itemsGrid.SetCellValue(c, 6, str(v[6]))
            itemsGrid.SetCellValue(c, 7, str(v[7]))

    
   
