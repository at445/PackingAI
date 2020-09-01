__author__ = "Chen JinSong <jingsong@foxmail.com>"

class Constants():
    class ConstError(TypeError): pass

    class ConstCaseError(ConstError): pass

    def __setattr__(self, key, value):
        print()
        if key in self.__dict__.keys():
            # 存在性验证
            raise self.ConstError("Can't change a const variable: '%s'" % key)

        if not key.isupper():
            # 语法规范验证
            raise self.ConstCaseError("Const variable must be combined with upper letters:'%s'" % key)

        self.__dict__[key] = value

const = Constants()

const.NOT_START_COLOR = "black"
const.NOT_START_STRING = " 未开始"

const.PROCESSING_COLOR = "green"
const.PROCESSING_STRING = " 检测中..."

const.ERROR_COLOR = "red"
const.ERROR_STRING = " 出错"

const.ITEM_RESET_COLOR = "white"
const.ITEM_FINISHED_COLOR = "green"
const.ITEM_ERROR_COLOR = "red"

const.NOT_FINISHED = 0
const.FINISHED = 1
const.ERROR = 2
const.MULTI_OBJ_ERROR = 3

const.ERROR_TOLERANCE = 3