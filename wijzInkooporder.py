from login import hoofdMenu
import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
             QDialog, QMessageBox 
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey, \
                        MetaData, create_engine, and_, Boolean)
from sqlalchemy.sql import select, update, insert, func

def invoerOK():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert successful!')
    msg.setWindowTitle('Insert purchase order')
    msg.exec_()
     
def closeRegels(m_email, minkordernr, mregel, self):
    self.close()
    inkoopOrder(m_email, minkordernr, mregel)
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def closeOrder(m_email, minkordernr, mregel, self):
    self.close()
    zoekInkooporder(m_email, minkordernr, mregel)
    
def foutCombinatie():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('This is not a purchase order for materials!')
    msg.setWindowTitle('Modify purchase order articles.')
    msg.exec_()   
    
def foutOrder():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Order number is incorrect!')
    msg.setWindowTitle('Modify purchase order articles.')
    msg.exec_()   
    
def foutInkooporder():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Order not found!')
    msg.setWindowTitle('Modify purchase order articles.')
    msg.exec_()
    
def zoekInkooporder(m_email, minkordernr, mregel):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Modify purchase order articles.")
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
 
            grid.addWidget(QLabel('Purchase order number materials'), 1, 0, 1, 2)
            grid.addWidget(inkordEdit, 1, 1)
       
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 2, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'),4 , 0, 1, 2, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(500, 250, 150, 150)
    
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
        inkoopOrder(m_email, minkordernr, mregel)
    else:
        foutInkooporder()
        zoekInkooporder(m_email, minkordernr, mregel)

def inkoopOrder(m_email, minkordernr, mregel):
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
    orders_inkoop_artikelen = Table('orders_inkoop_artikelen', metadata,
        Column('ordartlevID', Integer(), primary_key=True),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('bestelaantal', Float),
        Column('inkoopprijs', Float),
        Column('levering_start', String),
        Column('levering_eind', String),
        Column('reclamatie', String),
        Column('aantal_reclamaties', Integer),
        Column('ontvangstdatum', String),
        Column('ontvangen_hoeveelheid', Float),
        Column('acceptatie_datum', String),
        Column('hoeveelheid_acceptatie', Float),
        Column('betaald', Float),
        Column('regel', Integer))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()  
    
    sel1 = select([orders_inkoop]).where(orders_inkoop.c.orderinkoopID == minkordernr)
    sel2 = select([leveranciers]).where(and_(leveranciers.c.leverancierID==\
       orders_inkoop.c.leverancierID, orders_inkoop.c.orderinkoopID == minkordernr))
    sel3 = select([orders_inkoop_artikelen]).where(orders_inkoop_artikelen.\
           c.orderinkoopID == minkordernr).order_by(orders_inkoop_artikelen.c.regel)
    rp1 = conn.execute(sel1).first()
    rp2 = conn.execute(sel2).first()
    
    if conn.execute(sel3).fetchone():
        rp3 = conn.execute(sel3)
    else:
        foutCombinatie()
        zoekInkooporder(m_email, minkordernr, mregel)
        
    mpostcode = rp2[3]
    mhuisnr = int(rp2[4])
    import postcode
    mstrpls = postcode.checkpostcode(mpostcode, mhuisnr)
    mstraat = mstrpls[0]
    mplaats = mstrpls[1]
                    
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Change purchase order items.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                            
            self.Inkoopordernummer = QLabel()
            inkordEdit = QLineEdit(str(minkordernr))
            inkordEdit.setFixedWidth(110)
            inkordEdit.setAlignment(Qt.AlignRight)
            inkordEdit.setDisabled(True)
            inkordEdit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
            inkordEdit.textChanged.connect(self.inkordChanged)
          
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
            grid.addWidget(logo , 5, 2, 1 ,1, Qt.AlignCenter)
                      
            grid.addWidget(QLabel('Purchase order number'), 4, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(inkordEdit, 4, 1)
            
            grid.addWidget(QLabel('Order date'), 5, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q3Edit, 5, 1)  
                   
            grid.addWidget(QLabel('Approved yyyy-mm-dd'), 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q4Edit, 6, 1) 
            
            grid.addWidget(QLabel('Payed yyyy-mm-dd'), 7, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q5Edit, 7, 1)  
            
            grid.addWidget(QLabel('Unsubscribed yyyy-mm-dd'), 8, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q6Edit, 8, 1)  
          
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 3, Qt.AlignCenter)
            
            applyBtn = QPushButton('Order lines')
            applyBtn.clicked.connect(self.accept)
             
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: closeOrder(m_email, minkordernr, 0, self))
                       
            grid.addWidget(applyBtn, 8, 2, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(120)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
            grid.addWidget(cancelBtn, 7, 2, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(120)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(500, 200, 350, 300)
                  
        def inkordChanged(self, text):
            self.Inkoopordernummer.setText(text)
          
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
    u = update(orders_inkoop).where(orders_inkoop.c.orderinkoopID == minkordernr).\
        values(goedgekeurd = mgoedgek, betaald = mbetaald, afgemeld = mafgemeld)  
    conn.execute(u)
    conn.close()
    mregel = 0
    inkoopRegels(m_email, rp1, rp2, rp3, mstraat, mplaats, mregel)
     
def inkoopRegels(m_email, rp1, rp2, rp3, mstraat, mplaats, mregel): 
    minkordernr = int(rp1[0])
    for row in rp3:
        mregel += 1
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
        
                self.setFont(QFont('Arial', 10))
                self.setWindowTitle("Change purchase order line items")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                self.setFont(QFont('Arial', 10))
                                                       
                self.Inkoopordernummer = QLabel()
                q1Edit = QLineEdit(str(minkordernr))
                q1Edit.setDisabled(True)
                q1Edit.setFixedWidth(130)
                q1Edit.setAlignment(Qt.AlignRight)
                q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q1Edit.textChanged.connect(self.q1Changed) 
                
                self.BestelregelArtikel = QLabel()
                q2Edit = QLineEdit(str(row[2]))
                q2Edit.setDisabled(True)
                q2Edit.setAlignment(Qt.AlignRight)
                q2Edit.setFixedWidth(130)
                q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q2Edit.textChanged.connect(self.q2Changed) 
              
                self.BestelHoeveelheid = QLabel()
                q3Edit = QLineEdit(str(round(float(row[3]),2)))
                q3Edit.setFixedWidth(130)
                q3Edit.setFont(QFont("Arial",10))
                q3Edit.setAlignment(Qt.AlignRight)
                q3Edit.textChanged.connect(self.q3Changed) 
                rreg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                input_validator = QRegExpValidator(reg_ex, q3Edit)
                q3Edit.setValidator(input_validator)
                
                self.Inkoopeenheidsprijs = QLabel()
                q4Edit = QLineEdit(str(round(float(row[4]),2)))
                q4Edit.setFixedWidth(130)
                q4Edit.setFont(QFont("Arial",10))
                q4Edit.setAlignment(Qt.AlignRight)
                q4Edit.textChanged.connect(self.q4Changed) 
                rreg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                input_validator = QRegExpValidator(reg_ex, q4Edit)
                q4Edit.setValidator(input_validator)    
            
                self.Levering_start = QLabel()
                q5Edit = QLineEdit(str(row[5]))
                q5Edit.setCursorPosition(0)
                q5Edit.setFixedWidth(130)
                q5Edit.setFont(QFont("Arial",10))
                q5Edit.textChanged.connect(self.q5Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q5Edit)
                q5Edit.setValidator(input_validator)
                
                self.Levering_eind = QLabel()
                q13Edit = QLineEdit(str(row[6]))
                q13Edit.setCursorPosition(0)
                q13Edit.setFixedWidth(130)
                q13Edit.setFont(QFont("Arial",10))
                q13Edit.textChanged.connect(self.q13Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q13Edit)
                q13Edit.setValidator(input_validator) 
     
                self.Reclamatie = QLabel()
                q6Edit = QLineEdit(str(row[7]))
                q6Edit.setCursorPosition(0)
                q6Edit.setFixedWidth(130)
                q6Edit.setFont(QFont("Arial",10))
                q6Edit.setStyleSheet("color: black")
                q6Edit.setDisabled(True)
                q6Edit.textChanged.connect(self.q6Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q6Edit)
                q6Edit.setValidator(input_validator)  
                
                self.Aantal_reclamaties = QLabel()
                q7Edit = QLineEdit(str(row[8]))
                q7Edit.setFixedWidth(130)
                q7Edit.setAlignment(Qt.AlignRight)
                q7Edit.setFont(QFont("Arial",10))
                q7Edit.textChanged.connect(self.q7Changed) 
                reg_ex = QRegExp("^[0-9]{0,10}$")
                input_validator = QRegExpValidator(reg_ex, q7Edit)
                q7Edit.setValidator(input_validator)
                
                self.Ontvangstdatum = QLabel()
                q8Edit = QLineEdit(str(row[9]))
                q5Edit.setCursorPosition(0)
                q8Edit.setFixedWidth(130)
                q8Edit.setFont(QFont("Arial",10))
                q8Edit.setStyleSheet("color: black")
                q8Edit.setDisabled(True)
                q8Edit.textChanged.connect(self.q8Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q8Edit)
                q8Edit.setValidator(input_validator)  
                
                self.Ontvangen_Hoeveelheid = QLabel()
                q9Edit = QLineEdit(str(round(float(row[10]),2)))
                q9Edit.setFixedWidth(130)
                q9Edit.setFont(QFont("Arial",10))
                q9Edit.setAlignment(Qt.AlignRight)
                q9Edit.textChanged.connect(self.q9Changed) 
                rreg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                input_validator = QRegExpValidator(reg_ex, q9Edit)
                q9Edit.setValidator(input_validator) 
                
                self.Acceptatiedatum = QLabel()
                q10Edit = QLineEdit(str(row[11]))
                q10Edit.setCursorPosition(0)
                q10Edit.setFixedWidth(130)
                q10Edit.setFont(QFont("Arial",10))
                q10Edit.setStyleSheet("color: black")
                q10Edit.setDisabled(True)
                q10Edit.textChanged.connect(self.q10Changed) 
                reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, q10Edit)
                q10Edit.setValidator(input_validator)  
                
                self.Hoeveelheid_acceptatie = QLabel()
                q11Edit = QLineEdit(str(round(float(row[12]),2)))
                q11Edit.setFixedWidth(130)
                q11Edit.setFont(QFont("Arial",10))
                q11Edit.setAlignment(Qt.AlignRight)
                q11Edit.textChanged.connect(self.q11Changed) 
                rreg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                input_validator = QRegExpValidator(reg_ex, q11Edit)
                q11Edit.setValidator(input_validator) 
                
                self.Betaald = QLabel()
                q12Edit = QLineEdit(str(round(float(row[13]),2)))
                q12Edit.setFixedWidth(130)
                q12Edit.setFont(QFont("Arial",10))
                q12Edit.setAlignment(Qt.AlignRight)
                q12Edit.textChanged.connect(self.q12Changed) 
                rreg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                input_validator = QRegExpValidator(reg_ex, q12Edit)
                q12Edit.setValidator(input_validator) 
                   
                grid = QGridLayout()
                grid.setSpacing(20)
                              
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid.addWidget(lbl ,1, 0, 1, 2)
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 1, 3, 1 , 1 , Qt.AlignRight)
           
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'),15 , 0, 1, 4, Qt.AlignCenter)
             
                self.setFont(QFont('Arial', 10))
                grid.addWidget(QLabel('Order for\nSupplier: '+str(rp2[0])+\
                 ',\n'+rp2[1]+' '+rp2[2]+',\n'+mstraat+' '+str(rp2[4])+\
                 rp2[5]+',\n'+rp2[3]+' '+mplaats+'.\nOrder line '+str(mregel)), 1, 1, 1, 3)
                             
                lbl1 = QLabel('Order number')
                lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl1, 5, 0)
                grid.addWidget(q1Edit, 5, 1)
                                              
                lbl2 = QLabel('Order line article')
                lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl2, 6, 0)
                grid.addWidget(q2Edit, 6, 1)
                
                lbl3 = QLabel('Order quantity')  
                lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl3, 7, 0)
                grid.addWidget(q3Edit,7, 1)
                           
                lbl4 = QLabel('Purchase unit price')  
                lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl4, 8, 0)
                grid.addWidget(q4Edit,8, 1)
                
                lbl5 = QLabel('Delivery start')
                lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl5, 9, 0)
                grid.addWidget(q5Edit, 9, 1)
                
                lbl13 = QLabel('Delivery end')  
                lbl13.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl13, 9, 2)
                grid.addWidget(q13Edit, 9, 3)
                
                lbl6 = QLabel('Complaint date yyyy-mm-dd')  
                lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl6, 10, 0)  
                grid.addWidget(q6Edit, 10, 1)
                
                lbl7 = QLabel('Number of complaints')  
                lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl7, 10, 2)
                grid.addWidget(q7Edit, 10, 3)
    
                lbl8 = QLabel('Received date yyyy-mm-d')  
                lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl8, 11, 0)
                grid.addWidget(q8Edit, 11, 1)
                
                lbl9 = QLabel('Total received')  
                lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl9, 11, 2)
                grid.addWidget(q9Edit, 11, 3)
            
                lbl10 = QLabel('Approved yyyy-mm-dd')  
                lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl10, 12, 0)
                grid.addWidget(q10Edit, 12, 1)
                
                lbl11 = QLabel('Total accepted')  
                lbl11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl11, 12, 2)
                grid.addWidget(q11Edit, 12, 3)
            
                lbl12 = QLabel('Number payed')  
                lbl12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl12, 13, 0)
                grid.addWidget(q12Edit, 13, 1)
                
                self.setLayout(grid)
                self.setGeometry(500, 150, 150, 150)
        
                applyBtn = QPushButton('Modify or\nnext line')
                applyBtn.clicked.connect(self.accept)
        
                grid.addWidget(applyBtn, 14, 3, 1 , 1, Qt.AlignRight)
                applyBtn.setFont(QFont("Arial",10))
                applyBtn.setFixedWidth(140)
                applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                cancelBtn = QPushButton('Close')
                cancelBtn.clicked.connect(lambda: closeRegels(m_email, minkordernr, mregel, self))
                
                grid.addWidget(cancelBtn, 13, 3, 1, 1, Qt.AlignRight)
                cancelBtn.setFont(QFont("Arial",10))
                cancelBtn.setFixedWidth(140)
                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                                                           
            def q1Changed(self, text):
                self.Inkoopordernummer.setText(text)
                
            def q2Changed(self,text):
                self.BestelregelArtikel.setText(text)
                
            def q3Changed(self,text):
                self.BestelHoeveelheid.setText(text)
                
            def q4Changed(self,text):
                self.Inkoopeenheidsprijs.setText(text)
            
            def q5Changed(self,text):
                self.Levering_start.setText(text)
            
            def q13Changed(self,text):
                self.Levering_eind.setText(text)
                
            def q6Changed(self,text):
                self.Reclamatie.setText(text)  
              
            def q7Changed(self,text):
                self.Aantal_reclamaties.setText(text)
                
            def q8Changed(self,text):
                self.Ontvangstdatum.setText(text)
                
            def q9Changed(self,text):
                self.Ontvangen_Hoeveelheid.setText(text)
                
            def q10Changed(self,text):
                self.Acceptatiedatum.setText(text)
                
            def q11Changed(self,text):
                self.Hoeveelheid_acceptatie.setText(text)
                
            def q12Changed(self,text):
                self.Betaald.setText(text)   
                          
            def returnq1(self):
                return self.Inkoopordernummer.text()
            
            def returnq2(self):
                return self.BestelregelArtikel.text()
            
            def returnq3(self):
                return self.BestelHoeveelheid.text()
            
            def returnq4(self):
                return self.Inkoopeenheidsprijs.text()
            
            def returnq5(self):
                return self.Levering_start.text()
            
            def returnq13(self):
                return self.Levering_eind.text()
            
            def returnq6(self):
                return self.Reclamatie.text()
            
            def returnq7(self):
                return self.Aantal_reclamaties.text()
            
            def returnq8(self):
                return self.Ontvangstdatum.text()
            
            def returnq9(self):
                return self.Ontvangen_Hoeveelheid.text()
            
            def returnq10(self):
                return self.Acceptatiedatum.text()
            
            def returnq11(self):
                return self.Hoeveelheid_acceptatie.text()
            
            def returnq12(self):
                return self.Betaald.text()
            
            @staticmethod
            def getData(parent=None):
                dialog = Widget(parent)
                dialog.exec_()
                return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(),\
                        dialog.returnq4(), dialog.returnq5(), dialog.returnq13(),\
                        dialog.returnq6(), dialog.returnq7(), dialog.returnq8(),\
                        dialog.returnq9(), dialog.returnq10(), dialog.returnq11(),\
                        dialog.returnq12()]  
        
        window = Widget()
        data = window.getData()
        mID = row[0]
        mordnr = row[1]
        martikelnr = row[2]
        if data[2]:
            maantal = float(data[2])
        else:
            maantal = row[3]
        if data[3]:
            mprijs = float(data[3])
        else:
            mprijs = row[4]
        if data[4]:
            mlevstart = data[4]
        else:
            mlevstart = row[5]
        if data[5]:
            mlevend = data[6]
        else:
            mlevend = row[6] 
        if data[7]:
            mrecl = int(data[7])
            mrecldat = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10] 
        else:
            mrecl = row[8]
            mrecldat = row[7]
        if data[9]:
            montvangen = float(data[9])
            montvdat = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10] 
        else:
            montvangen = row[10]
            montvdat = row[9]
        maccptversch = 0
        if data[11]:
            maccpthoev = float(data[11])
            maccptversch = float(data[11]) - row[12]
            maccpt = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10] 
        else:
            maccpthoev = row[12]
            maccptversch = 0
            maccpt = row[11]
        if data[12]:
            mbetaald = float(data[12])
        else:
            mbetaald = row[13]
            
        metadata = MetaData()    
        orders_inkoop_artikelen = Table('orders_inkoop_artikelen', metadata,
            Column('ordartlevID', Integer(), primary_key=True),
            Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
            Column('artikelID', None, ForeignKey('artikelen.artikelID')),
            Column('bestelaantal', Float),
            Column('inkoopprijs', Float),
            Column('levering_start', String),
            Column('levering_eind', String),
            Column('reclamatie', String),
            Column('aantal_reclamaties', Integer),
            Column('ontvangstdatum', String),
            Column('ontvangen_hoeveelheid', Float),
            Column('acceptatie_datum', String),
            Column('hoeveelheid_acceptatie', Float),
            Column('betaald', Float))
          
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
       
        u = update(orders_inkoop_artikelen).where(and_(orders_inkoop_artikelen.\
          c.ordartlevID == mID, orders_inkoop_artikelen.c.orderinkoopID == mordnr,\
          orders_inkoop_artikelen.c.artikelID == martikelnr))\
          .values(bestelaantal = maantal, inkoopprijs = mprijs,\
          levering_start = mlevstart, levering_eind = mlevend, reclamatie = mrecldat,\
          aantal_reclamaties = mrecl, ontvangstdatum = montvdat, ontvangen_hoeveelheid =\
          montvangen, acceptatie_datum = maccpt, hoeveelheid_acceptatie = maccpthoev,\
          betaald = mbetaald)   
    
        conn.execute(u)
        
        if maccpthoev > 0.98*maantal:
            mbestst = True
        else:
            mbestst = False
                     
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer(), primary_key=True),
            Column('art_voorraad', Float),
            Column('bestelstatus'),
            Column('artikelprijs', Float),
            Column('bestelsaldo', Float))
        if maccptversch > 0:
            upd = update(artikelen).where(artikelen.c.artikelID == martikelnr).\
              values(art_voorraad = artikelen.c.art_voorraad + maccptversch,\
              bestelstatus = mbestst, bestelsaldo = artikelen.c.bestelsaldo - maccptversch)
            conn.execute(upd)
            artikelmutaties = Table('artikelmutaties', metadata,
                Column('mutatieID', Integer, primary_key=True),
                Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
                Column('hoeveelheid', Float),
                Column('boekdatum', String),
                Column('tot_mag_prijs', Float),
                Column('btw_hoog', Float),
                Column('regel', Integer))
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sel = select([artikelen.c.artikelID, artikelen.c.artikelprijs]).\
             where(artikelen.c.artikelID == martikelnr)
            rpsel = con.execute(sel).first()
            martprijs = rpsel[1]
            params_finance = Table('params_finance', metadata,
                Column('financeID', Integer, primary_key=True),
                Column('factor', Float),
                Column('item', String))

            selpar = select([params_finance]).order_by(params_finance.c.financeID)
            rppar = con.execute(selpar).fetchall()
            try: 
                mutnr=(conn.execute(select([func.max(artikelmutaties.c.mutatieID,\
                                type_=Integer)])).scalar())
                mutnr += 1
            except:
                mutnr = 1
            
            mboekd = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10] 
             
            ins = insert(artikelmutaties).values(mutatieID = mutnr, artikelID =\
            martikelnr, orderinkoopID = mordnr, hoeveelheid = maccptversch,\
            boekdatum = mboekd, tot_mag_prijs = maccptversch*martprijs,\
            btw_hoog = maccptversch*martprijs*(rppar[0][1]), regel = mregel)
            conn.execute(ins)
        y = 0
        for x in range(2,13):
            if data[x]:
                y =1
        if y:
            invoerOK()
 
    mregel = 0
    inkoopOrder(m_email, minkordernr, mregel)