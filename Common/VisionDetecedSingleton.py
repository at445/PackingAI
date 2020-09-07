import threading
import copy
from julesTk import ThreadSafeObject

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class VisionDetecedSingleton(ThreadSafeObject):
    _instance_lock = threading.Lock()

    def __init__(self):
        super(VisionDetecedSingleton, self).__init__()
        self.__detectedResult = []
        self.__ignoreItem = []
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(VisionDetecedSingleton, "_instance"):
            with VisionDetecedSingleton._instance_lock:
                if not hasattr(VisionDetecedSingleton, "_instance"):
                    VisionDetecedSingleton._instance = object.__new__(cls)  
        return VisionDetecedSingleton._instance

    def getFirstNode(self):
        return self.__detectedResult[0]
    
    @ThreadSafeObject.thread_safe
    def popFromPooling(self):
        if len(self.__detectedResult) is 0:
            return None
        return self.__detectedResult.pop(0)
    
    @ThreadSafeObject.thread_safe
    def pushToPooling(self, result):
        if not isinstance(result,list):
            raise ValueError("Expected a list value, not {}".format(type(result)))
        self.__detectedResult.append(result)

    @ThreadSafeObject.thread_safe
    def clearPooling(self):
        self.__detectedResult.clear()

    @ThreadSafeObject.thread_safe
    def fetchIgnoreContent(self):
        cpy = copy.deepcopy(self.__ignoreItem)
        return cpy

    @ThreadSafeObject.thread_safe
    def setIgnoreContent(self, name):
        if not isinstance(name,str):
            raise ValueError("Expected a string value, not {}".format(type(name)))
        if name in self.__ignoreItem:
            return
        self.__ignoreItem.append(name)
    
    @ThreadSafeObject.thread_safe
    def clearIgnoreContent(self):
        self.__ignoreItem.clear()
