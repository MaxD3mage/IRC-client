import wx
from threading import Thread
from IRCClient import IRCClient
from IRCConnect import ConnectDialog


class IRCFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="IRC Client", size=(600, 400))
        self.channel = None
        self.panel = wx.Panel(self)

        self.chat_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.command_text = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.send_button = wx.Button(self.panel, label="Send")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.chat_text, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.command_text, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.send_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.sizer)

        self.command_text.Bind(wx.EVT_TEXT_ENTER, self.on_send)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.connect_dialog = ConnectDialog(self)
        result = self.connect_dialog.ShowModal()
        if result == wx.ID_OK:
            server = self.connect_dialog.server_text.GetValue()
            nickname = self.connect_dialog.nickname_text.GetValue()
            self.irc_client = IRCClient(server, 6667, nickname)
            self.irc_client.connect()
            self.connect_dialog.Destroy()

            self.receive_thread = Thread(target=self.receive_messages)
            self.receive_thread.start()
        else:
            self.Destroy()

    def on_send(self, event):
        command = self.command_text.GetValue()
        self.process_command(command)
        self.command_text.Clear()

    def process_command(self, command):
        if command.startswith('/join'):
            channel = command.split()[1]
            message = f"\nПрисоединяюсь к каналу {channel}..."
            self.add_chat_message(message)
            self.irc_client.join_channel(channel)
            self.channel = channel
        elif command.startswith('/list'):
            self.irc_client.get_channels()
        elif command.startswith('/quit'):
            message = command.split()[1] if len(command.split()) > 1 else None
            self.irc_client.disconnect(message)
            self.Close()
        else:
            self.irc_client.send_message(command, self.channel)
        self.add_chat_message(f"{self.irc_client.nickname}: {command}")

    def receive_messages(self):
        while True:
            data = self.irc_client.receive_message()
            if not data:
                break
            self.add_chat_message(data)

    def add_chat_message(self, message):
        self.chat_text.AppendText(f"{message}\n")

    def on_close(self, event):
        try:
            self.irc_client.disconnect()
            self.receive_thread.join()
            self.Destroy()
        except OSError:
            pass
        finally:
            self.Destroy()
