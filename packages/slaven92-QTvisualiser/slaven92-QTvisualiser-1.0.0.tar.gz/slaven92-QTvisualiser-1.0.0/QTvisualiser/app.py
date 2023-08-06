from PyQt5.QtWidgets import QApplication

from .controllers import MainController, MainController2
from .views import mainWindow, mainWindow2

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.widget = mainWindow()
        self.widget.show()
        self.con = MainController(self.widget)


class App2(QApplication):
    def __init__(self, sys_argv):
        super(App2, self).__init__(sys_argv)
        self.widget = mainWindow2()
        self.widget.show()
        self.con = MainController2(self.widget)