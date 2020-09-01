import threading
from xml.dom.minidom import parse
import xml.dom.minidom

__author__ = "Chen JinSong <jingsong@foxmail.com>"

class AppConfigSingleton(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(AppConfigSingleton, "_instance"):
            with AppConfigSingleton._instance_lock:
                if not hasattr(AppConfigSingleton, "_instance"):
                    AppConfigSingleton._instance = object.__new__(cls)  
        return AppConfigSingleton._instance

    def __init__(self):
        self.__PatchValidationList = []
        self.__VisionIgnoredListFixed = []
        self.__SessionStartPoint = []
        self.__SessionContent = []
        self.__SessionEndPoint = []

        DOMTree = xml.dom.minidom.parse("AppConfig.xml")
        collection = DOMTree.documentElement

        VALIDATION = collection.getElementsByTagName("PatchValidation")[0]
        content =  VALIDATION.getElementsByTagName("Interval")[0]
        self.__PatchValidationInterval = content.childNodes[0].data
        content =  VALIDATION.getElementsByTagName("Picture")[0]
        self.__PatchValidationPicture = content.childNodes[0].data
        for items in VALIDATION.getElementsByTagName("Item"):
            name = items.getElementsByTagName("Name")[0]
            value = items.getElementsByTagName("Value")[0]
            contet = (name.childNodes[0].data, value.childNodes[0].data)
            self.__PatchValidationList.append(contet)

        DEBUG = collection.getElementsByTagName("Debug")[0]
        self.__debugFlg = DEBUG.childNodes[0].data
        
        CONFIG = collection.getElementsByTagName("YOLO_Config")[0]
        content =  CONFIG.getElementsByTagName("StructureFilePath")[0]
        self.__YoloConfigPath = content.childNodes[0].data
        content =  CONFIG.getElementsByTagName("WeightPath")[0]
        self.__YoloWeightPath = content.childNodes[0].data
        content =  CONFIG.getElementsByTagName("MetaPath")[0]
        self.__YoloMetaPath = content.childNodes[0].data
        
        IGNORE = collection.getElementsByTagName("VisionIgnoreds")[0]
        for item in IGNORE.getElementsByTagName("Name"):
            self.__VisionIgnoredListFixed.append(item.childNodes[0].data)
        
        SESSION = collection.getElementsByTagName("SessionInfo")[0]

        #startInfo = SESSION.getElementsByTagName("StartPoints")[0]
        #for items in startInfo.getElementsByTagName("Item"):
        #    name = items.getElementsByTagName("Name")[0]
        #    countRef = items.getElementsByTagName("CountRef")[0]
        #    contet = (name.childNodes[0].data, countRef.childNodes[0].data)
        #    self.__SessionStartPoint.append(contet)

        detectInfo = SESSION.getElementsByTagName("Detections")[0]
        for items in detectInfo.getElementsByTagName("Item"):
            name = items.getElementsByTagName("Name")[0]
            countRef = items.getElementsByTagName("CountRef")[0]
            contet = (name.childNodes[0].data, countRef.childNodes[0].data)
            self.__SessionContent.append(contet)

        #endInfo = SESSION.getElementsByTagName("EndPoints")[0]
        #for items in endInfo.getElementsByTagName("Item"):
        #    name = items.getElementsByTagName("Name")[0]
        #    countRef = items.getElementsByTagName("CountRef")[0]
        #    contet = (name.childNodes[0].data, countRef.childNodes[0].data)
        #    self.__SessionEndPoint.append(contet)

    @property
    def yoloConfigPath(self):
        return self.__YoloConfigPath

    @property
    def yoloWeightPath(self):
        return self.__YoloWeightPath
    
    @property
    def yoloMetaPath(self):
        return self.__YoloMetaPath
    
    @property
    def sessionStartPointList(self):
        return self.__SessionStartPoint

    @property
    def sessionContentList(self):
        return self.__SessionContent

    @property
    def sessionEndPointList(self):
        return self.__SessionEndPoint

    @property
    def visionIgnoredListFixed(self):
        return self.__VisionIgnoredListFixed
    
    @property
    def debugFlg(self):
        return self.__debugFlg

    @property
    def patchValidationInterval(self):
        return self.__PatchValidationInterval

    @property
    def patchValidationPicture(self):
        return self.__PatchValidationPicture

    @property
    def patchValidationList(self):
        return self.__PatchValidationList
