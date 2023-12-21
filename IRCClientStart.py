import wx
from core.IRCFrame import IRCFrame


if __name__ == '__main__':
    app = wx.App()
    frame = IRCFrame(None)
    frame.Show()
    app.MainLoop()
