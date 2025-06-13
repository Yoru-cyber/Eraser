import os
import wx
import taglib


class FileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        pathname = os.path.basename(filenames[0])
        self.window.dragFileName.SetValue(pathname)
        self.window.ReadFile(pathname)
        return True


class Eraser(wx.Frame):
    def __init__(self, *argrid, **kw):
        super(Eraser, self).__init__(*argrid, **kw)
        self.InitUI()
        self.file = None
        self.btnFilePath.Bind(wx.EVT_BUTTON, self.OpenFile)
        self.btnSaveChanges.Bind(wx.EVT_BUTTON, self.SaveChanges)
        self.btnResetFields.Bind(wx.EVT_BUTTON, self.ResetFields)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def SaveChanges(self, event):
        self.file.tagrid["ARTIST"][0] = self.artist.GetValue()
        self.file.save()

    def ResetFields(self):
        if self.file is not None:
            self.file.close()
        self.title.SetValue("")
        self.album.SetValue("")
        self.artist.SetValue("")
        self.dragFileName.SetValue("")

    def ReadFile(self, pathname):
        file = taglib.File(pathname, save_on_exit=False)
        self.file = file
        self.title.SetValue(file.tagrid["TITLE"][0])
        self.album.SetValue(file.tagrid["ALBUM"][0])
        self.artist.SetValue(file.tagrid["ARTIST"][0])

    def OpenFile(self, event):
        with wx.FileDialog(
            self,
            wildcard="All (*.wav, *.mp3, *.flac)|*.wav;*.mp3;*.flac|WAV files (*.wav)|*.wav|MP3 files (*.mp3)|*.mp3|FLAC files (*.flac)|*.flac",
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
        pathname = fileDialog.GetPath()
        self.ReadFile(pathname)

    def InitUI(self):
        self.mainPanel = wx.Panel(self)
        self.mainPanel.Centre()
        self.grid = wx.GridBagSizer(10, 10)
        self.btnFilePath = wx.Button(self.mainPanel, wx.ID_ANY, "Get file")
        self.btnSaveChanges = wx.Button(self.mainPanel, wx.ID_ANY, "Save")
        self.btnResetFields = wx.Button(self.mainPanel, wx.ID_ANY, "Reset")
        self.grid.Add(self.btnFilePath, pos=(4, 2), flag=wx.ALL, border=5)
        self.grid.Add(self.btnSaveChanges, pos=(4, 4), flag=wx.ALL, border=5)
        self.grid.Add(self.btnResetFields, pos=(7, 3), flag=wx.ALL, border=5)
        self.file_drop_target = FileDropTarget(self)
        self.dragFileName_label = wx.StaticText(
            self.mainPanel, label="Drag some files here:"
        )
        self.dragFileName = wx.TextCtrl(
            self.mainPanel, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY
        )
        self.dragFileName.SetDropTarget(self.file_drop_target)
        self.title_label = wx.StaticText(self.mainPanel, label="Title:")
        self.album_label = wx.StaticText(self.mainPanel, label="Album:")
        self.artist_label = wx.StaticText(self.mainPanel, label="Artist:")
        self.title = wx.TextCtrl(self.mainPanel, value="", style=wx.TE_MULTILINE)
        self.album = wx.TextCtrl(self.mainPanel, value="", style=wx.TE_MULTILINE)
        self.artist = wx.TextCtrl(self.mainPanel, value="", style=wx.TE_MULTILINE)
        self.grid.Add(self.title_label, pos=(0, 0), flag=wx.ALL | wx.EXPAND, border=10)
        self.grid.Add(self.title, pos=(0, 1), flag=wx.ALL | wx.EXPAND, border=10)
        self.grid.Add(self.album_label, pos=(0, 2), flag=wx.ALL | wx.EXPAND, border=10)
        self.grid.Add(self.album, pos=(0, 3), flag=wx.ALL | wx.EXPAND, border=10)
        self.grid.Add(self.artist_label, pos=(0, 4), flag=wx.ALL | wx.EXPAND, border=10)
        self.grid.Add(self.artist, pos=(0, 5), flag=wx.ALL | wx.EXPAND, border=10)
        self.grid.Add(
            self.dragFileName_label, pos=(5, 3), flag=wx.ALL | wx.EXPAND, border=10
        )
        self.grid.Add(self.dragFileName, pos=(6, 3), flag=wx.ALL | wx.EXPAND, border=10)
        self.panel_content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_content_sizer.Add(self.grid, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        self.mainPanel.SetSizer(self.panel_content_sizer)
        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizerAndFit(self.frame_sizer)

    def OnClose(self, event):
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
