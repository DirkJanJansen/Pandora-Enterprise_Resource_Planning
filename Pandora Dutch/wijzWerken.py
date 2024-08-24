from login import hoofdMenu
import datetime
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QLabel, QPushButton,QGridLayout,\
     QMessageBox, QDialog, QLineEdit, QCheckBox
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine, Float)
from sqlalchemy.sql import select, update

def _11check(mwerknr):
    number = str(mwerknr)
    total = 0       
    fullnumber = number                       
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total % 11
    if checkdigit == 10:
        checkdigit = 0
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False
    
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
        msg.setText('Verplichte velden\nniet allen ingevoerd!')
        msg.setWindowTitle('INVOERFOUT')
        msg.exec_()
      
def foutWerknr():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Werknummer niet gevonden\nWerknummer bestaat niet!')
    msg.setWindowTitle('Wijzigen Werken!')
    msg.exec_()
    
def werkGereed():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Werknummer is afgemeld,\nboekingen niet meer mogelijk!')
    msg.setWindowTitle('Wijzigen Werken!')
    msg.exec_()
    
def updateOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Je gegevens zijn aangepast!')
    msg.setWindowTitle('Wijzigen Werken!')
    msg.exec_()
       
def winSluit(self, m_email):
    self.close()
    zoekWerk(m_email)
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
             
def zoekWerk(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Werken Wijzigen.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Werknummer = QLabel()
            werknEdit = QLineEdit()
            werknEdit.setFixedWidth(100)
            werknEdit.setFont(QFont("Arial",10))
            werknEdit.textChanged.connect(self.werknChanged)
            reg_ex = QRegExp('^[8]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, werknEdit)
            werknEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
         
            grid.addWidget(QLabel('Werknummer'), 1, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(werknEdit, 1, 1)
            
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                     
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
           
            grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1 , 2, Qt.AlignCenter)
                        
            self.setLayout(grid)
            self.setGeometry(300, 300, 150, 150)
    
        def werknChanged(self, text):
            self.Werknummer.setText(text)
    
        def returnwerkn(self):
            return self.Werknummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnwerkn()]
    
    window = Widget()
    data = window.getData()
    import validZt
    if validZt.zt(data[0], 8):
        mwerknr = int(data[0])
    else:
        foutWerknr()
        zoekWerk(m_email)
        
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True),
        Column('voortgangstatus', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    s = select([werken]).where(werken.c.werknummerID == mwerknr)
    rp = conn.execute(s).first()
    if not rp:
        foutWerknr()
        zoekWerk(m_email)
    elif rp[1] == 'H':
        werkGereed()
        zoekWerk(m_email)
    else:
        wijzWerk(mwerknr, m_email)
 
def wijzWerk(mwerknr, m_email):
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
        Column('begr_voeding_uren', Float),
        Column('begr_lonen', Float),
        Column('startweek', String),
        Column('betaald_bedrag', Float),
        Column('meerminderwerk', Float),
        Column('kosten_materialen', Float),
        Column('kosten_lonen', Float),
        Column('kosten_materieel', Float),
        Column('kosten_leiding', Float),
        Column('kosten_huisv', Float),
        Column('kosten_overig', Float),
        Column('kosten_vervoer', Float),
        Column('kosten_inhuur', Float),
        Column('beton_bvl', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('opdracht_datum', String))
               
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
    rpwerk = conn.execute(selwerk).first()
                                          
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Wijzig begroting werk")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                  
            self.setFont(QFont('Arial', 10))
                                               
            self.Omschrijving = QLabel()
            q1Edit = QLineEdit(rpwerk[1])
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed) 
            reg_ex = QRegExp("^.{0,49}$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
                            
            self.Aanneemsom = QLabel()
            q2Edit = QLineEdit(str(round(float(rpwerk[4]),2)))
            q2Edit.setFixedWidth(150)
            q2Edit.setAlignment(Qt.AlignRight)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
             
            self.Materialen = QLabel()
            q3Edit = QLineEdit(str(round(float(rpwerk[5]),2)))
            q3Edit.setFixedWidth(150)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.setAlignment(Qt.AlignRight)
            q3Edit.textChanged.connect(self.q3Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Materieel = QLabel()
            q4Edit = QLineEdit(str(round(float(rpwerk[6]),2)))
            q4Edit.setFixedWidth(150)
            q4Edit.setAlignment(Qt.AlignRight)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            self.Huisvesting = QLabel()
            q5Edit = QLineEdit(str(round(float(rpwerk[7]),2)))
            q5Edit.setFixedWidth(150)
            q5Edit.setAlignment(Qt.AlignRight)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            self.Leiding = QLabel()
            q6Edit = QLineEdit(str(round(float(rpwerk[8]),2)))
            q6Edit.setFixedWidth(150)
            q6Edit.setAlignment(Qt.AlignRight)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
            
            self.Inhuur = QLabel()
            q7Edit = QLineEdit(str(round(float(rpwerk[9]),2)))
            q7Edit.setFixedWidth(150)
            q7Edit.setAlignment(Qt.AlignRight)
            q7Edit.setFont(QFont("Arial",10))
            q7Edit.textChanged.connect(self.q7Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q7Edit)
            q7Edit.setValidator(input_validator)
            
            self.Vervoer = QLabel()
            q8Edit = QLineEdit(str(round(float(rpwerk[10]),2)))
            q8Edit.setFixedWidth(150)
            q8Edit.setAlignment(Qt.AlignRight)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.textChanged.connect(self.q8Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q8Edit)
            q8Edit.setValidator(input_validator)
            
            self.Betonwerk = QLabel()
            q9Edit = QLineEdit(str(round(float(rpwerk[11]),2)))
            q9Edit.setFixedWidth(150)
            q9Edit.setAlignment(Qt.AlignRight)
            q9Edit.setFont(QFont("Arial",10))
            q9Edit.textChanged.connect(self.q9Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q9Edit)
            q9Edit.setValidator(input_validator)
            
            self.Kabelwerk = QLabel()
            q10Edit = QLineEdit(str(round(float(rpwerk[12]),2)))
            q10Edit.setFixedWidth(150)
            q10Edit.setAlignment(Qt.AlignRight)
            q10Edit.setFont(QFont("Arial",10))
            q10Edit.textChanged.connect(self.q10Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q10Edit)
            q10Edit.setValidator(input_validator)
            
            self.Grondverzet = QLabel()
            q11Edit = QLineEdit(str(round(float(rpwerk[13]),2)))
            q11Edit.setFixedWidth(150)
            q11Edit.setAlignment(Qt.AlignRight)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.textChanged.connect(self.q11Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q11Edit)
            q11Edit.setValidator(input_validator)
            
            self.Overig = QLabel()
            q12Edit = QLineEdit(str(round(float(rpwerk[14]),2)))
            q12Edit.setFixedWidth(150)
            q12Edit.setAlignment(Qt.AlignRight)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.textChanged.connect(self.q12Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q12Edit)
            q12Edit.setValidator(input_validator) 
                 
            self.Uren_Construktie = QLabel()
            q13Edit = QLineEdit(str(round(float(rpwerk[15]),2)))
            q13Edit.setFixedWidth(150)
            q13Edit.setAlignment(Qt.AlignRight)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.setDisabled(True)
            q13Edit.textChanged.connect(self.q13Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q13Edit)
            q13Edit.setValidator(input_validator)
            
            self.Uren_Montage = QLabel()
            q14Edit = QLineEdit(str(round(float(rpwerk[16]),2)))
            q14Edit.setFixedWidth(150)
            q14Edit.setAlignment(Qt.AlignRight)
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.setDisabled(True)
            q14Edit.textChanged.connect(self.q14Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q14Edit)
            q14Edit.setValidator(input_validator)
               
            self.Uren_Retourlas = QLabel()
            q15Edit = QLineEdit(str(round(float(rpwerk[17]),2)))
            q15Edit.setFixedWidth(150)
            q15Edit.setAlignment(Qt.AlignRight)
            q15Edit.setFont(QFont("Arial",10))
            q15Edit.setDisabled(True)
            q15Edit.textChanged.connect(self.q15Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q15Edit)
            q15Edit.setValidator(input_validator)
            
            self.Uren_Telecom = QLabel()
            q16Edit = QLineEdit(str(round(float(rpwerk[18]),2)))
            q16Edit.setFixedWidth(150)
            q16Edit.setAlignment(Qt.AlignRight)
            q16Edit.setFont(QFont("Arial",10))
            q16Edit.setDisabled(True)
            q16Edit.textChanged.connect(self.q16Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q16Edit)
            q16Edit.setValidator(input_validator)
            
            self.Uren_Bfi = QLabel()
            q17Edit = QLineEdit(str(round(float(rpwerk[19]),2)))
            q17Edit.setFixedWidth(150)
            q17Edit.setAlignment(Qt.AlignRight)
            q17Edit.setFont(QFont("Arial",10))
            q17Edit.setDisabled(True)
            q17Edit.textChanged.connect(self.q17Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q17Edit)
            q17Edit.setValidator(input_validator)
               
            self.Uren_Bvl = QLabel()
            q18Edit = QLineEdit(str(round(float(rpwerk[20]),2)))
            q18Edit.setFixedWidth(150)
            q18Edit.setFont(QFont("Arial",10))
            q18Edit.setDisabled(True)
            q18Edit.setAlignment(Qt.AlignRight)
            q18Edit.textChanged.connect(self.q17Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q18Edit)
            q18Edit.setValidator(input_validator)
                    
            self.Uren_Spoorleg = QLabel()
            q19Edit = QLineEdit(str(round(float(rpwerk[21]),2)))
            q19Edit.setFixedWidth(150)
            q19Edit.setAlignment(Qt.AlignRight)
            q19Edit.setFont(QFont("Arial",10))
            q19Edit.setDisabled(True)
            q19Edit.textChanged.connect(self.q19Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q19Edit)
            q19Edit.setValidator(input_validator)
            
            self.Uren_Spoorlas = QLabel()
            q20Edit = QLineEdit(str(round(float(rpwerk[22]),2)))
            q20Edit.setFixedWidth(150)
            q20Edit.setAlignment(Qt.AlignRight)
            q20Edit.setFont(QFont("Arial",10))
            q20Edit.setDisabled(True)
            q20Edit.textChanged.connect(self.q20Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q20Edit)
            q20Edit.setValidator(input_validator)
            
            self.Uren_Voeding = QLabel()
            q21Edit = QLineEdit(str(round(float(rpwerk[23]),2)))
            q21Edit.setFixedWidth(150)
            q21Edit.setAlignment(Qt.AlignRight)
            q21Edit.setFont(QFont("Arial",10))
            q21Edit.setDisabled(True)
            q21Edit.textChanged.connect(self.q21Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q21Edit)
            q21Edit.setValidator(input_validator)
            
            self.Begroot_Lonen = QLabel()
            q22Edit = QLineEdit(str(round(float(rpwerk[24]),2)))
            q22Edit.setFixedWidth(150)
            q22Edit.setAlignment(Qt.AlignRight)
            q22Edit.setFont(QFont("Arial",10))
            q22Edit.textChanged.connect(self.q22Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q22Edit)
            q22Edit.setValidator(input_validator)
            
            self.StartWerk = QLabel()
            q23Edit = QLineEdit(str(rpwerk[25]))
            q23Edit.setFixedWidth(80)
            q23Edit.setFont(QFont("Arial",10))
            q23Edit.textChanged.connect(self.q23Changed) 
            reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}[0-5]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, q23Edit)
            q23Edit.setValidator(input_validator)
            
            self.Betaald = QLabel()
            q24Edit = QLineEdit(str(round(float(rpwerk[26]),2)))
            q24Edit.setFixedWidth(150)
            q24Edit.setAlignment(Qt.AlignRight)
            q24Edit.setFont(QFont("Arial",10))
            q24Edit.textChanged.connect(self.q24Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q24Edit)
            q24Edit.setValidator(input_validator)
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl1 = QLabel('Werknummer')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            
            lbl2 = QLabel(str(mwerknr))
            grid.addWidget(lbl2, 1, 1)
                   
            lbl3 = QLabel('Omschrijving')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 2, 0)
            grid.addWidget(q1Edit, 2, 1, 1, 3) # RowSpan 1 ,ColumnSpan 3
                                                 
            lbl4 = QLabel('Aanneemsom')  
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 3, 0)
            grid.addWidget(q2Edit, 3, 1)
            
            lbl5 = QLabel('Materialen')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 4, 0)
            grid.addWidget(q3Edit, 4, 1)
            
            lbl6 = QLabel('Materieel')  
            lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl6, 5, 0)
            grid.addWidget(q4Edit, 5, 1)
            
            lbl7 = QLabel('Huisvesting')  
            lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl7, 6, 0)
            grid.addWidget(q5Edit, 6, 1)
            
            lbl8 = QLabel('Leiding')  
            lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl8, 7, 0)
            grid.addWidget(q6Edit, 7, 1)
            
            lbl9 = QLabel('Inhuur')  
            lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl9, 8, 0)
            grid.addWidget(q7Edit, 8, 1)
            
            lbl10 = QLabel('Vervoer')  
            lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl10, 9, 0)
            grid.addWidget(q8Edit, 9, 1)
            
            lbl11 = QLabel('Betonwerk')  
            lbl11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl11, 10, 0)
            grid.addWidget(q9Edit, 10, 1)
                
            lbl12 = QLabel('Kabelwerk')  
            lbl12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl12, 11, 0)
            grid.addWidget(q10Edit, 11, 1)
            
            lbl13 = QLabel('Grondverzet')  
            lbl13.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl13, 12, 0)
            grid.addWidget(q11Edit, 12, 1)
            
            lbl14 = QLabel('Overig')  
            lbl14.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl14, 13, 0)
            grid.addWidget(q12Edit, 13, 1)
            
            lblwk = QLabel('Status-JaarWeek')
            lblwk.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lblwk, 1,2)
            
            lblst = QLabel(rpwerk[2]+'  '+rpwerk[3])
            grid.addWidget(lblst,1,3)
               
            lbl15 = QLabel('Uren_Construktie')  
            lbl15.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl15, 3, 2)
            grid.addWidget(q13Edit, 3, 3)
         
            lbl16 = QLabel('Uren_Montage')  
            lbl16.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl16, 4, 2)
            grid.addWidget(q14Edit, 4, 3)
            
            lbl17 = QLabel('Uren_Retourlas')  
            lbl17.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl17, 5, 2)
            grid.addWidget(q15Edit, 5, 3)
            
            lbl18 = QLabel('Uren_Telecom')  
            lbl18.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl18, 6, 2)
            grid.addWidget(q16Edit, 6, 3)
            
            lbl19 = QLabel('Uren_Bfi')  
            lbl19.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl19, 7, 2)
            grid.addWidget(q17Edit, 7, 3)
            
            lbl20 = QLabel('Uren_Bvl')  
            lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl20, 8, 2)
            grid.addWidget(q18Edit, 8, 3)
              
            lbl21 = QLabel('Uren_Spoorleg')  
            lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl21, 9, 2)
            grid.addWidget(q19Edit, 9, 3)
            
            lbl22 = QLabel('Uren_Spoorlas')  
            lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl22, 10, 2)
            grid.addWidget(q20Edit, 10, 3)
            
            lbl23 = QLabel('Uren_Voeding')  
            lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl23, 11, 2)
            grid.addWidget(q21Edit, 11, 3)
            
            lbl24 = QLabel('Begroot_Lonen')  
            lbl24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl24, 12, 2)
            grid.addWidget(q22Edit, 12, 3)
            
            lbl25 = QLabel('Startweek werk')
            lbl25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl25, 13, 2)
            grid.addWidget(q23Edit, 13, 3)
  
            lbl26 = QLabel('Cumulatief betaald')  
            lbl26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl26, 14, 0)
            grid.addWidget(q24Edit, 14, 1)
            
            lbl27 = QLabel('Opdrachtdatum')
            grid.addWidget(lbl27, 15, 0, 1, 1, Qt.AlignRight)
            lbl28 =QLabel(rpwerk[39])
            grid.addWidget(lbl28, 15, 1)
            
            cBox1 = QCheckBox('Meerwerk akkoord')
            cBox1.stateChanged.connect(self.cBox1Changed)
            if rpwerk[2] != 'F':
                cBox1.setDisabled(True)
            grid.addWidget(cBox1, 14, 2)
            
            cBox = QCheckBox('Werk Afgemeld')
            cBox.stateChanged.connect(self.cBoxChanged)
            if rpwerk[2] != 'G':
                cBox.setDisabled(True)
            grid.addWidget(cBox, 14, 3)
           
            cBox2 = QCheckBox('Opdracht')
            cBox2.stateChanged.connect(self.cBox2Changed)
            if rpwerk[39]:
                cBox2.setDisabled(True)
            grid.addWidget(cBox2, 15, 2) 
                       
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
                                            
            grid.addWidget(QLabel('       \u00A9 2017 all rights reserved dj.jansen@casema.nl'), 17, 0, 1, 3, Qt.AlignRight)
              
            self.setLayout(grid)
            self.setGeometry(100, 100, 150, 150)
    
            applyBtn = QPushButton('Wijzigen')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 16, 3, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: winSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 16, 2, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                       
        def q1Changed(self,text):
            self.Omschrijving.setText(text)
    
        def q2Changed(self,text):
            self.Aanneemsom.setText(text)
    
        def q3Changed(self,text):
            self.Materialen.setText(text)
     
        def q4Changed(self,text):
            self.Materieel.setText(text)
            
        def q5Changed(self,text):
            self.Huisvesting.setText(text)
            
        def q6Changed(self,text):
            self.Leiding.setText(text)
            
        def q7Changed(self,text):
            self.Inhuur.setText(text)
            
        def q8Changed(self,text):
            self.Vervoer.setText(text)
        
        def q9Changed(self,text):
            self.Betonwerk.setText(text)
            
        def q10Changed(self,text):
            self.Kabelwerk.setText(text)
               
        def q11Changed(self,text):
            self.Grondverzet.setText(text)
            
        def q12Changed(self,text):
            self.Overig.setText(text)
            
        def q13Changed(self,text):
            self.Uren_Construktie.setText(text)
            
        def q14Changed(self,text):
            self.Uren_Montage.setText(text)
            
        def q15Changed(self,text):
            self.Uren_Retourlas.setText(text)
            
        def q16Changed(self,text):
            self.Uren_Telecom.setText(text)
            
        def q17Changed(self,text):
            self.Uren_Bfi.setText(text)
            
        def q18Changed(self,text):
            self.Uren_Bvl.setText(text)
            
        def q19Changed(self,text):
            self.Uren_Spoorleg.setText(text)
            
        def q20Changed(self,text):
            self.Uren_Spoorlas.setText(text)
            
        def q21Changed(self,text):
            self.Uren_Voeding.setText(text)
            
        def q22Changed(self,text):
            self.Begroot_Lonen.setText(text)
            
        def q23Changed(self,text):
            self.StartWerk.setText(text)
                
        def q24Changed(self,text):
            self.Betaald.setText(text)
            
        state = False  
        def cBoxChanged(self, state):
            if state == Qt.Checked:
                self.state = True

        state1 = False  
        def cBox1Changed(self, state1):
            if state1 == Qt.Checked:
                self.state1 = True

        state2 = False  
        def cBox2Changed(self, state2):
            if state2 == Qt.Checked:
                self.state2 = True

        def returnq1(self):
            return self.Omschrijving.text()
        
        def returnq2(self):
            return self.Aanneemsom.text()
        
        def returnq3(self):
            return self.Materialen.text()
        
        def returnq4(self):
            return self.Materieel.text()
    
        def returnq5(self):
            return self.Huisvesting.text()
    
        def returnq6(self):
            return self.Leiding.text()
        
        def returnq7(self):
            return self.Inhuur.text()
              
        def returnq8(self):
            return self.Vervoer.text()
        
        def returnq9(self):
            return self.Betonwerk.text()
        
        def returnq10(self):
            return self.Kabelwerk.text()
        
        def returnq11(self):
            return self.Grondverzet.text()
        
        def returnq12(self):
            return self.Overig.text()
        
        def returnq13(self):
            return self.Uren_Construktie.text()
        
        def returnq14(self):
            return self.Uren_Montage.text()
        
        def returnq15(self):
            return self.Uren_Retourlas.text()
        
        def returnq16(self):
            return self.Uren_Telecom.text()
        
        def returnq17(self):
            return self.Uren_Bfi.text()
        
        def returnq18(self):
            return self.Uren_Bvl.text()
        
        def returnq19(self):
            return self.Uren_Spoorleg.text()
        
        def returnq20(self):
            return self.Uren_Spoorlas.text()
        
        def returnq21(self):
            return self.Uren_Voeding.text()
        
        def returnq22(self):
            return self.Begroot_Lonen.text()
        
        def returnq23(self):
            return self.StartWerk.text()
      
        def returnq24(self):
            return self.Betaald.text()
        
        def returncBox(self):
            return self.state
        
        def returncBox1(self):
            return self.state1
        
        def returncBox2(self):
            return self.state2
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(),\
                    dialog.returnq4(), dialog.returnq5(), dialog.returnq6(),\
                    dialog.returnq7(), dialog.returnq8(), dialog.returnq9(),\
                    dialog.returnq10(), dialog.returnq11(), dialog.returnq12(),\
                    dialog.returnq13(),dialog.returnq14(), dialog.returnq15(),\
                    dialog.returnq16(), dialog.returnq17(), dialog.returnq18(),\
                    dialog.returnq19(), dialog.returnq20(), dialog.returnq21(),\
                    dialog.returnq22(), dialog.returnq23(), dialog.returnq24(),
                    dialog.returncBox(), dialog.returncBox1(), dialog.returncBox2()]  
                       
    window = Widget()
    data = window.getData()
    if data[0]:
        ms0 = str(data[0])
    else:
        ms0 = rpwerk[1]
    if data[1]:
        mf1 = float(data[1])
    else:
        mf1 = rpwerk[4]
    if data[2]:
        mf2 = float(data[2])
    else:
        mf2 = rpwerk[5]  
    if data[3]:
        mf3 = float(data[3])
    else:
        mf3 = rpwerk[6]
    if data[4]:
        mf4 = float(data[4])
    else:
        mf4 = rpwerk[7]
    if data[5]:
        mf5 = float(data[5])
    else:
        mf5 = rpwerk[8]
    if data[6]:
        mf6 = float(data[6])
    else:
        mf6 = rpwerk[9]
    if data[7]:
        mf7 = float(data[7])
    else:
        mf7 = rpwerk[10]
    if data[8]:
        mf8 = float(data[8])
    else:
        mf8 = rpwerk[11]
    if data[9]:
        mf9 = float(data[9])
    else:
        mf9 = rpwerk[12]
    if data[10]:
        mf10 = float(data[10])
    else:
        mf10 = rpwerk[13]
    if data[11]:
        mf11 = float(data[11])
    else:
        mf11 = rpwerk[14]
    if data[12]:
        mf12 = float(data[12])
    else:
        mf12 = rpwerk[15]
    if data[13]:
        mf13 = float(data[13])
    else:
        mf13 = rpwerk[16]
    if data[14]:
        mf14 = float(data[14])
    else:
        mf14 = rpwerk[17]
    if data[15]:
        mf15 = float(data[15])
    else:
        mf15 = rpwerk[18]
    if data[16]:
        mf16 = float(data[16])
    else:
        mf16 = rpwerk[19]
    if data[17]:
        mf17 = float(data[17])
    else:
        mf17 = rpwerk[20]
    if data[18]:
        mf18 = float(data[18])
    else:
        mf18 = rpwerk[21]
    if data[19]:
        mf19 = float(data[19])
    else:
        mf19 = rpwerk[22]
    if data[20]:
        mf20 = float(data[20])
    else:
        mf20 = rpwerk[23]
    if data[21]:
        mf21 = float(data[21])
    else:
        mf21 = rpwerk[24]
    if data[22]:
        mf22 = data[22]
    else:
        mf22 = rpwerk[25]
    if data[23]:
        mf23 = float(data[23])
    else:
        mf23 = rpwerk[26]
    if data[25]:
        mvgangst = 'G'
        mstatwk = jaarweek()
    elif data[24]:
        mvgangst = 'H'
        mstatwk =  jaarweek()
    else:
        mvgangst = rpwerk[2]
        mstatwk = rpwerk[3]
    if data[26]:
        mopdrdatum = str(datetime.datetime.now())[0:10]
    else:
        mopdrdatum = rpwerk[39]
                   
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()        
    uwrk = update(werken).where(werken.c.werknummerID == mwerknr).values(\
        werkomschrijving = ms0, aanneemsom = mf1, begr_materialen = mf2,\
        begr_materieel = mf3, begr_huisv = mf4, begr_leiding = mf5,\
        begr_inhuur = mf6, begr_vervoer = mf7, begr_beton_bvl = mf8,\
        begr_kabelwerk = mf9, begr_grondverzet = mf10, begr_overig = mf11,\
        begr_constr_uren = mf12, begr_mont_uren = mf13, begr_retourlas_uren = mf14,\
        begr_telecom_uren = mf15, begr_bfi_uren = mf16, begr_bvl_uren = mf17,\
        begr_spoorleg_uren = mf18, begr_spoorlas_uren = mf19, begr_voeding_uren = mf20,\
        begr_lonen = mf21, startweek = mf22, statusweek = mstatwk,\
        voortgangstatus = mvgangst, betaald_bedrag = mf23, opdracht_datum =\
        mopdrdatum)
    conn.execute(uwrk)
    conn.close()
    updateOK() 
    zoekWerk(m_email)