import wx
import re


class ConnectDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_text = wx.TextCtrl(self)
        self.nickname_text = wx.TextCtrl(self)
        self.password_text = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.connect_btn = wx.Button(self, label="Connect")

        self.connect_btn.Bind(wx.EVT_BUTTON, self.on_connect)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Server"), 0, wx.ALL, 5)
        sizer.Add(self.server_text, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(wx.StaticText(self, label="Nickname"), 0, wx.ALL, 5)
        sizer.Add(self.nickname_text, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(wx.StaticText(self, label="Password"), 0, wx.ALL, 5)
        sizer.Add(self.password_text, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.connect_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizerAndFit(sizer)

    def on_connect(self, event):
        server = self.server_text.GetValue().strip()  # Получение значения поля сервера
        nickname = self.nickname_text.GetValue().strip()  # Получение значения поля никнейма

        # Проверка корректности адреса сервера
        if not self.validate_server(server):
            wx.MessageBox("Invalid server address!", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Проверка корректности никнейма
        if not self.validate_nickname(nickname):
            wx.MessageBox("Invalid nickname, only english letters are allowed.", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.EndModal(wx.ID_OK)

    def validate_server(self, server):
        pattern = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, server) is not None

    def validate_nickname(self, nickname):
        # Паттерн для проверки никнейма (только английские буквы)
        pattern = r"^[a-zA-Z]+$"
        return re.match(pattern, nickname) is not None
