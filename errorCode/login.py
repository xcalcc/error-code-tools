import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QMessageBox, QApplication, QPushButton, QLabel, QGridLayout, QDesktopWidget
from ui import Ui_MainWindow
from initAction import initAction

class LoginForm(object):
    def login(self):
        username = "xxx"#self.userName.text()
        password = "xxx"#self.password.text()

        if username == "" or password == "":
            self.popMessage("Username or Password can't empty", QMessageBox.Critical)
            return
        if initAction.loginSharepoint(self, username, password):
            initAction.health_check(self, username, password)
            Ui_MainWindow.main(MainWindow, username, password)
            MainWindow.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 85)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.userLabel = QtWidgets.QLabel(self.centralwidget)
        self.userLabel.setGeometry(QtCore.QRect(5, 5, 150, 20))
        self.userLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.userLabel.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.userName = QtWidgets.QLineEdit(self.centralwidget)
        self.userName.setGeometry(QtCore.QRect(155, 5, 200, 20))

        self.passwordLabel = QtWidgets.QLabel(self.centralwidget)
        self.passwordLabel.setGeometry(QtCore.QRect(5, 30, 150, 20))
        self.passwordLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.passwordLabel.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(155, 30, 200, 20))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(5, 55, 350, 20))

        MainWindow.setCentralWidget(self.centralwidget)

        self.buttonEvent()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login to Sharepoint"))

        self.userLabel.setText(_translate("MainWindow", "UserName"))
        self.passwordLabel.setText(_translate("MainWindow", "Password"))
        self.loginButton.setText(_translate("MainWindow", "Login"))

    def buttonEvent(self):
        self.loginButton.clicked.connect(self.login)

    def popMessage(self, message, status):
        print("popMessage")
        popupMessage = QMessageBox()
        popupMessage.setWindowTitle("Message")
        popupMessage.setText(message)
        popupMessage.setIcon(status)
        popupMessage.exec_()

    def setCenter(self, MainWindow):
        screen = QDesktopWidget().screenGeometry()
        size = MainWindow.geometry()
        newL = (screen.width() - size.width()) / 2
        newT = (screen.height() - size.height()) /2
        MainWindow.move(int(newL), int(newT))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    loginWindow = LoginForm()
    loginWindow.setupUi(MainWindow)
    loginWindow.setCenter(MainWindow)
    Ui_MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())