import TaskController
import wx
import sys

if __name__ == '__main__':
    path_dlg = wx.DirDialog(None, "Choose working directory", "",
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

    while path_dlg.ShowModal() == wx.ID_CANCEL: # quit if cancelled
        sys.exit()

    working_path = path_dlg.GetPath()

    controller = TaskController.TaskController(working_path)
    controller.run()