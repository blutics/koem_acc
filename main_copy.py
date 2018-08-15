import sys

from Parsing_HTML import LoadParsing
from ProductPrice import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Main(QMainWindow):

    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.mainWidget = QTableWidget()
        self.main_layout = QVBoxLayout(self.mainWidget)
        self.main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.mainWidget.setLayout(self.main_layout)
        self.setCentralWidget(self.mainWidget)
        self.initUI()

    def initUI(self):

        loadAct = QAction('Load',self)
        loadAct.triggered.connect(self.LoadDialog)
        extractAct = QAction('Extract HTML',self)
        extractAct.triggered.connect(self.extract)
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.stitch_type = 0
        self.stitch_origin=QAction("본래값",self,checkable=True)
        self.stitch_paying=QAction("계산값",self,checkable=True)
        self.stitch_minus =QAction("빠진값",self,checkable=True)
        self.stitch_origin.triggered.connect(self.stitchOriginChanged)
        self.stitch_paying.triggered.connect(self.stitchPayingChanged)
        self.stitch_minus.triggered.connect(self.stitchMinusChanged)
        self.stitch_origin.setChecked(True)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadAct)
        fileMenu.addAction(extractAct)
        fileMenu.addAction(exitAct)

        stitchMenu = menubar.addMenu('&Stitch')
        stitchMenu.addAction(self.stitch_origin)
        stitchMenu.addAction(self.stitch_paying)
        stitchMenu.addAction(self.stitch_minus)

        self.setGeometry(300, 200, 850, 800)
        self.setWindowTitle('Simple menu')
        self.show()

    def LoadDialog(self):
        file = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","HTML Files (*.html)")
        if len(file[0])!=0:
            self.load=LoadParsing(file[0])
            self.list=self.load.getPairs()
            list=self.list
            self.mainWidget.setRowCount(len(list))
            self.mainWidget.setColumnCount(5)
            self.x=[0]*len(list)
            self.y=[0]*len(list)
            self.stitches=[[0,0,0]for i in range(len(list))]

            for i in range(len(list)):
                for j in range(len(list[0])):
                    self.mainWidget.setItem(i,j,QTableWidgetItem(list[i][j]))
                self.x[i]=QComboBox()
                self.x[i].addItems(['기본','극동','르노','송월','제외'])
                p=list[i][0][:2].lower()
                if p=='gd':
                    self.x[i].setCurrentIndex(1)
                elif p=='sw':
                    self.x[i].setCurrentIndex(3)
                elif p=='ex!@':
                    self.x[i].setCurrentIndex(4)
                elif p=='rn':
                    self.x[i].setCurrentIndex(2)
                    self.y[i]=QComboBox()
                    self.y[i].addItems(["일반","여자원숭이","남자원숭이","칠순","다이아칠순","팔순","다이아고희","고희","병아리","기획일반"])
                    self.mainWidget.setCellWidget(i, 4, self.y[i])
                    self.y[i].currentIndexChanged.connect(self.priceCalculateY)

                self.mainWidget.setCellWidget(i, 3, self.x[i])
                self.x[i].currentIndexChanged.connect(self.priceCalculateX)
                self.stitches[i][0]=self.list[i][1]
                c=modified_stitches(self.list[i][1])
                if p=='rn':
                    self.stitches[i][1] = c if int(c)>2500 else 2500
                else:
                    self.stitches[i][1] = self.list[i][1] if int(self.list[i][1]) > 2500 else 2500
                self.stitches[i][2] = c
                self.stitches[i]=[*map(str,self.stitches[i])]
                #self.mainWidget.setItem(i, 2, QTableWidgetItem(str(price(int(list[i][1]), p))))
                self.mainWidget.setItem(i, 2, QTableWidgetItem(price(self.stitches[i][0],p)))
    def priceCalculateX(self):
        row=self.x.index(app.sender())
        a=self.x[row].currentIndex()
        name=('normal','gd','rn','sw','ex!@')[a]
        self.mainWidget.setCurrentCell(row,4)
        #self.mainWidget.setItem(row, 2, QTableWidgetItem(str(price(int(self.list[row][1]), name))))
        c=modified_stitches(self.list[row][1])
        if name == 'rn':
            self.stitches[row][1] = c if int(c) > 2500 else 2500
            p=self.y[row]=QComboBox()
            self.y[row].addItems(["일반","여자원숭이","남자원숭이","칠순","다이아칠순","팔순","다이아고희","고희","병아리","기획일반"])
            self.mainWidget.setCellWidget(row, 4, self.y[row])
            self.y[row].currentIndexChanged.connect(self.priceCalculateY)
        else:
            self.stitches[row][1] = self.list[row][1] if int(self.list[row][1]) > 2500 else 2500
            self.mainWidget.removeCellWidget(row,4)
            #del self.y[row]
            self.y[row]=0
        self.stitches[row][2] = c
        self.mainWidget.setItem(row, 2, QTableWidgetItem(price(self.stitches[row][self.stitch_type],name)))

    def priceCalculateY(self):
        row=self.y.index(app.sender())
        a = self.x[row].currentIndex()
        name = ('normal', 'gd', 'rn','sw','ex!@')[a]
        b = self.y[row].currentIndex()
        self.mainWidget.setCurrentCell(row,4)
        #self.mainWidget.setItem(row, 1, QTableWidgetItem(modified_stitches(self.list[row][1],b)))
        #self.mainWidget.setItem(row, 2, QTableWidgetItem(str(price(int(self.list[row][1]), name,y=b))))
        print(self.stitches[row])
        c=modified_stitches(self.list[row][1],y=b)
        self.stitches[row][1] = str((2500,c)[int(c) > 2500])
        self.stitches[row][2] = str(c)
        print(self.stitches[row])

        self.mainWidget.setItem(row, 1, QTableWidgetItem(self.stitches[row][self.stitch_type]))
        self.mainWidget.setItem(row, 2, QTableWidgetItem(price(self.stitches[row][1],name,y=b)))

    def stitchOriginChanged(self,state):
        self.stitch_origin.setChecked(True)
        self.stitch_paying.setChecked(False)
        self.stitch_minus.setChecked(False)
        self.stitch_type = 0
        if 'list' in self.__dict__:
            for i in range(len(self.list)):
                self.mainWidget.setItem(i, 1, QTableWidgetItem(self.stitches[i][self.stitch_type]))

    def stitchPayingChanged(self, state):
        self.stitch_origin.setChecked(False)
        self.stitch_paying.setChecked(True)
        self.stitch_minus.setChecked(False)
        self.stitch_type = 1
        if 'list' in self.__dict__:
            for i in range(len(self.list)):
                self.mainWidget.setItem(i, 1, QTableWidgetItem(self.stitches[i][self.stitch_type]))

    def stitchMinusChanged(self,state):
        self.stitch_origin.setChecked(False)
        self.stitch_paying.setChecked(False)
        self.stitch_minus.setChecked(True)
        self.stitch_type = 2
        if 'list' in self.__dict__:
            for i in range(len(self.list)):
                self.mainWidget.setItem(i, 1, QTableWidgetItem(self.stitches[i][self.stitch_type]))

    def extract(self):
        if 'list'in self.__dict__:
            x=[self.mainWidget.item(i,2) for i in range(len(self.list))]
            self.load.extractHTML(x)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
