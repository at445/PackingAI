from julesTk import view
from tkinter import *
from cv2 import cv2

from Common.AppConfigSingleton import AppConfigSingleton

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class ProcessingView(view.View):

    def __init__(self, parent, controller):
        super(ProcessingView, self).__init__(parent, controller)
        self.__appConfig = AppConfigSingleton()

    def _prepare(self):
        paneWinTop = view.tk.PanedWindow(self, sashrelief=RIDGE, bg="white")
        paneWinTop.pack(fill = BOTH,expand = 1)

        mLeft = view.tk.PanedWindow(self, orient=VERTICAL, sashrelief=RAISED ,bg="white")
        paneWinTop.add(mLeft)

        picLable = view.tk.Label(mLeft,bg="white")
        mLeft.add(picLable, height=500, width=800)
        self.add_widget("picLable", picLable)

        statusLabel = view.tk.Label(mLeft,bg="white")
        statusLabel["text"] = "helloworld"
        mLeft.add(statusLabel, height=25, sticky = 'SW')
        self.add_widget("statusLabel", statusLabel)

        mRight = view.tk.PanedWindow(self, orient=VERTICAL, sashrelief=SOLID , bg="white")
        mRight.pack(fill=BOTH, expand=1)
        paneWinTop.add(mRight)

        for item in self.__appConfig.sessionContentList:
            TxtpLabel = view.tk.Label(mRight, bg="white")
            TxtpLabel["text"] = item[0]
            mRight.add(TxtpLabel, height=50, width=200, sticky = 'N')
            self.add_widget(item[0]+"Lable", TxtpLabel)
            
        # dummy, just for better appearance
        TxtpLabel = view.tk.Label(mRight, bg="white")
        mRight.add(TxtpLabel, height=50, width=200, sticky = 'N')
