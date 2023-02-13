# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIView.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UIView(object):
    def setupUi(self, UIView):
        if not UIView.objectName():
            UIView.setObjectName(u"UIView")
        UIView.resize(551, 421)
        UIView.setMinimumSize(QSize(0, 0))
        UIView.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u"robot.ico", QSize(), QIcon.Normal, QIcon.Off)
        UIView.setWindowIcon(icon)
        self.centralwidget = QWidget(UIView)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 241, 131))
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_stop = QLabel(self.groupBox)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout_3.addWidget(self.label_stop, 2, 0, 1, 1)

        self.label_num_order = QLabel(self.groupBox)
        self.label_num_order.setObjectName(u"label_num_order")

        self.gridLayout_3.addWidget(self.label_num_order, 0, 0, 1, 1)

        self.choice_num_order = QComboBox(self.groupBox)
        self.choice_num_order.addItem("")
        self.choice_num_order.addItem("")
        self.choice_num_order.addItem("")
        self.choice_num_order.setObjectName(u"choice_num_order")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choice_num_order.sizePolicy().hasHeightForWidth())
        self.choice_num_order.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_num_order, 0, 1, 1, 1)

        self.label_start = QLabel(self.groupBox)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout_3.addWidget(self.label_start, 1, 0, 1, 1)

        self.choice_start = QComboBox(self.groupBox)
        self.choice_start.addItem("")
        self.choice_start.addItem("")
        self.choice_start.setObjectName(u"choice_start")
        sizePolicy.setHeightForWidth(self.choice_start.sizePolicy().hasHeightForWidth())
        self.choice_start.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_start, 1, 1, 1, 1)

        self.choice_stop = QComboBox(self.groupBox)
        self.choice_stop.addItem("")
        self.choice_stop.setObjectName(u"choice_stop")
        sizePolicy.setHeightForWidth(self.choice_stop.sizePolicy().hasHeightForWidth())
        self.choice_stop.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_stop, 2, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 150, 241, 261))
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(50)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_1 = QLineEdit(self.groupBox_2)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_1, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.lineEdit_5 = QLineEdit(self.groupBox_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_5, 4, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.lineEdit_6 = QLineEdit(self.groupBox_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_6, 5, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.lineEdit_7 = QLineEdit(self.groupBox_2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setMaxLength(1)

        self.gridLayout.addWidget(self.lineEdit_7, 6, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(260, 10, 281, 401))
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.formLayout = QFormLayout(self.groupBox_4)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(7)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_13)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setDecimals(1)
        self.doubleSpinBox_2.setMaximum(2.500000000000000)
        self.doubleSpinBox_2.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_14)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setDecimals(1)
        self.doubleSpinBox_3.setMaximum(2.500000000000000)
        self.doubleSpinBox_3.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_3)

        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_12)

        self.doubleSpinBox_31 = QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_31.setObjectName(u"doubleSpinBox_31")
        self.doubleSpinBox_31.setDecimals(1)
        self.doubleSpinBox_31.setMaximum(2.500000000000000)
        self.doubleSpinBox_31.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox_31)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.groupBox_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.formLayout_2 = QFormLayout(self.groupBox_5)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(34)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.groupBox_5)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.doubleSpinBox_top = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_top.setObjectName(u"doubleSpinBox_top")
        self.doubleSpinBox_top.setDecimals(2)
        self.doubleSpinBox_top.setMinimum(0.000000000000000)
        self.doubleSpinBox_top.setMaximum(0.500000000000000)
        self.doubleSpinBox_top.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_top)

        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.doubleSpinBox_lbottom = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_lbottom.setObjectName(u"doubleSpinBox_lbottom")
        self.doubleSpinBox_lbottom.setDecimals(2)
        self.doubleSpinBox_lbottom.setMinimum(0.000000000000000)
        self.doubleSpinBox_lbottom.setMaximum(0.500000000000000)
        self.doubleSpinBox_lbottom.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_lbottom)

        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_10)

        self.doubleSpinBox_rbottom = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_rbottom.setObjectName(u"doubleSpinBox_rbottom")
        self.doubleSpinBox_rbottom.setMaximum(0.500000000000000)
        self.doubleSpinBox_rbottom.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox_rbottom)


        self.verticalLayout.addWidget(self.groupBox_5)

        UIView.setCentralWidget(self.centralwidget)

        self.retranslateUi(UIView)

        self.choice_num_order.setCurrentIndex(-1)
        self.choice_start.setCurrentIndex(-1)
        self.choice_stop.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(UIView)
    # setupUi

    def retranslateUi(self, UIView):
        UIView.setWindowTitle(QCoreApplication.translate("UIView", u"Robot", None))
        self.groupBox.setTitle(QCoreApplication.translate("UIView", u"\u8bbe\u7f6e/Config", None))
        self.label_stop.setText(QCoreApplication.translate("UIView", u"\u7ec8\u6b62\u952e/Stop", None))
        self.label_num_order.setText(QCoreApplication.translate("UIView", u"\u5355\u6570/Orders", None))
        self.choice_num_order.setItemText(0, QCoreApplication.translate("UIView", u"29", None))
        self.choice_num_order.setItemText(1, QCoreApplication.translate("UIView", u"30", None))
        self.choice_num_order.setItemText(2, QCoreApplication.translate("UIView", u"31", None))

        self.choice_num_order.setCurrentText("")
        self.label_start.setText(QCoreApplication.translate("UIView", u"\u542f\u52a8\u952e/Start", None))
        self.choice_start.setItemText(0, QCoreApplication.translate("UIView", u"F1", None))
        self.choice_start.setItemText(1, QCoreApplication.translate("UIView", u"Right Shift", None))

        self.choice_stop.setItemText(0, QCoreApplication.translate("UIView", u"Esc", None))

        self.choice_stop.setCurrentText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("UIView", u"\u952e\u4f4d/Key map", None))
        self.label.setText(QCoreApplication.translate("UIView", u"\u5411\u4e0a/Up", None))
        self.label_2.setText(QCoreApplication.translate("UIView", u"\u5411\u4e0b/Down", None))
        self.label_4.setText(QCoreApplication.translate("UIView", u"\u5411\u5de6/Left", None))
        self.label_5.setText(QCoreApplication.translate("UIView", u"\u5411\u53f3/Right", None))
        self.label_6.setText(QCoreApplication.translate("UIView", u"\u64cd\u4f5c/Operate", None))
        self.label_7.setText(QCoreApplication.translate("UIView", u"\u62ff\u653e/Pick up", None))
        self.label_3.setText(QCoreApplication.translate("UIView", u"\u52a0\u901f/Dash", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("UIView", u"\u9009\u9879/Option", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("UIView", u"\u9012\u76d8\u5ef6\u65f6\uff08\u79d2\uff09/Plate delay", None))
        self.label_13.setText(QCoreApplication.translate("UIView", u"\u7b2c\u4e8c\u4e2a\u76d8/2nd plate", None))
        self.label_14.setText(QCoreApplication.translate("UIView", u"\u7b2c\u4e09\u4e2a\u76d8/3rd plate", None))
        self.label_12.setText(QCoreApplication.translate("UIView", u"31\u5355\u7b2c\u4e00\u8f6e/\n"
"1st round(31 orders)", None))
        self.doubleSpinBox_31.setPrefix("")
        self.groupBox_5.setTitle(QCoreApplication.translate("UIView", u"\u843d\u5730\u5ef6\u65f6\uff08\u79d2\uff09/Landing delay", None))
        self.label_8.setText(QCoreApplication.translate("UIView", u"\u5de6\u4e0a&\u53f3\u4e0a/Top", None))
        self.label_9.setText(QCoreApplication.translate("UIView", u"\u5de6\u4e0b/Bottom left", None))
        self.label_10.setText(QCoreApplication.translate("UIView", u"\u53f3\u4e0b/Bottom right", None))
    # retranslateUi

