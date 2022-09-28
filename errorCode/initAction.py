#
#  Copyright (C) 2021 Xcalibyte (Shenzhen) Limited.
#

import json
import os, sys
from datetime import datetime
from errorCode import errorCode
from common.commonGlobals import OUTPUT_FILE_JSON, color, errorCodeInputData, FILE_DB_JSON, ERR_FILE_DB_JSON_NOT_EXIST, \
    SHAREPOINT_SITE, SHAREPOINT_WEB_SITE, SHAREPOINT_FOLDER
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from shareplum.errors import ShareplumRequestError

mydata = {}

class initAction(object):
    def __init__(self):
        pass

    def createQListWidgetItem(excelErrCode):
        qListWidgetItem = QListWidgetItem(str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)))
        qListWidgetItem.setBackground(QColor(excelErrCode.getColor()))
        qListWidgetItem.setIcon(QtGui.QIcon(os.getcwd()+"/"+excelErrCode.getIcon()))
        return qListWidgetItem

    def text_search(listView, text):
        print("text_search")
        listView.clear()
        if len(text) == 0:
            for index in mydata:
                excelErrCode = mydata[index]
                #qListWidgetItem = QListWidgetItem(str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)))
                #qListWidgetItem.setBackground(QColor(excelErrCode.getColor()))
                listView.addItem(initAction.createQListWidgetItem(excelErrCode))
                #listView.addItem(qListWidgetItem)
        else:
            for index in mydata:
                excelErrCode = mydata[index]
                if text in excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value):
                    listView.addItem(initAction.createQListWidgetItem(excelErrCode))

        if not text is None and text in mydata:
            excelErrCode = mydata[text]
            listView.addItem(initAction.createQListWidgetItem(excelErrCode))
        listView.update()

    def text_change(listView, field, subField=None, comboBox=None, text=None):
        if listView.currentRow() > -1:
            item = mydata[listView.currentItem().text()]
            value = ""
            if not comboBox is None:
                list_of_key = list(comboBox.keys())
                list_of_value = list(comboBox.values())
                position = list_of_value.index(text)
                value = list_of_key[position]
                item.setErrData(field, value)

            else:
                item.setErrData(field, text) if subField is None else item.setErrSubData(field, subField, text)

            mydata[item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)] = item
            listView.currentItem().setText(item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value))
            listView.update()

    def onClickedApproval(self, MainWindow, approvalBool, userName):
        if self.listView.currentRow() > -1:
            item = mydata[self.listView.currentItem().text()]
            item.setErrData(errorCodeInputData.ERR_APPROVAL.value.FIELD.value, approvalBool)
            item.setErrData(errorCodeInputData.ERR_APPROVAL_BY.value.FIELD.value, userName)
            mydata[item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)] = item
            self.listView.currentItem().setIcon(QtGui.QIcon(item.getIcon()))
            self.showView(item)

    def selectListView(listView):
        print("selectListView")
        return mydata[listView.currentItem().text()]

    @staticmethod
    def lenMyData():
        return len(mydata)+2

    def addToList(self, userName):
        print("addToList")
        listView = self.listView

        excelErrCode = errorCode(None, False)

        excelErrCode.setErrData(errorCodeInputData.ERR_WHAT.value.FIELD.value, initAction.lenMyData()+1)
        excelErrCode.setErrData(errorCodeInputData.ERR_CREATE.value.FIELD.value, userName)
        mydata["New"] = excelErrCode
        qListWidgetItem = initAction.createQListWidgetItem(excelErrCode)
        qListWidgetItem.setText("New")
        listView.addItem(qListWidgetItem)
        #qListWidgetItem = QListWidgetItem("New")
        #listView
        #qListWidgetItem.setBackground(QColor(excelErrCode.getColor()))
        #listView.addItem(qListWidgetItem)

    def saveAction(self):
        print("saveAction")

        listView = self.listView

        if listView.currentRow() < 0:
            return

        item = mydata[listView.currentItem().text()]
        if item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value) is None or item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value) == "":
            item.setErrData(errorCodeInputData.ERR_CODE.value.FIELD.value, item.getErrorCode())
        checkMessage = item.checking()

        self.popMessage(checkMessage, QMessageBox.Critical) if checkMessage else ""

        del mydata[listView.currentItem().text()] #remove old
        mydata[str(item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value))] = item #add new

        listView.item(listView.currentRow()).setText(str(item.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)))
        listView.item(listView.currentRow()).setBackground(QColor(item.getColor()))
        listView.update()


    def deleteAction(self):
        print("deleteAction")
        listView = self.listView

        del mydata[listView.currentItem().text()]
        listView.model().removeRow(listView.currentRow())
        listView.update()

    def loadExcelJson(listView):
        print("loadExcelJson")

        mydata.clear()
        listView.clear()

        input_file = open ("/home/user/csvjson.json")
        jsonFile = json.load(input_file)

        for item in jsonFile:
            excelErrCode = errorCode(item, True)
            excelErrCode.setErrData("approval_by", "Old Excel Recode")
            excelErrCode.setErrData("approval", True)
            qListWidgetItem = initAction.createQListWidgetItem(excelErrCode)#QListWidgetItem(str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)))

            if str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)) in mydata:
                qListWidgetItem.setBackground(QColor(color.GARY.value))
            listView.addItem(qListWidgetItem)
            #listView.update()
            mydata[str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value))] = excelErrCode

    def loadJson(listView):
        print("loadJson")
        mydata.clear()
        listView.clear()
        exedir = os.getcwd()
        input_file = open (exedir+"/.tmp_"+FILE_DB_JSON)
        jsonFile = json.load(input_file)

        for item in jsonFile:
            excelErrCode = errorCode(item, False)
            qListWidgetItem = initAction.createQListWidgetItem(excelErrCode)
            #qListWidgetItem = QListWidgetItem(str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)))

            #qListWidgetItem.setBackground(QColor(excelErrCode.getColor()))
            if str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)) in mydata:
                qListWidgetItem.setBackground(QColor(color.GARY.value))
            #qListWidgetItem.setIcon(QtGui.QIcon(exedir+"/approval.jpg"))

            listView.addItem(qListWidgetItem)
            mydata[str(excelErrCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value))] = excelErrCode
        listView.update()

    def outputJson(self, initAction, userName, password):
        initAction.outputFileDB(self, initAction, userName, password)
        initAction.outputFileForXcal(self, initAction, userName, password)

        self.popMessage("Save success! \n (%s)" % ("asdas"), QMessageBox.Information)

    def putToSharepoint(self, file, userName, password, outPutFileName):
        print("putToSharepoint")
        authcookie = Office365(SHAREPOINT_WEB_SITE, username=userName, password=password).GetCookies()
        site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=authcookie)
        folder = site.Folder(SHAREPOINT_FOLDER)

        with open(file, mode='rb') as file:
            fileContent = file.read()
        folder.upload_file(fileContent, outPutFileName)

    def outputFileDB(self, initAction, userName, password):
        print("outputFileDB")
        exedir = os.getcwd()
        filename = exedir+"/"+FILE_DB_JSON
        toJsonData = []
        for index in mydata:
            errCode = mydata[index]
            item = {}
            for i in errorCodeInputData:
                if not i.value.MULTI_LANG.value is None:
                    arrayList = {}
                    for lang in i.value.MULTI_LANG.value:
                        langV = errCode.getErrSubData(i.value.FIELD.value, lang.value)
                        arrayList.update({lang.value:langV if langV else ""})

                    item[i.value.FIELD.value] = arrayList
                else:
                    item[i.value.FIELD.value] = errCode.getErrData(i.value.FIELD.value)

            toJsonData.append(item)
        with open(filename, 'w') as outfile:
            json.dump(toJsonData, outfile, indent=1, ensure_ascii=False)
        initAction.putToSharepoint(self, filename, userName, password, FILE_DB_JSON)

    def outputFileForXcal(self, initAction, userName, password):
        print("outputFileForXcal")
        exedir = os.getcwd()
        filename = exedir+"/"+OUTPUT_FILE_JSON
        toJsonData = {}
        toJsonData["status"] = "success"

        now = datetime.now() # current date and time
        version  = now.strftime("%Y%m%d%I%p")
        toJsonData["version"] = version

        errors = {}
        for index in mydata:
            errCode = mydata[index]
            if errCode.getErrData(errorCodeInputData.ERR_APPROVAL.value.FIELD.value)=="True":
                err_message = {}
                errInfo = {}
                err_message["en"] = errCode.getErrSubData(errorCodeInputData.ERR_MESSAGE.value.FIELD.value, "eng") if not errCode.getErrSubData(errorCodeInputData.ERR_MESSAGE.value.FIELD.value, "eng") is None else ""
                err_message["cn"] = errCode.getErrSubData(errorCodeInputData.ERR_MESSAGE.value.FIELD.value, "cn") if not errCode.getErrSubData(errorCodeInputData.ERR_MESSAGE.value.FIELD.value, "cn") is None else ""
                errInfo["err_message"] = err_message
                errInfo["err_code"] = errCode.getErrData(errorCodeInputData.ERR_CODE.value.FIELD.value)

                errors[errCode.getErrData(errorCodeInputData.ERR_NAME.value.FIELD.value)] = errInfo
        toJsonData["errors"] = errors
        with open(filename, 'w') as outfile:
            json.dump(toJsonData, outfile, indent=1, ensure_ascii=False)

        initAction.putToSharepoint(self, filename, userName, password, OUTPUT_FILE_JSON)

    def health_check(self, userName, password):
        initAction.getSharepointFileDB(self, userName, password)

    def loginSharepoint(self, username, password):
        print("loginSharepoint")
        try:
            Office365(SHAREPOINT_WEB_SITE, username=username, password=password).GetCookies()
        except Exception as e:
            self.popMessage(e.args[0], QMessageBox.Critical)
            return False
        return True

    def getSharepointFileDB(self, userName, password):
        print("getSharepointFileDB")
        exedir = os.getcwd()
        filename = exedir+"/.tmp_"+FILE_DB_JSON

        try:
            authcookie = Office365(SHAREPOINT_WEB_SITE, username=userName, password=password).GetCookies()
            site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=authcookie)
            folder = site.Folder(SHAREPOINT_FOLDER)
            data = folder.get_file('fileDB.json')
            with open(filename, "wb") as fh:
                fh.write(data)
        except ShareplumRequestError as e:
            self.popMessage("Cannot get the fileDB from sharepoint", QMessageBox.Critical)
            sys.exit(1)

        #self.shUserName = userName[0:userName.index('@')]
