
from enum import Enum
from common.commonGlobals import errorCodeInputData, ERR_EMPTY_MESSAGE, color, APPROVAL_ICON, DIS_APPROVAL_ICON

class excelInputField(Enum):
    A = "err_index"
    M = "err_code"
    H = "who"
    I = "where"
    J = "which"
    K = "what"
    L = "user_visible"
    E = "desc_eng"
    F = "desc_cn"
    C = "err_name"
    Q = "err_message_eng"
    R = "err_message_cn"
    P = "producer"
    AA = "phase"
    G = "create_by"
    #BA - BC not use
    BA = "approval"
    BB = "approval_by"
    BC = "EXCEL"


class errorCode:
    # The init method or constructor
    def __init__(self, errorFromJson, isExcel, count=1):
        print("init- errorCode")
        self.item = {}
        self.isEmpty = False
        self.intError = False

        if not errorFromJson is None:
            for data in errorCodeInputData:
                if data.value.MULTI_LANG.value is None:
                    excelV = self.loadData(errorFromJson, isExcel, data.value.FIELD.value)
                    self.item[data.value.FIELD.value] = excelV if excelV else ""
                else:
                    arrayList = {}
                    for lang in data.value.MULTI_LANG.value:
                        langV = self.loadSubData(errorFromJson, isExcel, data.value.FIELD.value, lang.value)
                        arrayList.update({lang.value:langV if langV else ""})
                    self.item[data.value.FIELD.value] = arrayList
            #self.setErrData(errorCodeInputData.ERR_INDEX.value.FIELD.value, count) if isExcel else ""
            self.checking()

    def loadData(self, errorFromJson, isExcel, field):
        if isExcel:
            return errorFromJson.get(excelInputField(field).name)
        else:
            return errorFromJson.get(field)

    def loadSubData(self, errorFromJson, isExcel, field, subField):
        if isExcel:
            return self.loadData(errorFromJson, isExcel, field+"_"+subField)
        else:
            return errorFromJson.get(field).get(subField)

    def checking(self):
        print("checking")
        self.isEmpty = False
        self.intError = False
        checkMessage = ""
        for i in errorCodeInputData:
            if i.value.REQUEST.value:
                if i.value.MULTI_LANG.value is None:
                    if not self.getErrData(i.value.FIELD.value):
                        checkMessage = checkMessage + (ERR_EMPTY_MESSAGE % i.value.LABEL.value)
                        self.isEmpty = True
                else:
                    for lang in i.value.MULTI_LANG.value:
                        if not self.getErrSubData(i.value.FIELD.value, lang.value):
                            checkMessage = checkMessage + (ERR_EMPTY_MESSAGE % (i.value.LABEL.value+"("+lang.value+")"))
                            self.isEmpty = True

            if self.checkDataType(self.getErrData(i.value.FIELD.value), i.value.DATA_TYPE.value):
                self.intError = True

        return checkMessage

    def checkDataType(self, key, dataType):
        try:
            if dataType ==1:
                int(value)
                return False
        except ValueError:
            return True

    def haveProblem(self):
        return self.isEmpty or self.intError

    def setErrData(self, field, value):
        self.item[field] = value

    def getErrData(self, field):
        return str(self.item.get(field)) if not self.item.get(field) is None else ""

    def getErrSubData(self, listName, field):
        return str(self.item.get(listName).get(field)) if not self.item.get(listName) is None else ""

    def setErrSubData(self, listName, field, value):
        if listName in self.item:
            self.item[listName].update({field:value})
        else:
            self.item.update({listName: {field:value}})

    def getErrorCode(self):
        who = self.item.get(errorCodeInputData.ERR_WHO.value.FIELD.value) if not self.item.get(errorCodeInputData.ERR_WHO.value.FIELD.value) is None else -1
        where = self.item.get(errorCodeInputData.ERR_WHERE.value.FIELD.value) if not self.item.get(errorCodeInputData.ERR_WHERE.value.FIELD.value) is None else -1
        which = self.item.get(errorCodeInputData.ERR_WHICH.value.FIELD.value) if not self.item.get(errorCodeInputData.ERR_WHICH.value.FIELD.value) is None else -1
        what = self.item.get(errorCodeInputData.ERR_WHAT.value.FIELD.value) if not self.item.get(errorCodeInputData.ERR_WHAT.value.FIELD.value) is None else -1
        userVisible = self.item.get(errorCodeInputData.ERR_USER_VISIBLE.value.FIELD.value) if not self.item.get(errorCodeInputData.ERR_USER_VISIBLE.value.FIELD.value) is None else -1

        return self.padhexa(hex(int(who) + int(where)*8 + int(which)*256 + int(what)*65536 + int(userVisible)*65536 * 32768))

    def padhexa(self, hex):
        return '0x' + hex[2:].zfill(8)

    def getColor(self):
        colorValue = color.CYAN.value
        if self.intError:
            colorValue = color.RED.value
        if self.isEmpty:
            colorValue = color.ORANGE.value
        return colorValue
    
    def getIcon(self):
        return APPROVAL_ICON if self.item.get(errorCodeInputData.ERR_APPROVAL.value.FIELD.value) else DIS_APPROVAL_ICON

        