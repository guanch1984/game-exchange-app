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

        self.search_details = kwargs.pop("search_type")

        tmp = wx.StaticText(self, label="Search results: " + self.search_details)
        formSizer.Add(tmp, 0, wx.LEFT, 5)
        tmp = wx.StaticText(self, label="_"*80)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        
        self.AddItems()
        self.SetSizerAndFit(formSizer)

    def AddItems(self):
        # query the database to get item list
        self.itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        self.itemsGrid.CreateGrid(1, 9)
        self.itemsGrid.HideRowLabels()
        self.itemsGrid.SetColLabelValue(0, "Item #")
        self.itemsGrid.SetColLabelValue(1, "Game Type")
        self.itemsGrid.SetColLabelValue(2, "Title")
        self.itemsGrid.SetColLabelValue(3, "Condition")
        self.itemsGrid.SetColLabelValue(4, "Description")
        self.itemsGrid.SetColLabelValue(5, "Response Time (days)")
        self.itemsGrid.SetColLabelValue(6, "Rank")
        self.itemsGrid.SetColLabelValue(7, "Distance")
        self.itemsGrid.SetColLabelValue(8, "")

        self.itemsGrid.SetDefaultRowSize(30)
        self.itemsGrid.SetDefaultColSize(150)
        self.itemsGrid.SetColSize(4, 300)
        self.itemsGrid.SetColSize(5, 60)
        self.formSizer.Add(self.itemsGrid, 0, wx.ALL, 5)

        for c,v in enumerate(self.res):
            self.itemsGrid.AppendRows(numRows=1)
            self.itemsGrid.SetCellValue(c, 0, str(v[0]))
            self.itemsGrid.SetCellValue(c, 1, str(v[1]))
            self.itemsGrid.SetCellValue(c, 2, str(v[2]))
            self.itemsGrid.SetCellValue(c, 3, str(v[3]))
            self.itemsGrid.SetCellValue(c, 4, str(v[4]))
            self.itemsGrid.SetCellValue(c, 5, str(v[5]))
            self.itemsGrid.SetCellValue(c, 6, str(v[6]))
            self.itemsGrid.SetCellValue(c, 7, str(v[7]))
            self.itemsGrid.SetCellValue(c, 8, "Details")
            self.itemsGrid.SetCellTextColour(c, 8, 'blue')
            
            # Make grid not editable
            for i in range(9):
                self.itemsGrid.SetReadOnly(c, i, True)

            # Add coloring for response time
            if v[5] is None:
                pass
            elif v[5] <= 7:
                self.itemsGrid.SetCellTextColour(c, 5, 'green')
            elif v[5] <= 14:
                self.itemsGrid.SetCellTextColour(c, 5, 'yellow')
            elif v[5] <= 20.9:
                self.itemsGrid.SetCellTextColour(c, 5, 'orange')
            elif v[5] <= 27.9:
                self.itemsGrid.SetCellTextColour(c, 5, 'red')
            else:
                attr = wx.grid.GridCellAttr()
                attr.SetTextColour('red')
                attr.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                self.itemsGrid.SetAttr(c, 8, attr)


            # Highlight cell of element that contains the search word criteria
            if 'keyword' in self.search_details:
                search_text = self.search_details.split('keyword')[1].strip()
                
                if search_text in str(v[0]):
                    self.itemsGrid.SetCellBackgroundColour(c, 0, 'light blue')
                elif search_text in str(v[1]):
                    self.itemsGrid.SetCellBackgroundColour(c, 1, 'light blue')
                elif search_text in str(v[2]):
                    self.itemsGrid.SetCellBackgroundColour(c, 2, 'light blue')
                elif search_text in str(v[3]):
                    self.itemsGrid.SetCellBackgroundColour(c, 3, 'light blue')
                elif search_text in str(v[4]):
                    self.itemsGrid.SetCellBackgroundColour(c, 4, 'light blue')

        self.itemsGrid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onGridSelect)

    def onGridSelect(self, event):
        # Clear selected elements events
        self.itemsGrid.ClearSelection()

        # Goto detail view
        if event.Col == 8:
            print("Click on trade details")
            pass    # TODO: Fill with trade details view later