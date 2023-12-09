from login import hoofdMenu
import os, csv
from sys import platform
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
            QDialog, QMessageBox, QTableView, QVBoxLayout, QWidget
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp, QAbstractTableModel
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        ForeignKey,  MetaData, create_engine)
from sqlalchemy.sql import select, and_

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def winSluit(self, m_email):
    self.close()
    maandPeriode(m_email)

def ongPeriode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen geldige betaalperiode opgegeven!')
    msg.setWindowTitle('Controle werkuren')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
       
def printGeg(mjrmnd):
    if platform == 'win32':
        filename = '.\\forms\\Uren\\'+str(mjrmnd)+'.txt'
        os.startfile(filename, "print")
    else:
        filename = './forms/Uren/'+str(mjrmnd)+'.txt'
        os.system('lpr '+filename)
        
def selectRow(index):
    #print('Recordnummer is: ', index.row())
    pass
               
def toonGeg(mjrmnd):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 800, 600)
            self.setWindowTitle('Cluster Calculatie')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.setModel(table_model)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(selectRow)
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
            self.font = QFont('Arial', 10)
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
                 
    header = ['Accountnr', 'Voornaam', 'Tussenvoegsel', 'Achternaam', 'Uren', 'Geboekt']
    if platform == 'win32':
        with open('.\\forms\\Uren\\'+str(mjrmnd)+'.csv', newline='') as f:
            fname = csv.reader(f, delimiter='|', quotechar='@')
            
            data_list = []
            for row in fname:
                data_list += [(row)]
    else:
        with open('./forms/Uren/'+str(mjrmnd)+'.csv', newline='') as f:
            fname = csv.reader(f, delimiter='|', quotechar='@')
            
            data_list = []
            for row in fname:
                data_list += [(row)]
     
    win = MyWindow(data_list, header)
    win.exec_()
  
def maandPeriode(m_email):
    import validZt
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Periode opgeven tbv loonspecificaties")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    
            self.setFont(QFont('Arial', 10))
               
            self.Betaalperiode = QLabel()
            betEdit = QLineEdit()
            betEdit.setFixedWidth(100)
            betEdit.setFont(QFont("Arial",10))
            betEdit.textChanged.connect(self.betChanged)
            reg_ex = QRegExp('^[2]{1}[01]{1}[0-9]{2}[-][0-1]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, betEdit)
            betEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
                           
            grid.addWidget(QLabel('Betaalperiode jjjj-mm'), 1, 0)
            grid.addWidget(betEdit, 1, 1)
              
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Uitvoeren')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 1, 1 ,1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 0, 1 ,1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 2, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(400, 300, 150, 150)
                 
        def betChanged(self, text):
            self.Betaalperiode.setText(text)
    
        def returnBetaalperiode(self):
            return self.Betaalperiode.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnBetaalperiode()]
     
    window = Widget()
    data = window.getData()
    if data[0] and validZt.zt(data[0], 20):
        mjrmnd = data[0]
        controleUren(mjrmnd, m_email)
    else:
        ongPeriode()
        maandPeriode(m_email)
  
def controleUren(mjrmnd, m_email):
    mblad = 1
    rgl = 0
    metadata = MetaData()   
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('voornaam', String),
        Column('achternaam', String),
        Column('tussenvoegsel', String))
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('soort', String))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String),
        Column('lock', Boolean))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    selwerkn = select([werknemers, accounts]).where(werknemers.c\
        .accountID == accounts.c.accountID).order_by(werknemers.c.werknemerID)
    rpwerkn = conn.execute(selwerkn)
    selpar = select([params]).where(params.c.item == mjrmnd)
    rppar = conn.execute(selpar).first()
    if not rppar:
          ongPeriode()
          maandPeriode(m_email)
    for record in rpwerkn:
        if rgl == 0 or rgl%57 == 0: 
            if platform == 'win32':
                filename = '.\\forms\\Uren\\'+str(mjrmnd)+'.txt'
                csvfilename = './/forms//Uren//'+str(mjrmnd)+'.csv'
            else:
                filename = './forms/Uren/'+str(mjrmnd)+'.txt'
                csvfilename = './forms/Uren/'+str(mjrmnd)+'.csv' 
            open (csvfilename, "w").write("")
            kop = \
    ("Controle uren tbv loonbetalingen van periode "+str(mjrmnd)+" Pagina "+str(mblad)+"\n"+
     "============================================================\n"
     "Account   Werknemer                        Uren     Gewerkt \n"
     "============================================================\n")
            open(filename, "w").write(kop)
        elif rgl%57 == 0:
            open(filename, 'a').write(kop)
            mblad += 1
        
        uren100 = 0
        verlof = 0
        feestdag = 0
        dokter = 0
        ziek = 0
        geoorlverz = 0
        extraverl = 0
        selwrkwnrln = select([wrkwnrln]).where(and_(record[0]==wrkwnrln.c.werknemerID,\
                wrkwnrln.c.boekdatum.like(mjrmnd+'%')))\
            .order_by(wrkwnrln.c.werknemerID)
        rpwrkwnrln = conn.execute(selwrkwnrln)  
        for rec in rpwrkwnrln:
            if rec[5] == '100%':
                uren100 = uren100+rec[4]
            elif rec[5] == 'Verlof':
                verlof = verlof+rec[4]
            elif rec[5] == 'Extra Verlof':
                extraverl = extraverl+rec[4]
            elif rec[5] == 'Feestdag':
                feestdag = feestdag+rec[4]
            elif rec[5] == 'Geoorl. Verzuim':
                geoorlverz = geoorlverz+rec[4]
            elif rec[5] == 'Ziek':
                ziek = ziek+rec[4]
            elif rec[5] == 'Dokter':
                dokter= dokter+rec[4]
                                                 
        if uren100+verlof+extraverl+feestdag+geoorlverz+ziek+dokter < int(rppar[1]):
            urengemaakt = uren100+verlof+extraverl+feestdag+geoorlverz+ziek+dokter
            gegevens = str(record[2])+' '+"{:8.8}".format(record[3])+' '+"{:16.16}"\
                          .format(record[4])+"{:>12.0f}".format(rppar[1])+\
                          "{:>12.2f}".format(urengemaakt)+'\n'
            open (filename,'a').write(gegevens)
            csvgegevens = str(record[2])+'|'+record[3]+'|'+record[5]\
               +'|'+record[4]+'|'+"{:>12.0f}".format(rppar[1])+'|'+\
               "{:>12.2f}".format(urengemaakt)
            open (csvfilename,'a').write(str(csvgegevens))
            open (csvfilename,'a').write('\n')
            rgl += 1
                            
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Controle uren per periode")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid = QGridLayout()
            grid.setSpacing(20)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
            self.setFont(QFont('Arial', 10))
            
            self.setLayout(grid)
            self.setGeometry(400, 300, 500, 150)
            
            grid.addWidget(QLabel('''
            Deze module dient om het aantal geboekte uren 
            per periode en per werknemer te controleren, 
            voor de definitieve uitdraai wordt gemaakt.
            '''), 1, 0, 1, 3)
             
            toonBtn = QPushButton('Tonen')
            toonBtn.clicked.connect(lambda: toonGeg(mjrmnd))
          
            printBtn = QPushButton('Printen')
            printBtn.clicked.connect(lambda: printGeg(mjrmnd))
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: winSluit(self, m_email))
            
            grid.addWidget(toonBtn, 3, 2)
            toonBtn.setFont(QFont("Arial",10))
            toonBtn.setFixedWidth(120)
            toonBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(printBtn, 3, 1)
            printBtn.setFont(QFont("Arial",10))
            printBtn.setFixedWidth(120)
            printBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(cancelBtn, 3, 0)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(120)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
          
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
            
    window = Widget()
    window.exec_()