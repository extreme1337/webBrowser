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

        self.addressBar.returnPressed.connect(self.browseTo)

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

        self.tabs[i].content.titleChanged.connect(lambda: self.setTabText(i))

        # add webview to tabs layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)

        # set top level tab from list to layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # add tab to top level stackedwidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        # set the tab at top of screen
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": "tab" + str(i), "initial": i})

        self.tabbar.setCurrentIndex(i)

        self.tabCount += 1

    def switchTab(self, i):
        tab_data = self.tabbar.tabData(i)

        tab_content = self.findChild(QWidget, tab_data)
        self.container.layout.setCurretnWidget(tab_content)

    def browseTo(self):
        text = self.addressBar.text()

        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)
        web_view = self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url = "https://www.google.com/#q=" + text
            else:
                url = "http://" + text
        else:
            url = text

        web_view.load(QUrl.fromUserInput(url))

    def setTabText(self, i):
        """
            self.tabs[i].objectName = tab1
            self.tabbar.tabData(i)["object"] = tab1
        """
        tab_name = self.tabs[i].objectName()
        # tab1
        count = 0
        running = True
        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False

            if tab_name == tab_data_name["object"]:
                newTitle = self.findChild(QWidget, tab_name).content.title()
                self.tabbar.setTabText(count, newTitle)
                running = False
            else:
                count += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
