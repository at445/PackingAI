from Common.Constants import const
from Common.AppConfigSingleton import AppConfigSingleton
from Common.VisionDetecedSingleton import VisionDetecedSingleton
import time
__author__ = "Chen JinSong <jingsong@foxmail.com>"

class ItemControlRef():
    def __init__(self, name, maxCnt):
        if not isinstance(name, str):
            raise ValueError("Expected a string value, not {}".format(type(name)))
        if not isinstance(maxCnt, int):
            raise ValueError("Expected a int value, not {}".format(type(maxCnt)))

        self.__name = name
        self.__maxCnt = maxCnt
        self.__rtCnt = 0
        self.__accumuCnt = 0
        self.__Flg = const.NOT_FINISHED
        self.__errorCnt = 0
    
    @property
    def name(self):
        return self.__name
    
    @property
    def maxCount(self):
        return self.__maxCnt

    @property
    def errCnt(self):
        return self.__errorCnt
    
    @errCnt.setter
    def errCnt(self, num):
        if not isinstance(num, int):
            raise ValueError("Expected a int value, not {}".format(type(num)))
        
        self.__errorCnt = num
    
    @property
    def realtimeCnt(self):
        return self.__rtCnt
    
    @realtimeCnt.setter
    def realtimeCnt(self, num):
        if not isinstance(num, int):
            raise ValueError("Expected a int value, not {}".format(type(num)))
        
        self.__rtCnt = num
    
    @property
    def accumulativeCnt(self):
        return self.__accumuCnt
    
    @accumulativeCnt.setter
    def accumulativeCnt(self, num):
        if not isinstance(num, int):
            raise ValueError("Expected a int value, not {}".format(type(num)))
        
        self.__accumuCnt = num

    @property
    def Flag(self):
        return self.__Flg
    
    @Flag.setter
    def Flag(self, flg):
        if not isinstance(flg, int):
            raise ValueError("Expected a int value, not {}".format(type(flg)))
        
        self.__Flg = flg
    

class NumberCounterHelper():
    def __init__(self):
        self.__appConfigSingleton = AppConfigSingleton()
        self.__visDetctRstSingleton = VisionDetecedSingleton()
        self.__ItemControlRefList = []

        for info in self.__appConfigSingleton.sessionContentList:
            self.__ItemControlRefList.append(ItemControlRef(info[0], int(info[1])))

    def caculate(self):
        StopFlg = False
        while 1:
            if StopFlg is True:
                break

            temp = self.__visDetctRstSingleton.popFromPooling()
            if temp is None:
                time.sleep(0.03)
                break
            
            for item1 in temp:
                for item2 in self.__ItemControlRefList:
                    if item1[0].decode() == item2.name:
                        item2.realtimeCnt += 1
            
            #multi-object appeared at one time, this will be an error
            for item in self.__ItemControlRefList:
                if item.realtimeCnt > 1:
                    item.errCnt += 1
                    item.realtimeCnt = 0
                    continue
                item.accumulativeCnt += item.realtimeCnt
                item.realtimeCnt = 0

            for item in self.__ItemControlRefList:
                if item.Flag == const.NOT_FINISHED:
                    if item.accumulativeCnt >= item.maxCount:
                        item.Flag = const.FINISHED
                if item.errCnt >= const.ERROR_TOLERANCE:
                    item.Flag = const.MULTI_OBJ_ERROR
                    StopFlg = True
                    break
        return self.__ItemControlRefList

    def reset(self):
        for info in self.__ItemControlRefList:
            info.realtimeCnt = 0
            info.Flag = const.NOT_FINISHED
            info.accumulativeCnt = 0
            info.errCnt = 0
            self.__visDetctRstSingleton.clearPooling()
