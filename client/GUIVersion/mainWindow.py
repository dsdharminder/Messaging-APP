#!/usr/bin/env python

import configparser
import sys
import findFrame
import xmlrpc.client
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        # Reading configuration from file name"server.ini"
        config = configparser.ConfigParser()
        config.read('client_b.ini')
        self.server_ip = str(config['ServerInfo']['SERVER_IP'])
        self.server_port = int(config['ServerInfo']['SERVER_PORT'])
        self.client_ip = str(config['ClientInfo']['CLIENT_IP'])
        self.client_port = int(config['ClientInfo']['CLIENT_PORT'])

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(303, 241)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("lol.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.maincentralwidget = QtGui.QWidget(MainWindow)
        self.maincentralwidget.setObjectName(_fromUtf8("maincentralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.maincentralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(self.maincentralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidgetAuthenticate = QtGui.QTabWidget(self.frame)
        self.tabWidgetAuthenticate.setObjectName(_fromUtf8("tabWidgetAuthenticate"))
        self.tablogin = QtGui.QWidget()
        self.tablogin.setObjectName(_fromUtf8("tablogin"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tablogin)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.formLayoutlogin = QtGui.QFormLayout()
        self.formLayoutlogin.setObjectName(_fromUtf8("formLayoutlogin"))
        self.labelLU = QtGui.QLabel(self.tablogin)
        self.labelLU.setTextFormat(QtCore.Qt.AutoText)
        self.labelLU.setScaledContents(False)
        self.labelLU.setObjectName(_fromUtf8("labelLU"))
        self.formLayoutlogin.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelLU)
        self.labelLP = QtGui.QLabel(self.tablogin)
        self.labelLP.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLP.sizePolicy().hasHeightForWidth())
        self.labelLP.setSizePolicy(sizePolicy)
        self.labelLP.setObjectName(_fromUtf8("labelLP"))
        self.formLayoutlogin.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelLP)
        self.lineEditLU = QtGui.QLineEdit(self.tablogin)
        self.lineEditLU.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.lineEditLU.setObjectName(_fromUtf8("lineEditLU"))
        self.formLayoutlogin.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditLU)
        self.lineEditLP = QtGui.QLineEdit(self.tablogin)
        self.lineEditLP.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditLP.setObjectName(_fromUtf8("lineEditLP"))
        self.formLayoutlogin.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditLP)
        self.gridLayout_3.addLayout(self.formLayoutlogin, 0, 0, 1, 1)
        self.pushButtonL = QtGui.QPushButton(self.tablogin)
        self.pushButtonL.setObjectName(_fromUtf8("pushButtonL"))
        self.pushButtonL.clicked.connect(self.login)
        self.gridLayout_3.addWidget(self.pushButtonL, 1, 0, 1, 1)
        self.tabWidgetAuthenticate.addTab(self.tablogin, _fromUtf8(""))
        self.tabsignup = QtGui.QWidget()
        self.tabsignup.setObjectName(_fromUtf8("tabsignup"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabsignup)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pushButtonS = QtGui.QPushButton(self.tabsignup)
        self.pushButtonS.setObjectName(_fromUtf8("pushButtonS"))
        self.pushButtonS.clicked.connect(self.sign_up)
        self.gridLayout_4.addWidget(self.pushButtonS, 1, 0, 1, 1)
        self.formLayoutsignup = QtGui.QFormLayout()
        self.formLayoutsignup.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayoutsignup.setObjectName(_fromUtf8("formLayoutsignup"))
        self.labelSU = QtGui.QLabel(self.tabsignup)
        self.labelSU.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelSU.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelSU.setObjectName(_fromUtf8("labelSU"))
        self.formLayoutsignup.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelSU)
        self.lineEditSU = QtGui.QLineEdit(self.tabsignup)
        self.lineEditSU.setObjectName(_fromUtf8("lineEditSU"))
        self.formLayoutsignup.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditSU)
        self.labelSP = QtGui.QLabel(self.tabsignup)
        self.labelSP.setObjectName(_fromUtf8("labelSP"))
        self.formLayoutsignup.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelSP)
        self.lineEditSP = QtGui.QLineEdit(self.tabsignup)
        self.lineEditSP.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditSP.setObjectName(_fromUtf8("lineEditSP"))
        self.formLayoutsignup.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditSP)
        self.labelSCP = QtGui.QLabel(self.tabsignup)
        self.labelSCP.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelSCP.setObjectName(_fromUtf8("labelSCP"))
        self.formLayoutsignup.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelSCP)
        self.lineEditSCP = QtGui.QLineEdit(self.tabsignup)
        self.lineEditSCP.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditSCP.setObjectName(_fromUtf8("lineEditSCP"))
        self.formLayoutsignup.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEditSCP)
        self.gridLayout_4.addLayout(self.formLayoutsignup, 0, 0, 1, 1)
        self.tabWidgetAuthenticate.addTab(self.tabsignup, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidgetAuthenticate, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.maincentralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidgetAuthenticate.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.connectServer()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "LOL", None))
        self.labelLU.setText(_translate("MainWindow", "Username", None))
        self.labelLP.setText(_translate("MainWindow", "Password", None))
        self.pushButtonL.setText(_translate("MainWindow", "Login", None))
        self.tabWidgetAuthenticate.setTabText(self.tabWidgetAuthenticate.indexOf(self.tablogin), _translate("MainWindow", "Login", None))
        self.pushButtonS.setText(_translate("MainWindow", "Sign Up", None))
        self.labelSU.setText(_translate("MainWindow", "Username", None))
        self.labelSP.setText(_translate("MainWindow", "Password", None))
        self.labelSCP.setText(_translate("MainWindow", "Confirm Password", None))
        self.tabWidgetAuthenticate.setTabText(self.tabWidgetAuthenticate.indexOf(self.tabsignup), _translate("MainWindow", "Sign Up", None))

    def close_application(self, message):
        self.updateStatusBar(message)
        sys.exit(message)

    def updateStatusBar(self, string):
        self.statusbar.showMessage(string)

    def connectServer(self):
        # the auth from database but it is going to from server
        try:
            self.updateStatusBar("Connecting to server ...")
            self.db = xmlrpc.client.ServerProxy("http://"+self.server_ip+":"+str(self.server_port)+"/")
            self.db.check_friend("checking connection")
            self.updateStatusBar("Connected to server")
        except Exception as e:
            self.close_application(str(e))

    def login(self):
        self.updateStatusBar("Logging in ...")
        username = self.lineEditLU.text()
        password = self.lineEditLP.text()
        if not self.db.check_user(username,password):
            self.updateStatusBar("Wrong username or password")
        else:
            self.db.update_userinfo(username, password, self.client_ip, self.client_port)
            self.updateStatusBar("Logged in")
            MainWindow.hide()
            fFrame.show()


    def sign_up(self):
        self.updateStatusBar("Signing up ...")
        username = self.lineEditSU.text()
        password =self.lineEditSP.text()
        confirm_pass = self.lineEditSCP.text()
        if confirm_pass == password:
            if self.db.add_user(username,password,self.client_ip,self.client_port):
                if self.db.check_user(username,password):
                    self.updateStatusBar("Logged in")
                    MainWindow.hide()
                    fFrame.show()
            else:
                self.updateStatusBar("Invalid entry or user already exist")
        else:
            self.updateStatusBar("Password did not match")


if __name__ == "__main__":
    # Main window object
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    mainW = Ui_MainWindow()
    mainW.setupUi(MainWindow)
    MainWindow.show()
    fFrame = QtGui.QFrame()
    findW = findFrame.Ui_chatFrame()
    findW.setupUi(fFrame)
    sys.exit(app.exec_())

