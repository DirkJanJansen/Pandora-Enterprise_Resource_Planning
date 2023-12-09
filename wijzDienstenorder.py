from login import hoofdMenu
import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
             QDialog, QMessageBox 
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey, \
                        MetaData, create_engine, and_)
from sqlalchemy.sql import select, update

def closeRegels(m_email, minkordernr, mregel, self):
    self.close()
    dienstenOrder(m_email, minkordernr, mregel)

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def wijzSluit(m_email, minkordernr, mregel ,self):
    self.close()
    zoekInkooporder(m_email, minkordernr, mregel)

def invoerOK():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Change purchase order services')
    msg.exec_()
        
def foutCombinatie():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('This is not a purchase order for services!')
    msg.setWindowTitle('Change purchase order services')
    msg.exec_()   
       
def foutDienstorder():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Service order not found!')
    msg.setWindowTitle('Change purchase order services')
    msg.exec_()
                
def zoekInkooporder(m_email, minkordernr, mregel):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Change purchase order services.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
                            
            self.Inkoopordernummer = QLabel()
            inkordEdit = QLineEdit(str(minkordernr))
            inkordEdit.setFixedWidth(100)
            inkordEdit.setFont(QFont("Arial",10))
            inkordEdit.textChanged.connect(self.inkordChanged)
            reg_ex = QRegExp('^[4]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, inkordEdit)
            inkordEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
   
            grid.addWidget(QLabel('Purchase order services'), 1, 0, 1, 2)
            grid.addWidget(inkordEdit, 1, 1)
       
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
        
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'),3 , 0, 1, 2, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(600, 350, 150, 150)
    
        def inkordChanged(self, text):
            self.Inkoopordernummer.setText(text)
    
        def returnInkoopordernummer(self):
            return self.Inkoopordernummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnInkoopordernummer()]
       
    window = Widget()
    data = window.getData()
    if data[0]:
        minkordernr = data[0]
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer(), primary_key=True),
        Column('status', Integer))
           
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    s = select([orders_inkoop]).where(orders_inkoop.c.orderinkoopID == minkordernr)
    rp1 = conn.execute(s).first()
    mregel = 0
    if rp1:
        dienstenOrder(m_email, minkordernr, mregel)
    else:
        foutDienstorder()
        zoekInkooporder(m_email, minkordernr, mregel)

def dienstenOrder(m_email, minkordernr, mregel):
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer(), primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
        Column('besteldatum', String),
        Column('goedgekeurd', String),
        Column('betaald', String),
        Column('afgemeld', String))
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String))
    orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
        Column('orddienstlevID', Integer(), primary_key=True),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('werkomschr', String),
        Column('omschrijving', String),
        Column('aanneemsom', Float),
        Column('plan_start', String),
        Column('werk_start', String),
        Column('plan_gereed', String),
        Column('werk_gereed', String),
        Column('acceptatie_gereed', Float),
        Column('acceptatie_datum', String),
        Column('meerminderwerk', Float),
        Column('regel', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True))    
       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()  
    
    sel1 = select([orders_inkoop]).where(orders_inkoop.c.orderinkoopID == minkordernr)
    sel2 = select([leveranciers]).where(and_(leveranciers.c.leverancierID \
                   == orders_inkoop.c.leverancierID,
                   orders_inkoop.c.orderinkoopID == minkordernr))
    sel3 = select([orders_inkoop_diensten]).where(orders_inkoop_diensten.\
                c.orderinkoopID == minkordernr).order_by(orders_inkoop_diensten.c.regel)
    sel4 = select([werken]).where(and_(werken.c.werknummerID==\
                 orders_inkoop_diensten.c.werknummerID,\
                 orders_inkoop_diensten.c.orderinkoopID == minkordernr))
    rp1 = conn.execute(sel1).first()
    rp2 = conn.execute(sel2).first()
    rp3 = conn.execute(sel3)
    rp4 = conn.execute(sel4).first()
    mpostcode = rp2[3]
    mhuisnr = int(rp2[4])
    if conn.execute(sel3).fetchone():
        mwerknr = rp4[0]
        rp3 = conn.execute(sel3)
    else:
        foutCombinatie()
        zoekInkooporder(m_email, minkordernr, mregel)
    import postcode
    mstrpls = postcode.checkpostcode(mpostcode, mhuisnr)
    mstraat = mstrpls[0]
    mplaats = mstrpls[1]
                    
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify purchase order services.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                                            
            self.Inkoopordernummer = QLabel()
            inkordEdit = QLineEdit(str(minkordernr))
            inkordEdit.setFixedWidth(110)
            inkordEdit.setAlignment(Qt.AlignRight)
            inkordEdit.setDisabled(True)
            inkordEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            inkordEdit.textChanged.connect(self.inkordChanged)
 
            self.Werknummer = QLabel()
            werknEdit = QLineEdit(str(mwerknr))
            werknEdit.setFixedWidth(110)
            werknEdit.setAlignment(Qt.AlignRight)
            werknEdit.setDisabled(True)
            werknEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            werknEdit.textChanged.connect(self.werknChanged)
       
            self.Besteldatum = QLabel()
            q3Edit = QLineEdit()
            datum = str(datetime.datetime.now())
            q3Edit.setText((datum[8:10]+'-'+datum[5:8]+datum[0:4]))
            q3Edit.setDisabled(True)
            q3Edit.setFixedWidth(110)
            q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            
            self.Goedgekeurd = QLabel()
            q4Edit = QLineEdit(rp1[3])
            q4Edit.setCursorPosition(0)
            q4Edit.setFixedWidth(110)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)  
                    
            self.Betaald = QLabel()
            q5Edit = QLineEdit(rp1[4])
            q5Edit.setCursorPosition(0)
            q5Edit.setFixedWidth(110)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed)
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)  

            self.Afgemeld = QLabel()
            q6Edit = QLineEdit(rp1[5])
            q6Edit.setCursorPosition(0)
            q6Edit.setFixedWidth(110)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator) 
                                 
            grid = QGridLayout()
            grid.setSpacing(20)
                           
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0)
                    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Order for\nSupplier: '+str(rp2[0])+\
              ',\n'+rp2[1]+' '+rp2[2]+',\n'+mstraat+' '+str(rp2[4])+\
              rp2[5]+',\n'+rp2[3]+' '+mplaats+'.'), 1, 1, 1 , 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 5, 2, 1, 1, Qt.AlignCenter)
                      
            grid.addWidget(QLabel('Purchase order number'), 4, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(inkordEdit, 4, 1)
            
            grid.addWidget(QLabel('Work number'), 5, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(werknEdit, 5, 1)           
        
            grid.addWidget(QLabel('Order date'),6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q3Edit, 6, 1)  
                   
            grid.addWidget(QLabel('Approved yyyy-mm-dd'), 7, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q4Edit, 7, 1) 
            
            grid.addWidget(QLabel('Payed yyyy-mm-dd'), 8, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q5Edit, 8, 1)  
            
            grid.addWidget(QLabel('Unsubscribed yyyy-mm-dd'), 9, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q6Edit, 9, 1)  
          
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 0, 1, 3, Qt.AlignCenter)
            
            applyBtn = QPushButton('Order lines')
            applyBtn.clicked.connect(self.accept)
                          
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: wijzSluit(m_email, minkordernr, 0 ,self))
                       
            grid.addWidget(applyBtn, 9, 2, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
            grid.addWidget(cancelBtn, 8, 2, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(600, 300, 350, 300)
                  
        def inkordChanged(self, text):
            self.Inkoopordernummer.setText(text)
            
        def werknChanged(self, text):
            self.Werknummer.setText(text)
          
        def q3Changed(self, text):
            self.Besteldatum.setText(text)
            
        def q4Changed(self, text):
            self.Goedgekeurd.setText(text)
            
        def q5Changed(self, text):
            self.Betaald.setText(text)
            
        def q6Changed(self, text):
            self.Afgemeld.setText(text)
                                                          
        def returnInkoopordernummer(self):
            return self.Inkoopordernummer.text()
        
        def returnWerknummer(self):
            return self.Werknummer.text()     
        
        def returnBesteldatum(self):
            return self.Besteldatum.text()
        
        def returnGoedgekeurd(self):
            return self.Goedgekeurd.text()
        
        def returnBetaald(self):
            return self.Betaald.text()

        def returnAfgemeld(self):
            return self.Afgemeld.text()
                                 
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnGoedgekeurd(), dialog.returnBetaald(),\
                    dialog.returnAfgemeld()]
    
    window = Widget()
    data = window.getData()
    if data[0]:
        mgoedgek = data[0]
    else:
        mgoedgek = rp1[3]
    if data[1]:
        mbetaald = data[1]
    else:
        mbetaald = rp1[4]
    if data[2]:
        mafgemeld = data[2]
    else:
        mafgemeld = rp1[5]
             
    sel1 = select([orders_inkoop]).where(orders_inkoop.c.orderinkoopID == minkordernr)
    rp1 = conn.execute(sel1).first()
   
    if data[0] or data[1] or data[2]:
        u = update(orders_inkoop).where(orders_inkoop.c.orderinkoopID == minkordernr).\
           values(goedgekeurd=mgoedgek, betaald = mbetaald, afgemeld = mafgemeld)  
        conn.execute(u)
        invoerOK()
        conn.close()
    mregel = 0
    dienstenRegels(m_email, rp1,rp2, rp3, mstraat, mplaats, mregel)
             
def dienstenRegels(m_email, rp1,rp2, rp3, mstraat, mplaats, mregel):
    minkordernr = rp1[0]
    for row in rp3:
        mregel += 1
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
        
                self.setFont(QFont('Arial', 10))
                self.setWindowTitle("Change service purchase order lines")
                self.setFont(QFont('Arial', 10))
                                                          
                self.Inkoopordernummer = QLabel()
                q1Edit = QLineEdit(str(minkordernr))
                q1Edit.setDisabled(True)
                q1Edit.setFixedWidth(130)
                q1Edit.setAlignment(Qt.AlignRight)
                q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q1Edit.textChanged.connect(self.q1Changed) 
                
                self.Werknummer = QLabel()
                q2Edit = QLineEdit(str(row[2]))
                q2Edit.setDisabled(True)
                q2Edit.setFixedWidth(130)
                q2Edit.setAlignment(Qt.AlignRight)
                q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q2Edit.textChanged.connect(self.q2Changed) 
                 
                self.Werkomschrijving = QLabel()
                q3Edit = QLineEdit(row[3])
                q3Edit.setFixedWidth(400)
                q3Edit.setDisabled(True)
                q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q3Edit.textChanged.connect(self.q3Changed) 
                
                self.Omschrijving = QLabel()
                q4Edit = QLineEdit(str(row[4]))
                q4Edit.setFixedWidth(400)
                q4Edit.setFont(QFont("Arial",10))
                q4Edit.textChanged.connect(self.q4Changed) 
                reg_ex = QRegExp("^.{0,50}$")
                input_validator = QRegExpValidator(reg_ex, q4Edit)
                q4Edit.setValidator(input_validator)    
            
                self.Aanneemsom = QLabel()
                q5Edit = QLineEdit('{:12.2f}'.format(row[5]))
                q5Edit.setFixedWidth(130)
                q5Edit.setFont(QFont("Arial",10))
                q5Edit.setAlignment(Qt.AlignRight)
                q5Edit.textChanged.connect(self.q5Changed) 
                reg_ex = QRegExp(("^[-+]?[0-9]*\.?[0-9]+$"))
                input_validator = QRegExpValidator(reg_ex, q5Edit)
                q5Edit.setValidator(input_validator)  
    
                self.GeplandeStart = QLabel()
                q6Edit = QLineEdit(str(row[6]))
                q5Edit.setCursorPosition(0)
                q6Edit.setFixedWidth(130)
                q6Edit.setFont(QFont("Arial",10))
                q6Edit.textChanged.connect(self.q6Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q6Edit)
                q6Edit.setValidator(input_validator)  
                
                self.WerkelijkeStart = QLabel()
                q7Edit = QLineEdit(str(row[7]))
                q7Edit.setFixedWidth(130)
                q7Edit.setFont(QFont("Arial",10))
                q7Edit.textChanged.connect(self.q7Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q7Edit)
                q7Edit.setValidator(input_validator)
                
                self.GeplandGereed = QLabel()
                q8Edit = QLineEdit(str(row[8]))
                q5Edit.setCursorPosition(0)
                q8Edit.setFixedWidth(130)
                q8Edit.setFont(QFont("Arial",10))
                q8Edit.textChanged.connect(self.q8Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q8Edit)
                q8Edit.setValidator(input_validator)  
                
                self.WerkelijkGereed= QLabel()
                q9Edit = QLineEdit(str(row[9]))
                q9Edit.setFixedWidth(130)
                q9Edit.setFont(QFont("Arial",10))
                q9Edit.textChanged.connect(self.q9Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q9Edit)
                q9Edit.setValidator(input_validator) 
                
                self.BedragAcceptatie = QLabel()
                q10Edit = QLineEdit('{:12.2f}'.format(row[10]))
                q10Edit.setFixedWidth(130)
                q10Edit.setDisabled(True)
                q10Edit.setAlignment(Qt.AlignRight)
                q10Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q10Edit.textChanged.connect(self.q10Changed) 
                
                self.BedragMeerwerk = QLabel()
                q12Edit = QLineEdit('{:12.2f}'.format(row[12]))
                q12Edit.setFixedWidth(130)
                q12Edit.setDisabled(True)
                q12Edit.setAlignment(Qt.AlignRight)
                q12Edit.setFont(QFont("Arial",10))
                q12Edit.textChanged.connect(self.q12Changed) 
                                                    
                self.DatumAcceptatie = QLabel()
                q11Edit = QLineEdit(str(row[11]))
                q11Edit.setFixedWidth(130)
                q11Edit.setDisabled(True)
                q11Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q11Edit.textChanged.connect(self.q11Changed) 
                                                                            
                grid = QGridLayout()
                grid.setSpacing(20)
                              
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid.addWidget(lbl ,1, 0,)
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 1, 2, 1, 1, Qt.AlignRight)
           
                self.setFont(QFont('Arial', 10))
                grid.addWidget(QLabel('Order for\nSupplier: '+str(rp2[0])+\
                 ',\n'+rp2[1]+' '+rp2[2]+',\n'+mstraat+' '+str(rp2[4])+\
                 rp2[5]+',\n'+rp2[3]+' '+mplaats+'.\nOrder line '+str(mregel)), 1, 1, 1, 2)
                             
                lbl1 = QLabel('Order number')
                lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl1, 5, 0)
                grid.addWidget(q1Edit, 5, 1)
                                              
                lbl2 = QLabel('Work number')
                lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl2, 6, 0)
                grid.addWidget(q2Edit, 6, 1)
                
                lbl3 = QLabel('Work description')  
                lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl3, 7, 0)
                grid.addWidget(q3Edit,7, 1, 1, 2)
                           
                lbl4 = QLabel('Description')  
                lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl4, 8, 0)
                grid.addWidget(q4Edit, 8, 1, 1, 2)
                
                lbl5 = QLabel('Contract price')  
                lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl5, 9, 0)
                grid.addWidget(q5Edit, 9, 1)
                                        
                lbl6 = QLabel('Planned start')  
                lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl6, 10, 0)  
                grid.addWidget(q6Edit, 10, 1)
                
                lbl7 = QLabel('Real start')  
                lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl7, 11, 0)
                grid.addWidget(q7Edit, 11, 1)
    
                lbl8 = QLabel('Planned ready')  
                lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl8, 12, 0)
                grid.addWidget(q8Edit, 12, 1)
                
                lbl9 = QLabel('Real ready')  
                lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl9, 13, 0)
                grid.addWidget(q9Edit, 13, 1)
                
                lbl10 = QLabel('Amount approved')  
                lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl10, 14, 0)
                grid.addWidget(q10Edit, 14, 1)
                
                lbl11 = QLabel('Date acceptance')  
                lbl11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl11, 15, 0)
                grid.addWidget(q11Edit, 15, 1)
                  
                lbl12 = QLabel('Additional work\nProvisional sum')  
                lbl12.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                grid.addWidget(lbl12, 9, 2)
                grid.addWidget(q12Edit, 9, 2,Qt.AlignRight)
                
                lbl13 = QLabel('Changes to the original amount are recorded\nas additional work / Provisional sum')
                grid.addWidget(lbl13, 10, 2, 1 , 2)
                                 
                self.setLayout(grid)
                self.setGeometry(600, 150, 150, 150)
        
                applyBtn = QPushButton('Change /or\nNext line')
                applyBtn.clicked.connect(self.accept)
                
                grid.addWidget(applyBtn, 15, 2, 1 , 1, Qt.AlignRight)
                applyBtn.setFont(QFont("Arial",10))
                applyBtn.setFixedWidth(140)
                applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                cancelBtn = QPushButton('Close')
                cancelBtn.clicked.connect(lambda: closeRegels(m_email, minkordernr, mregel, self))
                
                grid.addWidget(cancelBtn, 14, 2, 1, 1, Qt.AlignRight)
                cancelBtn.setFont(QFont("Arial",10))
                cancelBtn.setFixedWidth(140)
                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 16 , 0, 1, 3, Qt.AlignCenter)
                                                                         
            def q1Changed(self, text):
                self.Inkoopordernummer.setText(text)
                
            def q2Changed(self,text):
                self.Werknummer.setText(text)
                
            def q3Changed(self,text):
                self.Werkomschrijving.setText(text)
                
            def q4Changed(self,text):
                self.Omschrijving.setText(text)
            
            def q5Changed(self,text):
                self.Aanneemsom.setText(text)
                
            def q6Changed(self,text):
                self.GeplandeStart.setText(text)  
              
            def q7Changed(self,text):
                self.WerkelijkeStart.setText(text)
                
            def q8Changed(self,text):
                self.GeplandGereed.setText(text)
                
            def q9Changed(self,text):
                self.WerkelijkGereed.setText(text)
                
            def q10Changed(self,text):
                self.BedragAcceptatie.setText(text)
                
            def q11Changed(self,text):
                self.DatumAcceptatie.setText(text)
                   
            def q12Changed(self,text):
                self.BedragMeerwerk.setText(text)
                
            def returnq1(self):
                return self.Inkoopordernummer.text()
            
            def returnq2(self):
                return self.Werknummer.text()
            
            def returnq3(self):
                return self.Werkomschrijving.text()
            
            def returnq4(self):
                return self.Omschrijving.text()
            
            def returnq5(self):
                return self.Aanneemsom.text()
            
            def returnq6(self):
                return self.GeplandeStart.text()
            
            def returnq7(self):
                return self.WerkelijkeStart.text()
            
            def returnq8(self):
                return self.GeplandGereed.text()
            
            def returnq9(self):
                return self.WerkelijkGereed.text()
            
            def returnq10(self):
                return self.BedragAcceptatie.text()
            
            def returnq11(self):
                return self.DatumAcceptatie.text()
            
            def returnq12(self):
                return self.BedragMeerwerk.text()
            
            @staticmethod
            def getData(parent=None):
                dialog = Widget(parent)
                dialog.exec_()
                return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(),\
                        dialog.returnq4(), dialog.returnq5(), dialog.returnq6(),\
                        dialog.returnq7(), dialog.returnq8(), dialog.returnq9(),
                        dialog.returnq10(), dialog.returnq11(), dialog.returnq12()]
         
        window = Widget()
        data = window.getData()
        mID = row[0]
        mordnr = row[1]
        mwerknr = row[2]
        if data[2]:
            mwerkomschr = data[2]
        else:
            mwerkomschr = row[3]
        if data[3]:
            momschr = data[3]
        else:
            momschr = row[4]
        if data[4]:
            maannsom = float(data[4])
        else:
            maannsom = row[5]
        if data[5]:
            mplstart = data[5]
        else:
            mplstart = row[6]
        if data[6]:
            mwerkstart = data[6]
        else:
            mwerkstart = row[7]
        if data[7]:
            mplgereed = data[7]
        else:
            mplgereed = row[8]
        if data[8]:
            mwerkgereed = data[8]
        else:
            mwerkgereed = row[9]
        macctbedr = float(row[10])
        if data[11]:
            maccptdat = data[10]
        else:
            maccptdat = row[11]
                               
        metadata = MetaData()    
       
        orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
            Column('orddienstlevID', Integer(), primary_key=True),
            Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
            Column('werknummerID', None, ForeignKey('werken.werknummerID')),
            Column('werkomschr', String),
            Column('omschrijving', String),
            Column('aanneemsom', Float),
            Column('plan_start', String),
            Column('werk_start', String),
            Column('plan_gereed', String),
            Column('werk_gereed', String),
            Column('acceptatie_gereed', Float),
            Column('acceptatie_datum', String),
            Column('meerminderwerk', Float),
            Column('regel', Integer),
            Column('meerminderwerk', Float))
          
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
                      
        u = update(orders_inkoop_diensten).where(and_(orders_inkoop_diensten.c.\
           orddienstlevID == mID, orders_inkoop_diensten.c.orderinkoopID == mordnr,\
           orders_inkoop_diensten.c.werknummerID == mwerknr, \
           orders_inkoop_diensten.c.regel == mregel)).values(werkomschr =\
           mwerkomschr, omschrijving = momschr, plan_start = mplstart,\
           plan_gereed = mplgereed, werk_start = mwerkstart, werk_gereed =  mwerkgereed,\
           acceptatie_gereed =  macctbedr, acceptatie_datum = maccptdat,\
           meerminderwerk = orders_inkoop_diensten.c.meerminderwerk+maannsom -row[5])
        
        conn.execute(u)
   
        metadata = MetaData()
        werken = Table('werken', metadata,
            Column('werknummerID', Integer(), primary_key=True),
            Column('meerminderwerk', Float))

        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
 
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr).\
            values(meerminderwerk = werken.c.meerminderwerk+maannsom-row[5])
        conn.execute(updwerk)
        y = 0
        for x in range(2,12):
            if data[x]:
                y =1
        if y:
            invoerOK()
          
    mregel = 0
    dienstenOrder(m_email, minkordernr, mregel)
      
                                                       
   