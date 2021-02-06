# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuration_tool.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(639, 372)
        Form.setStyleSheet(u"")
        self.username = QLineEdit(Form)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(60, 40, 151, 20))
        self.stop = QPushButton(Form)
        self.stop.setObjectName(u"stop")
        self.stop.setGeometry(QRect(550, 330, 75, 23))
        self.run = QPushButton(Form)
        self.run.setObjectName(u"run")
        self.run.setGeometry(QRect(460, 330, 75, 23))
        self.passwd = QLineEdit(Form)
        self.passwd.setObjectName(u"passwd")
        self.passwd.setGeometry(QRect(60, 80, 151, 20))
        self.email_host = QLineEdit(Form)
        self.email_host.setObjectName(u"email_host")
        self.email_host.setGeometry(QRect(60, 120, 151, 20))
        self.proxy = QLineEdit(Form)
        self.proxy.setObjectName(u"proxy")
        self.proxy.setGeometry(QRect(50, 290, 101, 20))
        self.port = QLineEdit(Form)
        self.port.setObjectName(u"port")
        self.port.setGeometry(QRect(160, 290, 51, 20))
        self.sender_modified = QPushButton(Form)
        self.sender_modified.setObjectName(u"sender_modified")
        self.sender_modified.setGeometry(QRect(60, 160, 75, 23))
        self.sender_save = QPushButton(Form)
        self.sender_save.setObjectName(u"sender_save")
        self.sender_save.setGeometry(QRect(140, 160, 75, 23))
        self.proxy_modified = QPushButton(Form)
        self.proxy_modified.setObjectName(u"proxy_modified")
        self.proxy_modified.setGeometry(QRect(50, 320, 75, 23))
        self.proxy_save = QPushButton(Form)
        self.proxy_save.setObjectName(u"proxy_save")
        self.proxy_save.setGeometry(QRect(140, 320, 75, 23))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 71, 16))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 31, 16))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 80, 41, 16))
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 120, 41, 16))
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 270, 31, 16))
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(160, 270, 41, 16))
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 290, 31, 16))
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(370, 10, 81, 16))
        self.recv_append = QPushButton(Form)
        self.recv_append.setObjectName(u"recv_append")
        self.recv_append.setGeometry(QRect(560, 80, 75, 23))
        self.recv_delete = QPushButton(Form)
        self.recv_delete.setObjectName(u"recv_delete")
        self.recv_delete.setGeometry(QRect(560, 120, 75, 23))
        self.recv_info = QListWidget(Form)
        self.recv_info.setObjectName(u"recv_info")
        self.recv_info.setGeometry(QRect(370, 40, 181, 271))
        self.recv_modified = QPushButton(Form)
        self.recv_modified.setObjectName(u"recv_modified")
        self.recv_modified.setGeometry(QRect(560, 40, 75, 23))
        self.recv_save = QPushButton(Form)
        self.recv_save.setObjectName(u"recv_save")
        self.recv_save.setGeometry(QRect(560, 160, 75, 23))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.username.setText(QCoreApplication.translate("Form", u"E-mail", None))
        self.stop.setText(QCoreApplication.translate("Form", u"\u505c\u6b62", None))
        self.run.setText(QCoreApplication.translate("Form", u"\u555f\u52d5", None))
        self.passwd.setText(QCoreApplication.translate("Form", u"password", None))
        self.email_host.setText(QCoreApplication.translate("Form", u"E-mail host", None))
        self.proxy.setText(QCoreApplication.translate("Form", u"127.0.0.1", None))
        self.port.setText(QCoreApplication.translate("Form", u"8080", None))
        self.sender_modified.setText(QCoreApplication.translate("Form", u"\u4fee\u6539", None))
        self.sender_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.proxy_modified.setText(QCoreApplication.translate("Form", u"\u4fee\u6539", None))
        self.proxy_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u767c\u4ef6\u4eba\u4fe1\u606f:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u90f5\u7bb1:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6388\u6b0a\u78bc:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u4f3a\u670d\u5668:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u4f4d\u5740:", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u9023\u63a5\u57e0:", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u4ee3\u7406:", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u6536\u4ef6\u4eba\u4fe1\u606f\u6b04:", None))
        self.recv_append.setText(QCoreApplication.translate("Form", u"\u589e\u52a0", None))
        self.recv_delete.setText(QCoreApplication.translate("Form", u"\u522a\u9664", None))
        self.recv_modified.setText(QCoreApplication.translate("Form", u"\u4fee\u6539", None))
        self.recv_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
    # retranslateUi

