#!/usr/bin/python3

import sys
from PySide import QtGui

import userchoice


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.stack = QtGui.QStackedWidget()
        self.setCentralWidget(self.stack)

        # create and move to the first page
        self.stack.addWidget(userchoice.ChoiceUser(self))
        self.stack.currentWidget().resize()


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 
