#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PySide import QtGui
from collections import OrderedDict

import mydao, userchoice, trainwindow, stat_window

#make mapping exercise name on its id in database: 
#{
ex_name_list = ['Exercise1', 'Exercise2', 'Exercise3', 
                'Exercise4', 'Exercise5', 'Exercise6', 
                'Exercise7', 'Exercise8', 'Exercise9', 
                'Exercise10']

exercise_dict = dict(zip(mydao.dbp.getExerciseId(), ex_name_list)) #unsorted dict
sorted_exercises = OrderedDict(sorted(exercise_dict.items())) #dict, sorted by its keys
#}

#some ugly staff for binding data from database with highlighter class
#{
mydao.dbp.getCurrentUserId('a_teem', 'roma')
#}

#highlighter class description
#{
#class MyHighLighter(QtGui.QSyntaxHighlighter):
#
#    def highlightBlock(self, text):
#        #choosing text format, which depends on what id have exercise
#        if ex_id < mydao.dbp.getCurrentExerciseId():
#            self.setFormat(0, len(text), QtGui.QColor('green'))      
#        else:
#            if ex_id > mydao.dbp.getCurrentExerciseId():
#                self.setFormat(0, len(text), QtGui.QColor('lightGray'))
#                self.setFormat(0, len(text), QtGui.QFont().setItalic(True))
#}

class Exercises(QtGui.QWidget):

    def __init__(self, mainwindow):
        super(Exercises, self).__init__()

        self.mainwindow = mainwindow

        self.initUI()

    def initUI(self):

       #make content
       self.backButton = QtGui.QPushButton('Back', self)
       self.nextButton = QtGui.QPushButton('Next', self)
       self.statButton = QtGui.QPushButton('Statistic', self)

       self.listWidget = QtGui.QListWidget(self)
       
       #forming and putting content to list widget
       for key, value in sorted_exercises.items():
           if key < mydao.dbp.getCurrentExerciseId():
            self.listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon('icons/tick.png'), value))
           else:
               if key == mydao.dbp.getCurrentExerciseId():
                   self.listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon('icons/pencil.png'), value))
               else:
                   self.listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon('icons/padlock.png'), value))

       #layout management
       self.hbox = QtGui.QHBoxLayout()
       self.hbox.addWidget(self.backButton)
       self.hbox.addStretch(1)
       self.hbox.addWidget(self.statButton)
       self.hbox.addStretch(1)
       self.hbox.addWidget(self.nextButton)

       self.vbox = QtGui.QVBoxLayout()
       self.vbox.addWidget(self.listWidget)
       self.vbox.addStretch(1)
       self.vbox.addLayout(self.hbox)

       self.setLayout(self.vbox)

       #send signals
       self.backButton.clicked.connect(self.backward)
       self.nextButton.clicked.connect(self.forward)
       self.statButton.clicked.connect(self.getStatistic)

    #create slots

    #Jump to previous widget -- userchoice
    def backward(self):
        index = self.mainwindow.stack.addWidget(userchoice.ChoiceUser(self.mainwindow))
        self.mainwindow.stack.setCurrentIndex(index)
        self.mainwindow.stack.currentWidget().resize()
    
    def forward(self):
        index = self.mainwindow.stack.addWidget(trainwindow.Trainer(self.mainwindow))
        self.mainwindow.stack.setCurrentIndex(index)
        self.mainwindow.stack.currentWidget().resize()

    def getStatistic(self):
        stat_window.StatWindow(1, 1)



    def resize(self):
        self.mainwindow.resize(600, 210)

