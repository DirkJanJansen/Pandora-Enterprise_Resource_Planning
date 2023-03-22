def maandBetalingen(m_email):
    from login import hoofdMenu
    import os, datetime 
    from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
        QDialog, QMessageBox, QWidget, QTableView, QVBoxLayout
    from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
    from PyQt5.QtCore import Qt, QRegExp, QAbstractTableModel
    from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                            ForeignKey,  MetaData, create_engine)
    from sqlalchemy.sql import select, insert, update, and_, func
    
    def info():
        class Widget(QDialog):
            def __init__(self):
                QDialog.__init__(self)
                self.setWindowTitle("Information on paying wages")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                self.setFont(QFont("Arial", 10))
                grid = QGridLayout()
                grid.setSpacing(20)
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
                
                lblinfo = QLabel('Paying wages.')
                grid.addWidget(lblinfo, 0, 0, 1, 4, Qt.AlignCenter)
                lblinfo.setStyleSheet("color:rgb(45, 83, 115); font: 25pt Comic Sans MS")
            
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid.addWidget(lbl, 0, 0)
                lblinfo = QLabel(
            '''
            Procedure: 
            
            Within a week after the end of a month, a printout should be created with
            the program "Control hours for monthly wages" in the menu Payroll.\t\t\t 
            This results in an inspection of which employees do not yet (fully) report
            their hours statement These employees must still enter their time statement
            of the month to be paid, which must hand in now within a few days.
            If the list is complete, that is, the time sheets are complete with all hours 
            (working hours, overtime sick leave, etc.), wages can be paid with the menu option
            "Monthly wage payments". This should be done in the middle of the month after the 
            previous book month.
            If a printout is made from April (this will take place in mid-May), after entering
            the program with the month yyyy-04 (yyyy stands for the relevant year) with the button
            'PRINT', first the holiday allowances and then the monthly wages are printed.               
                        
            ''')
                    
                grid.addWidget(lblinfo, 1, 0, 1, 4, Qt.AlignCenter)
                lblinfo.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF") 
                               
                cancelBtn = QPushButton('Close')
                cancelBtn.clicked.connect(self.close)  
                
                grid.addWidget(cancelBtn,  3, 0, 1, 4, Qt.AlignRight)
                cancelBtn.setFont(QFont("Arial",10))
                cancelBtn.setFixedWidth(90)
                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 4, Qt.AlignCenter)
                
                self.setLayout(grid)
                self.setMinimumWidth(650)
                self.setGeometry(550, 300, 900, 150)
                
        window = Widget()
        window.exec_()
        
    
    def windowSluit(self, m_email):
        self.close()
        hoofdMenu(m_email)
        
    def winSluit(self, m_email):
        self.close()
        maandBetalingen(m_email)
 
    def printing():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
        msg.setIcon(QMessageBox.Information)
        msg.setText('Just a moment printing is started!')
        msg.setWindowTitle('Paying wages')
        msg.exec_()
    
    def betaalVak(rpv):
        from sys import platform
        for row in rpv:
            jaar = str(row[1])[0:4]
            mnd = 'Vakantietoeslag'
            if platform == 'win32' :
                filename1 = '.\\forms\\Lonen\\wage_specification_'+str(row[2])+'-'+jaar+'_'+mnd+'.txt'
            else:
                filename1 = './forms/Lonen/wage_specification_'+str(row[2])+'-'+jaar+'_'+mnd+'.txt'
            gegevens =\
            ('                             Specification'+mnd+' '+str(jaar)+'                             \n'+
            '                                                                                             \n'+
            '                       proccessing date       accountnr employee                year period  \n'+
            'Addressee              '+str(datetime.datetime.now())[0:10]+'             '+str(row[2])+'     '+str(row[3])+'    emmployer      '+str(row[1])+'\n'+
            '=============================================================================================\n'+
            '                                                                 Pandora Connect B.V.,       \n'+
            '     '+'{:<30s}'.format(row[4]+' '+ row[5]+' '+row[6]+',')+'                              '+'Lange Dreef 7,\n'+
            '     '+'{:<30s}'.format(row[7]+' '+ str(row[8])+' '+row[9]+',')+'                              '+'4131 NJ Vianen.\n'+
            '     '+'{:<30s}'.format(row[10]+' '+ row[11]+'.')+'                              '+'Telephone: 0347377304\n'+
            '                                                                 e-mail: dj.jansen@casema.nl  \n'+                                                                   
            '=============================================================================================\n'+
            'Payments  /Deductions /Days/Hours/Amounts             taxable for                            \n'+
            'Description                    this period       table        special tax table              \n'+
            '---------------------------------------------------------------------------------------------\n'+
            'Holiday allowance             '+'{:>12.2f}'.format(row[14])+'                    '+'{:>12.2f}'.format(row[14]-row[16])+'\n'+
            '=============================================================================================\n'+
            'Tax special rate              '+'{:>12.2f}'.format(row[26])+'                    '+'{:>12.2f}'.format(row[26])+'\n'+
            'Pension contrib. not taxed    '+'{:>12.2f}'.format(row[16])+'                                \n'+
            '=============================================================================================\n'+
            'Net holiday allowance         '+'{:>12.2f}'.format(row[14]-row[16]-row[26])+'              \n'+
            '=============================================================================================\n'+
            'Employers share pension       '+'{:>12.2f}'.format(row[46])+'                                \n'+
            'Employers contrib. WIA,IVA,WGA'+'{:>12.2f}'.format(row[47])+'                                \n'+
            'Employers contrib. AWF        '+'{:>12.2f}'.format(row[48])+'                                \n'+
            'Employers contrib ZVW         '+'{:>12.2f}'.format(row[49])+'                                \n'+
            '=============================================================================================\n'+
            'Percentage special rate       '+'{:>12.2f}'.format(row[25]*100)+'                            \n')
            
            open(filename1, 'w').write(gegevens)
            if platform == 'win32':
                os.startfile(filename1, "print")
            else:
                os.system("lpr "+filename1)
                
    def printGeg(rpperln):
        from sys import platform
        if mjrmnd[5:7] == '04':
            mper = mjrmnd[0:4]+'vak'
            selv = select([loonbetalingen]).where(loonbetalingen.c.periode ==\
              mper).order_by(loonbetalingen.c.achternaam, loonbetalingen.c.voornaam)
            rpv = con.execute(selv)
            betaalVak(rpv)
            
        for row in rpperln:
            mbetmnd = ['January','February',' March', 'April', 'May', 'June', 'July',\
                    'August','September', 'October', 'November', 'December']
            jaar = row[1][0:4]
            mndidx = int(row[1][5:7])-1
            mnd = mbetmnd[mndidx]
            if platform == 'win32':
                filename = '.\\forms\\Lonen\\wage_specification_'+row[1]+'-'+str(row[2])+'.txt'
            else:
                filename = './forms/Lonen/wage_specification_'+row[1]+'-'+str(row[2])+'.txt'
            gegevens =\
            ('                           Wage specification '+str(mnd)+' '+str(jaar)+'           \n'+
            '                                                                                             \n'+
            '                       proccessing date       accountnr employee                year period  \n'+
            'Addressee              '+str(datetime.datetime.now())[0:10]+'             '+str(row[2])+'     '+str(row[3])+'    Employer       '+str(row[1])+'\n'+
            '=============================================================================================\n'+
            '                                                                 Pandora Connect B.V.,       \n'+
            '     '+'{:<30s}'.format(row[4]+' '+ row[5]+' '+row[6]+',')+'                              '+'Lange Dreef 7,\n'+
            '     '+'{:<30s}'.format(row[7]+' '+ str(row[8])+' '+row[9]+',')+'                              '+'4131 NJ Vianen.\n'+
            '     '+'{:<30s}'.format(row[10]+' '+ row[11]+'.')+'                              '+'Telephone: 0347377304\n'+
            '                                                                 e-mail: dj.jansen@casema.nl  \n'+                                                                   
            '=============================================================================================\n'+
            'Payments  /Deductions /Days/Hours/Amounts             taxable for                            \n'+
            'Description                    this period       table        special tax table              \n'+
            '---------------------------------------------------------------------------------------------\n'+
            'Gross wages                   '+'{:>12.2f}'.format(row[14])+'{:>12.2f}'.format(row[14])+'    \n'+
            '125% overtime                 '+'{:>12.2f}'.format(row[28]*row[32]*1.25)+'               '+'{:>12.2f}'.format(row[28]*row[32]*1.25)+'\n'+
            '150% overtime                 '+'{:>12.2f}'.format(row[29]*row[32]*1.50)+'               '+'{:>12.2f}'.format(row[29]*row[32]*1.50) +'\n'+
            '200% overtime                 '+'{:>12.2f}'.format(row[30]*row[32]*2)+'               '+'{:>12.2f}'.format(row[30]*row[32]*2)+'\n'+
            'Travel hours                  '+'{:>12.2f}'.format(row[27]*row[33])+'               '+'{:>12.2f}'.format(row[27]*row[33])+'\n'+
            'Travel allowance              '+'{:>12.2f}'.format(row[22])+'                                \n'+
            'Other fees                    '+'{:>12.2f}'.format(row[20])+'                                \n'+
            'Periodic fees                 '+'{:>12.2f}'.format(row[21])+'                                \n'+
            '                                                                                             \n'+
            '                   Payements  '+'{:>12.2f}'.format(row[14]+row[15]+row[22]+row[20]+row[21])+'{:>12.2f}'.format(row[14])+'   '+'{:>12.2f}'.format(row[15])+'\n'+
            '=============================================================================================\n'+
            'Pensioncontrib.SPF not taxed  '+'{:>12.2f}'.format(row[16])+'                                \n'+
            'Payroll tax minus deductions  '+'{:>12.2f}'.format(row[18])+'{:>12.2f}'.format(row[18])+'    \n'+
            'Special tax rate              '+'{:>12.2f}'.format(row[26])+'               '+'{:>12.2f}'.format(row[26])+'\n'+
            '                  Deductions  '+'{:>12.2f}'.format(row[16]+row[18]+row[26])+'                \n'+
            '------------------------------------------------------------------                           \n'+
            'Addition company car          '+'{:>12.2f}'.format(row[17])+'                                \n'+
            '                 Additions                '+'{:>12.2f}'.format(row[17])+'                    \n'+
            '------------------------------------------------------------------                           \n'+
            'Nett Wages                    '+'{:>12.2f}'.format(row[31])+'                                \n'+
            'Payment to bank account                      Other information                               \n'+
            '=============================================================================================\n'+
            'Weekday this month x 8 hours  '+'{:>12.2f}'.format(row[52])+'   Employer pensioncontributiom  '+'{:>12.2f}'.format(row[46])+'\n'+
            'Worked hours this month       '+'{:>12.2f}'.format(row[24])+'   Employer share WIA,IVA,WGA    '+'{:>12.2f}'.format(row[47])+'\n'+
            'Booked hours this month       '+'{:>12.2f}'.format(row[24]+row[34]+row[35]+row[36]+row[37]+row[38]+row[39])+'   Reservation AWF               '+'{:>12.2f}'.format(row[48])+'\n'+
            'Overtime 125% this month      '+'{:>12.2f}'.format(row[28])+'   Employer share ZVW            '+'{:>12.2f}'.format(row[49])+'\n'+
            'Overtime 150% this month      '+'{:>12.2f}'.format(row[29])+'   Res.holiday allowance cum.    '+'{:>12.2f}'.format(row[23])+'\n'+
            'Overtime 200% this month      '+'{:>12.2f}'.format(row[30])+'   Pay scale                     '+'{:>12.2f}'.format(row[41])+'\n'+
            'Hours leave this month        '+'{:>12.2f}'.format(row[34])+'   Wage step                     '+'{:>12.2f}'.format(row[42])+'\n'+
            'Hours extra leave this month  '+'{:>12.2f}'.format(row[35])+'   Percentage special rate       '+'{:>12.2f}'.format(row[25])+'\n'+
            'Hours holiday                 '+'{:>12.2f}'.format(row[36])+'   Date of birth                 '+'{:>12s}'.format(row[12])+'\n'+
            'Hours doctor visit            '+'{:>12.2f}'.format(row[38])+'   Date of employment            '+'{:>12s}'.format(row[13])+'\n'+
            'Hours illnes                  '+'{:>12.2f}'.format(row[37])+'   Leave credit in hours         '+'{:>12.2f}'.format(row[43])+'\n'+
            'Hours permitted leave         '+'{:>12.2f}'.format(row[39])+'   Hourly wage                   '+'{:>12.2f}'.format(row[32])+'\n'+
            '=========================================='+'   Reisuurloon                   '+'{:>12.2f}'.format(row[33])+'\n'+
            'Working hours cumulation      '+'{:>12.2f}'.format(row[51])+'                                \n'+
            '=============================================================================================\n'+
            'Amounts                                                                                      \n'+
            'Levy wages                    '+'{:>12.2f}'.format(row[14])+'                                \n'+
            'Payroll tax                   '+'{:>12.2f}'.format(row[18])+'                                \n'+
            'General levy shortfall        '+'{:>12.2f}'.format(row[44])+'                                \n'+
            'Labour tax credit             '+'{:>12.2f}'.format(row[45])+'                                \n'+
            '=============================================================================================\n'+
            '=============================================================================================\n')
            open(filename, 'w').write(gegevens)
            if platform == 'win32':
                os.startfile(filename, "print")
            else:
                os.system("lpr "+filename)
        printing()
        return(True)
    
    def acceptInvoer(self):
        reply = QMessageBox.question(self, 'Wage data',
          "Have all wage data been entered\nfor the specified period?",\
           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accept()
        else:
            winSluit(self, m_email)
            
    def recordLock():
            msg = QMessageBox()
            msg.setStyleSheet("color: black;  background-color: gainsboro")
            msg.setIcon(QMessageBox.Information)
            msg.setFont(QFont('Arial', 10))
            msg.setText('''
            
       This period has been blocked and closed 
       The printout has already taken place 
       the data will not be recreated 
       OK for STOP, PRINT or REQUEST!
      ''')
            msg.setWindowTitle('Pay wages')
            msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            msg.exec_()
                       
    def ongPeriode():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Warning)
        msg.setText('No valid payment period specified!')
        msg.setWindowTitle('Pay wages')
        msg.exec_()
    
    def progSluit():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Information)
        msg.setText('Program Closed\nSee you soon!')
        msg.setWindowTitle('Pay wages')
        msg.exec_()
     
    def toonMenu(rpwerknmr): 
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
                self.setWindowTitle("Pay employees' wages")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid = QGridLayout()
                grid.setSpacing(20)
                grid.addWidget(lbl , 0, 0, 1, 2)
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                self.setFont(QFont('Arial', 10))
                
                self.setLayout(grid)
                self.setGeometry(400, 300, 500, 150)
                
                grid.addWidget(QLabel
                ('''
                 The wage data has been successfully created
                 with REQUEST you can now view the data of 
                 the specified period and with 
                 PRINT all wage specifications printing.
                 '''),1,0,1,3)
                
                toonBtn = QPushButton('Request')
                toonBtn.clicked.connect(self.accept)
                
                printBtn = QPushButton('Print')
                printBtn.clicked.connect(lambda: printGeg(rpwerknmr))
                
                cancelBtn = QPushButton('Close')
                cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
               
                grid.addWidget(toonBtn, 3, 2)
                toonBtn.setFont(QFont("Arial",10))
                toonBtn.setFixedWidth(120)
                toonBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(printBtn, 3, 1)
                printBtn.setFont(QFont("Arial",10))
                printBtn.setFixedWidth(120)
                printBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(cancelBtn, 3, 0)
                cancelBtn.setFont(QFont("Arial",10))
                cancelBtn.setFixedWidth(120)
                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro") 
              
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
                   
        window = Widget()
        window.exec_()
        
    def maandPeriode():
        metadata = MetaData()
        params = Table('params', metadata,
            Column('paramID', Integer, primary_key=True),
            Column('tarief', Float),
            Column('item', String),
            Column('lock', Boolean))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
                self.setWindowTitle("Specify period for wage specifications")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
        
                self.setFont(QFont('Arial', 10))
                   
                self.Betaalperiode = QLabel()
                betEdit = QLineEdit()
                betEdit.setFixedWidth(100)
                betEdit.setFont(QFont("Arial",10))
                betEdit.textChanged.connect(self.betChanged)
                reg_ex = QRegExp('^[2]{1}[01]{1}[0-9]{2}[-][0-1]{1}[0-9]{1}$')
                input_validator = QRegExpValidator(reg_ex, betEdit)
                betEdit.setValidator(input_validator)
                                
                grid = QGridLayout()
                grid.setSpacing(20)
        
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid.addWidget(lbl , 0, 0, 1, 2)
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                               
                grid.addWidget(QLabel('Payment period yyyy-mm'), 1, 0, 1, 2, Qt.AlignRight)
                grid.addWidget(betEdit, 1, 2)
                
                infoBtn = QPushButton('Information')
                infoBtn.clicked.connect(lambda: info())
                  
                cancelBtn = QPushButton('Close')
                cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
             
                applyBtn = QPushButton('Proceed')
                applyBtn.clicked.connect(lambda: acceptInvoer(self))
                      
                grid.addWidget(applyBtn, 2, 2)
                applyBtn.setFont(QFont("Arial",10))
                applyBtn.setFixedWidth(100)
                applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
                grid.addWidget(cancelBtn, 2, 1)
                cancelBtn.setFont(QFont("Arial",10))
                cancelBtn.setFixedWidth(100)
                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(infoBtn, 2, 0)
                infoBtn.setFont(QFont("Arial",10))
                infoBtn.setFixedWidth(100)
                infoBtn.setStyleSheet("color: black;  background-color: gainsboro") 
           
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
                
                self.setLayout(grid)
                self.setGeometry(400, 300, 150, 150)
                     
            def betChanged(self, text):
                self.Betaalperiode.setText(text)
        
            def returnBetaalperiode(self):
                return self.Betaalperiode.text()
        
            @staticmethod
            def getData(parent=None):
                dialog = Widget(parent)
                dialog.exec_()
                return [dialog.returnBetaalperiode()]
       
        window = Widget()
        data = window.getData()
        if data[0] and len(data[0])==7:
              mjrmnd = data[0]
              selpar2 = select([params]).where(params.c.item == mjrmnd)
              rppar2 = con.execute(selpar2).first()
              if not rppar2:
                  ongPeriode()
                  maandBetalingen(m_email)
              elif rppar2[3]:
                  recordLock()
                  return(mjrmnd, 0)
              else:
                  updpar2 = update(params).where(params.c.item == mjrmnd).values(lock=True)
                  con.execute(updpar2)
                  con.close
              return(mjrmnd, 1)
        else:
             ongPeriode()
             maandBetalingen(m_email)
    
    mjrmndlck = maandPeriode()
    mjrmnd = mjrmndlck[0]
    lck = mjrmndlck[1]
    
    metadata = MetaData()   
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')), 
        Column('loontrede', Integer),
        Column('reiskosten_vergoeding', Float),
        Column('loonheffing', Float),
        Column('pensioenpremie', Float),
        Column('reservering_vakantietoeslag', Float),
        Column('werkgevers_pensioenpremie', Float),
        Column('periodieke_uitkeringen', Float),
        Column('overige_inhoudingen', Float),
        Column('overige_vergoedingen', Float),
        Column('bedrijfsauto', Float),
        Column('indienst', String),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float),
        Column('saldo_uren_geboekt', Float),
        Column('wnrloonID', Integer)) 
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('reisuur', Float),
        Column('maandloon', Float)) 
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('soort', String),
        Column('meerwerkstatus', Boolean),
        Column('bruto_loonbedrag', Float))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String),
        Column('geboortedatum', String),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String))
         
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    selwerknmr = select([werknemers, accounts]).where(werknemers.c.accountID ==\
                     accounts.c.accountID).order_by(werknemers.c.accountID)
    rpwerknmr = conn.execute(selwerknmr)
    
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String),
        Column('lock', Boolean),
        Column('ondergrens', Float),
        Column('bovengrens', Float))
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    
    import postcode
       
    for row in rpwerknmr:
        sellon = select([lonen]).where(lonen.c.loonID==row[17])
        rplon = conn.execute(sellon).first()
        conn.close
        mwerknmr = row[0]
        maccountnr = row[1]
        mvoornaam = row[19]
        mtussen = row[20]
        machternaam = row[21]
        mpostcode = row[23]
        mhuisnr = int(row[24])
        mtoev = row[25]
        mstrtplts = postcode.checkpostcode(mpostcode,mhuisnr)
        mstraat = mstrtplts[0]
        mplaats = mstrtplts[1]   
        mgebdat = row[22]
        mloonnr = row[17]
        mtred = row[3]
        mtrede = row[3]*0.03
        mreisk = row[4]
        mindienst = row[13]
        mverlof = row[14]
        mwerknsaldo = row[16]
        #mloonh = (uurloon*40*13)/3 #tabelloon.loonheffing
        if row[2] < 37 or (row[2] > 52 and row[2] < 125):
            mbruto = rplon[1]*520/3*(1+mtrede)
            #muurl = rplon[1]*(1+mtrede)
        else:
            mbruto =  rplon[2]*(1+mtrede)
            #muurl = mbruto*3/520
        mauto = row[12]   
        #pensioenpremie
        mjaarink = mbruto*12.96
        mpensink = mjaarink
        if mpensink >  rppar[44][5]:
            mpensprjr = (rppar[44][5]-rppar[44][4])*rppar[44][1]
        else:
            mpensprjr = (mpensink-rppar[44][4])*rppar[44][1]
        mpenspr = (mpensprjr)/12.96/3
        mpensprwg = mpenspr*2
        mvakpenspr =  mpenspr*0.96
        mvakpensprwg = mvakpenspr*2
        mresvaktslag = mbruto*0.08
        mbelink = mjaarink-mpensprjr+(mauto*12)
        # loonheffing 
        if mbelink > 0 and mbelink <= rppar[31][5]:
             lh1 = mbelink*rppar[31][1]
             lh = lh1
             if lh<0:
                 lh=0
        elif mbelink > rppar[32][4]  and mbelink <= rppar[32][5]:
             lh1 = rppar[31][5]*rppar[31][1]
             lh2 = (mbelink-rppar[31][5])*rppar[32][1]
             lh = lh1+lh2
        elif mbelink > rppar[32][5] and mbelink <= rppar[34][4]:
            lh1 = rppar[31][5]*rppar[31][1]
            lh2 = (mbelink-rppar[32][4])*rppar[32][1]
            lh3 = (mbelink-rppar[33][4])*rppar[33][1]
            lh = lh1+lh2+lh3
        elif mbelink >= rppar[33][4]:
            lh1 = rppar[31][5]*rppar[31][1]
            lh2 = (mbelink-rppar[31][5])*rppar[32][1]
            lh3 = (mbelink-rppar[32][4])*rppar[33][1]
            lh4 = (mbelink - rppar[34][4])*rppar[34][1]
            lh = lh1+lh2+lh3+lh4
        lh = lh/12
        #alg heffingkorting bepalen
        if mbelink <= rppar[36][4]:
            hk = rppar[35][1]
            if hk < 0:
                hk = 0
        elif mbelink > rppar[35][5] and mbelink <= rppar[37][4]:
            hk = rppar[35][1] - (mbelink-rppar[35][5])*rppar[36][1]
        elif mbelink >= rppar[36][5]:
            hk =  0
        hk = hk/12
        #arbeidskorting bepalen
        if mbelink <= rppar[39][4]:
            ak = mbelink*rppar[38][1]
        elif mbelink > rppar[38][5] and mbelink <= rppar[40][4]:
            ak1 = rppar[38][5]*rppar[38][1]
            ak2 = (mbelink-rppar[38][5])*rppar[39][1]
            ak = ak1+ak2
        elif mbelink > rppar[39][5] and mbelink <= rppar[41][4]:
            ak = rppar[40][1]
        elif mbelink > rppar[40][5] and mbelink <= rppar[42][4]:
            ak1 = rppar[40][1]
            ak2 = (mbelink-rppar[40][5])*rppar[41][1]
            ak = ak1 + ak2
        elif mbelink >= rppar[41][5]:
            ak = 0
        if ak > 0:
            ak = ak/12
        mwerkg_WAO_IVA_WGA = rppar[69][1]*mjaarink/12 
        mwerkg_AWF = rppar[70][1]*mjaarink/12 
        mwerkg_ZVW = rppar[71][1]*mjaarink/12 
        mloonh = lh -hk -ak
        # Bijzonder tarief bepalen
        if mbelink > 0 and mbelink <= 6512:
            mbyz = 0.3655
        elif mbelink > 6512 and mbelink <= 10226:
            mbyz = 0.3479
        elif mbelink > 10226 and mbelink <=18937:
            mbyz = 0.0849
        elif mbelink > 18937 and mbelink <= 20143:
            mbyz = 0.3655
        elif mbelink > 20143 and mbelink <= 22029:
            mbyz = 0.4553
        elif mbelink > 22029 and  mbelink <= 33113:
            mbyz = 0.4553
        elif mbelink > 33113 and mbelink <= 33995:
            mbyz = 0.4913
        elif mbelink > 33995 and mbelink <= 34405:
            mbyz = 0.4913
        elif mbelink > 34405 and mbelink <= 68508:
            mbyz = 0.4913
        elif mbelink > 68508 and mbelink <= 133232:
            mbyz = 0.5555
        elif mbelink > 133232:
            mbyz = 0.5195
      
        mbyztar = mbyz*100
        selwrkwnrln = select([wrkwnrln]).where(and_(row[0]==wrkwnrln.c.werknemerID,\
               wrkwnrln.c.boekdatum.like(mjrmnd+'%'))).\
           order_by(wrkwnrln.c.werknemerID, wrkwnrln.c.wrkwnrurenID)
        rpwrkwnrln = conn.execute(selwrkwnrln)
        sellon = select([lonen]).where(and_(lonen.c.loonID == werknemers.c.wnrloonID,\
                                      werknemers.c.werknemerID == mwerknmr))
        rplon = conn.execute(sellon).first()
        mtrede = row[3]
        muurloon = round(rplon[1]*(100+3*mtrede)/100, 2)
        mreisloon = round(rplon[2],2)
        #mmndloon = round(rplon[3]*(100+3*mtrede)/100,2)
        uren100 = 0
        uren125 = 0
        uren150 = 0
        uren200 = 0
        reisuren = 0
        verlof = 0
        feestdag = 0
        dokter = 0
        ziek = 0
        geoorlverz = 0
        ongeoorlverz = 0
        extraverl = 0
        
        for record in rpwrkwnrln:
            if record[5] == '100%':
                uren100 = uren100+record[4]
            elif record[5] == '125%':
                uren125 = uren125+record[4]
            elif record[5] == '150%':
                uren150 = uren150+record[4]
            elif record[5] == '200%':
                uren200 = uren200+record[4]
            elif record[5] == 'Reis':
                reisuren = reisuren+record[4]
            elif record[5] == 'Verlof':
                verlof = verlof+record[4]
            elif record[5] == 'Extra Verlof':
                extraverl = extraverl+record[4]
            elif record[5] == 'Feestdag':
                feestdag = feestdag+record[4]
            elif record[5] == 'Geoorl. Verzuim':
                geoorlverz = geoorlverz+record[4]
            elif record[5] == 'Ong. verzuim':
                ongeoorlverz = ongeoorlverz+record[4]
            elif record[5] == 'Ziek':
                ziek = ziek+record[4]
            elif record[5] == 'Dokter':
                dokter= dokter+record[4]
           
        mperiodiek = row[9]    
        movinhoud = row[10]
        movvergoed = row[11]
        #bedruren100 = uren100*muurloon
        bedruren125 = uren125*muurloon*1.25
        bedruren150 = uren150*muurloon*1.50
        bedruren200 = uren200*muurloon*200
        bedrreisuren = reisuren*mreisloon
        #bedrverlof = verlof*muurloon
        #bedrextraverl = extraverl*muurloon
        #bedrfeestdag = feestdag*muurloon
        #bedrgeoorlverz = geoorlverz*muurloon
        #bedrziek = ziek*muurloon
        #bedrdokter=dokter*muurloon
        con.close
        
        metadata = MetaData()   
        loonbetalingen = Table('loonbetalingen', metadata,
            Column('betalingID', Integer(), primary_key=True),
            Column('periode', String),
            Column('accountID', None, ForeignKey('accounts.accountID')),
            Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
            Column('voornaam', String),
            Column('tussenvoegsel', String),
            Column('achternaam', String),
            Column('straat', String),
            Column('huisnummer', Integer),
            Column('toevoeging', String),
            Column('postcode', String),
            Column('woonplaats', String),
            Column('geboortedatum', String),
            Column('indienst', String),
            Column('brutoloon', Float),
            Column('bruto_variabel', Float),
            Column('pensioenpremie', Float),
            Column('bijtelling_auto', Float),
            Column('loonheffing', Float),
            Column('inhouding_overig', Float),
            Column('periodieke_uitkering', Float),
            Column('vergoeding_overig', Float),
            Column('vergoeding_reiskosten',Float),
            Column('res_vakantietoeslag', Float),
            Column('werkuren', Float),
            Column('byz_tarief', Float),
            Column('bedrag_byz_tarief', Float),
            Column('reisuren', Float),
            Column('overuren_125', Float),
            Column('overuren_150', Float),
            Column('overuren_200', Float),
            Column('nettoloon', Float),
            Column('uurloon', Float),
            Column('reisuurloon', Float),
            Column('uren_verlof', Float),
            Column('uren_extra_verlof', Float),
            Column('uren_feestdag', Float),
            Column('uren_ziek', Float),
            Column('uren_dokter', Float),
            Column('uren_geoorloofd_verzuim', Float),
            Column('uren_ongeoorloofd_verzuim', Float),
            Column('loonschaal', Integer),
            Column('loontrede', Integer),
            Column('verlofsaldo', Float),
            Column('alg_heffingskorting', Float),
            Column('arbeidskorting', Float),
            Column('wg_pensioenpremie', Float),
            Column('wg_WAO_IVA_WGA', Float),
            Column('wg_AWF', Float),
            Column('wg_ZVW', Float),
            Column('boekdatum', String),
            Column('saldo_uren_geboekt'),
            Column('maandwerkuren', Float),
            Column('uren_geboekt', Float))
              
        selpar2 = select([params]).where(params.c.item == mjrmnd)
        rppar2 = con.execute(selpar2).first()
        
        if lck == 1:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
                 
            if mjrmnd[5:7] == '05':
                updvktslg = update(werknemers).where(werknemers.c.werknemerID == mwerknmr).\
                  values(reservering_vakantietoeslag = 0)
                con.execute(updvktslg)
            
            updwrkuren = update(werknemers).where(werknemers.c.werknemerID == mwerknmr).\
            values(saldo_uren_geboekt = werknemers.c.saldo_uren_geboekt-rppar2[1]+uren100\
               +verlof+extraverl+feestdag+dokter+ziek+geoorlverz, \
              reservering_vakantietoeslag = werknemers.c.reservering_vakantietoeslag+\
              mresvaktslag, pensioenpremie = mpenspr, werkgevers_pensioenpremie =\
              mpensprwg, loonheffing = mloonh)
            con.execute(updwrkuren)
            
            selvak = select([werknemers]).where(werknemers.c.werknemerID == mwerknmr)
            rpvak = con.execute(selvak).first()
            mresvaktslg = rpvak[7]
            con.close
                    
            mboekd = str(datetime.datetime.now())[0:10]
            try:
                mbetalingnr =(conn.execute(select([func.max(loonbetalingen.c.betalingID,\
                   type_=Integer)])).scalar())
                mbetalingnr += 1
            except:
                mbetalingnr = 1
            
            insloon = insert(loonbetalingen).values(betalingID = mbetalingnr, periode = mjrmnd,\
               accountID = maccountnr, werknemerID = mwerknmr, voornaam = mvoornaam,\
               tussenvoegsel = mtussen, achternaam = machternaam, straat = mstraat,\
               huisnummer = mhuisnr, toevoeging = mtoev, postcode = mpostcode,\
               woonplaats = mplaats, geboortedatum = mgebdat, brutoloon = mbruto,\
               pensioenpremie = mpenspr, bijtelling_auto = mauto, bruto_variabel =\
               bedrreisuren+bedruren125+bedruren150+bedruren200+mperiodiek, loonheffing\
               = mloonh, inhouding_overig = movinhoud, periodieke_uitkering = mperiodiek,\
               vergoeding_overig = movvergoed, vergoeding_reiskosten = mreisk,\
               res_vakantietoeslag =  mresvaktslg, werkuren = uren100, reisuren = reisuren,\
               overuren_125 = uren125, overuren_150 = uren150, overuren_200 = uren200,\
               nettoloon = mbruto- mpenspr-mloonh+bedrreisuren - bedrreisuren*mbyztar/100\
              +bedruren125 - bedruren125*mbyztar/100+bedruren150 - bedruren150*mbyztar/100\
              +bedruren200 - bedruren200*mbyztar/100+mperiodiek-mperiodiek*mbyztar/100+mreisk-\
              movinhoud+movvergoed, uurloon = muurloon, byz_tarief = mbyztar,\
              bedrag_byz_tarief = bedrreisuren*mbyztar/100+bedruren125*mbyztar/100+\
              bedruren150*mbyztar/100+bedruren200*mbyztar/100+mperiodiek*mbyztar/100,\
              reisuurloon = mreisloon,uren_verlof = verlof, uren_extra_verlof =\
              extraverl, uren_feestdag = feestdag, uren_ziek = ziek, uren_dokter =\
              dokter, uren_geoorloofd_verzuim = geoorlverz, uren_ongeoorloofd_verzuim =\
              ongeoorlverz, indienst = mindienst, loonschaal = mloonnr, loontrede = mtred,\
              verlofsaldo = mverlof, alg_heffingskorting = hk, arbeidskorting = ak,\
              wg_pensioenpremie = mpensprwg, wg_WAO_IVA_WGA = mwerkg_WAO_IVA_WGA,\
              wg_AWF = mwerkg_AWF, wg_ZVW = mwerkg_ZVW, boekdatum = mboekd, saldo_uren_geboekt =\
              mwerknsaldo-rppar2[1]+uren100+verlof+extraverl+feestdag+dokter+ziek+\
                           geoorlverz, maandwerkuren = rppar2[1], uren_geboekt =\
                           uren100+verlof+extraverl+feestdag+dokter+ziek+geoorlverz)
            con.execute(insloon)
            con.close
            
            metadata = MetaData()   
            afdrachten = Table('afdrachten', metadata,
                Column('afdrachtID', Integer(), primary_key=True),
                Column('soort', String),
                Column('bedrag', Float),
                Column('boekdatum', String),
                Column('betaaldatum', String),
                Column('instantie', String),
                Column('werknemerID', Integer),
                Column('werknummerID', Integer),
                Column('werkorderID', Integer),
                Column('rekeningnummer', String),
                Column('periode', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            try:
                mafdrachtnr =(conn.execute(select([func.max(afdrachten.c.afdrachtID,\
                    type_=Integer)])).scalar())
                mafdrachtnr += 1
            except:
                mafdrachtnr = 1
            insafdr = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'werkn_pensioenpr',\
                  bedrag = mpenspr , boekdatum = mboekd, instantie = 'Spoorwegpensioenfonds',\
                  werknemerID = mwerknmr, rekeningnummer = 'NL09 ABNA 9999999955', periode =mjrmnd)
            con.execute(insafdr)
            
            mafdrachtnr += 1
            insafdr1 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'werkg-pensioenpr',\
                  bedrag = mpensprwg , boekdatum = mboekd, instantie = 'Spoorwegpensioenfonds',\
                  werknemerID = mwerknmr, rekeningnummer = 'NL09 ABNA 9999999955', periode =mjrmnd)
            con.execute(insafdr1)
            
            mafdrachtnr += 1
            insafdr2 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'loonheffing',\
                 bedrag = mloonh, boekdatum = mboekd, instantie = 'Belastingdienst',\
                 werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977', periode =mjrmnd)
            con.execute(insafdr2)
            
            mafdrachtnr += 1
            insafdr3 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'WAO, IVA, WGA premie',\
                bedrag = mwerkg_WAO_IVA_WGA, boekdatum = mboekd, instantie = 'Belastingdienst',\
                werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977', periode =mjrmnd)
            con.execute(insafdr3)
            
            mafdrachtnr += 1
            insafdr4 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'AWF premie',\
               bedrag = mwerkg_AWF, boekdatum = mboekd, instantie = 'Belastingdienst',\
               werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977', periode =mjrmnd)
            con.execute(insafdr4)
            
            mafdrachtnr += 1
            insafdr5 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'ZVW premie',\
               bedrag = mwerkg_ZVW, boekdatum = mboekd, instantie = 'Belastingdienst',\
               werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977', periode =mjrmnd)
            con.execute(insafdr5)
            
            mafdrachtnr += 1
            insafdr6 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'Bijzonder tarief',\
               bedrag = bedrreisuren*mbyztar/100+bedruren125*mbyztar/100+\
              bedruren150*mbyztar/100+bedruren200*mbyztar/100+mperiodiek*mbyztar/100,\
              boekdatum = mboekd, instantie = 'Belastingdienst',\
               werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977', periode =mjrmnd)
            con.execute(insafdr6)
            
            updpar = update(params).where(params.c.item == mjrmnd).values(lock=True)
            con.execute(updpar)
            con.close
            
            if mjrmnd[5:7] == '04':
                selvak = select([werknemers]).where(werknemers.c.werknemerID == mwerknmr)
                rpvak=con.execute(selvak).first()
                mvaktslg = rpvak[7]
                con.close
                
                mper = mjrmnd[0:4]+'vak'
                mvakpenspr = mpenspr*0.96
                mvakpensprwg = mvakpenspr*2
                mbyzvak = (mvaktslg-mvakpenspr)*mbyz
                mvakwerkg_WAO_IVA_WGA = mvaktslg*rppar[69][1]
                mvakwerkg_AWF = mvaktslg*rppar[70][1]
                mvakwerkg_ZVW = mvaktslg*rppar[71][1]
         
                mbetalingnr += 1
                insvak = insert(loonbetalingen).values(betalingID = mbetalingnr,\
                    periode = mper, brutoloon = mvaktslg,\
                 accountID = maccountnr, werknemerID = mwerknmr, voornaam = mvoornaam,\
                 tussenvoegsel = mtussen, achternaam = machternaam, straat = mstraat,\
                 huisnummer = mhuisnr, toevoeging = mtoev, postcode = mpostcode,\
                 woonplaats = mplaats, geboortedatum = mgebdat, pensioenpremie =\
                 mvakpenspr, wg_pensioenpremie = mvakpensprwg, wg_WAO_IVA_WGA =\
                 mvakwerkg_WAO_IVA_WGA, wg_AWF = mvakwerkg_AWF, wg_ZVW = mvakwerkg_ZVW,\
                 byz_tarief = mbyz, bedrag_byz_tarief = mbyzvak, boekdatum = mboekd,\
                 nettoloon = mvaktslg-mbyzvak-mvakpenspr)
                con.execute(insvak)
                con.close
                mafdrachtnr += 1
                insvakafdr = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort =\
                 'Bijzonder tarief',bedrag = mbyzvak, boekdatum = mboekd, instantie = 'Belastingdienst',\
                 werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977',\
                 periode = mper)
                con.execute(insvakafdr)
                mafdrachtnr += 1
                insvakafdr1 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'WAO, IVA, WGA premie',\
                    bedrag = mvakwerkg_WAO_IVA_WGA, boekdatum = mboekd, instantie = 'Belastingdienst',\
                    werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977',\
                    periode = mper)
                con.execute(insvakafdr1)
                mafdrachtnr += 1
                insvakafdr2 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'AWF premie',\
                    bedrag = mvakwerkg_AWF, boekdatum = mboekd, instantie = 'Belastingdienst',\
                    werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977',\
                    periode = mper)
                con.execute(insvakafdr2)
                mafdrachtnr += 1
                insvakafdr3 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'ZVW premie',\
                     bedrag = mvakwerkg_ZVW, boekdatum = mboekd, instantie = 'Belastingdienst',\
                     werknemerID = mwerknmr, rekeningnummer = 'NL10 ABNA 9999999977',\
                     periode = mper)
                con.execute(insvakafdr3)
                mafdrachtnr += 1
                insvakafdr4 = insert(afdrachten).values(afdrachtID=mafdrachtnr, soort = 'werkg-pensioenpr',\
                  bedrag = mvakpensprwg , boekdatum = mboekd, instantie = 'Spoorwegpensioenfonds',\
                  werknemerID = mwerknmr, rekeningnummer = 'NL09 ABNA 9999999955',\
                  periode = mper)
                con.execute(insvakafdr4) 
                con.close

    def toonBetalingen():
        class MyWindow(QDialog):
            def __init__(self, data_list, header, *args):
                QWidget.__init__(self, *args,)
                self.setGeometry(30, 60, 1500, 900)
                self.setWindowTitle('Request wage payments')
                self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
                table_model = MyTableModel(self, data_list, header)
                table_view = QTableView()
                table_view.setModel(table_model)
                font = QFont("Arial", 10)
                table_view.setFont(font)
                table_view.hideColumn(3)
                table_view.hideColumn(36)
                table_view.hideColumn(37)
                table_view.resizeColumnsToContents()
                table_view.setSelectionBehavior(QTableView.SelectRows)
                table_view.clicked.connect(showSelection)
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
                  
        header = ['Payment no.', 'Monthly period', 'Account number', 'Employee', 'Thirst name',\
              'Infix','Surname', 'Street', 'House number', 'Suffix',\
              'Zipcode', 'Residence', 'Birth date', 'Into service date','Gross salary',\
              'Gross variable', 'Pension contribution', 'Addition car','Payroll tax',\
              'Withholding other','Periodic payment','Other compensation',\
              'Travel compensation','Res. holiday allowance cum.','Working hours',\
              'Special rate hours', 'Amount special rate','Travel hours', 'Overtime 125%',\
              'Overtime 150%', 'Overtime 200%', 'Net salary','Hourly wage', 'Travel hourly wage',\
              'Leave hours', 'Extra leave hours', 'Holiday hours', 'Illness hours',\
              'Doctor hours', 'Permitted leave hours', 'Illegal leave hours',\
              'Wage scale', 'Wage step', 'Leave balance', 'General tax credit',\
              'Employment tax credit', 'Employer pension contrib.','Employer WAO-IVA-WGA contrib.',\
              'Employer AWF contrib.', 'Employer ZVW costs','Booking date',\
              'Cumulative difference hours', 'Hours in this month', 'Booked this month']
    
        selperln = select([loonbetalingen]).where(loonbetalingen.c.periode == mjrmnd).order_by(loonbetalingen.c.achternaam, loonbetalingen.c.voornaam)
        rpperln = con.execute(selperln)
        status = toonMenu(rpperln)
        if status:
            status = False
            return(True)
        else:
            status = False
            selperln = select([loonbetalingen]).where(loonbetalingen.c.periode == mjrmnd)
            rpperlon = con.execute(selperln)
            
        data_list=[]
        for row in rpperlon:
            data_list += [(row)]
            
        def showSelection(idx):
            mbetaalnr = idx.data()
            if  idx.column() == 0:
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                selbet = select([loonbetalingen]).where(loonbetalingen.c.betalingID == mbetaalnr)
                rpbet = con.execute(selbet).first()
                                 
                class MainWindow(QDialog):
                    def __init__(self):
                        QDialog.__init__(self)
                        
                        grid = QGridLayout()
                        grid.setSpacing(20)
                        
                        self.setWindowTitle("Request wage payments")
                        self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                        
                        self.setFont(QFont('Arial', 10))   
                                                          
                        self.lbl = QLabel()
                        self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                        self.lbl.setPixmap(self.pixmap)
                        grid.addWidget(self.lbl , 0, 0)
                        
                        grid.addWidget(QLabel('Request wage payments per employee and period'),0, 2, 1, 3)
                
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
                            self.lbl = QLabel(header[index-3])
                            
                            self.Gegevens = QLabel()
                            if type(rpbet[index-3]) == float:
                                q1Edit = QLineEdit('{:12.2f}'.format(rpbet[index-3]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            elif type(rpbet[index-3]) == int:
                                q1Edit = QLineEdit(str(rpbet[index-3]))
                                q1Edit.setAlignment(Qt.AlignRight)
                            else:
                                q1Edit = QLineEdit(str(rpbet[index-3]))
                            q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                            q1Edit.setFixedWidth(200)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, verpos, horpos+horpos%3)
                            grid.addWidget(q1Edit, verpos, horpos+horpos%3+1)
                            
                            index +=1
                            
                        terugBtn = QPushButton('Close')
                        terugBtn.clicked.connect(self.accept)
                
                        grid.addWidget(terugBtn, verpos+1, 5, 1 , 1, Qt.AlignRight)
                        terugBtn.setFont(QFont("Arial",10))
                        terugBtn.setFixedWidth(100) 
                        terugBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                        grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), verpos+1, 2, 1, 2)
                                                                                
                        self.setLayout(grid)
                        self.setGeometry(100, 50, 150, 150)
                                
                mainWin = MainWindow()
                mainWin.exec_()
        
        win = MyWindow(data_list, header)
        win.exec_()
        maandBetalingen(m_email)
    toonBetalingen()