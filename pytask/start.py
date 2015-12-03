import TaskController
import wx
import sys

if __name__ == '__main__':
    app = wx.App(False)
    class Frame(wx.Frame):
        def __init__(self, title):
            wx.Frame.__init__(self, None, title=title, size=(1,1))
            self.timer = wx.Timer(self) 
            self.Bind(wx.EVT_TIMER, self.OnTimer) 
            self.timer.Start(1, True)
        def OnTimer(self,evt):
            self.Close()
    frame=Frame("Opening Directory Selector")
    frame.Show()
    app.MainLoop()
    path_dlg = wx.DirDialog(None, "Choose working directory", "",
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

    while path_dlg.ShowModal() == wx.ID_CANCEL: # quit if cancelled
        sys.exit()
    
    working_path = path_dlg.GetPath()

    controller = TaskController.TaskController(working_path)
    controller.run()