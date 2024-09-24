from login import hoofdMenu
import datetime
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QLabel, QPushButton,QGridLayout,\
     QMessageBox, QDialog, QLineEdit 

def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0                       
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11
   if checkdigit == 10:
            checkdigit = 0
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def bepaalWerknr():
    from sqlalchemy import (Table, Column, Integer, MetaData, create_engine)
    from sqlalchemy.sql import select, func
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    try:
        mwerknr=(conn.execute(select([func.max(werken.c.werknummerID,\
                type_=Integer)])).scalar())
        mwerknr=int(maak11proef(mwerknr))
    except:
        mwerknr = 800000006
    return(mwerknr)

def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def foutInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Required fields\nnot all entered!')
    msg.setWindowTitle('Incorrect Input')
    msg.exec_()
   
def Invoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Work number data')
    msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def invWerk(m_email):                                   
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Input works")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                                                 
            self.Omschrijving = QLabel()
            q1Edit = QLineEdit()
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed) 
            reg_ex = QRegExp("^.{0,49}$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
                            
            self.Aanneemsom = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(150)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)

            self.Huisvesting = QLabel()
            q5Edit = QLineEdit()
            q5Edit.setFixedWidth(150)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            self.Leiding = QLabel()
            q6Edit = QLineEdit()
            q6Edit.setFixedWidth(150)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
            
            self.Inhuur = QLabel()
            q7Edit = QLineEdit()
            q7Edit.setFixedWidth(150)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
            
            self.Vervoer = QLabel()
            q8Edit = QLineEdit()
            q8Edit.setFixedWidth(150)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
            
            self.Grondverzet = QLabel()
            q11Edit = QLineEdit()
            q11Edit.setFixedWidth(150)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.textChanged.connect(self.q11Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q11Edit)
            q11Edit.setValidator(input_validator)
            
            self.Overig = QLabel()
            q12Edit = QLineEdit()
            q12Edit.setFixedWidth(150)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.textChanged.connect(self.q12Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q12Edit)
            q12Edit.setValidator(input_validator)

            self.StartWerk = QLabel()
            q23Edit = QLineEdit()
            q23Edit.setFixedWidth(80)
            q23Edit.setFont(QFont("Arial",10))
            q23Edit.textChanged.connect(self.q23Changed) 
            reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}[0-5]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, q23Edit)
            q23Edit.setValidator(input_validator)
         
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl1 = QLabel('Work number')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            
            lbl2 = QLabel(str(bepaalWerknr()))
            grid.addWidget(lbl2, 1, 1)
                   
            lbl3 = QLabel('Description')
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 2, 0)
            grid.addWidget(q1Edit, 2, 1, 1, 3)

            lbl4 = QLabel('Contract price')
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 3, 0)
            grid.addWidget(q2Edit, 3, 1)

            lbl7 = QLabel('Provisional Work / Provisional Sum')
            lbl7.setStyleSheet("font: 12pt Comic Sans MS; color: #000000")
            lbl7.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl7, 4, 0, 1, 4)

            lbl7 = QLabel('Housing')
            lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl7, 5, 0)
            grid.addWidget(q5Edit, 5, 1)
            
            lbl8 = QLabel('Direction')
            lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl8, 6, 0)
            grid.addWidget(q6Edit, 6, 1)
            
            lbl9 = QLabel('Hiring')
            lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl9, 7, 0)
            grid.addWidget(q7Edit, 7, 1)
            
            lbl10 = QLabel('Transport')
            lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl10, 5, 2)
            grid.addWidget(q8Edit, 5, 3)
            
            lbl13 = QLabel('Earth moving')
            lbl13.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl13, 6, 2)
            grid.addWidget(q11Edit, 6, 3)
            
            lbl14 = QLabel('Remaining')
            lbl14.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl14, 7, 2)
            grid.addWidget(q12Edit, 7, 3)
            
            lblwk = QLabel('Status-YearWeek')
            lblwk.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lblwk, 1, 2)
            
            lblst = QLabel('A  '+str(jaarweek()))
            grid.addWidget(lblst, 1, 3)

            lbl25 = QLabel('Startweek work')
            lbl25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl25, 3, 2)
            grid.addWidget(q23Edit, 3, 3)
           
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1 , 1, Qt.AlignRight )
                                            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 11, 0, 1, 4, Qt.AlignCenter)
              
            self.setLayout(grid)
            self.setGeometry(600, 100, 150, 150)
    
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 14, 3, 1, 1, Qt.AlignCenter)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(120)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            sluitBtn = QPushButton('Close')
            sluitBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(sluitBtn, 14, 2, 1, 1, Qt.AlignRight)
            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(120)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                 
        def q1Changed(self,text):
            self.Omschrijving.setText(text)
    
        def q2Changed(self,text):
            self.Aanneemsom.setText(text)

        def q5Changed(self,text):
            self.Huisvesting.setText(text)
            
        def q6Changed(self,text):
            self.Leiding.setText(text)
            
        def q7Changed(self,text):
            self.Inhuur.setText(text)
            
        def q8Changed(self,text):
            self.Vervoer.setText(text)

        def q11Changed(self,text):
            self.Grondverzet.setText(text)
            
        def q12Changed(self,text):
            self.Overig.setText(text)

        def q23Changed(self,text):
            self.StartWerk.setText(text)
                 
        def returnq1(self):
            return self.Omschrijving.text()
        
        def returnq2(self):
            return self.Aanneemsom.text()
        
        def returnq5(self):
            return self.Huisvesting.text()
    
        def returnq6(self):
            return self.Leiding.text()
        
        def returnq7(self):
            return self.Inhuur.text()
              
        def returnq8(self):
            return self.Vervoer.text()

        def returnq11(self):
            return self.Grondverzet.text()
        
        def returnq12(self):
            return self.Overig.text()
        
        def returnq23(self):
            return self.StartWerk.text()
     
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnq1(), dialog.returnq2(),dialog.returnq5(), dialog.returnq6(),\
                    dialog.returnq7(), dialog.returnq8(), dialog.returnq11(), dialog.returnq12(),dialog.returnq23()]
                          
    window = Widget()
    data = window.getData()
    if data[0]:
        ms0 = str(data[0])
    else:
        foutInvoer()
        invWerk(m_email)
    if data[1]:
        mf1 = float(data[1])
    else:
        mf1 = 0
    if data[2]:
        mf2 = float(data[2])
    else:
        mf2 = 0   
    if data[3]:
        mf3 = float(data[3])
    else:
        mf3 = 0
    if data[4]:
        mf4 = float(data[4])
    else:
        mf4 = 0
    if data[5]:
        mf5 = float(data[5])
    else:
        mf5 = 0
    if data[6]:
        mf6 = float(data[6])
    else:
        mf6 = 0
    if data[7]:
        mf7 = float(data[7])
    else:
        mf7 = 0
    if data[8]:
        mf8 = str(data[8])
    else:
        mf8 = ''
        
    from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine, Float)
    from sqlalchemy.sql import insert
    
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True),
        Column('werkomschrijving', String(50)),
        Column('voortgangstatus', String(1)),
        Column('statusweek',  String(6)),
        Column('aanneemsom', Float),
        Column('begr_materialen', Float),
        Column('begr_materieel', Float),
        Column('begr_huisv', Float),
        Column('begr_leiding', Float),
        Column('begr_inhuur', Float),
        Column('begr_vervoer', Float),
        Column('begr_beton_bvl', Float),
        Column('begr_kabelwerk', Float),
        Column('begr_grondverzet', Float),
        Column('begr_overig', Float),
        Column('begr_constr_uren', Float),
        Column('begr_mont_uren', Float),
        Column('begr_retourlas_uren', Float),
        Column('begr_telecom_uren', Float),
        Column('begr_bfi_uren', Float),
        Column('begr_bvl_uren', Float),
        Column('begr_spoorleg_uren', Float),
        Column('begr_spoorlas_uren', Float),
        Column('begr_reis_uren', Float),
        Column('begr_lonen', Float),
        Column('startweek', String))
               
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    metadata.create_all(engine)
    conn = engine.connect()
    inswrk = insert(werken).values(
    werknummerID=bepaalWerknr(),  
    werkomschrijving=ms0,
    voortgangstatus='A',
    statusweek=jaarweek(),
    aanneemsom=mf1,
    begr_huisv=mf2,
    begr_leiding=mf3,
    begr_inhuur=mf4,
    begr_vervoer=mf5,
    begr_grondverzet=mf6,
    begr_overig=mf7,
    startweek=mf8)
     
    result = conn.execute(inswrk)
    inswrk.bind = engine
    result.inserted_primary_key
    result.close
    conn.close
    Invoer() 
    invWerk(m_email)