import threading
import time
from Common.AppConfigSingleton import AppConfigSingleton
from Common.Constants import const
from MODEL.NumberCounterHelper import NumberCounterHelper

class SessionStates():
    def ___init__(self):
        pass

    def Action(self):
        raise NotImplementedError

    def TransAction(self):
        raise NotImplementedError

class SessionStarted(SessionStates):
    
    _instance_lock = threading.Lock()

    def __init__(self):
        super(SessionStarted, self).__init__()
        self.__adjuster = NumberCounterHelper()
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SessionStarted, "_instance"):
            with SessionStarted._instance_lock:
                if not hasattr(SessionStarted, "_instance"):
                    SessionStarted._instance = object.__new__(cls)  
        return SessionStarted._instance
    
    def Action(self, obj):
        from MODEL.StateMachineModel import StateMachineModel
        if not isinstance(obj, StateMachineModel):
            raise ValueError("Expected a StateMachineModel value, not {}".format(type(obj)))
        self.__adjuster.reset()
        while 1:
            if obj.isAllItemStatusFinished() is True:
                self.__adjuster.reset()
                break
            for item in self.__adjuster.caculate():
                if item.Flag == const.FINISHED:
                    obj.setItemStatusByName(item.name)
                    obj.notify_observers()
                if item.Flag == const.MULTI_OBJ_ERROR:
                    obj.setItemStatusByName(item.name, const.ITEM_ERROR_COLOR)
                    obj.errorMessage = "检测到多个" +  item.name
                    obj.changeSessionState(SessionError())
                    obj.notify_observers()
                    return
        obj.cleanAllItemStatus()
        obj.changeSessionState(SessionStoped())
        obj.notify_observers()

class SessionStoped(SessionStates):
    _instance_lock = threading.Lock()

    def __init__(self):
        super(SessionStoped, self).__init__()
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SessionStoped, "_instance"):
            with SessionStoped._instance_lock:
                if not hasattr(SessionStoped, "_instance"):
                    SessionStoped._instance = object.__new__(cls)  
        return SessionStoped._instance

    def Action(self, obj):
        from MODEL.StateMachineModel import StateMachineModel
        if not isinstance(obj, StateMachineModel):
            raise ValueError("Expected a StateMachineModel value, not {}".format(type(obj)))

        while (obj.isFidInputAvalible() == False):
            time.sleep(0.2)
        
        print("do sncheck with FID {}".format(obj.fidInputString))
        #snCheck with obj.fidInputString
            # TBD --- 
            # -------
            # -------
        #ret = snCheck(obj.fidInputString)
        print("success!!")
        ret = True
        if ret is True:
            #send "SIT+Fid" to BCR
            # TBD --- 
            # -------
            # -------
            #bRet = sendToBCR("SIT+Fid")
            bRet = True
            if bRet is False:
                obj.errorMessage = "发送 “SIT+FID” 失败 FID：" +  obj.fidInputString
                obj.changeSessionState(SessionError())
                obj.notify_observers()
            else:
                obj.changeSessionState(SessionStarted())
                obj.notify_observers()
        else:
            obj.errorMessage = "snCheck 失败 FID：" +  obj.fidInputString
            obj.changeSessionState(SessionError())
            obj.notify_observers()

        obj.cleanFidInput()

class SessionError(SessionStates):
    _instance_lock = threading.Lock()

    def __init__(self):
        super(SessionError, self).__init__()
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SessionError, "_instance"):
            with SessionError._instance_lock:
                if not hasattr(SessionError, "_instance"):
                    SessionError._instance = object.__new__(cls)  
        return SessionError._instance

    def Action(self, obj):
        from MODEL.StateMachineModel import StateMachineModel
        if not isinstance(obj, StateMachineModel):
            raise ValueError("Expected a StateMachineModel value, not {}".format(type(obj)))
        while (obj.isErrorMessageAvalible() == True):
            time.sleep(0.2)
        obj.cleanAllItemStatus()
        obj.changeSessionState(SessionStoped())
        obj.notify_observers()

