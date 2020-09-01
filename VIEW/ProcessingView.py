from julesTk import view
from tkinter import *
from cv2 import cv2

from Common.AppConfigSingleton import AppConfigSingleton
from Common.Constants import const

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class ProcessingView(view.View):

    def __init__(self, parent, controller):
        super(ProcessingView, self).__init__(parent, controller)
        self.__appConfig = AppConfigSingleton()
        self.__checkItemColorBuf = {}

    def _prepare(self):
        paneWinTop = view.tk.PanedWindow(self, sashrelief=RIDGE, bg="white")
        paneWinTop.pack(fill = BOTH,expand = 1)

        mLeft = view.tk.PanedWindow(self, orient=VERTICAL, sashrelief=RIDGE ,bg="white")
        paneWinTop.add(mLeft)

        picLable = view.tk.Label(mLeft,bg="white")
        mLeft.add(picLable, height=500, width=800)
        self.add_widget("picLable", picLable)

        statusLabel = view.tk.Label(mLeft,font=("黑体", 15), bg="white")
        statusLabel["text"] = "未开始"
        mLeft.add(statusLabel, height=25, sticky = 'SW')
        self.add_widget("statusLabel", statusLabel)

        mRight = view.tk.PanedWindow(self, orient=VERTICAL, bg="white")
        paneWinTop.pack(fill = Y,expand = 1)
        mRightUp = view.tk.PanedWindow(self, orient=VERTICAL, height=500, sashrelief=SOLID , bg="white")
        mRightDown = view.tk.PanedWindow(self, orient=HORIZONTAL, bg="white")
        mRight.add(mRightUp)
        mRight.add(mRightDown)
        paneWinTop.add(mRight)

        for item in self.__appConfig.sessionContentList:
            TxtpLabel = view.tk.Label(mRightUp, bg=const.ITEM_RESET_COLOR)
            TxtpLabel["text"] = item[0]
            mRightUp.add(TxtpLabel, height=40, width=250, sticky = 'WE')
            self.add_widget(item[0], TxtpLabel)
            self.__checkItemColorBuf[item[0]] = const.ITEM_RESET_COLOR
        btn = view.tk.Button(mRightUp, font=("黑体", 10), text = "手动确认",command = self.buttonClicked)
        mRightUp.add(btn,height=50, width=150, sticky = 'S')
        btn.pack_forget()
        self.add_widget("manualButton",btn)

        TxtpLabel = view.tk.Label(mRightDown, text="请输入产品FID：", bg="white", anchor="sw")
        mRightDown.add(TxtpLabel)
        inputEntry = view.tk.Entry(mRightDown,show=None)
        inputEntry.focus_set()
        mRightDown.add(inputEntry, width=150, sticky = 'S')
        inputEntry.bind("<Return>", self.enterKeyPressEvent)
        self.add_widget("fidEntry",inputEntry)

    def enterKeyPressEvent(self, event):
         self.controller.fidInputHandling(self,self.widgets["fidEntry"].get())

    def buttonClicked(self):
        self.controller.checkVersion()

    def changeCheckItemBg(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Expected a subclass string value, not {}".format(type(value)))
        if not isinstance(key, str):
            raise ValueError("Expected a subclass string value, not {}".format(type(value)))
        if not self.has_widget(key):
            raise ValueError("Cannot find {} in current view".format(key))
        if self.__checkItemColorBuf[key] == value:
            return
        self.widgets[key]["bg"] = value
        self.__checkItemColorBuf[key] = value