# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GPX_SpaceTimeCube_dialog_base.ui'
#
# Created: Sat Aug 12 15:44:57 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

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

class Ui_GPXtoSpaceTimeCubeDialogBase(object):
    def setupUi(self, GPXtoSpaceTimeCubeDialogBase):
        GPXtoSpaceTimeCubeDialogBase.setObjectName(_fromUtf8("GPXtoSpaceTimeCubeDialogBase"))
        GPXtoSpaceTimeCubeDialogBase.resize(423, 273)
        self.pushButton = QtGui.QPushButton(GPXtoSpaceTimeCubeDialogBase)
        self.pushButton.setGeometry(QtCore.QRect(160, 190, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.toolButton = QtGui.QToolButton(GPXtoSpaceTimeCubeDialogBase)
        self.toolButton.setGeometry(QtCore.QRect(310, 130, 27, 22))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.label_3 = QtGui.QLabel(GPXtoSpaceTimeCubeDialogBase)
        self.label_3.setGeometry(QtCore.QRect(50, 130, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_5 = QtGui.QLabel(GPXtoSpaceTimeCubeDialogBase)
        self.label_5.setGeometry(QtCore.QRect(80, 20, 271, 24))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit = QtGui.QLineEdit(GPXtoSpaceTimeCubeDialogBase)
        self.lineEdit.setGeometry(QtCore.QRect(120, 130, 181, 22))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(GPXtoSpaceTimeCubeDialogBase)
        self.label.setGeometry(QtCore.QRect(60, 80, 281, 21))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(GPXtoSpaceTimeCubeDialogBase)
        QtCore.QMetaObject.connectSlotsByName(GPXtoSpaceTimeCubeDialogBase)

    def retranslateUi(self, GPXtoSpaceTimeCubeDialogBase):
        GPXtoSpaceTimeCubeDialogBase.setWindowTitle(_translate("GPXtoSpaceTimeCubeDialogBase", "GPXtoSpaceTimeCube", None))
        self.pushButton.setText(_translate("GPXtoSpaceTimeCubeDialogBase", "Run!", None))
        self.toolButton.setText(_translate("GPXtoSpaceTimeCubeDialogBase", "...", None))
        self.label_3.setText(_translate("GPXtoSpaceTimeCubeDialogBase", "Input GPX:", None))
        self.label_5.setText(_translate("GPXtoSpaceTimeCubeDialogBase", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">GPX To Space Time Cube</span></p></body></html>", None))
        self.label.setText(_translate("GPXtoSpaceTimeCubeDialogBase", "Simply enter the directory to your GPX file and press Run!", None))

