# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 01:37:54 2019

@author: User
"""
import  sys
import os
import csv
from subprocess import call
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import numpy as np
import pandas as pd



class PrettyWidget(QWidget):


    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600,300, 500, 300)
        self.center()
        self.setWindowTitle('plotter')

        #Grid Layout
        grid = QGridLayout()
        self.setLayout(grid)

        #Canvas and Toolbar
        self.figure = plt.figure(figsize=(15,5))
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 2,0,1,2)


        #Import CSV Button
        btn1 = QPushButton('File', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(self.getCSV)
        grid.addWidget(btn1, 1, 0)

        #DropDown mean / comboBox

        self.df = pd.DataFrame()
        self.rating_list = []
        self.yq_list = []


        #Plot Button
        btn2 = QPushButton('Plot', self)
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.plot)
        grid.addWidget(btn2, 1, 1)

        self.show()

    @pyqtSlot()
    def getCSV(self):
        filePath = QFileDialog.getOpenFileName(self,
                                                    'CSV File',
                                                    '~/Desktop/PyQt4',
                                                    '*.csv')
        print(filePath)
        self.df = pd.read_csv(str(filePath))
        self.rating_list = self.df.rating.unique().tolist()
        self.yq_list = [str(x) for x in self.df.yq.unique().tolist()]
        self.comboBox.addItems(self.rating_list)
        self.comboBox2.addItems(self.yq_list)
        print (self.rating_list)


    def plot(self):
        y = []
        for n in range(3):
            try:
                y.append(self.table.item(0, n).text())
            except:
                y.append(np.nan)

        p1 = self.df.ix[(self.df.rating ==  str(self.comboBox.currentText())) & (self.df.yq ==  int(str(self.comboBox2.currentText()))), :]
        print (p1)

        plt.cla()


        ax = self.figure.add_subplot(111)
        ax.plot(p1.ix[:, 0], 'g', label = "Pred on data with Model")
        ax.plot(p1.ix[:, 1], label = "adj Pred to non-decreasing")
        ax.plot(p1.ix[:, 3], label = "Fitting value in Model")
        ax.plot(p1.ix[:, 2], 'r', label = "Actual PD")
        ax.plot(p1.ix[:, 4], 'y', label = "Long Run Avg")

        ax.set_title('csv data plotter')
        ax.legend(loc = 0)
        self.canvas.draw()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
class MyTableWidget(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()

    def c_current(self):
        if self.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            print("The current cell is ", row, ", ", col)
            print("In this cell we have: ", value)

    def open_sheet(self):
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
        self.check_change = True

    def save_sheet(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                maker = csv.writer(csv_file, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    maker.writerow(row_data)


class MySheet(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.form_widget = MyTableWidget(0, 0)
        self.setCentralWidget(self.form_widget)
        col1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.form_widget.setHorizontalHeaderLabels(col1)
        self.setWindowTitle("csv to table")
        save1 = QAction('&Save', self)
        save1.setShortcut('Ctrl+S')
        open1 = QAction('&Load', self)
        quit1 = QAction('&Quit', self)
        b = self.menuBar()
        file = b.addMenu('File')
        edit=b.addMenu('Edit')
        plot=b.addMenu('plot')
        save=b.addMenu('save')
        exitapp1=b.addMenu('Exit')
        file.addAction(open1)
        exitapp1.addAction(quit1)
        save.addAction(save1)
        
        quit1.triggered.connect(self.quit_app)
        save1.triggered.connect(self.form_widget.save_sheet)
        open1.triggered.connect(self.form_widget.open_sheet)
        self.show()
        
    def run_myScript(self):
        call(["python", 'PlotterScipt.py'])
        QMainWindow.hide()    
  
    def quit_app(self):
        qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PrettyWidget()
    ask = MySheet()
    win = QMainWindow ()
    win.setCentralWidget (ask)
    win.setWindowTitle("csv to table")
    win.resize(600,400)
    win.show ()
    sys.exit(app.exec_())

