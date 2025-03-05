# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(728, 460)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(400, 300))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/images/ms_icon.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about_qt = QAction(MainWindow)
        self.action_about_qt.setObjectName(u"action_about_qt")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.action_dark_mode = QAction(MainWindow)
        self.action_dark_mode.setObjectName(u"action_dark_mode")
        self.action_dark_mode.setCheckable(True)
        self.action_dark_mode.setChecked(False)
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.line_access_key = QLineEdit(self.groupBox)
        self.line_access_key.setObjectName(u"line_access_key")
        self.line_access_key.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout.addWidget(self.line_access_key)

        self.line_secret_key = QLineEdit(self.groupBox)
        self.line_secret_key.setObjectName(u"line_secret_key")
        self.line_secret_key.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout.addWidget(self.line_secret_key)

        self.combo_region = QComboBox(self.groupBox)
        self.combo_region.setObjectName(u"combo_region")
        sizePolicy.setHeightForWidth(self.combo_region.sizePolicy().hasHeightForWidth())
        self.combo_region.setSizePolicy(sizePolicy)
        self.combo_region.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.combo_region)

        self.button_connect = QPushButton(self.groupBox)
        self.button_connect.setObjectName(u"button_connect")

        self.horizontalLayout.addWidget(self.button_connect)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_bucket_name = QLineEdit(self.groupBox)
        self.line_bucket_name.setObjectName(u"line_bucket_name")

        self.verticalLayout.addWidget(self.line_bucket_name)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_upload = QPushButton(self.groupBox_2)
        self.button_upload.setObjectName(u"button_upload")

        self.horizontalLayout_2.addWidget(self.button_upload)

        self.button_download = QPushButton(self.groupBox_2)
        self.button_download.setObjectName(u"button_download")

        self.horizontalLayout_2.addWidget(self.button_download)

        self.button_delete = QPushButton(self.groupBox_2)
        self.button_delete.setObjectName(u"button_delete")

        self.horizontalLayout_2.addWidget(self.button_delete)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.button_query = QPushButton(self.groupBox_2)
        self.button_query.setObjectName(u"button_query")
        sizePolicy.setHeightForWidth(self.button_query.sizePolicy().hasHeightForWidth())
        self.button_query.setSizePolicy(sizePolicy)
        self.button_query.setMinimumSize(QSize(100, 0))

        self.verticalLayout_3.addWidget(self.button_query)

        self.table = QTableWidget(self.groupBox_2)
        self.table.setObjectName(u"table")

        self.verticalLayout_3.addWidget(self.table)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.label_connection = QLabel(self.centralwidget)
        self.label_connection.setObjectName(u"label_connection")

        self.verticalLayout_2.addWidget(self.label_connection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 728, 22))
        self.menuAbout = QMenu(self.menuBar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuSetting = QMenu(self.menuBar)
        self.menuSetting.setObjectName(u"menuSetting")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuSetting.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())
        self.menuAbout.addAction(self.action_about)
        self.menuAbout.addAction(self.action_about_qt)
        self.menuSetting.addAction(self.action_dark_mode)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AWS S3 Bucket Tool", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_about_qt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_dark_mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.action_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.action_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"AWS Bucket Info", None))
#if QT_CONFIG(statustip)
        self.line_access_key.setStatusTip(QCoreApplication.translate("MainWindow", u"Enter your AWS Access Key", None))
#endif // QT_CONFIG(statustip)
        self.line_access_key.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AWS Access Key", None))
#if QT_CONFIG(statustip)
        self.line_secret_key.setStatusTip(QCoreApplication.translate("MainWindow", u"Enter your AWS Secret Access Key", None))
#endif // QT_CONFIG(statustip)
        self.line_secret_key.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AWS Secret Access Key", None))
#if QT_CONFIG(statustip)
        self.combo_region.setStatusTip(QCoreApplication.translate("MainWindow", u"Select the AWS Region", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.button_connect.setStatusTip(QCoreApplication.translate("MainWindow", u"Connect to AWS", None))
#endif // QT_CONFIG(statustip)
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
#if QT_CONFIG(statustip)
        self.line_bucket_name.setStatusTip(QCoreApplication.translate("MainWindow", u"Enter the name of the bucket you wish to use", None))
#endif // QT_CONFIG(statustip)
        self.line_bucket_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"S3 Bucket", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
#if QT_CONFIG(statustip)
        self.button_upload.setStatusTip(QCoreApplication.translate("MainWindow", u"Upload file to a bucket, drag-and-drop also works", None))
#endif // QT_CONFIG(statustip)
        self.button_upload.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
#if QT_CONFIG(statustip)
        self.button_download.setStatusTip(QCoreApplication.translate("MainWindow", u"Select a file in the table and download to a local storage", None))
#endif // QT_CONFIG(statustip)
        self.button_download.setText(QCoreApplication.translate("MainWindow", u"Download", None))
#if QT_CONFIG(statustip)
        self.button_delete.setStatusTip(QCoreApplication.translate("MainWindow", u"Select a file in the table and delete it from the bucket", None))
#endif // QT_CONFIG(statustip)
        self.button_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(statustip)
        self.button_query.setStatusTip(QCoreApplication.translate("MainWindow", u"Query the bucket to refresh the table", None))
#endif // QT_CONFIG(statustip)
        self.button_query.setText(QCoreApplication.translate("MainWindow", u"Query S3 Bucket", None))
#if QT_CONFIG(statustip)
        self.table.setStatusTip(QCoreApplication.translate("MainWindow", u"S3 Bucket", None))
#endif // QT_CONFIG(statustip)
        self.label_connection.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

