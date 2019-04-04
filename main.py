from PyQt5 import QtGui
import os, sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

style.use('ggplot')


class PrettyWidget(QWidget):


    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600,300, 1000, 600)
        self.center()
        self.setWindowTitle('fossee PyQt5 application')

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

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(self.rating_list)
        grid.addWidget(self.comboBox, 0, 0)

        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItems(self.yq_list)
        grid.addWidget(self.comboBox2, 0, 1)

        #Plot Button
        btn2 = QPushButton('Plot', self)
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.plot)
        grid.addWidget(btn2, 1, 1)

        self.show()


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

        ax.set_title('Canada C&I PD Plot')
        ax.legend(loc = 0)
        self.canvas.draw()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



def main():
    app = QApplication(sys.argv)
    w = PrettyWidget()
    app.exec_()


if __name__ == '__main__':
    main()
