from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mainfolder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.mainfolder, "icons")
        self.setWindowTitle("PyBrowser")
        self.setGeometry(150,50,900,600)
        self.setWindowIcon(QIcon(os.path.join(self.img_folder,"globe-green.png")))

        self.browser =  QWebEngineView()
        self.browser.load(QUrl("http://www.google.com/"))
        self.browser.show()

        self.setCentralWidget(self.browser)

        # creation of tool bar ....
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join(self.img_folder, "arrow-curve-180-left.png")), "Back", self)
        back_btn.setStatusTip("previous tab")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        forward_btn = QAction(QIcon(os.path.join(self.img_folder, "arrow-curve.png")), "forward", self)
        forward_btn.setStatusTip("Forward tab")
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        home_btn = QAction(QIcon(os.path.join(self.img_folder, "home.png")), "Home", self)
        home_btn.setStatusTip("Home")
        home_btn.triggered.connect(self.home_clicked)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.http_icon = QLabel()
        self.http_icon.setPixmap(QPixmap(os.path.join(self.img_folder, "lock.png")))
        navtb.addWidget(self.http_icon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_url)
        navtb.addWidget(self.urlbar)

        search_btn = QAction(QIcon(os.path.join(self.img_folder, "search.png")), "Search", self)
        search_btn.setStatusTip("Search")
        search_btn.triggered.connect(self.navigate_url)
        navtb.addAction(search_btn)

        refresh_btn = QAction(QIcon(os.path.join(self.img_folder, "arrow-circle-double-135.png")), "Refresh", self)
        refresh_btn.setStatusTip("Refresh")
        refresh_btn.triggered.connect(self.browser.reload)
        navtb.addAction(refresh_btn)

        stop_btn = QAction(QIcon(os.path.join(self.img_folder, "cross.png")), "Stop", self)
        stop_btn.setStatusTip("Stop")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # changing URL bar content per search ...
        self.browser.urlChanged.connect(self.update_urlbar)

    def update_urlbar(self,u):
        if u.scheme() == 'https':
            self.http_icon.setPixmap(QPixmap(os.path.join(self.img_folder, "lock-ssl.png")))
        else:
            self.http_icon.setPixmap(QPixmap(os.path.join(self.img_folder, "lock.png")))
        u= str(u)

        self.urlbar.setText(u[19:-2])
        self.urlbar.setCursorPosition(0)

    def navigate_url(self):
        u = QUrl(self.urlbar.text())
        try:
            if u.scheme() == "":
                u.setScheme('http')

            self.browser.load(u)
            self.browser.show()
        except Exception as e:
            print(e)

    def home_clicked(self):
        self.browser.load(QUrl("http://www.google.com/"))
        self.browser.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin =MainWindow()
    mainWin.show()
    sys.exit(app.exec_())