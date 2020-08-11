from julesTk import controller
from VIEW.ProcessingView import ProcessingView
from VIEW.ValidationView import ValidationView

__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class MainController(controller.ViewController):
    
    def __init__(self, parent, view=None):
        super(MainController, self).__init__(parent=parent)
        self.__pView = ProcessingView(self.parent_view, self)
        self.__vView = ValidationView(self.parent_view, self)
        self.set_view(self.__vView)
    
    def ProcessingClick(self):
        self.view.hide()
        self.set_view(self.__vView)
        self.view.show()

    def ValidationClick(self):
        self.view.hide()
        self.set_view(self.__pView)
        self.view.show()