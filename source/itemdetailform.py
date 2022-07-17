
import wx
import wx.grid
import numpy as np

class ItemDetailForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
            self.detailresult = kwargs.pop("result")
            self.user_status = kwargs.pop("user_status")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-Item Detail", size=(700,400))
        # self.SetIcon(parent.icon)
        self._new_user = None

        font_10n = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font_10b = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.SetBackgroundColour('white')
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        gs = wx.FlexGridSizer(8, 4, 5, 5)

        text_td = wx.StaticText(panel, -1, label="Item Details")
        text_td.SetFont(font_10n)
        gs.Add(text_td, 0, wx.EXPAND)
        
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        blue_line = wx.StaticText(panel, label="_"*30)
        blue_line.SetForegroundColour('blue')
        gs.Add(blue_line, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_in = wx.StaticText(panel, label="Item #")
        text_in.SetFont(font_10b)
        gs.Add(text_in, 0, wx.EXPAND)

        result_in = wx.StaticText(panel, label=str(self.detailresult[0]))
        result_in.SetFont(font_10n)
        gs.Add(result_in, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        user_nickname_query = 'select postal_code, first_name, last_name from TradePlazaUser where email = %(user_id)s'
        query_dict = {'user_id':self.detailresult[5]}
        cursor = self.connection.cursor()
        iterator = cursor.execute(user_nickname_query, query_dict)
        result_user = cursor.fetchall()

        text_ar = wx.StaticText(panel, label="Title")
        text_ar.SetFont(font_10b)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=self.detailresult[2])
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        text_d = wx.StaticText(panel, label="Location")
        text_d.SetFont(font_10n)
        gs.Add(text_d, 0, wx.EXPAND)

        addr_query = 'select city, state from Address where postal_code = %(user_id)s'
        query_dict = {'user_id':result_user[0][0]}
        cursor = self.connection.cursor()
        iterator = cursor.execute(addr_query, query_dict)
        result_add = cursor.fetchall()
        
        result_pd = wx.StaticText(panel, label=result_add[0][0] + ', ' +result_add[0][1]+ ' '+ result_user[0][0])
        result_pd.SetFont(font_10n)
        gs.Add(result_pd, 0, wx.EXPAND)

        text_ar = wx.StaticText(panel, label="Game Type")
        text_ar.SetFont(font_10b)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=self.detailresult[1])
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        text_rt = wx.StaticText(panel, label="Response Time")
        text_rt.SetFont(font_10n)
        gs.Add(text_rt, 0, wx.EXPAND)

        result_rt = wx.StaticText(panel, label=self.user_status[1] + ' days')
        result_rt.SetFont(font_10n)
        if self.user_status[1] == 'None':
            result_rt.SetForegroundColour("Black")
        elif float(self.user_status[1]) <= 7.0:
            result_rt.SetForegroundColour("Green")
        elif float(self.user_status[1]) <= 14.0:
            result_rt.SetForegroundColour("Yellow")
        elif float(self.user_status[1]) <= 20.9:
            result_rt.SetForegroundColour("Orange")
        elif float(self.user_status[1]) <= 27.9:
            result_rt.SetForegroundColour("Red")
        else:
            result_rt.SetForegroundColour("Red")
        gs.Add(result_rt, 0, wx.EXPAND)

        text_ar = wx.StaticText(panel, label="Platform")
        text_ar.SetFont(font_10b)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=self.detailresult[6])
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        text_ar = wx.StaticText(panel, label="Rank")
        text_ar.SetFont(font_10n)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=self.user_status[2])
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        text_ar = wx.StaticText(panel, label="Media")
        text_ar.SetFont(font_10b)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=self.detailresult[7])
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_ar = wx.StaticText(panel, label="Condition")
        text_ar.SetFont(font_10b)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=self.detailresult[3])
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        main_sizer.Add(gs, 1, wx.EXPAND|wx.ALL, border = 15)
        panel.SetSizer(main_sizer)
