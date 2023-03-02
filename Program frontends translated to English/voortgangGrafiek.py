from login import hoofdMenu
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries,\
                          QBarCategoryAxis, QPieSeries, QPieSlice     
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QRegExpValidator, QPen, QPageLayout
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout,\
        QPushButton, QMessageBox, QComboBox
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine, Float)
from sqlalchemy.sql import select
import datetime

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def sluit(self, m_email):
    self.close()
    zoekwk(m_email)   
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Progress charts')
    msg.exec_()

def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def geenWeek():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Week number is not present')
    msg.setWindowTitle('Progress charts')
    msg.exec_() 
    
def info(self):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Informatie status van externe werken")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 1, Qt.AlignRight)
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            
            infolbl = QLabel(
    '''
    
    Information about progress status 
    
     A. Preparation / Acquisition assignment / Reservation materials.
     
     B. Work has started / 1st delivery materials is done. 
     
     C. Work is 33% completed. (Invoice of 1st term of 33%) 
     
     D. Work is 50% completed. 
     
     E. Work is 75% completed. (Invoice of 2nd term of 33%) 
     
     F. Work is 90% completed. (Invoice of 3rd term of 20%)\t\t 
     
     G. Work is technically completed including additional work. (Invoice of 14% +/- additional work) \n
     
     H. Work has been financially completed and deregistered.
          
    ''')
            grid.addWidget(infolbl, 1, 0)
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")  
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 1, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(500, 200, 150, 100)
            
    window = Widget()
    window.exec_()
                
def zoekwk(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Printen status grafieken")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            
            self.Keuze = QLabel()
            kEdit = QComboBox()
            kEdit.setFixedWidth(300)
            kEdit.setFont(QFont("Arial", 10))
            kEdit.setStyleSheet("color: black;  background-color: #F8F7EE")
            kEdit.addItem('                  Choice graphs')
            kEdit.addItem('1. Graph status external works')
            kEdit.addItem('2. Graph works status-number\n    Pie chart')
            kEdit.addItem('3. Graph works status-number\n    Bar graph')
            kEdit.activated[str].connect(self.kChanged)
               
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(65)
            zktermEdit.setFont(QFont("Arial", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
            reg_ex = QRegExp("^[2]{1}[0-9]{1}[0-9]{2}[0-5]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, zktermEdit)
            zktermEdit.setValidator(input_validator)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
             
            grid.addWidget(kEdit, 1, 0, 1, 2, Qt.AlignRight)                     
            lbl1 = QLabel('Year week-report (yyyyww)')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0, 1, 2, Qt.AlignCenter)
            grid.addWidget(zktermEdit, 2, 1, 1, 1, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 200, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignRight)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
            
            sluitBtn = QPushButton('Close')
            sluitBtn.clicked.connect(lambda: windowSluit(self, m_email))            
          
            grid.addWidget(applyBtn, 3, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(sluitBtn, 3, 0, 1, 2, Qt.AlignCenter)
            sluitBtn.setFont(QFont("Arial", 10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                   
        def kChanged(self, text):
            self.Keuze.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk(self):
            return self.Keuze.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk(),dialog.returnzkterm()]       

    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        ongInvoer()
        zoekwk(m_email)
    if data[1] and len(data[1]) == 6:
        jrwk = data[1]
    else:
        ongInvoer()
        zoekwk(m_email)
    if keuze == 1:
        barGrafiek(keuze, jrwk, m_email)
    elif keuze == 2:
        statusPie(keuze, jrwk, m_email)
    elif keuze == 3:
        statusGrafiek(keuze, jrwk, m_email)
    zoekwk(m_email)
       
def barGrafiek(keuze, jrwk, m_email):
    metadata = MetaData()      
    resultaten_status = Table('resultaten_status', metadata,
        Column('rID', Integer, primary_key=True),
        Column('status', String),
        Column('aanneemsom', Float),
        Column('kosten', Float),
        Column('aantal', Integer),
        Column('boekweek', String),
        Column('betaald', Float),
        Column('meerminderwerk', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selsr = select([resultaten_status]).where(resultaten_status.c.boekweek == jrwk).order_by\
         (resultaten_status.c.status)
    rpsr = con.execute(selsr).fetchall()
    if not rpsr:
        geenWeek()
        return
    
    class Window(QDialog):
        def __init__(self):          
            QDialog.__init__(self)
            self.setWindowTitle("Printen grafiek status van externe werken over jaar "+jrwk[0:4]) 
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                  Qt.WindowMinMaxButtonsHint)
            self.chart = QChart()
            self.chart_view = QChartView(self.chart)
            self.chart_view.setRenderHint(QPainter.Antialiasing)
            self.buttonPreview = QPushButton('Print review', self)
            self.buttonPreview.clicked.connect(self.handle_preview)
            self.buttonPreview.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonPrint = QPushButton('Printing', self)
            self.buttonPrint.clicked.connect(self.handle_print) 
            self.buttonPrint.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonSluit = QPushButton('Close', self)
            self.buttonSluit.clicked.connect(lambda: sluit(self, m_email)) 
            self.buttonSluit.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonInfo = QPushButton('Info', self)
            self.buttonInfo.clicked.connect(lambda: info(self))
            self.buttonInfo.setStyleSheet("color: black;  background-color: gainsboro")
            layout = QGridLayout(self)
            layout.addWidget(self.chart_view, 0, 0, 1, 4)
            layout.addWidget(self.buttonInfo, 1, 0)
            layout.addWidget(self.buttonSluit, 1, 1)
            layout.addWidget(self.buttonPrint, 1, 2)
            layout.addWidget(self.buttonPreview, 1,3) 
 
            self.create_chart()
    
        def create_chart(self):
            self.chart.setTitle('Chart costs / avail of external works per status by year week '+jrwk)
            font = QFont("Sans Serif", 10)
            font.setWeight(QFont.Bold)
            self.chart.setTitleFont(font)
            set0 = QBarSet('Contract price +/- More/less work')
            set1 = QBarSet('Costs')
            set2 = QBarSet('Amount payed')
    
            set0 << rpsr[0][2]+rpsr[0][7] << rpsr[1][2]+rpsr[1][7] << rpsr[2][2]+rpsr[2][7]<< rpsr[3][2]+rpsr[3][7] << rpsr[4][2]+rpsr[4][7] << rpsr[5][2]+rpsr[5][7] << rpsr[6][2]+rpsr[6][7] << rpsr[7][2]+rpsr[7][7] 
            set1 << rpsr[0][3] << rpsr[1][3] << rpsr[2][3] << rpsr[3][3] << rpsr[4][3] << rpsr[5][3] << rpsr[6][3] << rpsr[7][3]
            set2 << rpsr[0][6] << rpsr[1][6] << rpsr[2][6] << rpsr[3][6] << rpsr[4][6] << rpsr[5][6] << rpsr[6][6] << rpsr[7][6] 
            
            barseries = QBarSeries()
            barseries.append(set0)
            barseries.append(set1)
            barseries.append(set2)
            barseries.append
                                      
            categories = ["Status A","Status B","Status C","Status D","Status E","Status F","Status G","Status H"]
                                               
            self.chart.addSeries(barseries)                                                         
            self.chart.axisX() 
            self.chart.createDefaultAxes()  
            axisX = QBarCategoryAxis()
            axisX.append(categories)
            self.chart.setAxisX(axisX, barseries)
            axisX.setRange(str("Status A"), str("Status H"))
                         
        def handle_print(self):
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            printer.setOrientation(QPrinter.Landscape)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.handle_paint_request(printer)
    
        def handle_preview(self):
            dialog = QPrintPreviewDialog()
            dialog.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            dialog.setWindowFlags(dialog.windowFlags()| Qt.WindowSystemMenuHint |
                                                    Qt.WindowMinMaxButtonsHint)
            dialog.resize(1485, 990)
            #dialog.setMinimumSize(1485, 990)
            dialog.paintRequested.connect(self.handle_paint_request)
            dialog.exec_()
    
        def handle_paint_request(self, printer):
            painter = QPainter(printer)
            painter.setViewport(self.chart_view.rect())
            painter.setWindow(self.chart_view.rect()) 
            printer.setPageOrientation(QPageLayout.Landscape)                       
            self.chart_view.render(painter)
            painter.end()
         
    window = Window()
    window.resize(1350, 900)
    window.exec_()
    
def statusGrafiek(keuze, jrwk, m_email):
    metadata = MetaData()      
    resultaten_status = Table('resultaten_status', metadata,
        Column('rID', Integer, primary_key=True),
        Column('status', String),
        Column('aantal', Integer),
        Column('boekweek', String))
   
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selr = select([resultaten_status]).where(resultaten_status.c.boekweek == jrwk).order_by\
         (resultaten_status.c.status)
    rpr = con.execute(selr).fetchall()
    if not rpr:
        geenWeek()
        return
    
    class Window(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle("Printing graph number of external works per status by year week "+jrwk[0:4])
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                  Qt.WindowMinMaxButtonsHint)
            self.chart = QChart()
            self.chart_view = QChartView(self.chart)
            self.chart_view.setRenderHint(QPainter.Antialiasing)
            self.buttonPreview = QPushButton('Print preview', self)
            self.buttonPreview.clicked.connect(self.handle_preview)
            self.buttonPreview.setStyleSheet("color: navy;  background-color: gainsboro")
            self.buttonPrint = QPushButton('Printing', self)
            self.buttonPrint.clicked.connect(self.handle_print) 
            self.buttonPrint.setStyleSheet("color: navy;  background-color: gainsboro")
            self.buttonSluit = QPushButton('Close', self)
            self.buttonSluit.clicked.connect(lambda: sluit(self, m_email))
            self.buttonSluit.setStyleSheet("color: navy;  background-color: gainsboro")
            self.buttonInfo = QPushButton('Info', self)
            self.buttonInfo.clicked.connect(lambda: info(self))
            self.buttonInfo.setStyleSheet("color: navy;  background-color: gainsboro")
           
            layout = QGridLayout(self)
            layout.addWidget(self.chart_view, 0, 0, 1, 4)
            layout.addWidget(self.buttonInfo, 1, 0)
            layout.addWidget(self.buttonSluit, 1, 1)
            layout.addWidget(self.buttonPrint, 1, 2)
            layout.addWidget(self.buttonPreview, 1, 3) 
            self.create_chart()
    
        def create_chart(self):
            self.chart.setTitle('Chart number of external works per status - by week '+jrwk)
            font = QFont("Sans Serif", 10)
            font.setWeight(QFont.Bold)
            self.chart.setTitleFont(font)
            set0 = QBarSet('Number of external works per status')
      
            set0 << rpr[0][2] << rpr[1][2] << rpr[2][2] << rpr[3][2] << rpr[4][2] << rpr[5][2] << rpr[6][2] << rpr[7][2]
 
            barseries = QBarSeries()
            barseries.append(set0)
            barseries.append
               
            categories = ["Status A","Status B","Status C","Status D","Status E","Status F","Status G","Status H"]
                                               
            self.chart.addSeries(barseries)                                                         
            self.chart.axisX() 
            self.chart.createDefaultAxes()  
            axisX = QBarCategoryAxis()
            axisX.append(categories)
            self.chart.setAxisX(axisX, barseries)
            axisX.setRange(str("Status A"), str("Status H"))
                           
        def handle_print(self):
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOrientation(QPrinter.Landscape) 
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.handle_paint_request(printer)
    
        def handle_preview(self):
            dialog = QPrintPreviewDialog()
            dialog.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            dialog.setWindowFlags(dialog.windowFlags()| Qt.WindowSystemMenuHint |
                                                      Qt.WindowMinMaxButtonsHint)
            dialog.resize(1485, 990)
            #dialog.setMinimumSize(1485, 990)
            dialog.paintRequested.connect(self.handle_paint_request)
            dialog.exec_()
    
        def handle_paint_request(self, printer):
            painter = QPainter(printer)
            painter.setViewport(self.chart_view.rect())
            painter.setWindow(self.chart_view.rect()) 
            printer.setPageOrientation(QPageLayout.Landscape)                       
            self.chart_view.render(painter)
            painter.end()
         
    window = Window()
    window.resize(1350, 900)
    window.exec_()
    
def statusPie(keuze, jrwk, m_email):
    metadata = MetaData()      
    resultaten_status = Table('resultaten_status', metadata,
        Column('rID', Integer, primary_key=True),
        Column('status', String),
        Column('aantal', Integer),
        Column('boekweek', String))
   
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selr = select([resultaten_status]).where(resultaten_status.c.boekweek == jrwk).order_by\
         (resultaten_status.c.status)
    rpr = con.execute(selr).fetchall()
    if not rpr:
        geenWeek()
        return
    
    class Window(QDialog):
        def __init__(self):          
            QDialog.__init__(self)
            self.setWindowTitle("Printing chart status of external works by year week "+jrwk[0:4])
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                  Qt.WindowMinMaxButtonsHint)
            self.chart = QChart()
            self.chart.legend().show()
            self.chart.legend().setAlignment(Qt.AlignRight)
            self.view = QChartView(self.chart)
            self.view.setRenderHint(QPainter.Antialiasing)
            self.buttonPreview = QPushButton('Print review', self)
            self.buttonPreview.clicked.connect(self.handle_preview)
            self.buttonPreview.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonPrint = QPushButton('Printing', self)
            self.buttonPrint.clicked.connect(self.handle_print)
            self.buttonPrint.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonSluit = QPushButton('Close', self)
            self.buttonSluit.clicked.connect(lambda: sluit(self, m_email))
            self.buttonSluit.setStyleSheet("color: black;  background-color: gainsboro")
            self.buttonInfo = QPushButton('Info', self)
            self.buttonInfo.clicked.connect(lambda: info(self))
            self.buttonInfo.setStyleSheet("color: black;  background-color: gainsboro") 
            layout = QGridLayout(self)
            layout.addWidget(self.view, 0, 0, 1, 4)
            layout.addWidget(self.buttonInfo, 1, 0)
            layout.addWidget(self.buttonSluit, 1, 1)
            layout.addWidget(self.buttonPrint, 1, 2)
            layout.addWidget(self.buttonPreview, 1, 3)             
            self.create_chart()
    
        def create_chart(self):
            self.chart.setTitle('Chart number of external works per status  by year week '+jrwk)
            font = QFont("Sans Serif", 10)
            font.setWeight(QFont.Bold)
            self.chart.setTitleFont(font)
            
            series = QPieSeries()
            slice_ = QPieSlice()
            series.setUseOpenGL(enable=True)
            series.append('Status A = '+str(rpr[0][2]), rpr[0][2])
            series.append('Status B = '+str(rpr[1][2]), rpr[1][2])
            series.append('Status C = '+str(rpr[2][2]), rpr[2][2])
            series.append('Status D = '+str(rpr[3][2]), rpr[3][2])
            series.append('Status E = '+str(rpr[4][2]), rpr[4][2])
            series.append('Status F = '+str(rpr[5][2]), rpr[5][2])
            series.append('Status G = '+str(rpr[6][2]), rpr[6][2])
            series.append('Status H = '+str(rpr[7][2]), rpr[7][2])
  
            for i, slice_ in enumerate(series.slices()):
                slice_.setLabelVisible()
                #slice_.setLabelPosition(3)
                if i == 0:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.green)
                elif i == 1:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.red)
                elif i == 2:
                    slice_.setExploded()
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.yellow)
                elif i == 3:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.magenta)
                elif i == 4:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.cyan)
                elif i == 5:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.blue)
                elif i == 6:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.darkYellow)
                elif i == 7:
                    slice_.setPen(QPen(Qt.black, 2))
                    slice_.setBrush(Qt.darkRed)
                       
            self.chart.addSeries(series)
            
        def handle_print(self):
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOrientation(QPrinter.Landscape) 
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.handle_paint_request(printer)
    
        def handle_preview(self):
            dialog = QPrintPreviewDialog()
            dialog.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            dialog.setWindowFlags(dialog.windowFlags()| Qt.WindowSystemMenuHint |
                                                      Qt.WindowMinMaxButtonsHint)
            dialog.resize(1050, 700)
            #dialog.setMinimumSize(1050, 700)
            dialog.paintRequested.connect(self.handle_paint_request)
            dialog.exec_()
    
        def handle_paint_request(self, printer):
            printer.setPageOrientation(QPageLayout.Landscape)
            painter = QPainter(printer)
            painter.setViewport(self.view.rect())
            painter.setWindow(self.view.rect()) 
            self.view.render(painter)
            painter.end()
            
    window = Window()
    window.resize(1050, 700)
    window.exec_()