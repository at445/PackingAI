from julesTk import view
from tkinter import *
import io
from PIL import Image
from PIL import ImageTk
from Common.AppConfigSingleton import AppConfigSingleton

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class ValidationView(view.View):
    def __init__(self, parent, controller):
        super(ValidationView, self).__init__(parent, controller)
        self.__appConfig = AppConfigSingleton()
        self.__entryWidgetList = []

    def _prepare(self):
        i = 1
        view.tk.Label(self, font=("黑体", 20), text= "请验证如下附件的版本号").grid(row = i, column = 1, columnspan = 3, sticky = "N")
        for item in self.__appConfig.patchValidationList:
            i += 1
            view.tk.Label(self, font=("黑体", 10), text= item[0], height=3, width=20).grid(row = i, column = 1, sticky = "E")
            entry = view.tk.Entry(self, font=("黑体", 10))
            entry.grid(row = i, column = 2, sticky = "E", pady=15)
            self.add_widget(item[0],entry)
            self.__entryWidgetList.append(entry)
        btn = view.tk.Button(self, font=("黑体", 20), text = "确认", height=3, width=5, command = self.buttonClicked)
        btn.grid(row = 1, rowspan = 5, column = 3, padx = 10)
        self.add_widget("button",btn)

        img = Image.open(self.__appConfig.patchValidationPicture)
        
        self.photo = ImageTk.PhotoImage(img.resize((500,500)))
        view.tk.Label(self,image=self.photo,bg="white").grid(row = 1,rowspan = 60, column = 4, padx = 10,pady = 10)

        self.__entryWidgetList[0].focus_set()
        for entry in self.__entryWidgetList:
            entry.bind("<Return>", self.enterKeyPressEvent)

    def enterKeyPressEvent(self, event):
        self.controller.switchFocus()

    def buttonClicked(self):
        self.controller.checkVersion()
