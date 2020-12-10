import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QTabBar, QFrame, QStackedLayout)
from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.createApp()
        self.setBaseSize(1366, 768)

    def createApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.closeTab)
        self.tabbar.tabBarClicked.connect(self.switchTab)

        self.tabbar.setCurrentIndex(0)

        # keep track of tabs
        self.tabCount = 0
        self.tabs = []

        # Create AddressBarr
        self.toolBar = QWidget()
        self.toolBarLayout = QHBoxLayout()
        self.addressBar = AddressBar()

        self.toolBar.setLayout(self.toolBarLayout)
        self.toolBarLayout.addWidget(self.addressBar)

        # set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)
        self.layout.addWidget(self.container)

        # new tab button
        self.addTabButton = QPushButton("+")
        self.addTabButton.clicked.connect(self.addTab)
        self.toolBarLayout.addWidget(self.addTabButton)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.toolBar)

        self.setLayout(self.layout)

        self.addTab()

        self.show()

    def closeTab(self, i):
        self.tabbar.removeTab(i)

    def addTab(self):
        i = self.tabCount

        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].setObjectName("tab" + str(i))

        # open webview
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

        # add webview to tabs layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)

        # set top level tab from list to layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # add tab to top level stackedwidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        # set the tab at top of screen
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, "tab" + str(i))
        self.tabbar.setCurrentIndex(i)

        self.tabCount += 1


    def switchTab(self, i):
        self.container.layout.setCurretnWidget(self.tabs[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
