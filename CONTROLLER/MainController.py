from julesTk import controller
from julesTk.utils.observe import Observer
from julesTk.utils import modals
from tkinter.messagebox import showerror
from Common.AppConfigSingleton import AppConfigSingleton
from Common.Constants import const
from VIEW.ProcessingView import ProcessingView
from VIEW.ValidationView import ValidationView

from MODEL.VisionDetectionModel import VisionDetectionModel
from MODEL.StateMachineModel import StateMachineModel, APPSTUS

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class MainController(controller.Controller, Observer):
    
    def __init__(self, parent, view=None, model=None):
        super(MainController, self).__init__(parent=parent)
        self.__circleTime = 0
        self.__appConfig = AppConfigSingleton()
        self.__pView = ProcessingView(self.parent_view, self)
        self.__vView = ValidationView(self.parent_view, self)
        self.set_view(self.__vView)
        self.__vModel = VisionDetectionModel()
        self.__vModel.register_observer(self)

        self.__sModel = StateMachineModel()
        self.__sModel.register_observer(self)
    
    def update(self, observable):
        
        if isinstance(observable, VisionDetectionModel) and isinstance(self.view, ProcessingView):
            imgRaw = observable.fetchDetectedPicture()
            self.view.widgets["picLable"].config(image=imgRaw)
            self.view.widgets["picLable"].image = imgRaw
        if isinstance(observable, StateMachineModel) and isinstance(self.view, ProcessingView):
            for item in observable.itemStatusMap.values():
                self.view.changeCheckItemBg(item.name, item.color)
            if observable.States is APPSTUS.SESSION_ERROR:
                self.__vModel.pauseFlg = True
                self.view.disableManualSetButton()
                self.view.widgets["statusLabel"].config(fg=const.ERROR_COLOR)
                self.view.widgets["statusLabel"].config(text=const.ERROR_STRING)
                showerror("错误", "详细信息" + observable.errorMessage)
                observable.cleanErrorMessage()
            elif observable.States is APPSTUS.SESSION_STOPED:
                self.__vModel.pauseFlg = True
                self.view.disableManualSetButton()
                self.view.widgets["statusLabel"].config(fg=const.NOT_START_COLOR)
                self.view.widgets["statusLabel"].config(text=const.NOT_START_STRING)
                #self.view.changeCheckItemBg("CD", const.ITEM_FINISHED_COLOR)
            elif observable.States is APPSTUS.SESSION_PROCESSING:
                self.__vModel.pauseFlg = False
                self.view.enableManualSetButton()
                self.view.widgets["statusLabel"].config(fg=const.PROCESSING_COLOR)
                self.view.widgets["statusLabel"].config(text=const.PROCESSING_STRING)
            elif observable.States is APPSTUS.SESSION_FINISHED:
                self.__vModel.pauseFlg = True
                self.__circleTime += 1
                if self.__circleTime % int(self.__appConfig.patchValidationInterval) == 0:
                    self.switchToValidationView()

    def switchToValidationView(self):
        self.view.hide()
        self.set_view(self.__vView)
        self.view.show()

    def switchToProcessingView(self):
        self.view.hide()
        self.set_view(self.__pView)
        self.view.show()
    
    def switchFocus(self, obj):
        if not isinstance(obj, ValidationView):
            raise ValueError("switch focus on view which is not ValidationView")
        focusedItem = self.view.focus_get()
        focusFud = False
        for item in self.view.widgets.values():
            if focusFud is True:
                item.focus_set()
                break
            if item  is focusedItem:
                focusFud = True
    def checkVersion(self, obj):
        if not isinstance(obj, ValidationView):
            raise ValueError("check version on view which is not ValidationView")
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
    
    def manualSetPass(self, obj):
        if not isinstance(obj, ProcessingView):
            raise ValueError("dealing fid input on view which is not ProcessingView")
        self.__sModel.setAllItemStatusFinished()
    
    def fidInputHandling(self, obj, content):
        if not isinstance(obj, ProcessingView):
            raise ValueError("dealing fid input on view which is not ProcessingView")
        self.__sModel.fidInputString = content
        widget = self.view.get_widget("fidEntry")
        widget.focus_set()
        widget.delete(0, 'end')

    def _stop(self):
        self.__vModel.stopFlg = True
        self.__vModel.join(0.5)
        self.__sModel.stopFlg = True
        self.__sModel.join(0.5)

    def _start(self):
        self.__vModel.start()
        self.__sModel.start()
        super(MainController, self)._start()
