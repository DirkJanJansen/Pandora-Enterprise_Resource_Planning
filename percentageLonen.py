import datetime
from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
      QDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QRegExpValidator, QPixmap
from PyQt5.QtCore import Qt,  QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, update
   
def eindModule(self,m_email):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Input aborted.')
    msg.setWindowTitle('Wages')
    msg.exec_()
    self.close()
    hoofdMenu(m_email)
    
def invoerOK(m_email):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Input successful!')
    msg.setWindowTitle('Wages')
    msg.exec_()
    hoofdMenu(m_email)
    
def invoerVerpl():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Input required\nor close the program!')
    msg.setWindowTitle('Wage table')
    msg.exec_()

def percLoonschaal(m_email):
    class Widget(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            
            grid = QGridLayout()
            grid.setSpacing(12)
            
            self.setWindowTitle("Percentage adjustment of wages")
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
            
            grid.addWidget(QLabel('     Adjust wages in percentage terms'), 1, 0, 1, 3, Qt.AlignCenter)
                
            self.Percentage = QLabel()
            q1Edit = QLineEdit()
            q1Edit.setFixedWidth(100)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
                          
            lbl1 = QLabel('Percentage increase')
            grid.addWidget(lbl1, 2, 0, 1, 2, Qt.AlignRight)
            grid.addWidget(q1Edit, 2, 2)
                 
            wijzig = QPushButton('Modify')
            wijzig.clicked.connect(self.accept)
    
            grid.addWidget(wijzig, 3, 1, 1 , 2, Qt.AlignRight)
            wijzig.setFont(QFont("Arial",10))           
            wijzig.setStyleSheet("color: black;  background-color: gainsboro; selection-background-color: gainsboro; selection-color: black")
            wijzig.setFixedWidth(100)  
            
            sluit = QPushButton('Close')
            sluit.clicked.connect(lambda: eindModule(self, m_email))
    
            grid.addWidget(sluit, 3, 0, 1 , 2, Qt.AlignRight)
            sluit.setFont(QFont("Arial",10))
            sluit.setStyleSheet("color: black;  background-color: gainsboro; selection-background-color: gainsboro; selection-color: black")
            sluit.setFixedWidth(100)  
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
                                                                    
            self.setLayout(grid)
            self.setGeometry(100, 50, 150, 150)
            
        def q1Changed(self,text):
            self.Percentage.setText(text)
    
        def returnq1(self):
            return self.Percentage.text()
     
        @staticmethod
        def getData(parent=None):
            dialog = Widget()
            dialog.exec_()
            return [dialog.returnq1()]  
                    
    window = Widget()
    data = window.getData()
    
    if data[0]:
        mperc = float(data[0])
    else:
        invoerVerpl()
        return
    
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
    sellon = select([lonen])
    rplon = con.execute(sellon)
      
    mboekd = str(datetime.datetime.now())[0:10] 
    for row in rplon:
        updlon = update(lonen).where(lonen.c.loonID==row[0]).values(maandloon = row[5]*1+mperc/100, tabelloon = row[1]*1+mperc/100,\
                werkuur =row[2]*1+mperc/100, reisuur = row[3]*1+mperc/100, boekdatum = mboekd)
        con.execute(updlon)
    invoerOK(m_email)