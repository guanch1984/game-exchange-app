
import wx
import wx.grid
import numpy as np

class TradeHistoryDetailForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
            self.detailresult = kwargs.pop("result")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-Trade History Detail", size=(800,400))
        # self.SetIcon(parent.icon)
        self._new_user = None

        font_10n = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font_10b = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.SetBackgroundColour('white')
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        gs = wx.FlexGridSizer(15, 4, 5, 5)

        text_td = wx.StaticText(panel, -1, label="Trade Details")
        text_td.SetFont(font_10n)
        gs.Add(text_td, 0, wx.EXPAND)
        
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_ud = wx.StaticText(panel, -1, label="User Details")
        text_ud.SetFont(font_10n)
        gs.Add(text_ud, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        blue_line = wx.StaticText(panel, label="_"*30)
        blue_line.SetForegroundColour('blue')
        gs.Add(blue_line, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        blue_line = wx.StaticText(panel, label="_"*30)
        blue_line.SetForegroundColour('blue')
        gs.Add(blue_line, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_proposed = wx.StaticText(panel, label="Proposed")
        text_proposed.SetFont(font_10b)
        gs.Add(text_proposed, 0, wx.EXPAND)

        result_pd = wx.StaticText(panel, label=self.detailresult[0])
        result_pd.SetFont(font_10n)
        gs.Add(result_pd, 0, wx.EXPAND)

        text_nn = wx.StaticText(panel, label="Nickname")
        text_nn.SetFont(font_10b)
        gs.Add(text_nn, 0, wx.EXPAND)

        user_nickname_query = 'select nickname, postal_code, first_name from TradePlazaUser where email = %(user_id)s or nickname = %(user_id)s'
        query_dict = {'user_id':self.user_id}
        cursor = self.connection.cursor()
        iterator = cursor.execute(user_nickname_query, query_dict)
        result_user = cursor.fetchall()
        
        result_pd = wx.StaticText(panel, label=result_user[0][0])
        result_pd.SetFont(font_10n)
        gs.Add(result_pd, 0, wx.EXPAND)

        text_ar = wx.StaticText(panel, label="Accepted/Rejected")
        text_ar.SetFont(font_10b)
        gs.Add(text_ar, 0, wx.EXPAND)

        result_ar = wx.StaticText(panel, label=str(self.detailresult[1]))
        result_ar.SetFont(font_10n)
        gs.Add(result_ar, 0, wx.EXPAND)

        text_d = wx.StaticText(panel, label="Distance")
        text_d.SetFont(font_10b)
        gs.Add(text_d, 0, wx.EXPAND)

        
        # print(self.detailresult[15:])
        lon1, lat1, lon2, lat2 = self.detailresult[15:]
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        a = np.sin(d_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        R = 3958.75
        d = np.round(R*c,2)
        text_d = wx.StaticText(panel, label=str(d)+' miles')
        text_d.SetFont(font_10n)
        gs.Add(text_d, 0, wx.EXPAND)

        text_status = wx.StaticText(panel, label="Status")
        text_status.SetFont(font_10b)
        gs.Add(text_status, 0, wx.EXPAND)

        result_status = wx.StaticText(panel, label=self.detailresult[2])
        result_status.SetFont(font_10n)
        gs.Add(result_status, 0, wx.EXPAND)

        text_name = wx.StaticText(panel, label="Name")
        text_name.SetFont(font_10b)
        gs.Add(text_name, 0, wx.EXPAND)

        result_fn = wx.StaticText(panel, label=result_user[0][2])
        result_fn.SetFont(font_10n)
        gs.Add(result_fn, 0, wx.EXPAND)

        text_myrole = wx.StaticText(panel, label="My role")
        text_myrole.SetFont(font_10b)
        gs.Add(text_myrole, 0, wx.EXPAND)

        result_mr = wx.StaticText(panel, label=self.detailresult[4])
        result_mr.SetFont(font_10n)
        gs.Add(result_mr, 0, wx.EXPAND)

        text_email = wx.StaticText(panel, label="Email")
        text_email.SetFont(font_10b)
        gs.Add(text_email, 0, wx.EXPAND)

        result_email = wx.StaticText(panel, label=self.user_id)
        result_email.SetFont(font_10n)
        gs.Add(result_email, 0, wx.EXPAND)

        text_rt = wx.StaticText(panel, label="Response time")
        text_rt.SetFont(font_10b)
        gs.Add(text_rt, 0, wx.EXPAND)

        result_rt = wx.StaticText(panel, label=str(self.detailresult[3])+' days')
        result_rt.SetFont(font_10n)
        gs.Add(result_rt, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_pi = wx.StaticText(panel, -1, label="Proposed Item")
        text_pi.SetFont(font_10n)
        gs.Add(text_pi, 0, wx.EXPAND)
        
        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_di = wx.StaticText(panel, -1, label="Desired Item")
        text_di.SetFont(font_10n)
        gs.Add(text_di, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        blue_line = wx.StaticText(panel, label="_"*30)
        blue_line.SetForegroundColour('blue')
        gs.Add(blue_line, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        blue_line = wx.StaticText(panel, label="_"*30)
        blue_line.SetForegroundColour('blue')
        gs.Add(blue_line, 0, wx.EXPAND)

        tmp = wx.StaticText(panel, -1, label="")
        gs.Add(tmp, 0, wx.EXPAND)

        text_in = wx.StaticText(panel, label="Item #")
        text_in.SetFont(font_10b)
        gs.Add(text_in, 0, wx.EXPAND)

        result_pi = wx.StaticText(panel, label=str(self.detailresult[8]))
        result_pi.SetFont(font_10n)
        gs.Add(result_pi, 0, wx.EXPAND)

        text_in = wx.StaticText(panel, label="Item #")
        text_in.SetFont(font_10b)
        gs.Add(text_in, 0, wx.EXPAND)

        result_di = wx.StaticText(panel, label=str(self.detailresult[9]))
        result_di.SetFont(font_10n)
        gs.Add(result_di, 0, wx.EXPAND)

        text_title = wx.StaticText(panel, label="Title")
        text_title.SetFont(font_10b)
        gs.Add(text_title, 0, wx.EXPAND)

        result_pi = wx.StaticText(panel, label=str(self.detailresult[5]))
        result_pi.SetFont(font_10n)
        gs.Add(result_pi, 0, wx.EXPAND)

        text_title = wx.StaticText(panel, label="Title")
        text_title.SetFont(font_10b)
        gs.Add(text_title, 0, wx.EXPAND)

        result_di = wx.StaticText(panel, label=str(self.detailresult[6]))
        result_di.SetFont(font_10n)
        gs.Add(result_di, 0, wx.EXPAND)

        text_gt = wx.StaticText(panel, label="Game Type")
        text_gt.SetFont(font_10b)
        gs.Add(text_gt, 0, wx.EXPAND)

        result_pgt = wx.StaticText(panel, label=str(self.detailresult[10]))
        result_pgt.SetFont(font_10n)
        gs.Add(result_pgt, 0, wx.EXPAND)

        text_gt = wx.StaticText(panel, label="Game Type")
        text_gt.SetFont(font_10b)
        gs.Add(text_gt, 0, wx.EXPAND)

        result_dgt = wx.StaticText(panel, label=str(self.detailresult[11]))
        result_dgt.SetFont(font_10n)
        gs.Add(result_dgt, 0, wx.EXPAND)

        text_condition = wx.StaticText(panel, label="Condition")
        text_condition.SetFont(font_10b)
        gs.Add(text_condition, 0, wx.EXPAND)

        result_pc = wx.StaticText(panel, label=str(self.detailresult[12]))
        result_pc.SetFont(font_10n)
        gs.Add(result_pc, 0, wx.EXPAND)

        text_condition = wx.StaticText(panel, label="Condition")
        text_condition.SetFont(font_10b)
        gs.Add(text_condition, 0, wx.EXPAND)

        result_dc = wx.StaticText(panel, label=str(self.detailresult[13]))
        result_dc.SetFont(font_10n)
        gs.Add(result_dc, 0, wx.EXPAND)

        text_des = wx.StaticText(panel, label="Description")
        text_des.SetFont(font_10b)
        gs.Add(text_des, 0, wx.EXPAND)

        result_des = wx.StaticText(panel, label=str(self.detailresult[14]))
        result_des.SetFont(font_10n)
        gs.Add(result_des, 0, wx.EXPAND)

        # panel.SetSizerAndFit(gs)
        # self.SetSizerAndFit(main_sizer)
        main_sizer.Add(gs, 1, wx.EXPAND|wx.ALL, border = 15)
        panel.SetSizer(main_sizer)
