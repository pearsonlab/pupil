import TaskController
import wx

if __name__ == '__main__':
    path_dlg = wx.DirDialog(None, "Choose working directory", "",
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

    while path_dlg.ShowModal() == wx.ID_CANCEL: # keep prompting for path until given
        path_dlg.SetMessage("You must choose a directory to continue")

    working_path = path_dlg.GetPath()

    controller = TaskController.TaskController(working_path)
    controller.run()