#!/usr/bin/env python

import configparser
import chatFrameW
import xmlrpc.client
import sys
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

class Ui_chatFrame(object):
    def __init__(self):
        # Reading configuration from file name"server.ini"
        config = configparser.ConfigParser()
        config.read('client_b.ini')
        self.server_ip = str(config['ServerInfo']['SERVER_IP'])
        self.server_port = int(config['ServerInfo']['SERVER_PORT'])
        self.client_ip = str(config['ClientInfo']['CLIENT_IP'])
        self.client_port = int(config['ClientInfo']['CLIENT_PORT'])

        # the auth from database but it is going to from server
        try:
            self.db = xmlrpc.client.ServerProxy("http://"+self.server_ip+":"+str(self.server_port)+"/")
            self.db.check_friend("checking connection")
        except Exception as e:
            self.close_application(str(e))

        self.count = 0

    def setupUi(self, chatFrame):
        chatFrame.setObjectName(_fromUtf8("chatFrame"))
        chatFrame.resize(640, 532)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("lol.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        chatFrame.setWindowIcon(icon)
        chatFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        chatFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(chatFrame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelFriend = QtGui.QLabel(chatFrame)
        self.labelFriend.setObjectName(_fromUtf8("labelFriend"))
        self.gridLayout_2.addWidget(self.labelFriend, 0, 0, 1, 1)
        self.lineEditFriend = QtGui.QLineEdit(chatFrame)
        self.lineEditFriend.setObjectName(_fromUtf8("lineEditFriend"))
        self.gridLayout_2.addWidget(self.lineEditFriend, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.pushButtonFriend = QtGui.QPushButton(chatFrame)
        self.pushButtonFriend.setObjectName(_fromUtf8("pushButtonFriend"))
        self.verticalLayout_3.addWidget(self.pushButtonFriend)
        self.pushButtonFriend.clicked.connect(self.find_friend)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(chatFrame)
        QtCore.QMetaObject.connectSlotsByName(chatFrame)

    def retranslateUi(self, chatFrame):
        chatFrame.setWindowTitle(_translate("chatFrame", "LOL", None))
        self.labelFriend.setText(_translate("chatFrame", "Friend username : ", None))
        self.pushButtonFriend.setText(_translate("chatFrame", "Find", None))

    def close_application(self,message):
        sys.exit(message)

    def find_friend(self):
        friend_name = self.lineEditFriend.text()
        if self.db.lookup_friend(friend_name):
            self.friend_ip, port = self.db.lookup_friend(friend_name)
            self.friend_port = int(port)
            self.f_username = friend_name
            print(self.friend_ip)
            print(self.friend_port)
            self.open_chat()

    def open_chat(self):
        Frame = QtGui.QFrame()
        chat_ui = chatFrameW.Ui_Frame(self.friend_ip, self.friend_port, self.f_username)
        chat_ui.setupUi(Frame)
        Frame.show()
        Frame.setParent()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    chatFrame = QtGui.QFrame()
    ui = Ui_chatFrame()
    ui.setupUi(chatFrame)
    chatFrame.show()
    sys.exit(app.exec_())


