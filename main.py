from pathlib import Path
import wx
import taglib


class Eraser(wx.Frame):
    def __init__(self, *args, **kw):
        super(Eraser, self).__init__(*args, **kw)
        self.InitUI()
        self.btnFilePath.Bind(wx.EVT_BUTTON, self.ReadFile)

    def ReadFile(self, event):
        with wx.FileDialog(self, wildcard="All (*.wav, *.mp3, *.flac)|*.wav;*.mp3;*.flac|WAV files (*.wav)|*.wav|MP3 files (*.mp3)|*.mp3|FLAC files (*.flac)|*.flac") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
        # Proceed loading the file chosen by the user
        pathname = fileDialog.GetPath()
        with taglib.File(pathname, save_on_exit=False) as file:
            self.title.SetLabel(file.tags['TITLE'][0])

    def InitUI(self):
        self.pnl = wx.Panel(self)
        # rows, columns, vgap, hgap
        self.gs = wx.GridSizer(4, 4, 5, 5)
        self.btnFilePath = wx.Button(self.pnl, wx.ID_ANY, "Get file")
        self.gs.Add(self.btnFilePath, 0, wx.EXPAND)
        self.title = wx.StaticText(self.pnl, label="Something")
        self.gs.Add(self.title, 1, wx.EXPAND)
        self.pnl.SetSizer(self.gs)
        # for i in range(1,17):
        #  btn = "Btn"+str(i)
        # gs.Add(wx.Button(pnl,label = btn),0,wx.EXPAND)
        # pnl.SetSizer(gs)


def main():
    app = wx.App()
    frm = Eraser(None, title="Eraser")
    frm.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
