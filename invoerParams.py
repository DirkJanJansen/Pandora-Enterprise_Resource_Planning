from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout,\
                            QPushButton, QMessageBox, QLineEdit
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData,\
                         create_engine, select, insert, func, ForeignKey)

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)    
    
def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Invoer gelukt')
    msg.setWindowTitle('INVOEREN')
    msg.exec_()
    
def invVerplicht():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Verplichte invoer')
    msg.setWindowTitle('INVOEREN')
    msg.exec_()
    
def invParams(m_email):
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('tarief', Float),
        Column('verrekening', String),
        Column('ondergrens', Float),
        Column('bovengrens', Float),
        Column('datum', String),
        Column('tarieffactor', Float),
        Column('loonID', None, ForeignKey('lonen.loonID')))
  
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    try:
        mparnr = (con.execute(select([func.max(params.c.paramID,\
                type_=Integer)])).scalar())
        mparnr += 1
    except:
        mparnr = 1
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            grid = QGridLayout()
            grid.setSpacing(20)
            self.setWindowTitle("Invoeren Parameters")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            
            self.setFont(QFont('Arial', 10))   
            
            self.Item = QLabel()
            q1Edit = QLineEdit()
            q1Edit.setCursorPosition(0)
            q1Edit.setFixedWidth(150)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed) 
            reg_ex = QRegExp("^.{0,20}$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
                            
            self.Tarief = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(100)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
             
            self.Verrekening = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setFixedWidth(200)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed) 
            reg_ex = QRegExp("^.{0,20}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
            
            self.Ondergrens = QLabel()
            q4Edit = QLineEdit()
            q4Edit.setFixedWidth(100)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            self.Bovengrens = QLabel()
            q5Edit = QLineEdit()
            q5Edit.setFixedWidth(100)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.textChanged.connect(self.q5Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            self.Tarieffactor = QLabel()
            q6Edit = QLineEdit()
            q6Edit.setFixedWidth(100)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed) 
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
  
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl1 = QLabel('Parameternummer')  
            grid.addWidget(lbl1, 1, 0)
            
            lbl2 = QLabel(str(mparnr))
            grid.addWidget(lbl2, 1, 1)
                   
            lbl3 = QLabel('Item')  
            grid.addWidget(lbl3, 2, 0)
            grid.addWidget(q1Edit, 2, 1, 1, 2) 
                                                 
            lbl4 = QLabel('Tarief')  
            grid.addWidget(lbl4, 3, 0)
            grid.addWidget(q2Edit, 3, 1)
            
            lbl5 = QLabel('Verrekening')  
            grid.addWidget(lbl5, 4, 0)
            grid.addWidget(q3Edit, 4, 1, 1, 2)
                                       
            lbl6 = QLabel('Ondergrens')  
            grid.addWidget(lbl6, 5, 0)
            grid.addWidget(q4Edit, 5, 1)
                           
            lbl7 = QLabel('Bovengrens')  
            grid.addWidget(lbl7, 6, 0)
            grid.addWidget(q5Edit, 6, 1)
            
            lbl8 = QLabel('Tarieffactor')  
            grid.addWidget(lbl8, 7, 0)
            grid.addWidget(q6Edit, 7, 1)     
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)
                         
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1 , 1, Qt.AlignRight)
                                            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 3, Qt.AlignCenter)
              
            self.setLayout(grid)
            self.setGeometry(400, 250, 450, 150)
    
            applyBtn = QPushButton('Invoer')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 8, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
    
            grid.addWidget(cancelBtn, 8, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
             
        def q1Changed(self,text):
            self.Item.setText(text)
    
        def q2Changed(self,text):
            self.Tarief.setText(text)
    
        def q3Changed(self,text):
            self.Verrekening.setText(text)

        def q4Changed(self,text):
            self.Ondergrens.setText(text)
     
        def q5Changed(self,text):
            self.Bovengrens.setText(text)
            
        def q6Changed(self,text):
            self.Tarieffactor.setText(text)
        
        def returnq1(self):
            return self.Item.text()
        
        def returnq2(self):
            return self.Tarief.text()
        
        def returnq3(self):
            return self.Verrekening.text()
    
        def returnq4(self):
            return self.Ondergrens.text()
        
        def returnq5(self):
            return self.Bovengrens.text()
        
        def returnq6(self):
            return self.Tarieffactor.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(),\
                    dialog.returnq4(), dialog.returnq5(), dialog.returnq6()]

    window = Widget()
    data = window.getData()
   
    if data[0]:
        mf0 = data[0]
    else:
        invVerplicht()
        return
    if data[1]:
        mf1 = float(data[1])
    else:
        invVerplicht()
        return 
    if data[2]:
        mf2 = data[2]
    else:
        invVerplicht()
        return
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
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    dt = str(datetime.datetime.now())  
    dt = dt[0:10]     
    inspar = insert(params).values(paramID = mparnr, item = mf0,tarief = mf1,\
                   verrekening = mf2, ondergrens = mf3, bovengrens = mf4, \
                   tarieffactor = mf5, datum = dt)   
    con.execute(inspar) 
    con.close()
    invoerOK()