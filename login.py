import os, sys, subprocess
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
    msg.setWindowIcon(QIcon('./image7s/logos/logo.jpg'))
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

            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(310)
            self.k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k0Edit.addItem('Accounts')
            self.k0Edit.setFont(QFont("Arial", 10))
            self.k0Edit.setEditable(True)
            self.k0Edit.lineEdit().setFont(QFont("Arial",10))
            self.k0Edit.lineEdit().setReadOnly(True)
            self.k0Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k0Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k0Edit.addItem('1. Modify account')
            self.k0Edit.addItem('2. Requesting accounts')
            self.k0Edit.addItem('3. Ordering web articles')
            self.k0Edit.addItem('4. Requesting order overview')
            self.k0Edit.addItem('5. Printing order invoices')

            self.k1Edit = QComboBox()
            self.k1Edit.setFixedWidth(310)
            self.k1Edit.setFont(QFont("Arial",10))
            self.k1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k1Edit.addItem('Suppliers')
            self.k1Edit.setEditable(True)
            self.k1Edit.lineEdit().setFont(QFont("Arial",10))
            self.k1Edit.lineEdit().setReadOnly(True)
            self.k1Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k1Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k1Edit.addItem('1. Insert supplier data')
            self.k1Edit.addItem('2. Modify supplier data')
            self.k1Edit.addItem('3. Request supplier data')
            self.k1Edit.addItem('4. Self requesting own data.')

            self.k2Edit = QComboBox()
            self.k2Edit.setFixedWidth(310)
            self.k2Edit.setFont(QFont("Arial",10))
            self.k2Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k2Edit.addItem('Employees')
            self.k2Edit.setEditable(True)
            self.k2Edit.lineEdit().setFont(QFont("Arial",10))
            self.k2Edit.lineEdit().setReadOnly(True)
            self.k2Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k2Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k2Edit.addItem('1. Connect account-employee')
            self.k2Edit.addItem('2. Modify employee data')
            self.k2Edit.addItem('3. Request employees data')
            self.k2Edit.addItem('4. Request employee-period')

            self.k3Edit = QComboBox()
            self.k3Edit.setFixedWidth(310)
            self.k3Edit.setFont(QFont("Arial",10))
            self.k3Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k3Edit.addItem('Purchase')
            self.k3Edit.setEditable(True)
            self.k3Edit.lineEdit().setFont(QFont("Arial",10))
            self.k3Edit.lineEdit().setReadOnly(True)
            self.k3Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k3Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k3Edit.addItem('1. Insert orders materials')
            self.k3Edit.addItem('2. Modify orders materials')
            self.k3Edit.addItem('3. Insert orders services/equipment')
            self.k3Edit.addItem('4. Modify orders services/equipment')
            self.k3Edit.addItem('5. Request orders materials')
            self.k3Edit.addItem('6. Request orders services/equipment')

            self.k4Edit = QComboBox()
            self.k4Edit.setFixedWidth(310)
            self.k4Edit.setFont(QFont("Arial",10))
            self.k4Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k4Edit.addItem('Sales')
            self.k4Edit.setEditable(True)
            self.k4Edit.lineEdit().setFont(QFont("Arial",10))
            self.k4Edit.lineEdit().setReadOnly(True)
            self.k4Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k4Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k4Edit.addItem('1. Sales-company create')
            self.k4Edit.addItem('2. Sales-company modify')
            self.k4Edit.addItem('3. Sales-companies request')
            self.k4Edit.addItem('4. Own data request')
            self.k4Edit.addItem('5. Web sales orders requesting')

            self.k5Edit = QComboBox()
            self.k5Edit.setFixedWidth(310)
            self.k5Edit.setFont(QFont("Arial",10))
            self.k5Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k5Edit.addItem('Warehouse')
            self.k5Edit.setEditable(True)
            self.k5Edit.lineEdit().setFont(QFont("Arial",10))
            self.k5Edit.lineEdit().setReadOnly(True)
            self.k5Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k5Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k5Edit.addItem('1. Insert articles')
            self.k5Edit.addItem('2. Modify articles')
            self.k5Edit.addItem('3. Request articles')
            self.k5Edit.addItem('4. Issuing materials (picklist)')
            self.k5Edit.addItem('5. Printing picklists')
            self.k5Edit.addItem('6. Booking differences/obsolete')
            self.k5Edit.addItem('7. Issuing web articles/printing')
            self.k5Edit.addItem('8. Return booking web items')
            self.k5Edit.addItem('9. Counter sales - barcode scan')

            self.k6Edit = QComboBox()
            self.k6Edit.setFixedWidth(310)
            self.k6Edit.setFont(QFont("Arial",10))
            self.k6Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k6Edit.addItem('Works internally')
            self.k6Edit.setEditable(True)
            self.k6Edit.lineEdit().setFont(QFont("Arial",10))
            self.k6Edit.lineEdit().setReadOnly(True)
            self.k6Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k6Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k6Edit.addItem('1. Insert work orders')
            self.k6Edit.addItem('2. Modify work orders')
            self.k6Edit.addItem('3. Request work orders/printing')
            self.k6Edit.addItem('4. Calling materials')
            self.k6Edit.addItem('5. Printing picklists')
            self.k6Edit.addItem('6. Mutate hourly consumption')

            self.k7Edit = QComboBox()
            self.k7Edit.setFixedWidth(310)
            self.k7Edit.setFont(QFont("Arial",10))
            self.k7Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k7Edit.addItem('Works externally')
            self.k7Edit.setEditable(True)
            self.k7Edit.lineEdit().setFont(QFont("Arial",10))
            self.k7Edit.lineEdit().setReadOnly(True)
            self.k7Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k7Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k7Edit.addItem('1. Insert work orders')
            self.k7Edit.addItem('2. Modify work orders')
            self.k7Edit.addItem('3. Request work orders')
            self.k7Edit.addItem('4. Calling materials')
            self.k7Edit.addItem('5. Printing picklists')
            self.k7Edit.addItem('6. Mutate cost services')
            self.k7Edit.addItem('7. Mutate hourly consumption')

            self.k8Edit = QComboBox()
            self.k8Edit.setFixedWidth(310)
            self.k8Edit.setFont(QFont("Arial",10))
            self.k8Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k8Edit.addItem('Calculation works internally')
            self.k8Edit.setEditable(True)
            self.k8Edit.lineEdit().setFont(QFont("Arial",10))
            self.k8Edit.lineEdit().setReadOnly(True)
            self.k8Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k8Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k8Edit.addItem('1. Create new clusters')
            self.k8Edit.addItem('2. Insert cluster data')
            self.k8Edit.addItem('3. Request cluster data')
            self.k8Edit.addItem('4. Insert article lines per cluster')
            self.k8Edit.addItem('5. Request article lines per cluster') 
            self.k8Edit.addItem('6. Create/change calculation')
            self.k8Edit.addItem('7. Calculation/Article list/printing')
            self.k8Edit.addItem('8. Calculation connect -> production')

            self.k9Edit = QComboBox()
            self.k9Edit.setFixedWidth(310)
            self.k9Edit.setFont(QFont("Arial",10))
            self.k9Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k9Edit.addItem('Calculation works externally')
            self.k9Edit.setEditable(True)
            self.k9Edit.lineEdit().setFont(QFont("Arial",10))
            self.k9Edit.lineEdit().setReadOnly(True)
            self.k9Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k9Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k9Edit.addItem('1. Create new clusters')
            self.k9Edit.addItem('2. Insert cluster data')
            self.k9Edit.addItem('3. Request cluster data')
            self.k9Edit.addItem('4. Insert article lines per cluster')
            self.k9Edit.addItem('5. Request article lines per cluster')
            self.k9Edit.addItem('6. Create/change calculation')
            self.k9Edit.addItem('7. Calculation/Article list/printing')
            self.k9Edit.addItem('8. Calculation connect -> production')

            self.k10Edit = QComboBox()
            self.k10Edit.setFixedWidth(310)
            self.k10Edit.setFont(QFont("Arial",10))
            self.k10Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k10Edit.addItem('Payroll administration')
            self.k10Edit.setEditable(True)
            self.k10Edit.lineEdit().setFont(QFont("Arial",10))
            self.k10Edit.lineEdit().setReadOnly(True)
            self.k10Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k10Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k10Edit.addItem('1. Request mutation of hours')
            self.k10Edit.addItem('2. Control hours for monthly wages')
            self.k10Edit.addItem('3. Payment of monthly wages')
            self.k10Edit.addItem('4. Request wages payments')
            self.k10Edit.addItem('5. Insert wages scales')
            self.k10Edit.addItem('6. Modify wages scales/requesting')
            self.k10Edit.addItem('7. Increase wages with percentage')

            self.k11Edit = QComboBox()
            self.k11Edit.setFixedWidth(310)
            self.k11Edit.setFont(QFont("Arial",10))
            self.k11Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k11Edit.addItem('Accounting')
            self.k11Edit.setEditable(True)
            self.k11Edit.lineEdit().setFont(QFont("Arial",10))
            self.k11Edit.lineEdit().setReadOnly(True)
            self.k11Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k11Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k11Edit.addItem('1. Article mutations requesting')
            self.k11Edit.addItem('2. Services mutations requesting')
            self.k11Edit.addItem('3. View and pay contributions')
            self.k11Edit.addItem('4. Weborders payments/print invoices')
            self.k11Edit.addItem('5. Book return payments')
            self.k11Edit.addItem('6. Print list to invoice external works')
            self.k11Edit.addItem('7. Request mutations of hours')

            self.k12Edit = QComboBox()
            self.k12Edit.setFixedWidth(310)
            self.k12Edit.setFont(QFont("Arial",10))
            self.k12Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k12Edit.addItem('Stock management')
            self.k12Edit.setEditable(True)
            self.k12Edit.lineEdit().setFont(QFont("Arial",10))
            self.k12Edit.lineEdit().setReadOnly(True)
            self.k12Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k12Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k12Edit.addItem('1. Stock management, order articles')
            self.k12Edit.addItem('2. Graph stocks, warehouse financial')
            self.k12Edit.addItem('3. Overview stocks financial')
            self.k12Edit.addItem('4. Request reservations')

            self.k13Edit = QComboBox()
            self.k13Edit.setFixedWidth(310)
            self.k13Edit.setFont(QFont("Arial",10))
            self.k13Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k13Edit.addItem('Management Information')
            self.k13Edit.setEditable(True)
            self.k13Edit.lineEdit().setFont(QFont("Arial",10))
            self.k13Edit.lineEdit().setReadOnly(True)
            self.k13Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k13Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k13Edit.addItem('1. Calculate financial data once/week')
            self.k13Edit.addItem('2. Print finance graphs external works')
            self.k13Edit.addItem('3. Print graphs by progress status')
            self.k13Edit.addItem('4. Request results works')

            self.k14Edit = QComboBox()
            self.k14Edit.setFixedWidth(310)
            self.k14Edit.setFont(QFont("Arial",10))
            self.k14Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k14Edit.addItem('Maintenance')
            self.k14Edit.setEditable(True)
            self.k14Edit.lineEdit().setFont(QFont("Arial",10))
            self.k14Edit.lineEdit().setReadOnly(True)
            self.k14Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k14Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k14Edit.addItem('1. Mutate authorisations')
            self.k14Edit.addItem('2. Connect account - supplier')
            self.k14Edit.addItem('3. Connect account - sales company')
            self.k14Edit.addItem('4. Insert parameters')
            self.k14Edit.addItem('5. Modify parameters')
            self.k14Edit.addItem('6. Request parameters')
            self.k14Edit.addItem('7. Sales work rates updating')

            self.k15Edit = QComboBox()
            self.k15Edit.setFixedWidth(310)
            self.k15Edit.setFont(QFont("Arial",10))
            self.k15Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k15Edit.addItem('Reprinting of forms')
            self.k15Edit.setEditable(True)
            self.k15Edit.lineEdit().setFont(QFont("Arial",10))
            self.k15Edit.lineEdit().setReadOnly(True)
            self.k15Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k15Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k15Edit.addItem('1. Calculation internal works')
            self.k15Edit.addItem('2. Calculation external works')  
            self.k15Edit.addItem('3. Internal orders purchase')
            self.k15Edit.addItem('4. Calling internal works')
            self.k15Edit.addItem('5. Calling external works')
            self.k15Edit.addItem('6. Picklists warehouse')
            self.k15Edit.addItem('7. Web orders packing slip')
            self.k15Edit.addItem('8. Control hours for paying wages')
            self.k15Edit.addItem('9. Wages specification employees')
            self.k15Edit.addItem('10. Invoices external works')
            self.k15Edit.addItem('11. Web orders payments')
            self.k15Edit.addItem('12. Purchase orders services/material')
            self.k15Edit.addItem('13. Counter sale order invoices')

            #disable menu's if no permission is granted in table accounts
            # list of Mainmenu
            mplist=[self.k0Edit,self.k1Edit,self.k2Edit,self.k3Edit,self.k4Edit,self.k5Edit,self.k6Edit,self.k7Edit,\
                    self.k8Edit,self.k9Edit,self.k10Edit,self.k11Edit,self.k12Edit,self.k13Edit,self.k14Edit,self.k15Edit]

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
                mplist[15].model().item(12).setEnabled(False)
                mplist[15].model().item(12).setForeground(QColor('darkgrey'))
                mplist[15].model().item(12).setBackground(QColor('gainsboro'))
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
                mplist[15].model().item(7).setEnabled(False)
                mplist[15].model().item(7).setForeground(QColor('darkgrey'))
                mplist[15].model().item(7).setBackground(QColor('gainsboro'))
                mplist[15].model().item(13).setEnabled(False)
                mplist[15].model().item(13).setForeground(QColor('darkgrey'))
                mplist[15].model().item(13).setBackground(QColor('gainsboro'))
            if mp[10][5] == '0':
                mplist[15].model().item(8).setEnabled(False)
                mplist[15].model().item(8).setForeground(QColor('darkgrey'))
                mplist[15].model().item(8).setBackground(QColor('gainsboro'))
                mplist[15].model().item(9).setEnabled(False)
                mplist[15].model().item(9).setForeground(QColor('darkgrey'))
                mplist[15].model().item(9).setBackground(QColor('gainsboro'))
            if mp[11][5] == '0':
                mplist[15].model().item(10).setEnabled(False)
                mplist[15].model().item(10).setForeground(QColor('darkgrey'))
                mplist[15].model().item(10).setBackground(QColor('gainsboro'))
                mplist[15].model().item(11).setEnabled(False)
                mplist[15].model().item(11).setForeground(QColor('darkgrey'))
                mplist[15].model().item(11).setBackground(QColor('gainsboro'))

            grid = QGridLayout()
            grid.setSpacing(20)
             
            grid.addWidget(self.k0Edit, 2, 0)
            grid.addWidget(self.k8Edit, 2, 1)
            
            grid.addWidget(self.k1Edit, 3, 0)
            grid.addWidget(self.k9Edit, 3, 1)
            
            grid.addWidget(self.k2Edit, 4, 0)
            grid.addWidget(self.k10Edit, 4, 1)
            
            grid.addWidget(self.k3Edit, 5, 0)
            grid.addWidget(self.k11Edit, 5, 1)
          
            grid.addWidget(self.k4Edit, 6, 0)
            grid.addWidget(self.k12Edit, 6, 1)
        
            grid.addWidget(self.k5Edit, 7, 0)
            grid.addWidget(self.k13Edit, 7, 1)
            
            grid.addWidget(self.k6Edit, 8, 0)
            grid.addWidget(self.k14Edit, 8, 1)
            
            grid.addWidget(self.k7Edit, 9 ,0)
            grid.addWidget(self.k15Edit, 9, 1)
                            
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

            cancelBtn = QPushButton('Logout')
            cancelBtn.clicked.connect(lambda: closeIt(self))
    
            grid.addWidget(cancelBtn, 13, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(130)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
                self.accept()
            self.k0Edit.currentIndexChanged.connect(k0Changed)

            def k1Changed():
                self.k1Edit.setCurrentIndex(self.k1Edit.currentIndex())
                self.accept()
            self.k1Edit.currentIndexChanged.connect(k1Changed)

            def k2Changed():
                self.k2Edit.setCurrentIndex(self.k2Edit.currentIndex())
                self.accept()
            self.k2Edit.currentIndexChanged.connect(k2Changed)

            def k3Changed():
                self.k3Edit.setCurrentIndex(self.k3Edit.currentIndex())
                self.accept()
            self.k3Edit.currentIndexChanged.connect(k3Changed)

            def k4Changed():
                self.k4Edit.setCurrentIndex(self.k4Edit.currentIndex())
                self.accept()
            self.k4Edit.currentIndexChanged.connect(k4Changed)

            def k5Changed():
                self.k5Edit.setCurrentIndex(self.k5Edit.currentIndex())
                self.accept()
            self.k5Edit.currentIndexChanged.connect(k5Changed)

            def k6Changed():
                self.k6Edit.setCurrentIndex(self.k6Edit.currentIndex())
                self.accept()
            self.k6Edit.currentIndexChanged.connect(k6Changed)

            def k7Changed():
                self.k7Edit.setCurrentIndex(self.k7Edit.currentIndex())
                self.accept()
            self.k7Edit.currentIndexChanged.connect(k7Changed)

            def k8Changed():
                self.k8Edit.setCurrentIndex(self.k8Edit.currentIndex())
                self.accept()
            self.k8Edit.currentIndexChanged.connect(k8Changed)

            def k9Changed():
                self.k9Edit.setCurrentIndex(self.k9Edit.currentIndex())
                self.accept()
            self.k9Edit.currentIndexChanged.connect(k9Changed)

            def k10Changed():
                self.k10Edit.setCurrentIndex(self.k10Edit.currentIndex())
                self.accept()
            self.k10Edit.currentIndexChanged.connect(k10Changed)

            def k11Changed():
                self.k11Edit.setCurrentIndex(self.k11Edit.currentIndex())
                self.accept()
            self.k11Edit.currentIndexChanged.connect(k11Changed)

            def k12Changed():
                self.k12Edit.setCurrentIndex(self.k12Edit.currentIndex())
                self.accept()
            self.k12Edit.currentIndexChanged.connect(k12Changed)

            def k13Changed():
                self.k13Edit.setCurrentIndex(self.k13Edit.currentIndex())
                self.accept()
            self.k13Edit.currentIndexChanged.connect(k13Changed)

            def k14Changed():
                self.k14Edit.setCurrentIndex(self.k14Edit.currentIndex())
                self.accept()
            self.k14Edit.currentIndexChanged.connect(k14Changed)

            def k15Changed():
                self.k15Edit.setCurrentIndex(self.k15Edit.currentIndex())
                self.accept()
            self.k15Edit.currentIndexChanged.connect(k15Changed)

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.k0Edit.currentIndex(), dialog.k1Edit.currentIndex(),dialog.k2Edit.currentIndex(),\
                dialog.k3Edit.currentIndex(), dialog.k4Edit.currentIndex(), dialog.k5Edit.currentIndex(),\
                dialog.k6Edit.currentIndex(), dialog.k7Edit.currentIndex(),  dialog.k8Edit.currentIndex(), \
                dialog.k9Edit.currentIndex(), dialog.k10Edit.currentIndex(), dialog.k11Edit.currentIndex(), \
                dialog.k12Edit.currentIndex(),dialog.k13Edit.currentIndex(), dialog.k14Edit.currentIndex(), \
                dialog.k15Edit.currentIndex()]
      
    window = Widget()
    dlist = window.getData()

    if dlist[0] == 1:
        import wijzAccount
        wijzAccount.updateAccount(m_email)
    elif dlist[0] == 2:
         import opvrAccounts
         opvrAccounts.accKeuze(m_email)
    elif dlist[0] == 3:
         klmail = '' 
         import bestelOrder
         bestelOrder.artKeuze(m_email, 0, klmail)
    elif dlist[0] == 4:
        import opvrKlantenorders
        opvrKlantenorders.bestellingen(m_email)
    elif dlist[0] == 5:
        import printFacturen
        printFacturen.kiesOrder(m_email)
    elif dlist[1] == 1:
        import invoerLeverancier
        invoerLeverancier.bepaalLeverancier(m_email)
    elif dlist[1] == 2:
        import wijzLeverancier
        wijzLeverancier.zoekLeverancier(m_email)
    elif dlist[1] == 3:
        import opvrLeveranciers
        opvrLeveranciers.leveranciersKeuze(m_email)
    elif dlist[1] == 4:
        import opvrEigenleverancier
        opvrEigenleverancier.eigenLeverancier(m_email)
    elif dlist[2] == 1:
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 0)
    elif dlist[2] == 2:
        import wijzWerknemer
        while True:
            wijzWerknemer.zoekWerknemer(m_email)
    elif dlist[2] == 3:
        import opvrWerknemers
        opvrWerknemers.accKeuze(m_email)
    elif dlist[2] == 4:
        import opvrWerknperiode
        opvrWerknperiode.zoekWerknemer(m_email)
    elif dlist[3] == 1:
        mlevnr = 3
        mregel = 1
        import invoerInkooporder
        invoerInkooporder.zoekLeverancier(m_email, mlevnr,mregel)
    elif dlist[3] == 2:
        import wijzInkooporder
        mregel = 0
        minkordernr = 4
        wijzInkooporder.zoekInkooporder(m_email, minkordernr, mregel)
    elif dlist[3] == 3:
        mlevnr = 3
        mwerknr = 8
        mregel = 1
        import invoerDienstenorder
        invoerDienstenorder.zoekLeverancier(m_email, mlevnr, mwerknr, mregel)
    elif dlist[3] == 4:
        import wijzDienstenorder
        mregel = 0
        minkordernr = 4
        wijzDienstenorder.zoekInkooporder(m_email, minkordernr, mregel)
    elif dlist[3] == 5:
        import opvrInkooporders
        opvrInkooporders.inkooporderKeuze(m_email)
    elif dlist[3] == 6:
        import opvrDienstenorders
        opvrDienstenorders.inkooporderKeuze(m_email)
    elif dlist[3] == 7:
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email) 
    elif dlist[4] == 1:
        import invoerVerkoopbedrijf
        while True:
            invoerVerkoopbedrijf.invBedrijf(m_email)
    elif dlist[4] == 2:
        import wijzVerkoopbedrijf
        while True:
            wijzVerkoopbedrijf.zoekKoper(m_email)
    elif dlist[4] == 3:
        import opvrVerkoopbedrijven
        opvrVerkoopbedrijven.koperKeuze(m_email)
    elif dlist[4] == 4:
        import opvrEigenbedrijf
        opvrEigenbedrijf.eigenBedrijf(m_email)
    elif dlist[4] == 5:
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 2) 
    elif dlist[5] == 1:
        import invoerArtikelen
        while True:
            invoerArtikelen.invArtikel(m_email)
    elif dlist[5] == 2:
        import wijzArtikel
        wijzArtikel.zoekArtikel(m_email)
    elif dlist[5] == 3:
        import opvrArtikelen
        opvrArtikelen.artKeuze(m_email)
    elif dlist[5] == 4:
        import magUitgifte
        magUitgifte.kiesSelektie(0, m_email)
    elif dlist[5] == 5:
        import magUitgifte
        magUitgifte.kiesSelektie(1, m_email)
    elif dlist[5] == 6:
        import dervingMutaties
        while True:
            dervingMutaties.dervingMut(m_email)
    elif dlist[5] == 7:
        import opvrWebverkorders
        while True:
            opvrWebverkorders.zoekWeborder(m_email, 0) 
    elif dlist[5] == 8:
        import retourPortalWeb
        klmail = ''
        while True:
            retourPortalWeb.zoekEmailadres(m_email, klmail) 
    elif dlist[5] == 9:
        if mp[5][1] == '1':
            mret = True
        else:
            mret = False
        import barcodeScan
        barcodeScan.barcodeScan(m_email, mret)
    elif dlist[6] == 1:
        import invoerInternorder
        invoerInternorder.invWerkorder(m_email)
    elif dlist[6] == 2:
        import wijzInternorder
        wijzInternorder.zoeken(m_email)        
    elif dlist[6] == 3:
        import opvrInternorders
        opvrInternorders.zoeken(m_email)
    elif dlist[6] == 4 :
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 0)
    elif dlist[6] == 5:
        import magUitgifte
        magUitgifte.kiesSelektie(2, m_email)
    elif dlist[6] == 6:
        import urenImutaties
        maccountnr = '1'
        mwerknr = 7
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
    elif dlist[7] == 1:
        import invoerWerken
        invoerWerken.invWerk(m_email)
    elif dlist[7] == 2:
        import wijzWerken
        wijzWerken.zoekWerk(m_email)
    elif dlist[7] == 3:
        import opvrWerken
        opvrWerken.werkenKeuze(m_email)        
    elif dlist[7] == 4:
        import artikelAfroep
        artikelAfroep.zoekWerk(m_email, 1)
    elif dlist[7] == 5:
        import magUitgifte
        magUitgifte.kiesSelektie(3, m_email)
    elif dlist[7] == 6:
        import dienstenMutaties
        dienstenMutaties.mutatieKeuze(m_email)
    elif dlist[7] == 7:
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
        import maakIcluster
        while True:
            maakIcluster.kiesCluster(m_email)
    elif dlist[8] == 2:
        import wijzIclusters
        while True:
            wijzIclusters.zoeken(m_email)
    elif dlist[8] == 3:
        import opvrIclusters
        opvrIclusters.zoeken(m_email)
    elif dlist[8] == 4:
        import invoerIcluster_artikelen
        while True:
            invoerIcluster_artikelen.zoeken(m_email)
    elif dlist[8] == 5:
        import opvrIcluster_artikelen
        opvrIcluster_artikelen.zoeken(m_email)
    elif dlist[8] == 6:
        import invoerIclustercalculatie
        invoerIclustercalculatie.zoeken(m_email)
    elif dlist[8] == 7:
        import opvrIclustercalculatie
        while True:
            opvrIclustercalculatie.zoekCalculatie(m_email)
    elif dlist[8] == 8:
        import koppelIbegroting
        while True:
            koppelIbegroting.zoekBegroting(m_email)
    elif dlist[9] == 1:
        import maakCluster
        while True:
            maakCluster.kiesCluster(m_email)
    elif dlist[9] == 2:
        import wijzClusters
        while True:
            wijzClusters.zoeken(m_email)
    elif dlist[9] == 3:
        import opvrClusters
        opvrClusters.zoeken(m_email)                
    elif dlist[9] == 4:
        import invoerCluster_artikelen
        while True:
            invoerCluster_artikelen.zoeken(m_email)
    elif dlist[9] == 5:
        import opvrCluster_artikelen
        opvrCluster_artikelen.zoeken(m_email)
    elif dlist[9] == 6:
        import invoerClustercalculatie
        while True:
            invoerClustercalculatie.zoeken(m_email)
    elif dlist[9] == 7:
        import opvrClustercalculatie
        while True:
            opvrClustercalculatie.zoekCalculatie(m_email)
    elif dlist[9] == 8:
        import koppelBegroting
        while True:
            koppelBegroting.zoekBegroting(m_email)
    elif dlist[10] == 1:
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif dlist[10] == 2:
        import proefrun
        proefrun.maandPeriode(m_email)
    elif dlist[10] == 3:
        import uitbetalenLonen
        uitbetalenLonen.maandBetalingen(m_email)
    elif dlist[10] == 4:
        import opvrLoonbetalingen
        opvrLoonbetalingen.zoeken(m_email)
    elif dlist[10] == 5:
        import invoerLoontabel
        while True:
            invoerLoontabel.invoerSchaal(m_email)        
    elif dlist[10] == 6:
        import wijzLoontabel
        wijzLoontabel.zoeken(m_email)
    elif dlist[10] == 7:
        import percentageLonen
        while True:
            percentageLonen.percLoonschaal(m_email)
    elif dlist[11] == 1:
        import opvrArtikelmutaties
        opvrArtikelmutaties.mutatieKeuze(m_email)
    elif dlist[11] == 2:
        import opvrDienstenmutaties
        opvrDienstenmutaties.mutatieKeuze(m_email)
    elif dlist[11] == 3:
        import afdrBetalen
        afdrBetalen.zoeken(m_email)
    elif dlist[11] == 4:
        import opvrWebverkorders
        opvrWebverkorders.zoekWeborder(m_email, 1)
    elif dlist[11] == 5:
        import webRetouren
        webRetouren.retKeuze(m_email)
    elif dlist[11] == 6:
        import printFacturatie
        printFacturatie.maakLijst(m_email) 
    elif dlist[11] == 7:
        import opvrUrenmutaties
        opvrUrenmutaties.loonKeuze(m_email)
    elif dlist[12] == 1:
        import voorraadbeheersing
        voorraadbeheersing.vrdKeuze(m_email)
    elif dlist[12] == 2:
        import magvrdGrafiek
        magvrdGrafiek.toonGrafiek(m_email)
    elif dlist[12] == 3:
        import magvrdGrafiek
        magvrdGrafiek.magVoorraad(m_email)  
    elif dlist[12] == 4:
        import opvrReserveringen
        opvrReserveringen.resKeuze(m_email)
    elif dlist[13]== 1:
        import rapportage
        rapportage.JN(m_email)
    elif dlist[13] == 2:
        import toonGrafieken
        toonGrafieken.zoekwk(m_email)
    elif dlist[13] == 3:
        import voortgangGrafiek
        while True:
            voortgangGrafiek.zoekwk(m_email)
    elif dlist[13] == 4:
        import toonResultaten
        toonResultaten.toonResult(m_email)
    elif dlist[14] == 1:
        import maakAuthorisatie
        while True:
             maakAuthorisatie.zoekAccount(m_email)
    elif dlist[14] == 2:
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 2)
    elif dlist[14] == 3:
        import koppelAccount
        koppelAccount.zoekAccount(m_email, 1)
    elif dlist[14] == 4:
        import invoerParams
        while True:
            invoerParams.invParams(m_email)
    elif dlist[14] == 5:
        import wijzigParams
        wijzigParams.toonParams(m_email) 
    elif dlist[14] == 6:
        import opvrParams
        opvrParams.toonParams(m_email)
    elif dlist[14] == 7:
        import wijzWerktarief
        wijzWerktarief.winKeuze(m_email)
    elif dlist[15] == 1:
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Clustercalculaties\\'
        else:
            path = './forms/Intern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 2:
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties\\'
        else:
            path = './forms/Extern_Clustercalculaties/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif dlist[15] == 3:
        if sys.platform == 'win32':
            path = '.\\forms\\Intern_Orderbrieven\\'
        else:
            path = './forms/Intern_Orderbrieven/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 4:
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 5:
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    elif dlist[15] == 6:
        if sys.platform == 'win32':
            path = '.\\forms\\Raaplijsten\\'
        else:
            path = './forms/Raaplijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif dlist[15] == 7:
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Pakbonnen\\'
        else:
            path = './forms/Weborders_Pakbonnen/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif dlist[15] == 8:
        if sys.platform == 'win32':
            path = '.\\forms\\Uren\\'
        else:
            path = './forms/Uren/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif dlist[15] == 9:
        if sys.platform == 'win32':
            path = '.\\forms\\Lonen\\'
        else:
            path = './forms/Lonen/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif dlist[15] == 10:
        if sys.platform == 'win32':
            path = '.\\forms\\Facturen_Werken\\'
        else:
            path = './forms/Facturen_Werken/'
        import filePicklist
        filePicklist.fileList(m_email, path)    
    elif dlist[15] == 11:
        if sys.platform == 'win32':
            path = '.\\forms\\Weborders_Facturen\\'
        else:
            path = './forms/Weborders_Facturen/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif dlist[15] == 12:
        if sys.platform == 'win32':
            path = '.\\forms\\Extern_Clustercalculaties_Diensten\\'
        else:
            path = './forms/Extern_Clustercalculaties_Diensten/'
        import filePicklist
        filePicklist.fileList(m_email, path) 
    elif dlist[15] == 13:
        if sys.platform == 'win32':
            path = '.\\forms\\Barcodelijsten\\'
        else:
            path = './forms/Barcodelijsten/'
        import filePicklist
        filePicklist.fileList(m_email, path)
    else:
        hoofdMenu(m_email)
        
inlog()
