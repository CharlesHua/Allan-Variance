#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Allan Variance

@author: Jiannan Hua
last edited: Mar.3  2018
"""

import sys

import numpy as np
from PyQt4 import QtCore, QtGui
#from numpy import loadtxt
#from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_tight_layout({'h_pad'})
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def compute_initial_figure(self):
       # print 'initial_figure'
       pass


class ApplicationWindow(QtGui.QMainWindow):
    """docstring for ApplicationWindow"""
    def __init__(self, arg):
        super(ApplicationWindow, self).__init__()
        self.arg = arg

        # def Init_Data():
        self.length = 0
        self.x = []
        self.y = []

        # Init_Data()
        self.Init_Ui()


    def Init_Ui(self):

        '''statusBar and menuBar'''
        self.statusBar()
        menubar = self.menuBar()

        openFileAction = QtGui.QAction('Open File...', self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Open New File')
        openFileAction.triggered.connect(self.OpenFile)

        clearFitAction = QtGui.QAction('Clear Fit', self)
        clearFitAction.setStatusTip('Clear Fit')
        clearFitAction.triggered.connect(self.ClearFit)

        AllanVarianceAction = QtGui.QAction('Allan Variance', self)
        AllanVarianceAction.setStatusTip('Allan Variance on XY data')
        AllanVarianceAction.triggered.connect(self.AllanVariance)

        aboutAction = QtGui.QAction('About', self)
        aboutAction.triggered.connect(self.about)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFileAction)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(clearFitAction)

        analysisMenu = menubar.addMenu('&Analysis')
        analysisMenu.addAction(AllanVarianceAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)

        '''data table'''
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['X', 'Y'])


        # set data
        for col in range(2):
            newItem = QtGui.QTableWidgetItem('0')
            newItem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.table.setItem(0, col, newItem)

        # tooltip text
        self.table.horizontalHeaderItem(0).setToolTip("Column 1")
        self.table.horizontalHeaderItem(1).setToolTip("Column 2")

        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setFrameShape(QtGui.QFrame.StyledPanel)


        # picture
        self.pictr = MyMplCanvas(width=5, height=4, dpi=100)
        self.pictr.axes.set_xlabel('t')
        self.pictr.axes.set_ylabel('x')
        self.pictr.draw()

        #print "τ".decode("utf-8").encode("gbk")
        self.pictr2 = MyMplCanvas(width=5, height=3, dpi=100)
        self.pictr2.axes.set_xlabel("tau")
        self.pictr2.axes.set_ylabel('sigma')
        self.pictr2.draw()

        self.mplToolbar = NavigationToolbar(self.pictr, None)
        self.mplToolbar2 = NavigationToolbar(self.pictr2, None)


        # splitter (assemble widgets)
        splitterV1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitterV2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitterV1.addWidget(self.mplToolbar)
        splitterV1.addWidget(self.pictr)
        splitterV2.addWidget(self.mplToolbar2)
        splitterV2.addWidget(self.pictr2)
    #    splitterV.setStretchFactor(1, 5)
    #    splitterV.setStretchFactor(2, 4)

        splitterH = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterH.addWidget(self.table)
        splitterH.addWidget(splitterV1)
        splitterH.addWidget(splitterV2)


        self.setCentralWidget(splitterH)
        self.setGeometry(200, 100, 800, 600)
        self.setWindowTitle('Allan Variance')

        self.show()


    def DrawDataPoint(self):
        self.pictr.axes.cla()
        self.pictr.axes.set_xbound(min(self.x), max(self.x))

        self.pictr.axes.scatter(self.x, self.y, c='k', s = 3)
        self.pictr.axes.axhline(y=0, color='r', linestyle='--', linewidth=1.0)

        ybound = max(abs(min(self.y)), abs(max(self.y))) * 1.1
        self.pictr.axes.set_ybound(-ybound, ybound)
        self.pictr.axes.set_xlabel('t')
        self.pictr.axes.set_ylabel('x')
        self.pictr.draw()


        self.pictr2.axes.cla()
        self.pictr2.axes.set_xbound(self.pictr.axes.get_xbound())
        self.pictr2.axes.set_xlabel('tau')
        self.pictr2.axes.set_ylabel('sigma')
        self.pictr2.draw()


    def OpenFile(self):
        def ImportData():
            data = np.loadtxt(address_str)
           # print data
            self.x = data[:, 0]
            self.y = data[:, 1]


        def DisplayInTable():
            self.table.setRowCount(len(self.x))
            self.length = len(self.x)
            for i in range(self.length):
                # Align left
                # self.table.setItem(i,0, QtGui.QTableWidgetItem(str(self.x[i])))
                # self.table.setItem(i,1, QtGui.QTableWidgetItem(str(self.y[i])))
                # Align right
                newItem = QtGui.QTableWidgetItem(str(self.x[i]))
                newItem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.table.setItem(i, 0, newItem)
                newItem = QtGui.QTableWidgetItem(str(self.y[i]))
                newItem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.table.setItem(i, 1, newItem)
               

        fileAddress = QtGui.QFileDialog.getOpenFileName(self, 'Open file', directory='')
        address_str = str(fileAddress)
        f = open(fileAddress, 'r')
        with f:
            ImportData()
            DisplayInTable()
            self.DrawDataPoint()
            self.setStatusTip(fileAddress)


    def ClearFit(self):
        # empty is False
        if len(self.x):
            self.DrawDataPoint()


    def DisplayResult(self):
        self.pictr2.axes.cla()
        self.pictr2.axes.set_xlabel('tau')
        self.pictr2.axes.set_ylabel('sigma')
        self.pictr2.axes.loglog()        

        # draw a line
        self.pictr2.axes.plot(self.tau, self.sigma_tau, label=str())
        #self.pictr.axes.legend(handles=, loc=1)
        self.pictr2.draw()


    def AllanVariance(self):
        
        self.sigma_tau = []
        self.tau = []
        M = self.length
        n = 1
        tau0 = self.x[1] - self.x[0]
        while (M > 2*n+10):
            sum = 0
            for k in range(0, M-2*n):
                sum += (self.y[k+2*n] - 2 * self.y[k+n] + self.y[k])**2
                sigma_2 = sum / (2 *tau0 * n *tau0 * n *(M+1-2*n)) 
            self.sigma_tau.append(np.sqrt( sigma_2) )
            self.tau.append(tau0 * n )
        #    print n, "  ", self.tau[-1],"  " ,self.sigma_tau[-1]
            n = max (n+1, int(n*1.001))
        

        self.DisplayResult()


    def about(self):
        pass


def main():
    QtCore.pyqtRemoveInputHook()
    app = QtGui.QApplication(sys.argv)
    orange = ApplicationWindow(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
