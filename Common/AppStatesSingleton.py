import threading
from enum import Enum
import copy
from julesTk import ThreadSafeObject
class APPSTUS(Enum):
    SessionNotStart = 1
    SessionProcessing = 2
    SessionEnd = 3
    ApplicationPause = 4

class AppStatesSingleton(ThreadSafeObject):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.__States = APPSTUS.SessionNotStart
        self.__ignoreItem = []
        pass


    def __new__(cls, *args, **kwargs):
        if not hasattr(AppStatesSingleton, "_instance"):
            with AppStatesSingleton._instance_lock:
                if not hasattr(AppStatesSingleton, "_instance"):
                    AppStatesSingleton._instance = object.__new__(cls)  
        return AppStatesSingleton._instance

    
    @property
    def States(self):
        return self.__States 
    
    @States.setter
    @AppStatesSingleton.thread_safe
    def States(self, num):
        if not isinstance(num, APPSTUS):
            raise ValueError("Expected a APPSTUS value, not {}".format(type(num)))
        self.__States = num

    @AppStatesSingleton.thread_safe
    def fetchIgnoreContent(self):
        cpy = copy.deepcopy(self.__ignoreItem)
        return cpy

    @AppStatesSingleton.thread_safe
    def setIgnoreContent(self, name):
        if not isinstance(name,str):
            raise ValueError("Expected a string value, not {}".format(type(name)))
        self.__ignoreItem.append(name)
    
    @AppStatesSingleton.thread_safe
    def clearIgnoreContent(self):
        self.__ignoreItem.clear()
