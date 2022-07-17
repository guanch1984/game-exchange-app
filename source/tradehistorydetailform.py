import wx
import wx.grid

class TradeHistoryDetailForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
            self.detailresult = kwargs.pop("result")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-Trade History Detail")
        # self.SetIcon(parent.icon)
        self._new_user = None

        self.SetBackgroundColour('white')
        # panel = wx.Panel(self)
        # hbox = wx.BoxSizer(wx.HORIZONTAL)

        # fgs = wx.FlexGridSizer(2, 2, 15, 15)
        font_10n = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font_10b = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        

        formSizer_td = wx.BoxSizer(wx.VERTICAL)
        text_td = wx.StaticText(self, label="Trade Details")
        text_td.SetFont(font_10n)
        blue_line = wx.StaticText(self, label="_"*80)
        blue_line.SetForegroundColour('blue')
        text_proposed = wx.StaticText(self, label="Proposed")
        text_proposed.SetFont(font_10b)
        text_ar = wx.StaticText(self, label="Accepted/Rejected")
        text_ar.SetFont(font_10b)
        text_status = wx.StaticText(self, label="Status")
        text_status.SetFont(font_10b)
        text_myrole = wx.StaticText(self, label="My role")
        text_myrole.SetFont(font_10b)
        text_rt = wx.StaticText(self, label="Response time")
        text_rt.SetFont(font_10b)
        formSizer_td.Add(text_td, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(blue_line, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_proposed, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_ar, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_status, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_myrole, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_rt, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)

        formSizer_ud = wx.BoxSizer(wx.VERTICAL)
        text_ud = wx.StaticText(self, label="User Details")
        text_ud.SetFont(font_10n)
        
        text_nn = wx.StaticText(self, label="Nickname")
        text_nn.SetFont(font_10b)
        text_d = wx.StaticText(self, label="Disctance")
        text_d.SetFont(font_10b)
        text_name = wx.StaticText(self, label="Name")
        text_name.SetFont(font_10b)
        text_email = wx.StaticText(self, label="Email")
        text_email.SetFont(font_10b)
        formSizer_ud.Add(text_ud, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_ud.Add(blue_line, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_ud.Add(text_nn, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_ud.Add(text_d, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_ud.Add(text_name, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_ud.Add(text_email, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        
        formSizer_td = wx.BoxSizer(wx.VERTICAL)
        text_td = wx.StaticText(self, label="Trade Details")
        text_td.SetFont(font_10n)
        blue_line = wx.StaticText(self, label="_"*80)
        blue_line.SetForegroundColour('blue')
        text_proposed = wx.StaticText(self, label="Proposed")
        text_proposed.SetFont(font_10b)
        text_ar = wx.StaticText(self, label="Accepted/Rejected")
        text_ar.SetFont(font_10b)
        text_status = wx.StaticText(self, label="Status")
        text_status.SetFont(font_10b)
        text_myrole = wx.StaticText(self, label="My role")
        text_myrole.SetFont(font_10b)
        text_rt = wx.StaticText(self, label="Response time")
        text_rt.SetFont(font_10b)
        formSizer_td.Add(text_td, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(blue_line, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_proposed, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_ar, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_status, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_myrole, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        formSizer_td.Add(text_rt, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 5)
        
        # fgs.AddMany([(formSizer_td), (formSizer_td), (formSizer_td),(formSizer_td)])
        # hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        # panel.SetSizer(hbox)

        self.SetSizerAndFit(formSizer_td)


        

        # tmp = wx.StaticText(self, label="User Details")
        # formSizer.Add(tmp, 0, wx.LEFT, 5)
        # tmp = wx.StaticText(self, label="_"*80)
        # tmp.SetForegroundColour('blue')
        # formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        # tmp = wx.StaticText(self, label="Proposed Item")
        # formSizer.Add(tmp, 0, wx.LEFT, 5)
        # tmp = wx.StaticText(self, label="_"*80)
        # tmp.SetForegroundColour('blue')
        # formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)

        # tmp = wx.StaticText(self, label="Desired Item")
        # formSizer.Add(tmp, 0, wx.LEFT, 5)
        # tmp = wx.StaticText(self, label="_"*80)
        # tmp.SetForegroundColour('blue')
        # formSizer.Add(tmp, 0, wx.LEFT|wx.RIGHT, 5)