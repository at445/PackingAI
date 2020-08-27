import threading
from julesTk import ThreadSafeObject

class VisionDetecedResultSingleton(ThreadSafeObject):
    _instance_lock = threading.Lock()

    def __init__(self):
        super(VisionDetecedResultSingleton, self).__init__()
        self.__detectedResult = []
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(VisionDetecedResultSingleton, "_instance"):
            with VisionDetecedResultSingleton._instance_lock:
                if not hasattr(VisionDetecedResultSingleton, "_instance"):
                    VisionDetecedResultSingleton._instance = object.__new__(cls)  
        return VisionDetecedResultSingleton._instance

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

