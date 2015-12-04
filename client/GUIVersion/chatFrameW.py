#!/usr/bin/env python

import configparser
import socket
import sys
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

class Ui_Frame(object):
    def __init__(self, friend_ip, friend_port, f_username):
        # Reading configuration from file name"server.ini"
        config = configparser.ConfigParser()
        config.read('client_b.ini')
        self.server_ip = str(config['ServerInfo']['SERVER_IP'])
        self.server_port = int(config['ServerInfo']['SERVER_PORT'])
        self.client_ip = str(config['ClientInfo']['CLIENT_IP'])
        self.client_port = int(config['ClientInfo']['CLIENT_PORT'])
        self.friend_ip = str(friend_ip)
        self.friend_port = int(friend_port)
        self.f_username = str(f_username)
        # empty chat
        self.doc = ""

        # the auth from database but it is going to from server
        try:
            self.db = xmlrpc.client.ServerProxy("http://"+self.server_ip+":"+str(self.server_port)+"/")
            self.db.check_friend("checking connection")
        except Exception as e:
            self.close_application(str(e))

        # Running initializing methods and printing info to console
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.client_ip, self.client_port))
        self.sock.settimeout(0.1)

    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(640, 480)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout_2 = QtGui.QGridLayout(Frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.textBrowserSend = QtGui.QTextBrowser(Frame)
        self.textBrowserSend.setObjectName(_fromUtf8("textBrowserSend"))
        self.gridLayout_2.addWidget(self.textBrowserSend, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonSend = QtGui.QPushButton(Frame)
        self.pushButtonSend.setObjectName(_fromUtf8("pushButtonSend"))
        self.pushButtonSend.clicked.connect(self.send_msg)
        self.gridLayout.addWidget(self.pushButtonSend, 0, 0, 1, 1)
        self.lineEditSend = QtGui.QLineEdit(Frame)
        self.lineEditSend.setObjectName(_fromUtf8("lineEditSend"))
        self.gridLayout.addWidget(self.lineEditSend, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.pushButtonSend.setText(_translate("Frame", "Send", None))

    def close_application(self, message):
        sys.exit(message)

    def get_msg(self):
        """
        This method receive the msg from friend with given by friend_name and returns
        the msg. If there is no message received before the socket timeouts, it returns
        empty string. Else returns nothing.
        """
        msg = ""
        try:
            while(True):
                data, addr = self.sock.recvfrom(1024)
                ip, port = addr
                if ip == self.friend_ip:
                    msg += data.decode("utf-8")
        except socket.timeout:
            self.doc += self.f_username + ": " + msg + "\n"
            self.textBrowserSend.setText(self.doc)

    def send_msg(self):
        """
        This method take following parameter
        message: a message client sending to friend
        And send the message to friend_name
        """
        message = self.lineEditSend.text()
        self.sock.sendto(message.encode('utf-8'), (self.friend_ip, self.friend_port))
        self.doc += "You: " + message + "\n"
        self.textBrowserSend.setText(self.doc)
        self.get_msg()

if __name__ == '__main__':
    # Reading configuration from file name"server.ini"
    config = configparser.ConfigParser()
    config.read('client_b.ini')
    client_ip = str(config['ClientInfo']['CLIENT_IP'])
    client_port = int(config['ClientInfo']['CLIENT_PORT'])

    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    ui = Ui_Frame(client_ip, client_port, "yolo")
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())