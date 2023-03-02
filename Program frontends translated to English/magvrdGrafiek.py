from datetime import date
from login import hoofdMenu
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QIcon, QPainter, QPageLayout
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton,QVBoxLayout,\
    QTableView, QWidget, QMessageBox
from sqlalchemy import (Table, Column, String, MetaData,\
                       create_engine, Float, select)

def sluiten(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def alertText(m_email):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Data for chart not complete!')
    msg.setWindowTitle('Warning message')
    msg.exec_() 
    hoofdMenu(m_email)
   
def toonGrafiek(m_email):
    mjrmnd = str(date.today())[0:7]
    mjrmndvj = str(int(str(date.today())[0:4])-1)+'-'+('0'+str(int(str(date.today())[5:7])))[-2:]
    metadata = MetaData()
    magazijnvoorraad = Table('magazijnvoorraad', metadata,
        Column('jaarmaand', String, primary_key=True),
        Column('totaal', Float),
        Column('courant', Float),                     
        Column('incourant', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selvrd = select([magazijnvoorraad]).where(magazijnvoorraad.c.jaarmaand.between(mjrmndvj, mjrmnd)).order_by(magazijnvoorraad.c.jaarmaand)
    rpvrd = con.execute(selvrd).fetchall()
    if len(rpvrd) < 12:
        alertText(m_email)
    
    class Window(QDialog):
        def __init__(self):          
            QDialog.__init__(self)
            self.setWindowTitle("Printing chart warehouse stock amounts")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                  Qt.WindowMinMaxButtonsHint)
            self.chart = QChart()
            self.chart_view = QChartView(self.chart)
            self.chart_view.setRenderHint(QPainter.Antialiasing)
            self.buttonPreview = QPushButton('Printing review', self)
            self.buttonPreview.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonPreview.clicked.connect(self.handle_preview)
            self.buttonPrint = QPushButton('Printing', self)
            self.buttonPrint.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonPrint.clicked.connect(self.handle_print) 
            self.sluiten = QPushButton('Close', self)
            self.sluiten.setStyleSheet("color: black;  background-color: gainsboro")
            self.sluiten.clicked.connect(lambda: sluiten(self, m_email))
            layout = QGridLayout(self)
            layout.addWidget(self.buttonPrint, 1, 1)
            layout.addWidget(self.sluiten, 1, 0)
            layout.addWidget(self.chart_view, 0, 0, 1, 3)
            layout.addWidget(self.buttonPreview, 1, 2)        
            self.create_chart()
  
        def create_chart(self):
            self.chart.setTitle('Chart finances warehouse inventory')
            font = QFont("Sans Serif", 10)
            font.setWeight(QFont.Bold)
            self.chart.setTitleFont(font)
           
            set0 = QBarSet('Total')
            set1 = QBarSet('Current')
            set2 = QBarSet('Obsolete')
            
            set0 << rpvrd[0][1] << rpvrd[1][1] << rpvrd[2][1] << rpvrd[3][1] << rpvrd[4][1] << rpvrd[5][1] << rpvrd[6][1] << rpvrd[7][1] << rpvrd[8][1] << rpvrd[9][1] << rpvrd[10][1] << rpvrd[11][1] 
            set1 << rpvrd[0][2] << rpvrd[1][2] << rpvrd[2][2] << rpvrd[3][2] << rpvrd[4][2] << rpvrd[5][2] << rpvrd[6][2] << rpvrd[7][2] << rpvrd[8][2] << rpvrd[9][2] << rpvrd[10][2] << rpvrd[11][2] 
            set2 << rpvrd[0][3] << rpvrd[1][3] << rpvrd[2][3] << rpvrd[3][3] << rpvrd[4][3] << rpvrd[5][3] << rpvrd[6][3] << rpvrd[7][3] << rpvrd[8][3] << rpvrd[9][3] << rpvrd[10][3] << rpvrd[11][3] 

            barseries = QBarSeries()
            barseries.append(set0)
            barseries.append(set1)
            barseries.append(set2)
                                                  
            categories = [rpvrd[0][0],rpvrd[1][0],rpvrd[2][0],rpvrd[3][0],rpvrd[4][0],\
                          rpvrd[5][0],rpvrd[6][0],rpvrd[7][0],rpvrd[8][0],rpvrd[9][0],\
                          rpvrd[10][0],rpvrd[11][0]]
                                               
            self.chart.addSeries(barseries)                                                         
            self.chart.axisX() 
            self.chart.createDefaultAxes()  
            axisX = QBarCategoryAxis()
            axisX.append(categories)
            axisX.setTitleText('12-month rolling period')
            self.chart.setAxisX(axisX, barseries)
            axisX.setRange(rpvrd[0][0], rpvrd[11][0])
            axisX.setLabelsAngle(-90)
                         
        def handle_print(self):
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOrientation(QPrinter.Landscape) 
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.handle_paint_request(printer)
    
        def handle_preview(self):
            dialog = QPrintPreviewDialog()
            dialog.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                  Qt.WindowMinMaxButtonsHint)
            dialog.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            dialog.setWindowFlags(dialog.windowFlags()| Qt.WindowSystemMenuHint |
                                                    Qt.WindowMinMaxButtonsHint)
            dialog.resize(1200,800)
            #dialog.setMinimumSize(1200, 800)
            dialog.paintRequested.connect(self.handle_paint_request)
            dialog.exec_()
    
        def handle_paint_request(self, printer):
            printer.setPageOrientation(QPageLayout.Landscape)
            painter = QPainter(printer)
            painter.setViewport(self.chart_view.rect())
            painter.setWindow(self.chart_view.rect())                        
            self.chart_view.render(painter)
            painter.end()

    window = Window()
    window.resize(1350, 900)
    window.exec_()
    hoofdMenu(m_email)
    
def magVoorraad(m_email):
    metadata = MetaData()
    metadata = MetaData()
    magazijnvoorraad = Table('magazijnvoorraad', metadata,
        Column('jaarmaand', String, primary_key=True),
        Column('totaal', Float),
        Column('courant', Float),                     
        Column('incourant', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selvrd = select([magazijnvoorraad]).order_by(magazijnvoorraad.c.jaarmaand)
    rpvrd = con.execute(selvrd)
          
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 600, 900)
            self.setWindowTitle('Annual consumption last year')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
                                        
    header = ['Year-Month', 'Total stock', 'Current stock', 'Obsolete stock']
        
    data_list=[]
    for row in rpvrd:
        data_list += [(row)] 
  
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)
