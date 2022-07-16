from itertools import count
import wx
from datetime import date

class AcceptRejectForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_email = kwargs.pop("user_email")
            self.user_id = kwargs.pop("user_id")
        except:
            self.Destroy()
        super().__init__(parent, title="TradePlaza")
        self.SetIcon(parent.icon)
        
        self.SetBackgroundColour('white')
        formSizer = wx.BoxSizer(wx.VERTICAL)
        formSizer.Add(wx.StaticText(self, label="Accept/Reject Trades"), 0, wx.ALL, 1)
        tmp = wx.StaticText(self, label="_"*120)
        tmp.SetForegroundColour('blue')
        formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 2)

        self.populateTrades()
        formSizer.Add(self.itemsGrid, 0, wx.ALL, 2)

        self.SetSizerAndFit(formSizer)

        # Go back to the main menu if there are no items to trade
        if self.itemsGrid.GetNumberRows() == 0:
            res = wx.MessageBox("No pending trades to accept/reject. Returning to main menu.")
            self.Destroy()


    def populateTrades(self):
        query = """
        SELECT proposed_date, my_item.title, my_item.item_number, my_user.nickname, my_user.email, offered_user.nickname, offered_user.email, offered_item.title, offered_item.item_number, (3958.75 * 2 * POWER(ATAN(SQRT((POWER(SIN((offered_address.Latitude - my_address.Latitude) / 2), 2) + COS(my_address.Latitude) * COS(offered_address.Latitude) * POWER(SIN((offered_address.Longitude - my_address.Longitude) / 2), 2))), SQRT(1 - (POWER(SIN((offered_address.Latitude - my_address.Latitude) / 2), 2) + COS(my_address.Latitude) * COS(offered_address.Latitude) * POWER(SIN((offered_address.Longitude - my_address.Longitude) / 2), 2)))), 2)) as distance
        FROM Trade INNER JOIN
            (SELECT item_number, email, title FROM BoardGame UNION
                SELECT item_number, email, title FROM CollectibleCardGame UNION
                SELECT item_number, email, title FROM ComputerGame UNION
                SELECT item_number, email, title FROM PlayingCardGame UNION
                SELECT item_number, email, title FROM VideoGame
            ) AS offered_item ON counter_party_item_number = offered_item.item_number INNER JOIN
            tradeplazauser as offered_user ON offered_user.email = offered_item.email INNER JOIN
            address as offered_address ON offered_user.postal_code = offered_address.postal_code INNER JOIN
            (SELECT item_number, email, title FROM BoardGame UNION
                SELECT item_number, email, title FROM CollectibleCardGame UNION
                SELECT item_number, email, title FROM ComputerGame UNION
                SELECT item_number, email, title FROM PlayingCardGame UNION
                SELECT item_number, email, title FROM VideoGame
            ) AS my_item ON proposer_item_number = my_item.item_number INNER JOIN
            tradeplazauser as my_user ON my_user.email = my_item.email INNER JOIN
            address as my_address ON my_user.postal_code = my_address.postal_code
        WHERE (my_user.email = "{}" OR my_user.nickname = "{}") AND (trade_status = "PENDING" or trade_status is null)
        """.format(self.user_email, self.user_id)

        cursor = self.connection.cursor()
        cursor.execute(query)

        self.itemsGrid = wx.grid.Grid(self, wx.ID_ANY)
        self.itemsGrid.CreateGrid(0, 12)
        self.itemsGrid.HideRowLabels()
        self.itemsGrid.SetColLabelValue(0, "Date")
        self.itemsGrid.SetColLabelValue(1, "Desired Item")
        self.itemsGrid.SetColLabelValue(2, "Proposer")
        self.itemsGrid.SetColLabelValue(3, "Rank")
        self.itemsGrid.SetColLabelValue(4, "Distance")
        self.itemsGrid.SetColLabelValue(5, "Proposed Item")
        self.itemsGrid.SetColLabelValue(6, "")
        self.itemsGrid.SetColLabelValue(7, "")
        self.itemsGrid.SetColLabelValue(8, "my_item_number")
        self.itemsGrid.SetColLabelValue(9, "offered_item_number")
        self.itemsGrid.SetColLabelValue(10, "my_email")
        self.itemsGrid.SetColLabelValue(11, "offered_email")

        self.itemsGrid.HideCol(8)
        self.itemsGrid.HideCol(9)
        self.itemsGrid.HideCol(10)
        self.itemsGrid.HideCol(11)
        self.itemsGrid.SetDefaultRowSize(30)
        self.itemsGrid.SetDefaultColSize(100)
        self.itemsGrid.SetColSize(1, 150)
        self.itemsGrid.SetColSize(5, 150)

        for row, (proposed_date, my_title, my_item_number, my_nickname, my_email, offered_nickname, offered_email, offered_title, offered_item_number, distance) in enumerate(cursor.fetchall()):
            item = (proposed_date, my_title, offered_nickname, "RANK", distance, offered_title, "ACCEPT", "REJECT", my_item_number, offered_item_number, my_email, offered_email)
            self.itemsGrid.AppendRows(numRows=1)
            for col, attribute in enumerate(item):
                self.itemsGrid.SetCellValue(row, col, str(attribute))
                self.itemsGrid.SetReadOnly(row, col, True)
                if col == 6:
                    self.itemsGrid.SetCellBackgroundColour(row, col, 'blue')
                elif col == 7:
                    self.itemsGrid.SetCellBackgroundColour(row, col, 'red')
                elif col == 1:
                    self.itemsGrid.SetCellTextColour(row, col, 'blue')
                elif col == 5:
                    self.itemsGrid.SetCellTextColour(row, col, 'blue')

        self.itemsGrid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onGridSelect)

    def onGridSelect(self, event):
        self.itemsGrid.ClearSelection()
        query = """
        UPDATE Trade SET trade_status = "{}", accept_reject_date = NOW() WHERE proposer_item_number = {} AND counter_party_item_number = {}
        """
        cursor = self.connection.cursor()
        propose_number = self.itemsGrid.GetCellValue(event.Row, 8)
        counter_number = self.itemsGrid.GetCellValue(event.Row, 9)
        
        # Accept trade
        if event.Col == 6:
            other_name = self.itemsGrid.GetCellValue(event.Row, 2)
            other_email = self.itemsGrid.GetCellValue(event.Row, 11)

            # Execute query to update database
            query = query.format("ACCEPT", str(propose_number), str(counter_number))
            cursor.execute(query)
            self.connection.commit()

            res = wx.MessageBox("Trade Accepted\nContact the proposer to trade items!\n\nEmail: {}\nName: {}".format(other_email, other_name))
        # Reject trade
        elif event.Col == 7:
            # Execute query to update database
            query = query.format("REJECT", str(propose_number), str(counter_number))
            cursor.execute(query)
            self.connection.commit()
        # Go to trade details page for proposed item
        elif event.Col == 1:
            pass
        # Go to trade details page for counter item
        elif event.Col == 5:
            pass
        # Ignore event
        else:
            return

        print(query)
        print(propose_number, counter_number)
        
        # Remove row from table
        self.itemsGrid.DeleteRows(event.Row)

        # Go back to the main menu if there are no items to trade
        if self.itemsGrid.GetNumberRows() == 0:
            res = wx.MessageBox("No pending trades to accept/reject. Returning to main menu.")
            self.EndModal(wx.ID_EXIT)