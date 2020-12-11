import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QTabBar, QFrame, QStackedLayout, QShortcut, QKeySequenceEdit, QSplitter)
from PyQt5.QtGui import QIcon, QWindow, QImage, QKeySequence
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
        self.setMinimumSize(1366, 720)
        self.createApp()
        self.setWindowIcon(QIcon("logo.png"))

    def createApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # create tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.closeTab)
        self.tabbar.tabBarClicked.connect(self.switchTab)
        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.tabbar.setLayoutDirection(Qt.LeftToRight)
        self.tabbar.setElideMode(Qt.ElideLeft)

        # shortcuts
        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.addTab)

        self.shorcutReload = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shorcutReload.activated.connect(self.reloadPage)

        # keep track of tabs
        self.tabCount = 0
        self.tabs = []

        # create addressBar
        self.toolbar = QWidget()
        self.toolbar.setObjectName("toolbar")
        self.toolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()
        self.addTabButton = QPushButton("+")

        # connect addressBar + button signals
        self.addressbar.returnPressed.connect(self.browseTo)
        self.addTabButton.clicked.connect(self.addTab)

        # set toolbar buttons
        self.backButton = QPushButton("<")
        self.backButton.clicked.connect(self.goBack)

        self.forwardButton = QPushButton(">")
        self.forwardButton.clicked.connect(self.goForward)

        self.reloadButton = QPushButton("R")
        self.reloadButton.clicked.connect(self.reloadPage)

        # build toolbar
        self.toolbar.setLayout(self.toolbarLayout)
        self.toolbarLayout.addWidget(self.backButton)
        self.toolbarLayout.addWidget(self.forwardButton)
        self.toolbarLayout.addWidget(self.reloadButton)
        self.toolbarLayout.addWidget(self.addressbar)
        self.toolbarLayout.addWidget(self.addTabButton)

        # set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        # construct main view from top level elements
        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)

        self.addTab()

        self.show()

    def closeTab(self, i):
        self.tabbar.removeTab(i)

    def addTab(self):

        i = self.tabCount
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)


        self.tabs[i].setObjectName("tab" + str(i))

        # open webview
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.setTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.setTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.setTabContent(i, "url"))

        # add webview to tabs layout
        self.tabs[i].splitview = QSplitter()
        self.tabs[i].layout.addWidget(self.tabs[i].splitview)

        self.tabs[i].splitview.addWidget(self.tabs[i].content)

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
        # Switch to tab. get current tabs tabData ("tab0") and find object
        # with that name
        if self.tabbar.tabData(1):
            tab_data = self.tabbar.tabData(i)["object"]
            tab_content = self.findChild(QWidget, tab_data)
            self.container.layout.setCurrentWidget(tab_content)
            new_url = tab_content.content.url().toString()
            self.addressbar.setText(new_url)

    def browseTo(self):
        text = self.addressbar.text()

        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        web_view = self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url = "https://www.google.com/#q=" + text
            else:
                url = "http://" + text
        else:
            url = text

        web_view.load(QUrl.fromUserInput(url))

    def setTabContent(self, i, type):
        """
            self.tabs[i].objectName = tab1
            self.tabbar.tabData(i)["object"] = tab1
        """
        tab_name = self.tabs[i].objectName()
        # tab1
        count = 0
        running = True

        current_tab = self.tabbar.tabData(self.tabbar.currentIndex())["object"]
        if current_tab == tab_name and type == "url":
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.addressbar.setText(new_url)
            return False

        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False

            if tab_name == tab_data_name["object"]:
                if type == "title":
                    newTitle = self.findChild(QWidget, tab_name).content.title()
                    self.tabbar.setTabText(count, newTitle)
                elif type == "icon":
                    newIcon = self.findChild(QWidget, tab_name).content.icon()
                    self.tabbar.setTabIcon(count, newIcon)
                running = False
            else:
                count += 1

    def goBack(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.back()

    def goForward(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.forward()

    def reloadPage(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.reload()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()

    with open("style.css", "r") as style:
        app.setStyleSheet(style.read())

    sys.exit(app.exec_())
