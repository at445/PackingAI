from julesTk import controller
from tkinter.messagebox import showerror
from VIEW.ProcessingView import ProcessingView
from VIEW.ValidationView import ValidationView
from Common.AppConfigSingleton import AppConfigSingleton
from julesTk.utils import modals

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class MainController(controller.ViewController):
    
    def __init__(self, parent, view=None):
        super(MainController, self).__init__(parent=parent)
        self.__appConfig = AppConfigSingleton()
        self.__pView = ProcessingView(self.parent_view, self)
        self.__vView = ValidationView(self.parent_view, self)
        self.set_view(self.__vView)
    
    def switchToValidationView(self):
        self.view.hide()
        self.set_view(self.__vView)
        self.view.show()

    def switchToProcessingView(self):
        self.view.hide()
        self.set_view(self.__pView)
        self.view.show()
    
    def switchFocus(self):
        focusedItem = self.view.focus_get()
        focusFud = False
        for item in self.view.widgets.values():
            if focusFud is True:
                item.focus_set()
                break
            if item  is focusedItem:
                focusFud = True
    def checkVersion(self):
        errFlg = False
        for refPair in self.__appConfig.patchValidationList:
            widget = self.view.get_widget(refPair[0])
            if widget.get() != refPair[1]:
                showerror("错误", "验证失败，请重新验证")
                errFlg = True
                break
        firstEntry = True
        for refPair in self.__appConfig.patchValidationList:
            widget = self.view.get_widget(refPair[0])
            if firstEntry is True:
                widget.focus_set()
            widget.delete(0, 'end')
            firstEntry = False
        if errFlg is False:
            self.switchToProcessingView()
            