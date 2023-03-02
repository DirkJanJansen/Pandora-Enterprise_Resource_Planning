from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout,\
       QDialog, QLabel, QGridLayout, QPushButton, QLineEdit
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine)
from sqlalchemy.sql import select
        
def toonParams(m_email):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(300, 50, 900, 900)
            self.setWindowTitle('Request parameters')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(selParam)
            #table_view.clicked.connect(showSelection)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
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
             
    header = ['ParamID', 'Item', 'Tariff', 'Conversion', 'Lower limit', 'Upper limit', 'Date','Lock','Rate factor']
    
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
        
    sel = select([params]).order_by(params.c.paramID)
    
    rp = con.execute(sel)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def selParam(idx):
        mparam = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params]).where(params.c.paramID == mparam)
            rppar = con.execute(selpar).first()
            
            '''
            colnr = idx.column()
            cell = idx.data()
            rownr = idx.row()
            model = idx.model()
            print('Column nummer: ',colnr,'Row nummer: ', rownr,'Veld: ', cell, model)
            '''
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Opvragen Parameters")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setFont(QFont('Arial', 10))   
                    
                    self.Item = QLabel()
                    q1Edit = QLineEdit(rppar[1])
                    q1Edit.setCursorPosition(0)
                    q1Edit.setFixedWidth(150)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    self.Tarief = QLabel()
                    q2Edit = QLineEdit('{:12.2f}'.format(rppar[2]))
                    q2Edit.setFixedWidth(100)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                     
                    self.Verrekening = QLabel()
                    q3Edit = QLineEdit(rppar[3])
                    q3Edit.setFixedWidth(200)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                                               
                    self.Ondergrens = QLabel()
                    q4Edit = QLineEdit('{:12.2f}'.format(rppar[4]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    self.Bovengrens = QLabel()
                    q5Edit = QLineEdit('{:12.2f}'.format(rppar[5]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    self.Tarieffactor = QLabel()
                    q6Edit = QLineEdit('{:12.2f}'.format(rppar[8]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
          
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Paramete number')
                    grid.addWidget(lbl1, 1, 0)
                    
                    lbl2 = QLabel(str(rppar[0]))
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Item')  
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q1Edit, 2, 1, 1, 2) 
                                                         
                    lbl4 = QLabel('Tariff')
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(q2Edit, 3, 1)
                    
                    lbl5 = QLabel('Conversion')
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q3Edit, 4, 1, 1, 2)
                    
                    lbl6 = QLabel('Lower limit')
                    grid.addWidget(lbl6, 5, 0)
                    grid.addWidget(q4Edit, 5, 1)
                                   
                    lbl7 = QLabel('Upper limit')
                    grid.addWidget(lbl7, 6, 0)
                    grid.addWidget(q5Edit, 6, 1)
                    
                    lbl8 = QLabel('Adaptation')
                    grid.addWidget(lbl8, 7, 0)
                    lbl9 = QLabel(rppar[6])
                    grid.addWidget(lbl9, 7, 1)
                    
                    lbl10 = QLabel('Lock: '+str(rppar[7]))
                    grid.addWidget(lbl10, 7, 2)
                    
                    lbl11 = QLabel('Rate factor: ')
                    grid.addWidget(lbl11, 8, 0)
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
            
                    applyBtn = QPushButton('Close')
                    applyBtn.clicked.connect(self.accept)
            
                    grid.addWidget(applyBtn, 9, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
            mainWin = MainWindow()
            mainWin.exec_() 
              
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)