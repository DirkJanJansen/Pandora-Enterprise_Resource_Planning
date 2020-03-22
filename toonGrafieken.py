from login import hoofdMenu
import datetime
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QFont, QPixmap, QRegExpValidator, QBrush, QColor,\
      QPen, QPainter, QPageLayout
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout,\
        QPushButton, QMessageBox, QComboBox
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine, Float, select, and_)

def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def sluit(self, m_email):
    self.close()
    zoekwk(m_email)   
    
def ongInvoer():
    msg = QMessageBox()
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Voortgangsgrafieken')               
    msg.exec_()
 
def zoekwk(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Keuze grafieken externe werken")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
            
            self.Keuze = QLabel()
            kEdit = QComboBox()
            kEdit.setFixedWidth(300)
            kEdit.setFont(QFont("Arial", 10))
            kEdit.setStyleSheet("color: black;  background-color: #F8F7EE")
            kEdit.addItem('                  Keuze Grafieken')
            kEdit.addItem('1. Kosten totaal begroot-werkelijk')
            kEdit.addItem('2. Lonen begroot-werkelijk')
            kEdit.addItem('3. Materialen begroot-werkelijk')
            kEdit.addItem('4. Materiëel begroot-werkelijk')
            kEdit.addItem('5. Inhuur begroot-werkelijk')
            kEdit.addItem('6. Diensten begroot-werkelijk')            
            kEdit.addItem('7. Projektkosten begroot-werkelijk')
            kEdit.addItem('8. Bruto winst - prognose / aktueel')
            kEdit.addItem('9. Onderhandenwerk - Betaald bedrag')
            kEdit.addItem('A. Opbrengsten - prognose / aktueel')
            kEdit.addItem('B. Bruto winst werkelijk\n     Meerminderwerk')           
    
            kEdit.activated[str].connect(self.kChanged)
               
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(65)
            zktermEdit.setFont(QFont("Arial", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
            reg_ex = QRegExp("^[2]{1}[0-9]{3}[0-5]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, zktermEdit)
            zktermEdit.setValidator(input_validator)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
             
            grid.addWidget(kEdit, 1, 0, 1, 2, Qt.AlignRight)                     
            lbl1 = QLabel('Jaarweek-uitdraai (jjjjww)')  
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
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
 
            sluitBtn = QPushButton('Sluiten')
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
        ongInvoer()
        zoekwk(m_email)
    elif data[0]:
        keuze = data[0][0]
    else:
        ongInvoer()
        zoekwk(m_email)
    if data[1] and len(data[1]) == 6:
        jrwk = data[1]
        printGrafiek(keuze, jrwk, m_email)
    else:
        ongInvoer()
        zoekwk(m_email)
        
def printGrafiek(keuze, jrwk, m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle('Financieële grafieken externe werken')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
  
            grid = QGridLayout()
            grid.setSpacing(20)
            
            metadata = MetaData()
            resultaten = Table('resultaten', metadata,
                Column('resID', Integer(), primary_key=True),
                Column('statusweek', String),
                Column('btotaal', Float),
                Column('wtotaal', Float),
                Column('betaald_bedrag', Float),
                Column('meerminderwerk', Float),
                Column('onderhandenwerk', Float),
                Column('aanneemsom', Float),
                Column('blonen', Float),
                Column('wlonen', Float),
                Column('bmaterialen', Float),
                Column('wmaterialen', Float),
                Column('bmaterieel', Float),
                Column('wmaterieel', Float),
                Column('bprojectkosten', Float),
                Column('wprojectkosten', Float),
                Column('binhuur', Float),
                Column('winhuur', Float),
                Column('bdiensten', Float),
                Column('wdiensten', Float),
                Column('bruto_winst', Float),
                Column('boekweek', String))
            params = Table('params', metadata,
                Column('paramID', Integer(), primary_key=True),
                Column('tarief', String))
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            
            selpar1 = select([params]).where(params.c.paramID == 97)
            rppar1 = con.execute(selpar1).first()
            bo_incr = rppar1[1]/52  #begrote omzet per week
            selpar2 = select([params]).where(params.c.paramID == 98)
            rppar2 = con.execute(selpar2).first()
            bw_incr = rppar2[1]/52  #begrote winst per week
                                          
            jaar = jrwk[0:4]
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selres = select([resultaten]).where(and_(resultaten.c.boekweek == jrwk,\
              resultaten.c.statusweek.like(jaar+'%'))).order_by(resultaten.c.statusweek)
            rpres = con.execute(selres)
            if keuze == '1':
                s1 = 2
                s2 = 3
                t1 = 'Kosten totaal begroot'
                t2 = 'Kosten totaal werkelijk'
                t3 = 'Kosten totaal '
                c1 = Qt.red
                c2 = Qt.blue
                ysch =  160000000
            elif keuze == '2':
                s1 = 8
                s2 = 9
                t1 = 'Lonen begroot'
                t2 = 'Lonen werkelijk'
                t3 = 'Lonen '
                c1 = Qt.green
                c2 = Qt.darkBlue
                ysch =  100000000
            elif keuze == '3':
                s1 = 10
                s2 = 11
                t1 = 'Materialen begroot'
                t2 = 'Materialen werkelijk'
                t3 = 'Materialen'
                c1 = Qt.cyan
                c2 = Qt.magenta
                ysch =  60000000       
            elif keuze == '4':
                s1 = 12
                s2 = 13
                t1 = 'Materiëel begroot'
                t2 = 'Materiëel werkelijk'
                t3 = 'Materiëel '
                c1 = Qt.darkYellow
                c2 = Qt.darkGreen
                ysch =  20000000
            elif keuze == '5':
                s1 = 16
                s2 = 17
                t1 = 'Inhuur begroot'
                t2 = 'Inhuur werkelijk'
                t3 = 'Inhuur '
                c1 = Qt.darkBlue
                c2 = Qt.darkRed
                ysch =  30000000
            elif keuze == '6':
                s1 = 18
                s2 = 19
                t1 = 'Diensten begroot'
                t2 = 'Diensten werkelijk'
                t3 = 'Diensten '
                c1 = Qt.red
                c2 = Qt.blue
                ysch =  30000000    
            elif keuze == '7':
                s1 = 14
                s2 = 15
                t1 = 'Projektkosten begroot'
                t2 = 'Projektkosten werkelijk'
                t3 = 'Projektkosten '
                c1 = Qt.darkYellow
                c2 = Qt.darkCyan
                ysch =  10000000    
            elif keuze == '8':
                y3 = [0,]
                y3val = 0
                x1 = [0,]
                xval1 = 0
                # prognose winst
                for teller in range(0,53):
                    y3val = y3val+bw_incr
                    y3 = y3 +[(y3val)]
                    xval1 = xval1+1
                    x1 = x1 + [(xval1)]
                s1 = 20
                s2 = 20 
                t1 = 'Bruto winst prognose'
                t2 = 'Bruto winst actueel'
                t3 = 'Bruto winst - prognose / aktueel '
                c1 = Qt.darkCyan
                c2 = Qt.darkMagenta
                ysch =  20000000
            elif keuze == '9':
                s1 = 6
                s2 = 4
                t1 = 'Onderhandenwerk'
                t2 = 'Betaald bedrag'
                t3 = 'Onderhandenwerk - Betaald bedrag '
                c1 = Qt.yellow
                c2 = Qt.green
                ysch =  160000000
            elif keuze == 'A':
                y4 = [0,]
                y4val = 0
                x2 =[0,]
                xval2 = 0
                #prognose omzet
                for teller in range(0,53):
                    y4val = y4val+bo_incr
                    y4 = y4 +[(y4val)]
                    xval2 = xval2+1
                    x2 = x2 + [(xval2)]
                s1 = 7
                s2 = 7
                t1 = 'Omzet prognose'
                t2 = 'Omzet aktueel'
                t3 = 'Omzet '
                c1 = Qt.red
                c2 = Qt.blue
                ysch =  160000000
            elif keuze == 'B':
                s1 = 20
                s2 = 5
                t1 = 'Bruto winst werkelijk'
                t2 = 'Meerminderwerk'
                t3 = 'Bruto winst werkelijk / Meerminderwerk '
                c1 = Qt.darkRed
                c2 = Qt.darkBlue
                ysch =  30000000
      
            x = [0,]
            y1 = [0,]
            y2 = [0,]
            idx = 0
            yval1 = 0
            yval2 = 0
            for row in rpres:
                yval1 = y1[idx]+row[s1]
                y1 = y1 +[(yval1)]
                yval2 = y2[idx]+row[s2]
                y2 = y2 +[(yval2)]
                x = x +[(int(row[1][4:]))]
                idx += 1
  
            series1 = QLineSeries()
            if keuze == '8':
                for t, val in zip(x1, y3):
                    series1.append(int(t), val)
            elif keuze == 'A':
                for t, val in zip(x2, y4):
                    series1.append(int(t), val)
            else:
                for t, val in zip(x, y1):
                    series1.append(int(t), val)
            series2 = QLineSeries()
            for t, val in zip(x, y2):
                series2.append(int(t), val)
               
            chart = QChart()
            chart.addSeries(series1)
            chart.addSeries(series2)
             
            series1.setColor(QColor(c1))
            series2.setColor(QColor(c2))
            series1.setName(t1)
            series2.setName(t2)
            chart.legend().setVisible(True)
         
            font = QFont()
            font.setPixelSize(22)
            chart.setTitleFont(font)
            chart.setTitle(t3+jaar)
            chart.setTitleBrush(QBrush(Qt.black))
            chart.legend().setLabelBrush(QColor(Qt.black))
  
            axisX = QCategoryAxis()
            axisY = QCategoryAxis()
        
            axisX.setTitleText('Jaar '+jaar+' - Weeknummers')
            axisX.setTitleBrush(QBrush(Qt.black))
            font = QFont("Sans Serif")
            axisX.setTitleFont(font)
           
            axisPen = QPen(QColor(100,100,100))    # 100,100,100
            axisPen.setWidth(3)
            axisX.setLinePen(axisPen)
            axisY.setLinePen(axisPen)
        
            axisBrush = QBrush(Qt.black)
            axisX.setLabelsBrush(axisBrush)
            axisY.setLabelsBrush(axisBrush)
      
            axisX.setGridLineVisible(False)
            axisY.setGridLineVisible(True)
            axisX.setShadesBrush(QBrush(QColor(245, 245 , 245)))
            axisX.setShadesVisible(True)
            for x in range(1,54):
                axisX.append(jaar+"-"+("0"+str(x))[-2:], x)
            axisX.setRange(0, 53)
            axisX.setLabelsAngle(-90)
                 
            axisY = QValueAxis()
            axisY.setTickCount(33)
            axisY.setTitleText("Bedragen in Euro")
            axisY.setTitleFont(font)
            axisY.setLabelFormat('%d')
            axisY.setTitleBrush(QBrush(Qt.black))
            axisY.setRange(0,ysch)    #disable for automatic Y scale 
            #axisY.applyNiceNumbers() #enable by automatic Y scale
        
            Lfont = QFont("Sans Serif")         
            Dfont = QFont("Sans Serif")
            Lfont.setPixelSize(10)
            Dfont.setPixelSize(10)
            axisX.setLabelsFont(Dfont)
            axisY.setLabelsFont(Lfont)
            
            axisPen = QPen(QColor('black'))
            axisPen = QPen()
            axisPen.setWidth(2)
            axisX.setLinePen(axisPen)
            axisX.setLabelsColor(QColor('black'))
            axisY.setLinePen(axisPen)
            axisY.setLabelsColor(QColor('black'))
           
            chart.addAxis(axisX, Qt.AlignBottom)
            series1.attachAxis(axisX)
            axisX.setLabelsAngle(-90)
                      
            chart.addAxis(axisY, Qt.AlignLeft)
            series1.attachAxis(axisY)
            series2.attachAxis(axisY)
 
            self.chartView = QChartView(chart)
            self.chartView.setRenderHint(QPainter.Antialiasing)
                     
            buttonPreview = QPushButton('Afdrukvoorbeeld')
            buttonPreview.clicked.connect(self.handle_preview)
            buttonPreview.setStyleSheet("color: black;  background-color: gainsboro")
            buttonPrint = QPushButton('Printen')
            buttonPrint.clicked.connect(self.handle_print)
            buttonPrint.setStyleSheet("color: black;  background-color: gainsboro")
            buttonSluit = QPushButton('Sluiten')
            buttonSluit.clicked.connect(lambda: sluit(self, m_email))
            buttonSluit.setStyleSheet("color: black;  background-color: gainsboro")
            grid.addWidget(self.chartView, 0, 0, 0, 3)
            grid.addWidget(buttonSluit, 1, 0)
            grid.addWidget(buttonPrint, 1, 1)
            grid.addWidget(buttonPreview, 1, 2) 
                       
            self.setLayout(grid)
            self.setGeometry(200, 40, 1395, 930)
            
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
            dialog.paintRequested.connect(self.handle_paint_request)
            dialog.resize(1470, 980)
            #dialog.setMinimumSize(1470, 980)
            dialog.exec_()
    
        def handle_paint_request(self, printer):
            printer.setPageOrientation(QPageLayout.Landscape)
            painter = QPainter(printer)            
            painter.setViewport(self.chartView.rect())
            painter.setWindow(self.chartView.rect()) 
            self.chartView.render(painter)
            painter.end()

    win = Widget()
    win.exec_()
    zoekwk(m_email)