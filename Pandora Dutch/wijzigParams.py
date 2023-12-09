from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QDialog, QLabel,\
            QGridLayout, QPushButton, QMessageBox, QLineEdit
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine)
from sqlalchemy.sql import select, update
 
def geenWijz():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Geen wijzigingen verwerkt')
    msg.setWindowTitle('Parameters wijzigen')
    msg.exec_()
     
def wijzigOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Wijziging gelukt')
    msg.setWindowTitle('Parameters wijzigen')
    msg.exec_()
    
def refresh(m_email, self):
    self.close()
    toonParams(m_email)
    
def toonParams(m_email):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Parameters wijzigen')
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
            freshBtn.clicked.connect(lambda: refresh(m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 5, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 4, 1, 1, Qt.AlignRight | Qt.AlignBottom)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 2, 1, 1, Qt.AlignBottom)
            
            self.setLayout(grid)
            self.setGeometry(300, 50, 900, 900)
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
             
    header = ['ParamID', 'Item', 'Tarief', 'Verrekening', 'Ondergrens', 'Bovengrens', 'Aanpassing','Lock', 'Tarieffactor']
    
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('tarief', Float),
        Column('verrekening', String),
        Column('ondergrens', Float),
        Column('bovengrens', Float),
        Column('datum', String),
        Column('lock', Boolean),
        Column('tarieffactor', Float))
   
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
        
    sel = select([params]).order_by(params.c.paramID.asc())
    
    rp = con.execute(sel)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        paramnr = idx.data()
        if idx.column() == 0: 
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params]).where(params.c.paramID == paramnr)
            rppar = con.execute(selpar).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Wijzigen parameters")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setFont(QFont('Arial', 10))   
                    
                    self.Item = QLabel()
                    q1Edit = QLineEdit(rppar[1])
                    q1Edit.setCursorPosition(0)
                    q1Edit.setFixedWidth(150)
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.textChanged.connect(self.q1Changed) 
                    reg_ex = QRegExp("^.{0,20}$")
                    input_validator = QRegExpValidator(reg_ex, q1Edit)
                    q1Edit.setValidator(input_validator)
                                    
                    self.Tarief = QLabel()
                    q2Edit = QLineEdit(str(round(float(rppar[2]),2)))
                    q2Edit.setFixedWidth(100)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.textChanged.connect(self.q2Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q2Edit)
                    q2Edit.setValidator(input_validator)
                     
                    self.Verrekening = QLabel()
                    q3Edit = QLineEdit(rppar[3])
                    q3Edit.setFixedWidth(200)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.textChanged.connect(self.q3Changed) 
                    reg_ex = QRegExp("^.{0,20}$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                                               
                    self.Ondergrens = QLabel()
                    q4Edit = QLineEdit(str(round(float(rppar[4]),2)))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.textChanged.connect(self.q4Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)
                    
                    self.Bovengrens = QLabel()
                    q5Edit = QLineEdit(str(round(float(rppar[5]),2)))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.textChanged.connect(self.q5Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q5Edit)
                    q5Edit.setValidator(input_validator)
                    
                    self.Tarieffactor = QLabel()
                    q6Edit = QLineEdit(str(round(float(rppar[8]),2)))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.textChanged.connect(self.q6Changed) 
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q6Edit)
                    q5Edit.setValidator(input_validator)
                                             
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Parameternummer')  
                    grid.addWidget(lbl1, 1, 0)
                    lbl2 = QLabel(str(paramnr))
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
                    
                    lbl8 = QLabel('Aanpassing')
                    grid.addWidget(lbl8, 7, 0)
                    lbl9 = QLabel(rppar[6])
                    grid.addWidget(lbl9, 7, 1)
                    
                    lbl10 = QLabel('Lock: '+str(rppar[7]))
                    grid.addWidget(lbl10, 7, 2)
                    
                    lbl11 = QLabel('Tarieffactor')
                    grid.addWidget(lbl11, 8,0)
                    grid.addWidget(q6Edit, 8, 1)
                                                  
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl, 0, 0, 1, 2)
                                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 2, 1 , 1, Qt.AlignRight)
                                                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 0, 1, 3, Qt.AlignCenter)                  
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
            
                    applyBtn = QPushButton('Wijzig')
                    applyBtn.clicked.connect(self.accept)
            
                    grid.addWidget(applyBtn, 9, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
 
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
            
                    grid.addWidget(cancelBtn, 9, 1, 1, 1, Qt.AlignRight)
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
                    dialog = MainWindow()
                    dialog.exec_()
                    return [dialog.returnq1(), dialog.returnq2(), dialog.returnq3(),\
                            dialog.returnq4(), dialog.returnq5(), dialog.returnq6()]
    
            mainWin = MainWindow()
            data = mainWin.getData()
            
            flag = 0
            for k in range(0,6):
                if data[k]:
                    flag = 1
            if flag == 0:
                return
            
            if data[0]:
                mf0 = data[0]
            else:
                mf0 = rppar[1]
            if data[1]:
                mf1 = float(data[1])
            else:
                mf1 = rppar[2]  
            if data[2]:
                mf2 = data[2]
            else:
                mf2 = rppar[3]
            if data[3]:
                mf3 = float(data[3])
            else:
                mf3 = rppar[4]
            if data[4]:
                mf4 = float(data[4])
            else:
                mf4 = rppar[5]
            if data[5]:
                mf5 = float(data[5])
            else:
                mf5 = rppar[8]
                       
            dt = str(datetime.datetime.now())[0:10]  
           
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            updpar = update(params).where(params.c.paramID==paramnr).values(item = mf0,\
                    tarief = mf1, verrekening = mf2, ondergrens = mf3, bovengrens = mf4,\
                    tarieffactor = mf5, datum = dt, lock = False)
            con.execute(updpar)
            con.close()                      
            wijzigOK()
   
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)
        