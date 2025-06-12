from pathlib import Path
import wx
import taglib


class Eraser(wx.Frame):
    def __init__(self, *args, **kw):
        super(Eraser, self).__init__(*args, **kw)
        self.InitUI()
        self.file = None
        self.btnFilePath.Bind(wx.EVT_BUTTON, self.ReadFile)
        self.btnSaveChanges.Bind(wx.EVT_BUTTON, self.SaveChanges)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def SaveChanges(self, event):
        self.file.tags['ARTIST'][0] = self.artist.GetValue()
        self.file.save()

    def ReadFile(self, event):
        with wx.FileDialog(self, wildcard="All (*.wav, *.mp3, *.flac)|*.wav;*.mp3;*.flac|WAV files (*.wav)|*.wav|MP3 files (*.mp3)|*.mp3|FLAC files (*.flac)|*.flac") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
        # Proceed loading the file chosen by the user
        pathname = fileDialog.GetPath()
        file = taglib.File(pathname, save_on_exit=False)
        # TITLE, ALBUM, ALBUMARTIST, ARTIST,
        self.file = file
        self.title.SetValue(file.tags['TITLE'][0])
        self.album.SetValue(file.tags['ALBUM'][0])
        self.artist.SetValue(file.tags['ARTIST'][0])

    def InitUI(self):
        self.pnl = wx.Panel(self)
        self.pnl.Centre()
        # rows, columns, vgap, hgap
        self.gs = wx.GridBagSizer(10, 10)
        self.btnFilePath = wx.Button(self.pnl, wx.ID_ANY, "Get file")
        self.btnSaveChanges = wx.Button(self.pnl, wx.ID_ANY, "Save Changes")
        self.gs.Add(self.btnFilePath, pos=(4, 2), flag=wx.ALL, border=5)
        self.gs.Add(self.btnSaveChanges, pos=(4, 4), flag=wx.ALL, border=5)
        self.title_label = wx.StaticText(self.pnl, label="Title:")
        self.album_label = wx.StaticText(self.pnl, label="Album:")
        self.artist_label = wx.StaticText(self.pnl, label="Artist:")
        self.title = wx.TextCtrl(self.pnl, value="", style=wx.TE_MULTILINE)
        self.album = wx.TextCtrl(self.pnl, value="", style=wx.TE_MULTILINE)
        self.artist = wx.TextCtrl(self.pnl, value="", style=wx.TE_MULTILINE)
        self.gs.Add(self.title_label, pos=(0, 0),
                    flag=wx.ALL | wx.EXPAND, border=10)
        self.gs.Add(self.title, pos=(0, 1), flag=wx.ALL | wx.EXPAND, border=10)
        self.gs.Add(self.album_label, pos=(0, 2),
                    flag=wx.ALL | wx.EXPAND, border=10)
        self.gs.Add(self.album, pos=(0, 3), flag=wx.ALL | wx.EXPAND, border=10)
        self.gs.Add(self.artist_label, pos=(0, 4),
                    flag=wx.ALL | wx.EXPAND, border=10)
        self.gs.Add(self.artist, pos=(0, 5),
                    flag=wx.ALL | wx.EXPAND, border=10)
        self.panel_content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_content_sizer.Add(self.gs, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        self.pnl.SetSizer(self.panel_content_sizer)
        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(self.pnl, 1, wx.EXPAND)
        self.SetSizerAndFit(self.frame_sizer)

    def OnClose(self, event):
        print("Something")
        if self.file is not None:
            self.file.close()
        event.Skip()


def main():
    app = wx.App()
    frm = Eraser(None, title="Eraser")
    frm.SetSize(920, 500)
    frm.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
