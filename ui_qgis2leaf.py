# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qgis2leaf.ui'
#
# Created: Thu Apr 24 21:53:27 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_qgis2leaf(object):
    def setupUi(self, qgis2leaf):
        qgis2leaf.setObjectName(_fromUtf8("qgis2leaf"))
        qgis2leaf.resize(449, 237)
        self.gridLayoutWidget = QtGui.QWidget(qgis2leaf)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 110, 431, 121))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 2, 1, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.okButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.gridLayout.addWidget(self.okButton, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label = QtGui.QLabel(qgis2leaf)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(qgis2leaf)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 431, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(qgis2leaf)
        self.line.setGeometry(QtCore.QRect(10, 60, 431, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayoutWidget = QtGui.QWidget(qgis2leaf)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 341, 31))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_5 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        self.width_box = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.width_box.setObjectName(_fromUtf8("width_box"))
        self.horizontalLayout.addWidget(self.width_box)
        self.height_box = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.height_box.setObjectName(_fromUtf8("height_box"))
        self.horizontalLayout.addWidget(self.height_box)
        self.actionLoadList = QtGui.QAction(qgis2leaf)
        self.actionLoadList.setObjectName(_fromUtf8("actionLoadList"))

        self.retranslateUi(qgis2leaf)
        QtCore.QMetaObject.connectSlotsByName(qgis2leaf)

    def retranslateUi(self, qgis2leaf):
        qgis2leaf.setWindowTitle(_translate("qgis2leaf", "qgis2leaf", None))
        self.pushButton_2.setText(_translate("qgis2leaf", "...", None))
        self.label_3.setText(_translate("qgis2leaf", "output project folder:", None))
        self.cancelButton.setText(_translate("qgis2leaf", "Cancel", None))
        self.okButton.setText(_translate("qgis2leaf", "OK", None))
        self.label_4.setText(_translate("qgis2leaf", "basemap", None))
        self.label.setText(_translate("qgis2leaf", "QGIS2leaf", None))
        self.label_2.setText(_translate("qgis2leaf", "Export your current vector features to a working leaflet based webmap", None))
        self.label_5.setText(_translate("qgis2leaf", "frame width x height", None))
        self.actionLoadList.setText(_translate("qgis2leaf", "loadList", None))

