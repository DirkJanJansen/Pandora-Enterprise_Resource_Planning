from login import hoofdMenu
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout,\
                 QPushButton, QLineEdit, QWidget, QTableView, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, and_

def noRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record present, first insert record(s)!')
    msg.setWindowTitle('Insert parameters')
    msg.exec_()

def eigenBedrijf(m_email):
    metadata = MetaData()
    kopers = Table('kopers', metadata,
       Column('koperID', Integer(), primary_key=True),
       Column('bedrijfsnaam', String),
       Column('rechtsvorm', String),
       Column('afdeling', String),
       Column('btwnummer', String),
       Column('kvknummer', String),
       Column('telnr', String),
       Column('huisnummer', String),
       Column('toevoeging', String),
       Column('postcode', String))
    koper_accounts = Table('koper_accounts', metadata,
       Column('koperaccID', Integer, primary_key=True),
       Column('accountID', Integer, ForeignKey('accounts.accountID')),
       Column('koperID', Integer, ForeignKey('kopers.koperID')))
    accounts = Table('accounts', metadata,
       Column('accountID', Integer, primary_key=True),
       Column('email', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    selkop = select([kopers, koper_accounts, accounts]).where(and_(kopers.c.koperID == koper_accounts.c.koperID,\
              koper_accounts.c.accountID == accounts.c.accountID, accounts.c.email == m_email))
    rpkop = conn.execute(selkop)
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Request own sales company')
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
            table_view.clicked.connect(showBedrijf)
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
            try:
                return len(self.mylist[0])
            except:
                noRecord()
                hoofdMenu(m_email)
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
 
    header = ['Sales companyID','Company name', 'Legal status','Department', 'VAT number', 'KVK number',\
              'Telephone number','Street', 'House number', 'Suffix', 'Zipcode', 'Residence']

    import postcode
    
    data_list=[]
    for row in rpkop:
        msp = postcode.checkpostcode(row[9],int(row[7]))
        mstraat = msp[0]
        mplaats = msp[1]
        
        data_list += [(row[0],row[1],row[2],row[3],row[4],row[5],\
                     row[6],mstraat,int(row[7]),row[8],row[9],mplaats)]  
                                    
    def showBedrijf(idx):
        mbedrnr = idx.data()
        if idx.column() == 0:
            selkoper = select([kopers]).where(kopers.c.koperID == mbedrnr)
            rpkoper = conn.execute(selkoper).first()
            mpostcode = rpkoper[9]
            mhuisnr = int(rpkoper[7])
            import postcode
            mstrtplts = postcode.checkpostcode(mpostcode,mhuisnr)
            mstraat = mstrtplts[0]
            mplaats = mstrtplts[1]

            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Request sales companies")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))

                    self.setFont(QFont('Arial', 10))

                    self.Bedrijfsnaam = QLabel()
                    q3Edit = QLineEdit(rpkoper[1])
                    q3Edit.setFixedWidth(540)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setDisabled(True)
                    q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Afdeling = QLabel()
                    q16Edit = QLineEdit(rpkoper[3])
                    q16Edit.setFixedWidth(540)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.setDisabled(True)
                    q16Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Rechtsvorm = QLabel()
                    q5Edit = QLineEdit(rpkoper[2])
                    q5Edit.setFixedWidth(100)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setDisabled(True)
                    q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.BTWnummer =  QLabel()
                    q2Edit = QLineEdit(rpkoper[4])
                    q2Edit.setDisabled(True)
                    q2Edit.setFixedWidth(170)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.KvKnummer =  QLabel()
                    q4Edit = QLineEdit(rpkoper[5])
                    q4Edit.setFixedWidth(110)
                    q4Edit.setDisabled(True)
                    q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Straat =  QLabel()
                    q1Edit = QLineEdit()
                    q1Edit.setText(mstraat)
                    q1Edit.setFixedWidth(540)
                    q1Edit.setDisabled(True)
                    q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Huisnummer = QLabel()
                    q7Edit = QLineEdit(str(mhuisnr))
                    q7Edit.setFixedWidth(60)
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setFont(QFont("Arial",10))
                    q7Edit.setDisabled(True)
                    q7Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Toevoeging = QLabel()
                    q8Edit = QLineEdit(rpkoper[8])
                    q8Edit.setFixedWidth(80)
                    q8Edit.setFont(QFont("Arial",10))
                    q8Edit.setDisabled(True)
                    q8Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Postcode = QLabel()
                    q6Edit = QLineEdit(mpostcode)
                    q6Edit.setFixedWidth(80)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.setDisabled(True)
                    q6Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Woonplaats =  QLabel()
                    q15Edit = QLineEdit(mplaats)
                    q15Edit.setFixedWidth(400)
                    q15Edit.setDisabled(True)
                    q15Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Telefoonnr = QLabel()
                    q13Edit = QLineEdit(rpkoper[6])
                    q13Edit.setFixedWidth(120)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.setDisabled(True)
                    q13Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    self.Bedrijfverkoopnummer =  QLabel()
                    q14Edit = QLineEdit(str(rpkoper[0]))
                    q14Edit.setFixedWidth(120)
                    q14Edit.setAlignment(Qt.AlignRight)
                    q14Edit.setDisabled(True)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")

                    grid = QGridLayout()
                    grid.setSpacing(20)

                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl , 0, 0)

                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 1, 1, 2, Qt.AlignRight)

                    self.setFont(QFont('Arial', 10))
                    grid.addWidget(QLabel('Request sales companies'), 0, 1)

                    grid.addWidget(QLabel('Company name'), 1, 0)
                    grid.addWidget(q3Edit, 1, 1, 1, 3)

                    grid.addWidget(QLabel('Department name/Room/\nContact person'), 2, 0)
                    grid.addWidget(q16Edit, 2, 1, 1, 3)

                    grid.addWidget(QLabel('Legal status'), 3, 0)
                    grid.addWidget(q5Edit, 3, 1)

                    grid.addWidget(QLabel('VAT number'), 3, 1, 1, 1, Qt.AlignRight)
                    grid.addWidget(q2Edit, 3, 2)

                    grid.addWidget(QLabel('KvK number'), 4, 0)
                    grid.addWidget(q4Edit, 4, 1)

                    grid.addWidget(QLabel('Street'), 5, 0)
                    grid.addWidget(q1Edit, 5, 1, 1, 3)

                    grid.addWidget(QLabel('House number'), 6, 0)
                    grid.addWidget(q7Edit, 6, 1)

                    grid.addWidget(QLabel('Suffix'), 6, 1, 1, 1, Qt.AlignRight)
                    grid.addWidget(q8Edit, 6, 2)

                    grid.addWidget(QLabel('Zipcode Residence'), 7, 0)
                    grid.addWidget(q6Edit, 7, 1)

                    grid.addWidget(q15Edit, 7, 1, 1, 2, Qt.AlignRight)

                    grid.addWidget(QLabel('Telephone number'), 8, 0)
                    grid.addWidget(q13Edit, 8, 1)

                    grid.addWidget(QLabel('Sales company number'), 9, 0)
                    grid.addWidget(q14Edit, 9, 1)

                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 1)

                    terugBtn = QPushButton('Close')
                    terugBtn.clicked.connect(self.accept)

                    grid.addWidget(terugBtn, 9, 2, 1, 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100)
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    self.setLayout(grid)
                    self.setGeometry(500, 100, 150, 150)

            mainWin = Widget()
            mainWin.exec_()
       
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)
 
