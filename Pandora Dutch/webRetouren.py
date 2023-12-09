from login import hoofdMenu
import datetime
from PyQt5.QtGui import  QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QWidget, QTableView, QComboBox, QMessageBox,\
          QGridLayout, QDialog, QPushButton, QLabel, QLineEdit,QCheckBox
from sqlalchemy import (Table, Column, Integer, Float, String, MetaData,\
                                create_engine)
from sqlalchemy.sql import select, update

def refresh(m_email, keuze, self):
    self.close()
    toonRetouren(m_email, keuze) 

def windowSluit(m_email, self):
    self.close()
    hoofdMenu(m_email)

def betalingGeboekt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Betaling is geboekt!')
    msg.setWindowTitle('RETOURBETALING')               
    msg.exec_() 

def retKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen Webretouren")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem(' Sorteersleutel voor zoeken')
            k0Edit.addItem('1. Gesorteerd op e-mailadres')
            k0Edit.addItem('2. Gefilterd niet betaald')
            k0Edit.addItem('3. Gefilterd betaald')
            k0Edit.activated[str].connect(self.k0Changed)
                   
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0, 1 ,2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 2, Qt.AlignRight)
                                  
            grid.addWidget(k0Edit, 2, 1, 1, 2)
                       
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3)
        
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 5, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            closeBtn = QPushButton('Sluiten')
            closeBtn.clicked.connect(lambda: windowSluit(m_email, self))
    
            grid.addWidget(closeBtn, 5, 1, 1, 1)
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def returnk0(self):
            return self.Keuze.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0()] 
        
    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        retKeuze(m_email)
    toonRetouren(m_email, keuze)
                    
def toonRetouren(m_email, keuze):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Webretouren betalen/ opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0, 1, 8)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 7, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Verversen')
            freshBtn.clicked.connect(lambda: refresh(m_email, keuze, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 6, 1, 1, Qt.AlignRight)
            
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 5)
          
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 1, 1, 5, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(50, 50, 1050, 900)
    
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
  
    header = ['Retournummer','E-mailadres', 'Bedrag','Rekeningnummer', 'Artikelnummer',\
              'Aantal','Ordernummer','Betaald', 'Boeking']
    
    metadata = MetaData()              
    webretouren = Table('webretouren', metadata,
        Column('retourID', Integer(), primary_key=True),
        Column('e_mail', String),
        Column('bedrag', Float),
        Column('rekening', String),
        Column('artikelID', Integer),
        Column('aantal', Float),
        Column('ordernummer', Integer),
        Column('betaald', String),
        Column('boeking', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    if keuze == 1:
        sel = select([webretouren]).order_by(webretouren.c.e_mail)
    elif keuze == 2:
        sel = select([webretouren]).where(webretouren.c.betaald == '')\
         .order_by(webretouren.c.e_mail.asc()) 
    elif keuze == 3:
        sel = select([webretouren]).where(webretouren.c.betaald != '').\
         order_by(webretouren.c.betaald)
    else:
        sel = select([webretouren]).order_by(webretouren.c.e_mail)
        
    rp = con.execute(sel)
     
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        mretnr = idx.data()
        if idx.column() == 0:
            
            header = ['Retournummer','E-mailadres', 'Bedrag','Rekeningnummer', 'Artikelnummer',\
                  'Aantal','Ordernummer','Betaald', 'Boeking']
            
            metadata = MetaData()              
            webretouren = Table('webretouren', metadata,
                Column('retourID', Integer(), primary_key=True),
                Column('e_mail', String),
                Column('bedrag', Float),
                Column('rekening', String),
                Column('artikelID', Integer),
                Column('aantal', Float),
                Column('ordernummer', Integer),
                Column('betaald', String),
                Column('boeking', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
              
            sel = select([webretouren]).where(webretouren.c.retourID == mretnr)
            rpret = con.execute(sel).first()
            mbet = rpret[7]
               
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                     
                    self.setWindowTitle("Retouren Webartikelen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Retouren Webartikelen'),0, 1, 1, 2)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignRight)    
                    
                    index = 1
                    for item in header:
                        self.lbl = QLabel(header[index-1])
                        if type(rpret[index-1]) == float:
                            q1Edit = QLineEdit('{:12.2f}'.format(rpret[index-1]))
                            q1Edit.setAlignment(Qt.AlignRight)
                        elif type(rpret[index-1]) == int:
                            q1Edit = QLineEdit(str(rpret[index-1]))
                            q1Edit.setAlignment(Qt.AlignRight)
                        else:
                            q1Edit = QLineEdit(str(rpret[index-1]))
                        q1Edit.setFixedWidth(200)
                        q1Edit.setDisabled(True)
                        q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        grid.addWidget(self.lbl, index, 0)
                        grid.addWidget(q1Edit, index, 1)
                        index +=1
                        
                    cBox = QCheckBox('Betalen')
                    if mbet:
                        cBox.setDisabled(True)
                    cBox.stateChanged.connect(self.cBoxChanged)
                    grid.addWidget(cBox, index -1, 2)
                         
                    retourBtn = QPushButton('OK')
                    retourBtn.clicked.connect(self.accept)
                    
                    grid.addWidget(retourBtn, index+1, 2)
                    retourBtn.setFont(QFont("Arial",10))
                    retourBtn.setFixedWidth(100)  
                    retourBtn.setStyleSheet("color: black;  background-color: gainsboro")
                   
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), index+2, 0, 1, 3, Qt.AlignCenter)
                    
                    self.setLayout(grid)
                    self.setGeometry(100, 150, 150, 150)
       
                state = False
                def cBoxChanged(self, state):
                    if state == Qt.Checked:
                        self.state = True                    
                    
                def returncBox(self):
                      return self.state
                       
                @staticmethod
                def getData(parent=None):
                    dialog = MainWindow()
                    dialog.exec_()
                    return [dialog.returncBox()] 
                
            mainWin = MainWindow()
            data = mainWin.getData()
                 
            if data[0] and not mbet:
                upd = update(webretouren).where(webretouren.c.retourID == mretnr).\
                 values(betaald = str(datetime.datetime.now())[0:10])
                con.execute(upd) 
                betalingGeboekt()
           
    win = MyWindow(data_list, header)
    win.exec_()
    retKeuze(m_email)