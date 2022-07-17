
from proposetradeform import ProposeTradeForm
import wx,mysql
import wx.grid


def form_query(item_number):

    query = """
    
WITH items_union AS(
    Select
        temp.item_number,
        title,
        description,
        game_condition,
        game_type,
        vg_platform,
        cg_platform,
        media,
        number_of_cards,
        email
    from
        Item it
        INNER JOIN (
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Video game" as game_type,
                    email,
                    null as number_of_cards,
                    null as cg_platform,
                    media,
                    name as vg_platform
                from
                    VideoGame
                    INNER JOIN platform on VideoGame.platform_id = platform.platform_id
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Computer game" as game_type,
                    email,
                    null as number_of_cards,
                    platform as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    ComputerGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Collectible card game" as game_type,
                    email,
                    number_of_cards,
                    null as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    CollectibleCardGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Playing card game" as game_type,
                    email,
                    null as number_of_cards,
                    null as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    PlayingCardGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Board game" as game_type,
                    email,
                    null as number_of_cards,
                    null as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    BoardGame
            )
        ) temp ON temp.item_number = it.item_number
)
select
    vg_platform,
    cg_platform,
    media,
    number_of_cards,
    email
from
    items_union
where
    item_number = {item_number}
    """.format(item_number=item_number)

    return query


def form_query_propose_trade(user_email):

    query = """
    
WITH items_union AS(
    Select
        temp.item_number,
        title,
        description,
        game_condition,
        game_type,
        vg_platform,
        cg_platform,
        media,
        number_of_cards,
        email
    from
        Item it
        INNER JOIN (
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Video game" as game_type,
                    email,
                    null as number_of_cards,
                    null as cg_platform,
                    media,
                    name as vg_platform
                from
                    VideoGame
                    INNER JOIN platform on VideoGame.platform_id = platform.platform_id
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Computer game" as game_type,
                    email,
                    null as number_of_cards,
                    platform as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    ComputerGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Collectible card game" as game_type,
                    email,
                    number_of_cards,
                    null as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    CollectibleCardGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Playing card game" as game_type,
                    email,
                    null as number_of_cards,
                    null as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    PlayingCardGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Board game" as game_type,
                    email,
                    null as number_of_cards,
                    null as cg_platform,
                    null as media,
                    null as vg_platform
                from
                    BoardGame
            )
        ) temp ON temp.item_number = it.item_number
)
    SELECT
        count(*) as no_of_trades
    FROM
        items_union i
        INNER JOIN TradePlazaUser u ON i.email = u.email
    WHERE
        u.email = '{user_email}'
        AND item_number IN(
            
                SELECT
                    counter_party_item_number
                FROM
                    Trade
                where trade_status = 'PENDING'
             )

    """.format(user_email=user_email)

    return query


class ItemDetailsForm(wx.Dialog):
    def __init__(self, parent, **kwargs):
        try:
            self.connection = kwargs.pop("connection")
            self.user_id = kwargs.pop("user_id")
            self.searchresult = kwargs.pop("result")
        except:
            self.Destroy()

        super().__init__(parent, title="TradePlaza-Item Details", size=(700,400))
        self._new_user = None

        try:
            cursor = self.connection.cursor()
            self.query = form_query(self.searchresult[0])

            cursor.execute(self.query)
            self.itemresult = cursor.fetchone()

            if self.user_id != self.itemresult[4]:
                self.is_another_user = True
                cursor.execute(" select nickname, postal_code from TradePlazaUser where email='{0}' ".format(self.itemresult[4]))
                res = cursor.fetchone()
                self.another_u_nickname = res[0]
                self.another_u_pc = res[1]

                cursor.execute(" select city, state from Address where postal_code='{0}' ".format(self.another_u_pc))
                res = cursor.fetchone()
                self.another_u_city = res[0]
                self.another_u_state = res[1]

                cursor.execute(" select postal_code from TradePlazaUser where email='{0}' ".format(self.user_id))
                res = cursor.fetchone()
                if res[0] != self.another_u_pc:
                    self.is_diff_pc = True

        except(mysql.connector.Error,Exception) as e:
            wx.MessageBox("Error in retrieving item details: " + str(e), "Error", style=wx.OK|wx.ICON_ERROR)
            return False

        font_10n = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font_10b = wx.Font(10,wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.SetBackgroundColour('white')
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        if not self.is_another_user:
            gs = wx.FlexGridSizer(10, 2, 5, 5)

            text_pi = wx.StaticText(panel, -1, label="Item Details")
            text_pi.SetFont(font_10n)
            gs.Add(text_pi, 0, wx.EXPAND)
            
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

            result_pi = wx.StaticText(panel, label=str(self.searchresult[0]))
            result_pi.SetFont(font_10n)
            gs.Add(result_pi, 0, wx.EXPAND)

            text_title = wx.StaticText(panel, label="Title")
            text_title.SetFont(font_10b)
            gs.Add(text_title, 0, wx.EXPAND)

            result_pi = wx.StaticText(panel, label=str(self.searchresult[2]))
            result_pi.SetFont(font_10n)
            gs.Add(result_pi, 0, wx.EXPAND)

            text_gt = wx.StaticText(panel, label="Game Type")
            text_gt.SetFont(font_10b)
            gs.Add(text_gt, 0, wx.EXPAND)

            result_dgt = wx.StaticText(panel, label=str(self.searchresult[1]))
            result_dgt.SetFont(font_10n)
            gs.Add(result_dgt, 0, wx.EXPAND)

            if self.searchresult[1] == "Video game":
                text_title = wx.StaticText(panel, label="Platform")
                text_title.SetFont(font_10b)
                gs.Add(text_title, 0, wx.EXPAND)

                result_pi = wx.StaticText(panel, label=str(self.itemresult[0]))
                result_pi.SetFont(font_10n)
                gs.Add(result_pi, 0, wx.EXPAND)

                text_gt = wx.StaticText(panel, label="Media")
                text_gt.SetFont(font_10b)
                gs.Add(text_gt, 0, wx.EXPAND)

                result_dgt = wx.StaticText(panel, label=str(self.itemresult[2]))
                result_dgt.SetFont(font_10n)
                gs.Add(result_dgt, 0, wx.EXPAND)
            
            elif self.searchresult[1] == "Computer game":
                text_title = wx.StaticText(panel, label="Platform")
                text_title.SetFont(font_10b)
                gs.Add(text_title, 0, wx.EXPAND)

                result_pi = wx.StaticText(panel, label=str(self.itemresult[1]))
                result_pi.SetFont(font_10n)
                gs.Add(result_pi, 0, wx.EXPAND)
            
            elif self.searchresult[1] == "Collectible card game":
                text_title = wx.StaticText(panel, label="No Of Cards")
                text_title.SetFont(font_10b)
                gs.Add(text_title, 0, wx.EXPAND)

                result_pi = wx.StaticText(panel, label=str(self.itemresult[3]))
                result_pi.SetFont(font_10n)
                gs.Add(result_pi, 0, wx.EXPAND)

            text_condition = wx.StaticText(panel, label="Condition")
            text_condition.SetFont(font_10b)
            gs.Add(text_condition, 0, wx.EXPAND)

            result_pc = wx.StaticText(panel, label=str(self.searchresult[3]))
            result_pc.SetFont(font_10n)
            gs.Add(result_pc, 0, wx.EXPAND)

            if self.searchresult[4].strip():
                text_condition = wx.StaticText(panel, label="Description")
                text_condition.SetFont(font_10b)
                gs.Add(text_condition, 0, wx.EXPAND)

                result_pc = wx.StaticText(panel, label=str(self.searchresult[3]))
                result_pc.SetFont(font_10n)
                gs.Add(result_pc, 0, wx.EXPAND)
        
        else:
            gs = wx.FlexGridSizer(10, 4, 5, 5)

            text_pi = wx.StaticText(panel, -1, label="Item Details")
            text_pi.SetFont(font_10n)
            gs.Add(text_pi, 0, wx.EXPAND)
            
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

            result_pi = wx.StaticText(panel, label=str(self.searchresult[0]))
            result_pi.SetFont(font_10n)
            gs.Add(result_pi, 0, wx.EXPAND)

            text_in = wx.StaticText(panel, label="Offered by")
            text_in.SetFont(font_10b)
            gs.Add(text_in, 0, wx.EXPAND)

            result_pi = wx.StaticText(panel, label=str(self.another_u_nickname))
            result_pi.SetFont(font_10n)
            gs.Add(result_pi, 0, wx.EXPAND)

            text_title = wx.StaticText(panel, label="Title")
            text_title.SetFont(font_10b)
            gs.Add(text_title, 0, wx.EXPAND)

            result_pi = wx.StaticText(panel, label=str(self.searchresult[2]))
            result_pi.SetFont(font_10n)
            gs.Add(result_pi, 0, wx.EXPAND)

            text_title = wx.StaticText(panel, label="Location")
            text_title.SetFont(font_10b)
            gs.Add(text_title, 0, wx.EXPAND)

            result_pi = wx.StaticText(panel, label=self.another_u_city + ", " + self.another_u_state + " " + self.another_u_pc)
            result_pi.SetFont(font_10n)
            gs.Add(result_pi, 0, wx.EXPAND)

            text_gt = wx.StaticText(panel, label="Game Type")
            text_gt.SetFont(font_10b)
            gs.Add(text_gt, 0, wx.EXPAND)

            result_dgt = wx.StaticText(panel, label=str(self.searchresult[1]))
            result_dgt.SetFont(font_10n)
            gs.Add(result_dgt, 0, wx.EXPAND)

            text_gt = wx.StaticText(panel, label="Response Time")
            text_gt.SetFont(font_10b)
            gs.Add(text_gt, 0, wx.EXPAND)

            result_dgt = wx.StaticText(panel, label=str(self.searchresult[5]))
            result_dgt.SetFont(font_10n)
            gs.Add(result_dgt, 0, wx.EXPAND)

            if self.searchresult[1] == "Video game":
                text_title = wx.StaticText(panel, label="Platform")
                text_title.SetFont(font_10b)
                gs.Add(text_title, 0, wx.EXPAND)

                result_pi = wx.StaticText(panel, label=str(self.itemresult[0]))
                result_pi.SetFont(font_10n)
                gs.Add(result_pi, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

                text_gt = wx.StaticText(panel, label="Media")
                text_gt.SetFont(font_10b)
                gs.Add(text_gt, 0, wx.EXPAND)

                result_dgt = wx.StaticText(panel, label=str(self.itemresult[2]))
                result_dgt.SetFont(font_10n)
                gs.Add(result_dgt, 0, wx.EXPAND)
            
            elif self.searchresult[1] == "Computer game":
                text_title = wx.StaticText(panel, label="Platform")
                text_title.SetFont(font_10b)
                gs.Add(text_title, 0, wx.EXPAND)

                result_pi = wx.StaticText(panel, label=str(self.itemresult[1]))
                result_pi.SetFont(font_10n)
                gs.Add(result_pi, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)
            
            elif self.searchresult[1] == "Collectible card game":
                text_title = wx.StaticText(panel, label="No Of Cards")
                text_title.SetFont(font_10b)
                gs.Add(text_title, 0, wx.EXPAND)

                result_pi = wx.StaticText(panel, label=str(self.itemresult[3]))
                result_pi.SetFont(font_10n)
                gs.Add(result_pi, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

            text_condition = wx.StaticText(panel, label="Condition")
            text_condition.SetFont(font_10b)
            gs.Add(text_condition, 0, wx.EXPAND)

            result_pc = wx.StaticText(panel, label=str(self.searchresult[3]))
            result_pc.SetFont(font_10n)
            gs.Add(result_pc, 0, wx.EXPAND)

            text_condition = wx.StaticText(panel, label="Rank")
            text_condition.SetFont(font_10b)
            gs.Add(text_condition, 0, wx.EXPAND)

            result_pc = wx.StaticText(panel, label=str(self.searchresult[6]))
            result_pc.SetFont(font_10n)
            gs.Add(result_pc, 0, wx.EXPAND)

            if self.searchresult[4].strip():
                text_condition = wx.StaticText(panel, label="Description")
                text_condition.SetFont(font_10b)
                gs.Add(text_condition, 0, wx.EXPAND)

                result_pc = wx.StaticText(panel, label=str(self.searchresult[3]))
                result_pc.SetFont(font_10n)
                gs.Add(result_pc, 0, wx.EXPAND)
            else:
                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

                tmp = wx.StaticText(panel, -1, label="")
                gs.Add(tmp, 0, wx.EXPAND)

            if self.is_diff_pc:
                text_condition = wx.StaticText(panel, label="Distance")
                text_condition.SetFont(font_10b)
                gs.Add(text_condition, 0, wx.EXPAND)

                result_pc = wx.StaticText(panel, label=str(self.searchresult[7]))

                if self.searchresult[7] >=0.0 and self.searchresult[7] <= 25.0:
                    result_pc.SetBackgroundColour("green")
                elif self.searchresult[7] >=25.0 and self.searchresult[7] <= 50.0:
                    result_pc.SetBackgroundColour("yellow")
                elif self.searchresult[7] >=50.0 and self.searchresult[7] <= 100.0:
                    result_pc.SetBackgroundColour("orange")
                elif self.searchresult[7] >100.0:
                    result_pc.SetBackgroundColour("red")

                result_pc.SetFont(font_10n)
                gs.Add(result_pc, 0, wx.EXPAND)

            cursor = self.connection.cursor()
            query = form_query_propose_trade(self.user_id)

            cursor.execute(query)
            res = cursor.fetchone()

            if res <2:
                self.ptBtn = wx.Button(self, label="Propose trade", style=wx.BORDER_NONE)
                self.ptBtn.SetBackgroundColour('blue')
                self.ptBtn.SetForegroundColour('white')
                self.Bind(wx.EVT_BUTTON, self.invoke_propose_trade, self.ptBtn)
                gs.Add(self.ptBtn, 0, wx.ALL, 5)
                self.SetSizerAndFit(gs)
        
        main_sizer.Add(gs, 1, wx.EXPAND|wx.ALL, border = 15)
        panel.SetSizer(main_sizer)

    def invoke_propose_trade(self):
        
        self.Hide()
        sr=ProposeTradeForm(self.Parent, tradeitem=self.searchresult[2],tradeitemnumber=self.searchresult[0],user_id=self.user_id)
        r=sr.ShowModal()
        if r == wx.ID_OK:
            self.EndModal(wx.ID_OK)
