from login import hoofdMenu
import  datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
     QDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QRegExpValidator, QPixmap
from PyQt5.QtCore import Qt,  QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, insert, func

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def eindProgram():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Program closed.\nGoodbye!')
    msg.setWindowTitle('Orders')
    msg.exec_() 
    
def invoerOK(mloonnr, momschr):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert of pay scale: '+mloonnr+' '+momschr+' successful!')
    msg.setWindowTitle('Pay scale')
    msg.exec_()
    
def invoerVerpl():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Input all fields required\nStart again with enter\nOr end the program!')
    msg.setWindowTitle('Pay scale')
    msg.exec_()

def invoerSchaal(m_email):
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
    try:
        mloonnr = (con.execute(select([func.max(lonen.c.loonID,\
                        type_=Integer)])).scalar())
        mloonnr += 1
    except:
        mloonnr = 1
    mboekd = str(datetime.datetime.now())[0:10] 
    
    class Widget(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            
            grid = QGridLayout()
            grid.setSpacing(12)
            
            self.setWindowTitle("Input wage table")
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
            
            grid.addWidget(QLabel('        Entering pay scales'), 0, 0, 1, 3, Qt.AlignCenter)
                
            self.Loontabelnummer = QLabel()
            q1Edit = QLineEdit(str(mloonnr))
            q1Edit.setAlignment(Qt.AlignRight)
            q1Edit.setStyleSheet("color: black")
            q1Edit.setFixedWidth(100)
            q1Edit.setDisabled(True)
            q1Edit.setFont(QFont("Arial",10))
         
            self.Omschrijving = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(320)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed)
            
            self.Maandloon = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setFixedWidth(100)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
                                       
            self.Tabelloon = QLabel()
            q4Edit = QLineEdit()
            q4Edit.setFixedWidth(100)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed)
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)

            self.Reisuurloon = QLabel()
            q6Edit = QLineEdit()
            q6Edit.setFixedWidth(100)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.textChanged.connect(self.q6Changed)
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q6Edit)
            q6Edit.setValidator(input_validator)
       
            lbl1 = QLabel('Wage table number')
            grid.addWidget(lbl1, 1, 0)
            grid.addWidget(q1Edit, 1, 1)
            
            lbl2 = QLabel('Job description')
            grid.addWidget(lbl2, 2, 0)
            grid.addWidget(q2Edit, 2, 1, 1, 2)
            
            lbl3 = QLabel('Monthly salary')
            grid.addWidget(lbl3, 3, 0)
            grid.addWidget(q3Edit, 3, 1)
                      
            lbl5 = QLabel('Tabular wages')
            grid.addWidget(lbl5, 4, 0)
            grid.addWidget(q4Edit, 4, 1)
           
            lbl7 = QLabel('Travel hourly wage')
            grid.addWidget(lbl7, 5, 0)
            grid.addWidget(q6Edit, 5, 1)
            
            lbl8 = QLabel('Modification date')
            lbl9 = QLabel(mboekd)
            grid.addWidget(lbl8, 6 ,0)
            grid.addWidget(lbl9, 6, 1)
       
            wijzig = QPushButton('Insert')
            wijzig.clicked.connect(self.accept)
    
            grid.addWidget(wijzig, 7, 1, 1 , 2, Qt.AlignRight)
            wijzig.setFont(QFont("Arial",10))
            wijzig.setFixedWidth(100)  
            
            sluit = QPushButton('Close')
            sluit.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(sluit, 7, 1, 1, 2, Qt.AlignCenter)
            sluit.setFont(QFont("Arial",10))
            sluit.setFixedWidth(100)  
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 0, 1, 3, Qt.AlignCenter)
                                                                    
            self.setLayout(grid)
            self.setGeometry(100, 50, 150, 150)
            
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
    
    if data[0]:
        momschr = data[0]
    else:
        invoerVerpl()
        return
    if data[1]:
        mmndloon = float(data[1])
    else:
        invoerVerpl()
        return
    if data[2]:
        mtabelloon = float(data[2])
    else:
        invoerVerpl()
        return
    if data[3]:
        mreisuurloon = float(data[3])
    else:
        invoerVerpl()
        return
    
    inslon = insert(lonen).values(loonID = mloonnr,functieomschr=momschr,\
            maandloon = mmndloon, tabelloon = mtabelloon,\
            reisuur=mreisuurloon, boekdatum = mboekd)
    con.execute(inslon)
    invoerOK(str(mloonnr), momschr)
