#!/usr/bin/python3

from PySide import QtGui, QtCore
import mydao, exersises


class TrainerEdit(QtGui.QTextEdit):

    keyPressed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(TrainerEdit, self).__init__(parent)

    def keyPressEvent(self, event):
        key = event.text()
        if key:
            self.keyPressed.emit(key)


class Trainer(QtGui.QWidget):

    def __init__(self, mainwindow):
        super(Trainer, self).__init__()

        self.mainwindow = mainwindow
        self.pos = 0
        self.time = QtCore.QTime()
        self.firstTouch = False

        self.initUI()

    def initUI(self):

        #forming content
        self.backButton = QtGui.QPushButton('Back', self)
        self.nextButton = QtGui.QPushButton('Next', self)

        self.timeLabel = QtGui.QLabel('Time: ', self)
        self.speedLabel = QtGui.QLabel('Speed: ', self)

        self.nonEditText = QtGui.QTextEdit(self)
        self.nonEditText.setReadOnly(True)
        self.nonEditText.setText(mydao.dbp.getExerciseText(1))

        self.editText = TrainerEdit(self)
        self.editText.setFocus()

        #layout management
        self.labels = QtGui.QHBoxLayout()
        self.labels.addWidget(self.timeLabel, 2)
        self.labels.addStretch(1)
        self.labels.addWidget(self.speedLabel, 2)
        self.labels.addStretch(1)

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.backButton)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.nextButton)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.nonEditText)
        self.vbox.addLayout(self.labels)
        self.vbox.addWidget(self.editText)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        
        self.setLayout(self.vbox)
        self.highlightCurrent()
        
        #send signals
        self.backButton.clicked.connect(self.back)
        self.nextButton.clicked.connect(self.nextExercise)
        self.editText.keyPressed.connect(self.keyPressed)

    #make slots
    def back(self):
        index = self.mainwindow.stack.addWidget(exersises.Exercises(self.mainwindow))
        self.mainwindow.stack.setCurrentIndex(index)
        self.mainwindow.stack.currentWidget().resize()

    def keyPressed(self, key):
        if not self.firstTouch:
            self.time.start()
            self.firstTouch = True

        self.speedLabel.setText("Velocity: {} c/s".format(self.velocity()))
        self.timeLabel.setText("Time elapsed: {} s".format(self.time_elapsed()))

        if self.pos < len(self.nonEditText.toPlainText()):
            if self.nonEditText.toPlainText()[self.pos] == key:
                self.editText.insertPlainText(key)
                self.pos += 1
                self.highlightCurrent()
            else:
                QtGui.QMessageBox.critical(self, "Error", "Error")
        else:
            QtGui.QMessageBox.information(
                self,
                "Congratulations!",
                "You've done the exercise in {} seconds!".format(self.time_elapsed())
            )

    def time_elapsed(self):
        return self.time.elapsed() / 1000

    def velocity(self):
        return len(self.editText.toPlainText()) / self.time_elapsed()

    def highlightCurrent(self):
        if self.pos >= len(self.nonEditText.toPlainText()):
            return

        params = {
            'before': self.nonEditText.toPlainText()[:self.pos],
            'hl': self.nonEditText.toPlainText()[self.pos],
            'after': self.nonEditText.toPlainText()[self.pos + 1:]
        }
        self.nonEditText.setHtml("{before}<font color='red'>{hl}</font>{after}".format(**params))

    def nextExercise(self):
        pass

    def resize(self):
        self.mainwindow.resize(400, 400)
