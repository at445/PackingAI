from julesTk import model
import threading
from MODEL.SessionStates import SessionStates, SessionStarted, SessionStoped, SessionError
from Common.AppConfigSingleton import AppConfigSingleton
from Common.Constants import const
from julesTk import ThreadSafeObject
from enum import Enum

class APPSTUS(Enum):
    SESSION_STARTED = 1
    SESSION_STOPED = 2
    SESSION_ERROR = 3

class CheckItemRef():
    def __init__(self, name, color):
        if not isinstance(name, str):
            raise ValueError("Expected a string value, not {}".format(type(name)))
        if not isinstance(color, str):
            raise ValueError("Expected a string value, not {}".format(type(color)))

        self.__name = name
        self.__color = color
    
    @property
    def name(self):
        return self.__name
    
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise ValueError("Expected a int value, not {}".format(type(value)))
        self.__color = value

class StateMachineModel(model.Model, threading.Thread):
    def __init__(self):
        super(StateMachineModel, self).__init__()
        self.daemon = True
        self._lock = threading.RLock()

        self.__fidInputString = "None"
        self.__errorMessage = "None"
        self.__States = APPSTUS.SESSION_STOPED
        self.__itemStatusMap = {}

        self.__stopFlg = False
        self.__appConfigSingleton = AppConfigSingleton()
        self.__sessionStates = SessionStoped()


        for item in self.__appConfigSingleton.sessionContentList:
            self.__itemStatusMap[item[0]] = CheckItemRef(item[0], const.ITEM_RESET_COLOR)

    def changeSessionState(self, obj):
        if isinstance(obj, SessionStarted):
            self.__sessionStates = SessionStarted()
            self.States = APPSTUS.SESSION_STARTED
        elif isinstance(obj, SessionStoped):
            self.__sessionStates = SessionStoped()
            self.States = APPSTUS.SESSION_STOPED
        elif isinstance(obj, SessionError):
            self.__sessionStates = SessionError()
            self.States = APPSTUS.SESSION_ERROR
        else:
            raise ValueError("Expected a subclass SessionStates value, not {}".format(type(obj)))

    def run(self):
        while 1:
            if self.__stopFlg == True:
                print("State Machine model stopped")
                break
            self.__sessionStates.Action(self)
    
    @property
    def itemStatusMap(self):
        return self.__itemStatusMap

    @model.Model.thread_safe
    def setItemStatusByName(self, name, value = const.ITEM_FINISHED_COLOR):
        try:
            self.itemStatusMap[name].color = value

        except KeyError:
            raise ValueError("try to assign one unknow key")


    @model.Model.thread_safe
    def setAllItemStatusFinished(self):
        for key in self.itemStatusMap.keys():
            self.itemStatusMap[key].color = const.ITEM_FINISHED_COLOR

    def isAllItemStatusFinished(self):
        ret = True
        for item in self.itemStatusMap.items():
            if item[1].color is not const.ITEM_FINISHED_COLOR:
                ret = False
                break
        return ret

    @model.Model.thread_safe
    def cleanAllItemStatus(self):
        for key in self.itemStatusMap.keys():
            self.itemStatusMap[key].color = const.ITEM_RESET_COLOR
    
    @property
    def fidInputString(self):
        return self.__fidInputString

    @fidInputString.setter
    @model.Model.thread_safe
    def fidInputString(self,obj):
        if obj is None:
            obj = "None"
        if not isinstance(obj, str):
            raise ValueError("Expected a str value, not {}".format(type(obj)))
        self.__fidInputString = obj
    
    def cleanFidInput(self):
        self.fidInputString = "None"

    def isFidInputAvalible(self):
        return self.fidInputString != "None"


    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    @model.Model.thread_safe
    def errorMessage(self,obj):
        if obj is None:
            obj = "None"
        if not isinstance(obj, str):
            raise ValueError("Expected a str value, not {}".format(type(obj)))
        self.__errorMessage = obj
    
    def cleanErrorMessage(self):
        self.errorMessage = "None"
       
    def isErrorMessageAvalible(self):
        return self.errorMessage != "None"

    @property
    def States(self):
        return self.__States 
    
    @States.setter
    @model.Model.thread_safe
    def States(self, num):
        if not isinstance(num, APPSTUS):
            raise ValueError("Expected a APPSTUS value, not {}".format(type(num)))
        self.__States = num