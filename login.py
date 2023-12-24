import os, sys
from datetime import datetime
from validZt import zt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon, QMovie, QColor
from PyQt5.QtWidgets import (QDialog, QGridLayout, QMessageBox,\
                             QLabel, QLineEdit, QPushButton, QComboBox)
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                    create_engine, select)

def check_password(hashed_password, user_password):
    import hashlib
    (password, salt) = hashed_password.split(':')
    return (password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())

def goodbye():
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    '''
    # release lock
    home = os.path.expanduser("~")
    os.remove(str(home)+'/.pandora_lock')
    '''
    msg.setText('Goodbye!       ')
    msg.setWindowTitle('LOGON')
    msg.exec_()
    sys.exit()
     
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Information ERP System Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Information ERP Pandora')
            grid.addWidget(lblinfo, 0, 0, 1, 2, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 1, Qt.AlignRight)
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            
            infolbl = QLabel(
      '''

        Information Enterprise Resource Planning (ERP) system Pandora 
        
        The software is licensed under GNU GPLv3 (License is enclosed).
         
        The system is designed in Python 3 with PyQt5 as the graphical interface.
        As relational database system is applied PostgreSQL with interface SQLAlchemy Core.
        The login is realized with encrypted SHA256 control with authorized
        and account-adjustable permissions. This at menu level and on other operations
        e.g. ordering, requesting, entering, changing, printing, etc. The permissions can be assigned
        by authorized persons. The creation of a account can be done by any person.
        By default, the account is created with the permissions to query and change own account,
        placing web orders, requesting and printing order data.
        All other authorizations must be carried out by an authorized person.
        Linking of the account is possible to employee, supplier, or buyer. 
        The other authorizations can then be granted for each department or work discipline.
        For this privileges, see the info for maintenance menu authorizations.
        The following submenus can be accessed from the main menu:
        Accounts, Suppliers, Employees, Purchasing, Sales, Warehouse, Working Internally, Working Externally,\t
        Calculation Internal, External Calculation, Wages Administration, Accounting, Stock Management,
        Management Information, Maintenance, Reprinting forms. 
        Authorizing these submenus and operations can be assigned with
        the maintenance menu, mutate permissions.                                 
  
     ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 50, 150, 100)
            
    window = Widget()
    window.exec_()
    
def closeIt(self):
    self.close()
    inlog()  
      
def noChoice():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No choice\nor more than one choice made!')
    msg.setWindowTitle('MENU')
    msg.exec_()
    
def capslkOn():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Capslock is enabled!')
    msg.setWindowTitle('ENTRY!')
    msg.exec_()

def wrongemailAddress():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('E-mail address incorrect')
    msg.setWindowTitle('ENTRY')
    msg.exec_()

def wrongPassword():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Password incorrect')
    msg.setWindowTitle('ENTRY')
    msg.exec_()
    
def wrongcustomNumber():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Customnumber incorrect!')
    msg.setWindowTitle('ENTRY')
    msg.exec_()
    
def wrongLogon():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Logon failed!')
    msg.setWindowTitle('ENTRY')
    msg.exec_()

def createAccount(self):
    from invoerAccount import nieuwAccount
    nieuwAccount(self)
     
def inlog():
    #verification and logon
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Pandora business information system logon screen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))

            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")
            grid = QGridLayout()
            grid.setSpacing(20)

            self.email = QLabel()
            emailEdit = QLineEdit()
            emailEdit.setStyleSheet("background: #F8F7EE")
            emailEdit.setFixedWidth(200)
            emailEdit.setFont(QFont("Arial",10))
            emailEdit.textChanged.connect(self.emailChanged)

            self.Wachtwoord = QLabel()
            wachtwEdit = QLineEdit()
            wachtwEdit.setStyleSheet("background: #F8F7EE")
            wachtwEdit.setEchoMode(QLineEdit.Password)
            wachtwEdit.setFixedWidth(200)
            wachtwEdit.setFont(QFont("Arial",10))
            wachtwEdit.textChanged.connect(self.wachtwChanged)

            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)

            lblinfo = QLabel(' Pandora logon')
            grid.addWidget(lblinfo, 0, 1, 1, 2, Qt.AlignLeft)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)

            pandora = QLabel()
            movie = QMovie('./images/logos/pyqt5.gif')
            pandora.setMovie(movie)
            movie.start()
            grid.addWidget(pandora, 1 ,0, 1, 3, Qt.AlignCenter)

            grid.addWidget(QLabel('emailaddress or\nAccountnumber'), 3, 1)
            grid.addWidget(emailEdit, 3, 2)

            grid.addWidget(QLabel('Password'), 4, 1)
            grid.addWidget(wachtwEdit, 4, 2)

            self.setLayout(grid)
            self.setGeometry(600, 250, 150, 150)

            applyBtn = QPushButton('Logon')
            applyBtn.clicked.connect(self.accept)

            grid.addWidget(applyBtn, 5, 1, 1 , 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(90)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

            cancelBtn = QPushButton('Shutdown')
            cancelBtn.clicked.connect(lambda: goodbye())

            grid.addWidget(cancelBtn,  5, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

            nwBtn = QPushButton('New Account')
            nwBtn.clicked.connect(lambda: createAccount(self))

            grid.addWidget(nwBtn,  5, 0, 1, 2, Qt.AlignRight)
            nwBtn.setFont(QFont("Arial",10))
            nwBtn.setFixedWidth(140)
            nwBtn.setStyleSheet("color: black;  background-color: gainsboro")

            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())

            grid.addWidget(infoBtn,  5, 0, 1, 2)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(120)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3, Qt.AlignCenter)

        def emailChanged(self, text):
            self.email.setText(text)

        def wachtwChanged(self, text):
            self.Wachtwoord.setText(text)

        def returnemail(self):
            return self.email.text()

        def returnWachtwoord(self):
            return self.Wachtwoord.text()

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnemail(), dialog.returnWachtwoord()]

    window = Widget()
    data = window.getData()
    for item in data:
         if item.startswith(' '):
            noChoice()
            inlog()
    if sys.platform == 'win32':
        from win32api import GetKeyState
        from win32con import VK_CAPITAL
        capslk = GetKeyState(VK_CAPITAL)
        if capslk == 1:
            capslkOn()
            inlog()
    else:
        import subprocess
        if (subprocess.getoutput("xset q | grep LED")[65]) == '1':
            capslkOn()
            inlog()
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String, nullable=False),
        Column('password', String, nullable=False))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()

    if data[0] and zt(data[0],12):
        m_email = data[0]
        sel = select([accounts]).where(accounts.c.email == m_email)
        rpaccount = conn.execute(sel).first()
        if rpaccount:
            maccountnr = rpaccount[0]
            maccountnr = int(maccountnr)
            m_email = rpaccount[1]
            mpassword = rpaccount[2]
        else:
            wrongemailAddress()
            inlog()
    elif data[0] and zt(data[0],1):
        mklantnr = data[0]
        sel = select([accounts]).where(accounts.c.accountID == mklantnr)
        rpaccount = conn.execute(sel).first()
        if rpaccount:
            maccountnr = rpaccount[0]
            maccountnr = int(maccountnr)
            m_email = rpaccount[1]
            mpassword = rpaccount[2]
        else:
            wrongcustomNumber()
            inlog()
    else:
        wrongLogon()
        inlog()

    if data[1]:
        mwachtw = data[1]
    else:
        wrongPassword()
        inlog()

    if not check_password(mpassword,mwachtw):
        wrongPassword()
        inlog()
    hoofdMenu(m_email)

def hoofdMenu(m_email):
    # declare database table accounts for authorizations
    metadata = MetaData()
    accounts = Table('accounts', metadata,
                     Column('accountID', Integer(), primary_key=True),
                     Column('email', String, nullable=False),
                     Column('p1', String),
                     Column('p2', String),
                     Column('p3', String),
                     Column('p4', String),
                     Column('p5', String),
                     Column('p6', String),
                     Column('p7', String),
                     Column('p8', String),
                     Column('p9', String),
                     Column('p10', String),
                     Column('p11', String),
                     Column('p12', String),
                     Column('p13', String),
                     Column('p14', String),
                     Column('p15', String),
                     Column('p16', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([accounts]).where(accounts.c.email == m_email)
    rpaccount = conn.execute(sel).first()
    mp = rpaccount[2:18]

    # structure Menu's
    class Widget(QDialog):
        def __init__(self, parent=None, accperms=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Pandora Business Information System")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")

            self.Keuze0 = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(310)
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('Accounts')
            k0Edit.setFont(QFont("Arial", 10))
            k0Edit.setEditable(True)
            k0Edit.lineEdit().setFont(QFont("Arial",10))
            k0Edit.lineEdit().setReadOnly(True)
            k0Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k0Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k0Edit.addItem('1. Modify account')
            k0Edit.addItem('2. Requesting accounts')
            k0Edit.addItem('3. Ordering web articles')
            k0Edit.addItem('4. Requesting order overview')
            k0Edit.addItem('5. Printing order invoices')
            k0Edit.activated[str].connect(self.k0Changed)

            self.Keuze1 = QLabel()
            k1Edit = QComboBox()
            k1Edit.setFixedWidth(310)
            k1Edit.setFont(QFont("Arial",10))
            k1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k1Edit.addItem('Suppliers')
            k1Edit.setEditable(True)
            k1Edit.lineEdit().setFont(QFont("Arial",10))
            k1Edit.lineEdit().setReadOnly(True)
            k1Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k1Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k1Edit.addItem('1. Insert supplier data')
            k1Edit.addItem('2. Modify supplier data')
            k1Edit.addItem('3. Request supplier data')
            k1Edit.addItem('4. Self requesting own data.')
            k1Edit.activated[str].connect(self.k1Changed)
            
            self.Keuze2 = QLabel()
            k2Edit = QComboBox()
            k2Edit.setFixedWidth(310)
            k2Edit.setFont(QFont("Arial",10))
            k2Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k2Edit.addItem('Employees')
            k2Edit.setEditable(True)
            k2Edit.lineEdit().setFont(QFont("Arial",10))
            k2Edit.lineEdit().setReadOnly(True)
            k2Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k2Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k2Edit.addItem('1. Connect account-employee')
            k2Edit.addItem('2. Modify employee data')
            k2Edit.addItem('3. Request employees data')
            k2Edit.addItem('4. Request employee-period')
            k2Edit.activated[str].connect(self.k2Changed)
            
            self.Keuze3 = QLabel()
            k3Edit = QComboBox()
            k3Edit.setFixedWidth(310)
            k3Edit.setFont(QFont("Arial",10))
            k3Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k3Edit.addItem('Purchase')
            k3Edit.setEditable(True)
            k3Edit.lineEdit().setFont(QFont("Arial",10))
            k3Edit.lineEdit().setReadOnly(True)
            k3Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k3Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k3Edit.addItem('1. Insert orders materials')
            k3Edit.addItem('2. Modify orders materials')
            k3Edit.addItem('3. Insert orders services/equipment')
            k3Edit.addItem('4. Modify orders services/equipment')
            k3Edit.addItem('5. Request orders materials')
            k3Edit.addItem('6. Request orders services/equipment')
            k3Edit.activated[str].connect(self.k3Changed)
            
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(310)
            k4Edit.setFont(QFont("Arial",10))
            k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k4Edit.addItem('Sales')
            k4Edit.setEditable(True)
            k4Edit.lineEdit().setFont(QFont("Arial",10))
            k4Edit.lineEdit().setReadOnly(True)
            k4Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k4Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k4Edit.addItem('1. Sales-company create')
            k4Edit.addItem('2. Sales-company modify')
            k4Edit.addItem('3. Sales-companies request')
            k4Edit.addItem('4. Own data request')
            k4Edit.addItem('5. Web sales orders requesting')
            k4Edit.activated[str].connect(self.k4Changed)
 
            self.Keuze5 = QLabel()
            k5Edit = QComboBox()
            k5Edit.setFixedWidth(310)
            k5Edit.setFont(QFont("Arial",10))
            k5Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k5Edit.addItem('Warehouse')
            k5Edit.setEditable(True)
            k5Edit.lineEdit().setFont(QFont("Arial",10))
            k5Edit.lineEdit().setReadOnly(True)
            k5Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k5Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k5Edit.addItem('1. Insert articles')
            k5Edit.addItem('2. Modify articles')
            k5Edit.addItem('3. Request articles')
            k5Edit.addItem('4. Issuing materials (picklist)')
            k5Edit.addItem('5. Printing picklists')
            k5Edit.addItem('6. Booking differences/obsolete')
            k5Edit.addItem('7. Issuing web articles/printing')
            k5Edit.addItem('8. Return booking web items')
            k5Edit.addItem('9. Counter sales - barcode scan')
            k5Edit.activated[str].connect(self.k5Changed)
              
            self.Keuze6 = QLabel()
            k6Edit = QComboBox()
            k6Edit.setFixedWidth(310)
            k6Edit.setFont(QFont("Arial",10))
            k6Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k6Edit.addItem('Works internally')
            k6Edit.setEditable(True)
            k6Edit.lineEdit().setFont(QFont("Arial",10))
            k6Edit.lineEdit().setReadOnly(True)
            k6Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k6Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k6Edit.addItem('1. Insert work orders')
            k6Edit.addItem('2. Modify work orders')
            k6Edit.addItem('3. Request work orders/printing')
            k6Edit.addItem('4. Calling materials')
            k6Edit.addItem('5. Printing picklists')
            k6Edit.addItem('6. Mutate hourly consumption')
            k6Edit.activated[str].connect(self.k6Changed)
            
            self.Keuze7 = QLabel()
            k7Edit = QComboBox()
            k7Edit.setFixedWidth(310)
            k7Edit.setFont(QFont("Arial",10))
            k7Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k7Edit.addItem('Works externally')
            k7Edit.setEditable(True)
            k7Edit.lineEdit().setFont(QFont("Arial",10))
            k7Edit.lineEdit().setReadOnly(True)
            k7Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k7Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k7Edit.addItem('1. Insert work orders')
            k7Edit.addItem('2. Modify work orders')
            k7Edit.addItem('3. Request work orders')
            k7Edit.addItem('4. Calling materials')
            k7Edit.addItem('5. Printing picklists')
            k7Edit.addItem('6. Mutate cost services')
            k7Edit.addItem('7. Mutate hourly consumption')
            k7Edit.activated[str].connect(self.k7Changed)
            
            self.Keuze8 = QLabel()
            k8Edit = QComboBox()
            k8Edit.setFixedWidth(310)
            k8Edit.setFont(QFont("Arial",10))
            k8Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k8Edit.addItem('Calculation works internally')
            k8Edit.setEditable(True)
            k8Edit.lineEdit().setFont(QFont("Arial",10))
            k8Edit.lineEdit().setReadOnly(True)
            k8Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k8Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k8Edit.addItem('1. Create new clusters')
            k8Edit.addItem('2. Insert cluster data')
            k8Edit.addItem('3. Request cluster data')
            k8Edit.addItem('4. Insert article lines per cluster')
            k8Edit.addItem('5. Request article lines per cluster') 
            k8Edit.addItem('6. Create/change calculation')
            k8Edit.addItem('7. Calculation/Article list/printing')
            k8Edit.addItem('8. Calculation connect -> production')
            k8Edit.activated[str].connect(self.k8Changed)
        
            self.Keuze9 = QLabel()
            k9Edit = QComboBox()
            k9Edit.setFixedWidth(310)
            k9Edit.setFont(QFont("Arial",10))
            k9Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k9Edit.addItem('Calculation works externally')
            k9Edit.setEditable(True)
            k9Edit.lineEdit().setFont(QFont("Arial",10))
            k9Edit.lineEdit().setReadOnly(True)
            k9Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k9Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k9Edit.addItem('1. Create new clusters')
            k9Edit.addItem('2. Insert cluster data')
            k9Edit.addItem('3. Request cluster data')
            k9Edit.addItem('4. Insert article lines per cluster')
            k9Edit.addItem('5. Request article lines per cluster')
            k9Edit.addItem('6. Create/change calculation')
            k9Edit.addItem('7. Calculation/Article list/printing')
            k9Edit.addItem('8. Calculation connect -> production')
            k9Edit.activated[str].connect(self.k9Changed)
  
            self.Keuze10 = QLabel()
            k10Edit = QComboBox()
            k10Edit.setFixedWidth(310)
            k10Edit.setFont(QFont("Arial",10))
            k10Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k10Edit.addItem('Payroll administration')
            k10Edit.setEditable(True)
            k10Edit.lineEdit().setFont(QFont("Arial",10))
            k10Edit.lineEdit().setReadOnly(True)
            k10Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k10Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k10Edit.addItem('1. Request mutation of hours')
            k10Edit.addItem('2. Control hours for monthly wages')
            k10Edit.addItem('3. Payment of monthly wages')
            k10Edit.addItem('4. Request wages payments')
            k10Edit.addItem('5. Insert wages scales')
            k10Edit.addItem('6. Modify wages scales/requesting')
            k10Edit.addItem('7. Increase wages with percentage')
            k10Edit.activated[str].connect(self.k10Changed)
            
            self.Keuze11 = QLabel()
            k11Edit = QComboBox()
            k11Edit.setFixedWidth(310)
            k11Edit.setFont(QFont("Arial",10))
            k11Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k11Edit.addItem('Accounting')
            k11Edit.setEditable(True)
            k11Edit.lineEdit().setFont(QFont("Arial",10))
            k11Edit.lineEdit().setReadOnly(True)
            k11Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k11Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k11Edit.addItem('1. Article mutations requesting')
            k11Edit.addItem('2. Services mutations requesting')
            k11Edit.addItem('3. View and pay contributions')
            k11Edit.addItem('4. Weborders payments/print invoices')
            k11Edit.addItem('5. Book return payments')
            k11Edit.addItem('6. Print list to invoice external works')
            k11Edit.addItem('7. Request mutations of hours')
            k11Edit.activated[str].connect(self.k11Changed)
            
            self.Keuze12 = QLabel()
            k12Edit = QComboBox()
            k12Edit.setFixedWidth(310)
            k12Edit.setFont(QFont("Arial",10))
            k12Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k12Edit.addItem('Stock management')
            k12Edit.setEditable(True)
            k12Edit.lineEdit().setFont(QFont("Arial",10))
            k12Edit.lineEdit().setReadOnly(True)
            k12Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k12Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k12Edit.addItem('1. Stock management, order articles')
            k12Edit.addItem('2. Graph stocks, warehouse financial')
            k12Edit.addItem('3. Overview stocks financial')
            k12Edit.addItem('4. Request reservations')
            k12Edit.activated[str].connect(self.k12Changed)
            
            self.Keuze13 = QLabel()
            k13Edit = QComboBox()
            k13Edit.setFixedWidth(310)
            k13Edit.setFont(QFont("Arial",10))
            k13Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k13Edit.addItem('Management Information')
            k13Edit.setEditable(True)
            k13Edit.lineEdit().setFont(QFont("Arial",10))
            k13Edit.lineEdit().setReadOnly(True)
            k13Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k13Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k13Edit.addItem('1. Calculate financial data once/week')
            k13Edit.addItem('2. Print finance graphs external works')
            k13Edit.addItem('3. Print graphs by progress status')
            k13Edit.addItem('4. Request results works')
            k13Edit.activated[str].connect(self.k13Changed)
         
            self.Keuze14 = QLabel()
            k14Edit = QComboBox()
            k14Edit.setFixedWidth(310)
            k14Edit.setFont(QFont("Arial",10))
            k14Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k14Edit.addItem('Maintenance')
            k14Edit.setEditable(True)
            k14Edit.lineEdit().setFont(QFont("Arial",10))
            k14Edit.lineEdit().setReadOnly(True)
            k14Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k14Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k14Edit.addItem('1. Mutate authorisations')
            k14Edit.addItem('2. Connect account - supplier')
            k14Edit.addItem('3. Connect account - sales company')
            k14Edit.addItem('4. Insert parameters')
            k14Edit.addItem('5. Modify parameters')
            k14Edit.addItem('6. Request parameters')
            k14Edit.addItem('7. Sales work rates updating')
            k14Edit.activated[str].connect(self.k14Changed)

            self.Keuze15 = QLabel()
            k15Edit = QComboBox()
            k15Edit.setFixedWidth(310)
            k15Edit.setFont(QFont("Arial",10))
            k15Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k15Edit.addItem('Reprinting of forms')
            k15Edit.setEditable(True)
            k15Edit.lineEdit().setFont(QFont("Arial",10))
            k15Edit.lineEdit().setReadOnly(True)
            k15Edit.lineEdit().setAlignment(Qt.AlignCenter)
            k15Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            k15Edit.addItem('1. Calculation internal works')
            k15Edit.addItem('2. Calculation external works')  
            k15Edit.addItem('3. Internal orders purchase')
            k15Edit.addItem('4. Calling internal works')
            k15Edit.addItem('5. Calling external works')
            k15Edit.addItem('6. Picklists warehouse')
            k15Edit.addItem('7. Web orders packing slip')
            k15Edit.addItem('8. Control hours for paying wages')
            k15Edit.addItem('9. Wages specification employees')
            k15Edit.addItem('A. Invoices external works')
            k15Edit.addItem('B. Web orders payments') 
            k15Edit.addItem('C. Purchase orders services/material')  
            k15Edit.addItem('D. Counter sale order invoices') 
            k15Edit.activated[str].connect(self.k15Changed)
            
            #disable menu's if no permission is granted in table accounts
            # list of Mainmenu
            mplist=[k0Edit,k1Edit,k2Edit,k3Edit,k4Edit,k5Edit,k6Edit,k7Edit,\
                    k8Edit,k9Edit,k10Edit,k11Edit,k12Edit,k13Edit,k14Edit,k15Edit]

            # list of pointers by mainmenu and menulines per groups pointers towards database table accountpermissions
            lineperm = ([0, 4, 6, 2, 2, 5],[0, 3, 4, 6, 1],[0, 1, 4, 6, 6],[0, 3, 4, 3, 4, 6, 6],[0, 3, 4, 6, 1, 6],\
                        [0, 3, 4, 6, 4, 5, 1, 6, 3, 6],[0, 3, 4, 6, 3, 5, 3],[0, 3, 4, 6, 2, 6, 3, 3],\
                        [0, 3, 4, 6, 3, 6, 3, 6, 1],[0, 4, 4, 6, 3, 6, 3, 6, 1],[0, 6, 2, 1, 6, 3, 4, 1],\
                        [0, 6, 6, 2, 6, 2, 5, 6],[0, 2, 1, 1, 1],[0, 1, 6, 6, 6],[0, 1, 3, 3, 3, 4, 6, 4],[0])
            # loop on mainmenu and permissions in table accounts
            for menu in range(0,16):
                menuperms = lineperm[menu]
                perms = mp[menu]
                # if value in database is 0 for index 0 then disable mainmenulines
                if mp[menu][0] == '0':
                    mplist[menu].setDisabled(True)
                    mplist[menu].setStyleSheet("color: darkgrey; background-color: gainsboro")
                # subloop on menulines per menu
                # translate submenuline with linepointer from lineperm list, check if 0 in accounts table
                # if so disable menuline from selecting
                for lines in range(0,len(menuperms)):
                    linepointer = menuperms[lines]
                    mperm = perms[linepointer]
                    if mperm == '0' and linepointer > 0:
                         mplist[menu].model().item(lines).setEnabled(False)
                         mplist[menu].model().item(lines).setForeground(QColor('darkgrey'))
                         mplist[menu].model().item(lines).setBackground(QColor('gainsboro'))
            # combine account table functions with reprint functions, disable if 0
            if mp[8][5] == '0':
                 mplist[15].model().item(1).setEnabled(False)
                 mplist[15].model().item(1).setForeground(QColor('darkgrey'))
                 mplist[15].model().item(1).setBackground(QColor('gainsboro'))
            if mp[9][5] == '0':
                mplist[15].model().item(2).setEnabled(False)
                mplist[15].model().item(2).setForeground(QColor('darkgrey'))
                mplist[15].model().item(2).setBackground(QColor('gainsboro'))
            if mp[3][5] == '0':
                mplist[15].model().item(3).setEnabled(False)
                mplist[15].model().item(3).setForeground(QColor('darkgrey'))
                mplist[15].model().item(3).setBackground(QColor('gainsboro'))
            if mp[6][5] == '0':
                mplist[15].model().item(4).setEnabled(False)
                mplist[15].model().item(4).setForeground(QColor('darkgrey'))
                mplist[15].model().item(4).setBackground(QColor('gainsboro'))
            if mp[7][5] == '0':
                mplist[15].model().item(5).setEnabled(False)
                mplist[15].model().item(5).setForeground(QColor('darkgrey'))
                mplist[15].model().item(5).setBackground(QColor('gainsboro'))
            if mp[5][5] == '0':
                mplist[15].model().item(6).setEnabled(False)
                mplist[15].model().item(6).setForeground(QColor('darkgrey'))
                mplist[15].model().item(6).setBackground(QColor('gainsboro'))
            if mp[5][5] == '0':
                mplist[15].model().item(7).setEnabled(False)
                mplist[15].model().item(7).setForeground(QColor('darkgrey'))
                mplist[15].model().item(7).setBackground(QColor('gainsboro'))
            if mp[10][5] == '0':
                mplist[15].model().item(8).setEnabled(False)
                mplist[15].model().item(8).setForeground(QColor('darkgrey'))
                mplist[15].model().item(8).setBackground(QColor('gainsboro'))
            if mp[10][5] == '0':
                mplist[15].model().item(9).setEnabled(False)
                mplist[15].model().item(9).setForeground(QColor('darkgrey'))
                mplist[15].model().item(9).setBackground(QColor('gainsboro'))
            if mp[11][5] == '0':
                mplist[15].model().item(10).setEnabled(False)
                mplist[15].model().item(10).setForeground(QColor('darkgrey'))
                mplist[15].model().item(10).setBackground(QColor('gainsboro'))
            if mp[11][5] == '0':
                mplist[15].model().item(11).setEnabled(False)
                mplist[15].model().item(11).setForeground(QColor('darkgrey'))
                mplist[15].model().item(11).setBackground(QColor('gainsboro'))
            if mp[3][5] == '0':
                mplist[15].model().item(12).setEnabled(False)
                mplist[15].model().item(12).setForeground(QColor('darkgrey'))
                mplist[15].model().item(12).setBackground(QColor('gainsboro'))
            if mp[5][5] == '0':
                mplist[15].model().item(13).setEnabled(False)
                mplist[15].model().item(13).setForeground(QColor('darkgrey'))
                mplist[15].model().item(13).setBackground(QColor('gainsboro'))

            grid = QGridLayout()
            grid.setSpacing(20)
             
            grid.addWidget(k0Edit, 2, 0)
            grid.addWidget(k8Edit, 2, 1)
            
            grid.addWidget(k1Edit, 3, 0)
            grid.addWidget(k9Edit, 3, 1)
            
            grid.addWidget(k2Edit, 4, 0)
            grid.addWidget(k10Edit, 4, 1)
            
            grid.addWidget(k3Edit, 5, 0)
            grid.addWidget(k11Edit, 5, 1)
          
            grid.addWidget(k4Edit, 6, 0)
            grid.addWidget(k12Edit, 6, 1)
        
            grid.addWidget(k5Edit, 7, 0)
            grid.addWidget(k13Edit, 7, 1)
            
            grid.addWidget(k6Edit, 8, 0)
            grid.addWidget(k14Edit, 8, 1)
            
            grid.addWidget(k7Edit, 9 ,0)
            grid.addWidget(k15Edit, 9, 1)
                            
            pandora = QLabel()
            pixmap = QPixmap('./images/logos/menu.png')
            pandora.setPixmap(pixmap)
            grid.addWidget(pandora, 0 ,0, 1, 3, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 11, 1, 2, 1, Qt.AlignRight)

            pandora = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            pandora.setPixmap(pixmap)
            grid.addWidget(pandora, 11 ,0, 2, 1)
                                                       
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 14, 0, 1, 3, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(600, 100, 150, 150)
            
            applyBtn = QPushButton('Choose')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 13, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(130)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Logout')
            cancelBtn.clicked.connect(lambda: closeIt(self))
    
            grid.addWidget(cancelBtn, 13, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(130)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                   
        def k0Changed(self, text):
            self.Keuze0.setText(text)
    
        def k1Changed(self, text):
            self.Keuze1.setText(text)
            
        def k2Changed(self,text):
            self.Keuze2.setText(text)
            
        def k3Changed(self,text):
             self.Keuze3.setText(text)
            
        def k4Changed(self,text):
             self.Keuze4.setText(text)
            
        def k5Changed(self,text):
             self.Keuze5.setText(text)
            
        def k6Changed(self,text):
            self.Keuze6.setText(text)
            
        def k7Changed(self,text):
            self.Keuze7.setText(text)
               
        def k8Changed(self,text):
            self.Keuze8.setText(text)
            
        def k9Changed(self,text):
            self.Keuze9.setText(text)
            
        def k10Changed(self,text):
            self.Keuze10.setText(text)
            
        def k11Changed(self,text):
            self.Keuze11.setText(text)
            
        def k12Changed(self,text):
            self.Keuze12.setText(text)
            
        def k13Changed(self,text):
            self.Keuze13.setText(text)
            
        def k14Changed(self,text):
            self.Keuze14.setText(text)
            
        def k15Changed(self,text):
            self.Keuze15.setText(text)
    
        def returnk0(self):
            return self.Keuze0.text()
    
        def returnk1(self):
            return self.Keuze1.text()
    
        def returnk2(self):
            return self.Keuze2.text()
        
        def returnk3(self):
            return self.Keuze3.text()
      
        def returnk4(self):
            return self.Keuze4.text()
    
        def returnk5(self):
            return self.Keuze5.text()
    
        def returnk6(self):
            return self.Keuze6.text()
        
        def returnk7(self):
            return self.Keuze7.text()
        
        def returnk8(self):
            return self.Keuze8.text()
        
        def returnk9(self):
            return self.Keuze9.text()   
        
        def returnk10(self):
            return self.Keuze10.text()
        
        def returnk11(self):
            return self.Keuze11.text()
        
        def returnk12(self):
            return self.Keuze12.text()
        
        def returnk13(self):
            return self.Keuze13.text()
        
        def returnk14(self):
            return self.Keuze14.text()
        
        def returnk15(self):
            return self.Keuze15.text()

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnk1(),dialog.returnk2(),\
                dialog.returnk3(), dialog.returnk4(), dialog.returnk5(),\
                dialog.returnk6(), dialog.returnk7(),  dialog.returnk8(),\
                dialog.returnk9(), dialog.returnk10(), dialog.returnk11(),\
                dialog.returnk12(), dialog.returnk13(), dialog.returnk14(),\
                dialog.returnk15()]
      
    window = Widget()
    data = window.getData()

    mk0, mk1, mk2, mk3, mk4, mk5, mk6, mk7, mk8, mk9, mk10, mk11, mk12, mk13, mk14, mk15 = (0,)*16

    dlist = []
    for item in data:
        if item.startswith(' '):
            item = ''
        dlist += [item]
    del data

    if dlist[0]:
        mk0 = dlist[0][0]
    elif dlist[1]:
        mk1 = dlist[1][0]
    elif dlist[2]:
        mk2 = dlist[2][0]
    elif dlist[3]:
        mk3 = dlist[3][0]
    elif dlist[4]:
        mk4 = dlist[4][0]
    elif dlist[5]:
        mk5 = dlist[5][0]
    elif dlist[6]:
        mk6 = dlist[6][0]
    elif dlist[7]:
        mk7 = dlist[7][0]
    elif dlist[8]:
        mk8 = dlist[8][0]
    elif dlist[9]:
        mk9 = dlist[9][0]
    elif dlist[10]:
        mk10 = dlist[10][0]
    elif dlist[11]:
        mk11 = dlist[11][0]
    elif dlist[12]:
        mk12 = dlist[12][0]
    elif dlist[13]:
        mk13 = dlist[13][0]
    elif dlist[14]:
        mk14 = dlist[14][0]
    elif dlist[15]:
        mk15 = dlist[15][0] 
    else:
        hoofdMenu(m_email)
        
    if mk0 == '1':
        import wijzAccount
        wijzAccount.updateAccount(m_email)
    elif mk0 == '2':
         import opvrAccounts
         opvrAccounts.accKeuze(m_email)
    elif mk0 == '3':
         klmail = '' 
         import bestelOrder
         bestelOrder.artKeuze(m_email, 0, klmail)
    elif mk0 == '4':
        import opvrKlantenorders
        opvrKlantenorders.bestellingen(m_email)
    elif mk0 == '5':
        import printFacturen
        printFacturen.kiesOrder(m_email)
    elif mk1 == '1':
        import invoerLeverancier
        invoerLeverancier.bepaalLeverancier(m_email)
    elif mk1 == '2':
        import wijzLeverancier
        wijzLeverancier.zoekLeverancier(m_email)
    elif mk1 == '3':
        import opvrLeveranciers
        opvrLeveranciers.leveranciersKeuze(m_email)
    elif mk1 == '4':
        import opvrEigenleverancier
        opvrEigenleverancier.eigenLeverancier(m_email)
    elif mk2 == '1':
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 0)
    elif mk2 == '2':
        import wijzWerknemer
        while True:
            wijzWerknemer.zoekWerknemer(m_email)
    elif mk2 == '3':
        import opvrWerknemers
        opvrWerknemers.accKeuze(m_email)
    elif mk2 == '4':
        import opvrWerknperiode
        opvrWerknperiode.zoekWerknemer(m_email)
    elif mk3 == '1':
        mlevnr = 3
        mregel = 1
        import invoerInkooporder
        invoerInkooporder.zoekLeverancier(m_email, mlevnr,mregel)
    elif mk3 == '2':
        import wijzInkooporder
        mregel = 0
        minkordernr = 4
        wijzInkooporder.zoekInkooporder(m_email, minkordernr, mregel)
    elif mk3 == '3':
        mlevnr = 3
        mwerknr = 8
        mregel = 1
        import invoerDienstenorder
        invoerDienstenorder.zoekLeverancier(m_email, mlevnr, mwerknr, mregel)
    elif mk3 == '4':
        import wijzDienstenorder
        mregel = 0
        minkordernr = 4
        wijzDienstenorder.zoekInkooporder(m_email, minkordernr, mregel)
    elif mk3 == '5':
        import opvrInkooporders
        opvrInkooporders.inkooporderKeuze(m_email)
    elif mk3 == '6':
        import opvrDienstenorders
        opvrDienstenorders.inkooporderKeuze(m_email)
    elif mk3 == '7':
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email) 
    elif mk4 == '1':
        import invoerVerkoopbedrijf
        while True:
            invoerVerkoopbedrijf.invBedrijf(m_email)
    elif mk4 == '2':
        import wijzVerkoopbedrijf
        while True:
            wijzVerkoopbedrijf.zoekKoper(m_email)
    elif mk4 == '3':
        import opvrVerkoopbedrijven
        opvrVerkoopbedrijven.koperKeuze(m_email)
    elif mk4 == '4':
        import opvrEigenbedrijf
        opvrEigenbedrijf.eigenBedrijf(m_email)
    elif mk4 == '5':
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 2) 
    elif mk5 == '1':
        import invoerArtikelen
        while True:
            invoerArtikelen.invArtikel(m_email)
    elif mk5 == '2':
        import wijzArtikel
        wijzArtikel.zoekArtikel(m_email)
    elif mk5 == '3':
        import opvrArtikelen
        opvrArtikelen.artKeuze(m_email)
    elif mk5 == '4':
        import magUitgifte
        magUitgifte.kiesSelektie(0, m_email)
    elif mk5 == '5':
        import magUitgifte
        magUitgifte.kiesSelektie(1, m_email)
    elif mk5 == '6':
        import dervingMutaties
        while True:
            dervingMutaties.dervingMut(m_email)
    elif mk5 == '7':
        import opvrWebverkorders
        while True:
            opvrWebverkorders.zoekWeborder(m_email, 0) 
    elif mk5 == '8':
        import retourPortalWeb
        klmail = ''
        while True:
            retourPortalWeb.zoekEmailadres(m_email, klmail) 
    elif mk5 == '9':
        if mp[5][1] == '1':
            mret = True
        else:
            mret = False
        import barcodeScan
        barcodeScan.barcodeScan(m_email, mret)
    elif mk6 == '1':
        import invoerInternorder
        invoerInternorder.invWerkorder(m_email)
    elif mk6 == '2':
        import wijzInternorder
        wijzInternorder.zoeken(m_email)        
    elif mk6 == '3':
        import opvrInternorders
        opvrInternorders.zoeken(m_email)
    elif mk6 == '4' :
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 0)
    elif mk6 == '5':
        import magUitgifte
        magUitgifte.kiesSelektie(2, m_email)
    elif mk6 == '6':
        import urenImutaties
        maccountnr = '1'
        mwerknr = '7'
        mboekd = str(datetime.now())[0:10]
        while True:
            accwerk = urenImutaties.urenMut(maccountnr, mwerknr, mboekd, m_email)
	        # for convenience start with last used work , employee and mboekd 
            try:
                maccountnr = accwerk[0]
                mwerknr = accwerk[1]
                mboekd = accwerk[2]
            except:
                maccountnr = '1'
                mwerknr = '7'
                mboekd = str(datetime.now())[0:10]
    elif mk7 == '1':
        import invoerWerken
        invoerWerken.invWerk(m_email)
    elif mk7 == '2':
        import wijzWerken
        wijzWerken.zoekWerk(m_email)
    elif mk7 == '3':
        import opvrWerken
        opvrWerken.werkenKeuze(m_email)        
    elif mk7 == '4':
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 1)
    elif mk7 == '5':
        import magUitgifte
        magUitgifte.kiesSelektie(3, m_email)
    elif mk7 == '6':
        import dienstenMutaties
        dienstenMutaties.mutatieKeuze(m_email)
    elif mk7 == '7':
        import urenMutaties
        maccountnr = '1'
        mwerknr = '8'
        mboekd = str(datetime.now())[0:10]
        while True:
            accwerk = urenMutaties.urenMut(maccountnr, mwerknr, mboekd, m_email)
            # for convenience start with last used work , employee and mboekd
            try:
                maccountnr = accwerk[0]
                mwerknr = accwerk[1]
                mboekd = accwerk[2]
            except:
                maccountnr = '1'
                mwerknr = '8'
                mboekd = str(datetime.now())[0:10]
    elif mk8 == '1':
        import maakIcluster
        while True:
            maakIcluster.kiesCluster(m_email)
    elif mk8 == '2':
        import wijzIclusters
        while True:
            wijzIclusters.zoeken(m_email)
    elif mk8 == '3':
        import opvrIclusters
        opvrIclusters.zoeken(m_email)
    elif mk8 == '4':
        import invoerIcluster_artikelen
        while True:
            invoerIcluster_artikelen.zoeken(m_email)
    elif mk8 == '5':
        import opvrIcluster_artikelen
        opvrIcluster_artikelen.zoeken(m_email)
    elif mk8 == '6':
        import invoerIclustercalculatie
        invoerIclustercalculatie.zoeken(m_email)
    elif mk8 == '7':
        import opvrIclustercalculatie
        while True:
            opvrIclustercalculatie.zoekCalculatie(m_email)
    elif mk8 == '8':
        import koppelIbegroting
        while True:
            koppelIbegroting.zoekBegroting(m_email)
    elif mk9 == '1':
        import maakCluster
        while True:
            maakCluster.kiesCluster(m_email)
    elif mk9 == '2':
        import wijzClusters
        while True:
            wijzClusters.zoeken(m_email)
    elif mk9 == '3':
        import opvrClusters
        opvrClusters.zoeken(m_email)                
    elif mk9 == '4':
        import invoerCluster_artikelen
        while True:
            invoerCluster_artikelen.zoeken(m_email)
    elif mk9 == '5':
        import opvrCluster_artikelen
        opvrCluster_artikelen.zoeken(m_email)
    elif mk9 == '6':
        import invoerClustercalculatie
        while True:
            invoerClustercalculatie.zoeken(m_email)
    elif mk9 == '7':
        import opvrClustercalculatie
        while True:
            opvrClustercalculatie.zoekCalculatie(m_email)
    elif mk9 == '8':
        import koppelBegroting
        while True:
            koppelBegroting.zoekBegroting(m_email)
    elif mk10 == '1':
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif mk10 == '2':
        import proefrun
        proefrun.maandPeriode(m_email)
    elif mk10 == '3':
        import uitbetalenLonen
        uitbetalenLonen.maandBetalingen(m_email)
    elif mk10 == '4':
        import opvrLoonbetalingen
        opvrLoonbetalingen.zoeken(m_email)
    elif mk10 == '5':
        import invoerLoontabel
        while True:
            invoerLoontabel.invoerSchaal(m_email)        
    elif mk10 == '6':
        import wijzLoontabel
        wijzLoontabel.zoeken(m_email)
    elif mk10 == '7':
        import percentageLonen
        while True:
            percentageLonen.percLoonschaal(m_email)
    elif mk11 == '1' :
        import opvrArtikelmutaties
        opvrArtikelmutaties.mutatieKeuze(m_email)
    elif mk11 == '2':
        import opvrDienstenmutaties
        opvrDienstenmutaties.mutatieKeuze(m_email)
    elif mk11 == '3':
        import afdrBetalen
        afdrBetalen.zoeken(m_email)
    elif mk11 == '4':
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 1)
    elif mk11 == '5':
        import webRetouren
        webRetouren.retKeuze(m_email)
    elif mk11 == '6':
        import printFacturatie
        printFacturatie.maakLijst(m_email) 
    elif mk11 == '7':
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif mk12 == '1':
        import voorraadbeheersing
        voorraadbeheersing.vrdKeuze(m_email)
    elif mk12 == '2':
        import magvrdGrafiek
        magvrdGrafiek.toonGrafiek(m_email)
    elif mk12 == '3':
        import magvrdGrafiek
        magvrdGrafiek.magVoorraad(m_email)  
    elif mk12 == '4':
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email)
    elif mk13== '1':
        import rapportage
        rapportage.JN(m_email)
    elif mk13 == '2':
        import toonGrafieken
        toonGrafieken.zoekwk(m_email)
    elif mk13 == '3':
        import voortgangGrafiek
        while True:
            voortgangGrafiek.zoekwk(m_email)
    elif mk13 == '4':
        import toonResultaten
        toonResultaten.toonResult(m_email)
    elif mk14 == '1':
        import maakAuthorisatie
        while True:
             maakAuthorisatie.zoekAccount(m_email)
    elif mk14 == '2':
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 2)
    elif mk14 == '3':
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 1)
    elif mk14 == '4':
        import invoerParams
        while True:
            invoerParams.invParams(m_email)
    elif mk14 == '5':
        import wijzigParams
        wijzigParams.toonParams(m_email) 
    elif mk14 == '6':
        import opvrParams
        opvrParams.toonParams(m_email)
    elif mk14 == '7':
        import wijzWerktarief
        wijzWerktarief.winKeuze(m_email)
    elif mk15 == '1':
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Clustercalculaties\\'
        else:
            path = './forms/Intern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '2':
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties\\'
        else:
            path = './forms/Extern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif mk15 == '3':
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Orderbrieven\\'
        else:
            path = './forms/Intern_Orderbrieven/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '4':
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '5':
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif mk15 == '6':
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == '7':
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Pakbonnen\\'
        else:
            path = './forms/Weborders_Pakbonnen/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == '8':
        if sys.platform == 'win32':
            path = '.\\forms\\Uren\\'
        else:
            path = './forms/Uren/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == '9':
        if sys.platform == 'win32':
            path = '.\\forms\\Lonen\\'
        else:
            path = './forms/Lonen/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == 'A':
        if sys.platform == 'win32':
            path = '.\\forms\\Facturen_Werken\\'
        else:
            path = './forms/Facturen_Werken/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif mk15 == 'B':
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Facturen\\'
        else:
            path = './forms/Weborders_Facturen/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif (mk15 == 'C'):
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties_Diensten\\'
        else:
            path = './forms/Extern_Clustercalculaties_Diensten/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif (mk15 == 'D'):
        if sys.platform == 'win32':
            path = '.\\forms\\Barcodelijsten\\'
        else:
            path = './forms/Barcodelijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    else:
        hoofdMenu(m_email)
        
inlog()
