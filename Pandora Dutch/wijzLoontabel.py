from login import hoofdMenu
import  datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton, QComboBox,\
      QDialog, QMessageBox, QWidget, QTableView
from PyQt5.QtGui import QFont, QIcon, QRegExpValidator, QPixmap
from PyQt5.QtCore import Qt,  QRegExp, QAbstractTableModel
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, update

def refresh(keuze, m_email, self):
    self.close()
    loonTabellen(keuze, m_email)

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Loontabel wijzigen')               
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Loontabel wijzigen')               
    msg.exec_() 
   
def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt!')
    msg.setWindowTitle('Loontabel wijzigen')
    msg.exec_()
    
def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Wijzigen Loontabel")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(210)
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.addItem('   Sorteersleutel zoeken')
            k0Edit.addItem('1. Looontabel intern')
            k0Edit.addItem('2. Loontabel extern')
            k0Edit.addItem('3. Loontabel indirekt')
            k0Edit.activated[str].connect(self.k0Changed)
                 
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1 , 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
            grid.addWidget(cancelBtn, 3, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
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
        keuze = 0
    loonTabellen(keuze, m_email)

def loonTabellen(keuze, m_email):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Loonbetalingen opvragen')
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
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.resizeColumnsToContents()
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(wijzLoonschaal)
            grid.addWidget(table_view, 0, 0, 1, 7)
             
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 6, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Verversen')
            freshBtn.clicked.connect(lambda: refresh(keuze, m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 5, 1, 1, Qt.AlignRight |Qt.AlignTop)
        
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 4, 1, 1, Qt.AlignTop)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 0, 1, 7, Qt.AlignCenter | Qt.AlignBottom)
            
            self.setLayout(grid)
            self.setGeometry(500, 100, 950, 800)
            self.setLayout(grid)
    
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
              
    header = ['LoonID', 'Tabeluurloon', 'Werkuurloon', 'Reisuurloon', 'Direct',\
      'Maandloon','Functieomschrijving', 'Wijzigingsdatum']
      
    metadata = MetaData()   
    lonen = Table('lonen', metadata,
        Column('loonID', Integer(), primary_key=True),
        Column('tabelloon', Float),
        Column('werkuur',Float),
        Column('reisuur', Float),
        Column('direct', Boolean),
        Column('maandloon', Float),
        Column('functieomschr', String),
        Column('boekdatum', String))
                       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == 1:
        sellon = select([lonen]).where(lonen.c.loonID > 52).order_by(lonen.c.loonID)
    elif keuze == 2:
        sellon = select([lonen]).where(lonen.c.loonID < 37).order_by(lonen.c.loonID)
    elif keuze == 3:
        sellon = select([lonen]).where(lonen.c.loonID.between(37,52)).order_by(lonen.c.loonID)
    else:
        ongInvoer()
        zoeken(m_email)
     
    if con.execute(sellon).fetchone():
        rplon = con.execute(sellon)
    else:
        geenRecord()
        zoeken(m_email)
        
    data_list=[]
    for row in rplon:
        data_list += [(row)]

    def wijzLoonschaal(idx):
        mloonnr = idx.data()
        if  idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sellon = select([lonen]).where(lonen.c.loonID == mloonnr)
            rplon = con.execute(sellon).first()
    
            class Widget(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(12)
                    
                    self.setWindowTitle("Opvragen / wijzigen loontabellen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 1, 1, 2, Qt.AlignRight) 
                    
                    grid.addWidget(QLabel('Opvragen / wijzigen loontabellen'), 0, 1)
                        
                    self.Loontabelnummer = QLabel()
                    q1Edit = QLineEdit(str(rplon[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setAlignment(Qt.AlignRight)
                    q1Edit.setDisabled(True)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                 
                    self.Omschrijving = QLabel()
                    q2Edit = QLineEdit(rplon[6])
                    q2Edit.setFixedWidth(320)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.textChanged.connect(self.q2Changed)
                    q2Edit.setDisabled(True)
                    
                    self.Maandloon = QLabel()
                    q3Edit = QLineEdit(str(round(float(rplon[5]),2)))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setAlignment(Qt.AlignRight)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.textChanged.connect(self.q3Changed)
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                                               
                    self.Tabelloon = QLabel()
                    q4Edit = QLineEdit(str(round(float(rplon[1]),2)))
                    q4Edit.setFixedWidth(100) 
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.textChanged.connect(self.q4Changed)
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)
                                            
                    self.Werkuurloon = QLabel()
                    q5Edit = QLineEdit('{:12.2f}'.format(rplon[2]))
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setFixedWidth(100)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                  
                    self.Reisuurloon = QLabel()
                    q6Edit = QLineEdit(str(round(float(rplon[3]),2)))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.textChanged.connect(self.q6Changed)
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q6Edit)
                    q6Edit.setValidator(input_validator)
                    
                    lbl1 = QLabel('Loontabelnummer')
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1, 1)
                    
                    lbl2 = QLabel('Functieomschrijving')
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(q2Edit, 2, 1, 1, 2)
                    
                    lbl3 = QLabel('Maandloon')
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(q3Edit, 3, 1)
                              
                    lbl5 = QLabel('Tabeluurloon')
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q4Edit, 4, 1)
                    
                    lbl6 = QLabel('Werkuurloon begroot')
                    grid.addWidget(lbl6, 5, 0)
                    grid.addWidget(q5Edit, 5, 1)
                    
                    lbl7 = QLabel('Reisuurloon begroot')
                    grid.addWidget(lbl7, 6, 0)
                    grid.addWidget(q6Edit, 6, 1)
                    
                    lbl8 = QLabel('Wijzigingsdatum')
                    lbl9 = QLabel(str(rplon[7]))
                    grid.addWidget(lbl8, 7 ,0)
                    grid.addWidget(lbl9, 7, 1)
                           
                    wijzig = QPushButton('Wijzig')
                    wijzig.clicked.connect(self.accept)
            
                    grid.addWidget(wijzig, 8, 1, 1 , 2, Qt.AlignRight)
                    wijzig.setFont(QFont("Arial",10))
                    wijzig.setFixedWidth(100) 
                     
                    sluit = QPushButton('Sluiten')
                    sluit.clicked.connect(self.close)
            
                    grid.addWidget(sluit, 8, 1, 1, 2, Qt.AlignCenter)
                    sluit.setFont(QFont("Arial",10))
                    sluit.setFixedWidth(100)  
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 3, Qt.AlignCenter)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(600, 250, 150, 150)
                    
                def q2Changed(self,text):
                    self.Omschrijving.setText(text)
            
                def q3Changed(self,text):
                    self.Maandloon.setText(text)
            
                def q4Changed(self,text):
                    self.Tabelloon.setText(text)
                                    
                def q6Changed(self,text):
                    self.Reisuurloon.setText(text)
                          
                def returnq2(self):
                    return self.Omschrijving.text()
                
                def returnq3(self):
                    return self.Maandloon.text()
                
                def returnq4(self):
                    return self.Tabelloon.text()
                
                def returnq6(self):
                    return self.Reisuurloon.text()
                        
                @staticmethod
                def getData(parent=None):
                    dialog = Widget()
                    dialog.exec_()
                    return [dialog.returnq2(), dialog.returnq3(), dialog.returnq4(),\
                            dialog.returnq6()]  
                            
            window = Widget()
            data = window.getData()
            if data[0] == '' and data[1]== ''   and data[2] == '' and data[3] =='':
                return()
            if data[0]:
                momschr = data[0]
            else:
                momschr = rplon[6]
            if data[1]:
                mmndloon = float(data[1])
            else:
                mmndloon = rplon[5]
            if data[2]:
                mtabelloon = float(data[2])
            else:
                mtabelloon = rplon[1]
            if data[3]:
                mreisuurloon = float(data[3])
            else:
                mreisuurloon = rplon[3]
                
            mboekd = str(datetime.datetime.now())[0:10] 
            
            updlon = update(lonen).where(lonen.c.loonID==mloonnr)\
                .values(functieomschr=momschr, maandloon = mmndloon, tabelloon = mtabelloon,\
                 reisuur = mreisuurloon, boekdatum = mboekd)
            con.execute(updlon)
            invoerOK()
    
    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)     