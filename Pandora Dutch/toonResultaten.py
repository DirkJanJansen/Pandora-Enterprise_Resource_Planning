from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QTableView, QVBoxLayout, QLabel,\
      QLineEdit, QGridLayout, QPushButton
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData,\
                        create_engine, select)

def toonResult(m_email):
    metadata = MetaData()
    resultaten = Table('resultaten', metadata,
        Column('resID', Integer(), primary_key=True),
        Column('boekweek', String),
        Column('statusweek', String),
        Column('btotaal', Float),
        Column('wtotaal', Float),
        Column('betaald_bedrag', Float),
        Column('meerminderwerk', Float),
        Column('onderhandenwerk', Float),
        Column('aanneemsom', Float),
        Column('blonen', Float),
        Column('wlonen', Float),
        Column('bmaterialen', Float),
        Column('wmaterialen', Float),
        Column('bmaterieel', Float),
        Column('wmaterieel', Float),
        Column('bprojectkosten', Float),
        Column('wprojectkosten', Float),
        Column('binhuur', Float),
        Column('winhuur', Float),
        Column('bdiensten', Float),
        Column('wdiensten', Float),
        Column('bruto_winst', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selres = select([resultaten]).order_by(resultaten.c.boekweek, resultaten.c.statusweek)
    rpres = con.execute(selres)
    
    class window(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1700, 900)
            self.setWindowTitle('Resultaten opvragen per boekweek')
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
            table_view.clicked.connect(Resultaten)
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
                                       
    header = ['ID','Boekweek','Statusweek','Totaal begroot','Totaal werkelijk','Betaald bedrag',\
          'Meer-/minderwerk','Onderhanden werk','Aanneemsom','Lonen begroot','Lonen werkelijk',\
          'Materialen begroot','Materialen werkelijk','Materiëel begroot','Materiëel werkelijk',\
          'Projectkosten begroot','Projectkosten werkelijk','Inhuur begroot','Inhuur werkelijk',\
          'Diensten begroot','Diensten Werkelijk','Brutowinst']    

    data_list=[]
    for row in rpres:
        data_list += [(row)]
        
    def Resultaten(idx):
        idxnr = idx.data()
        if  idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selres = select([resultaten]).where(resultaten.c.resID == idxnr)
            rpres = con.execute(selres).first()
   
            class Window(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setWindowTitle("Opvragen resultaten per boekweek")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Opvragen resultaten werken extern per boekweek'),0, 2, 1, 3)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 5, 1, 1, Qt.AlignRight)                
                    index = 3
                    for item in header:
                        horpos = index%3
                        verpos = index
                        if index%3 == 1:
                            verpos = index - 1
                        elif index%3 == 2:
                            verpos = index -2
                        self.lbl = QLabel('{:15}'.format(header[index-3]))
                        
                        self.Gegevens = QLabel()
                        if index-3 > 2:
                            q1Edit = QLineEdit('{:12.2f}'.format(rpres[index-3]))
                        else:
                            q1Edit = QLineEdit(str(rpres[index-3]))
                        q1Edit.setAlignment(Qt.AlignRight)
                        q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                        q1Edit.setFixedWidth(150)
                        q1Edit.setDisabled(True)
                        grid.addWidget(self.lbl, verpos, horpos+horpos%3)
                        grid.addWidget(q1Edit, verpos, horpos+horpos%3+1)
                        
                        index +=1
                        
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, verpos+1, 5, 1 , 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100)  
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), verpos+2, 2, 1, 2)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(200, 300, 150, 150)
                            
            mainWin = Window()
            mainWin.exec_()
                        
    win = window(data_list, header)
    win.exec_()
    hoofdMenu(m_email)