from login import hoofdMenu
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QFont, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel,\
            QPushButton, QComboBox, QCheckBox
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine,\
                        ForeignKey, Float, select, update, func, and_, Boolean)
    
def _11check(mcontr):
    number = str(mcontr)
    total = 0       
    fullnumber = number                       
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total %11 %10
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
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
        \t\t\t\t\t\t\t\t\t\t 
                                        Information about hours to mutate.  
        The module starts with the following variable data: 
        Account number: blank field to be filled in with the employee's account number. 
        Work number: empty field to be filled in with the work number, for which work is being done. 
        Present/Absent: choose here the type of hours for which the booking must be made, 
        e.g. 100% regular hours, 125% overtime, 150% overtime, 200% overtime,
        or one of the various hours of absence mentioned for sick leave etc.
        Number of hours: Hours worked on the day of work.
        The label for the actual total hours indicates the professional discipline,
        for which the hours are booked. 
        Date of work: date of the current day in the format yyyy-mm-dd 
        Button 'Mutate' Standard button with text 'Mutate' 
        When modifying or filling in the 'Account number' fields, 'Account number', 'Work number' and 
        'Date of work', the system will remember the last keyed data when the fields arise,
        so that a quick entry is possible. 
        The option Present/Absent will be filled in by default with 100% hours,
        because this will be the most common choice.
        When entering the data, if entered correctly, the button Mutate' turn green.
        In the event of an incorrect or unsuccessful entry, the button 'Mutate' turn red,
        in this case a correction should be created, because the entry was not booked!
        In the status field below the input fields, the status and information of the absence hours is showed,
        e.g. in the case of leave hours the leave balance is showed.
        This status field also displays the error messages, in the case of a invalid entry.  
                                     
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

def urenBoeking(self, m_email):
    maccountnr = self.zkaccEdit.text()
    mwerknr = self.zkwerknEdit.text()
    mboekd = self.boekdatumEdit.text()
    mstatus = self.cBox.checkState()
    if mstatus == 0:
        mstatus = False
    else:
        mstatus = True
    metadata = MetaData()
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('werknummerID',Integer),       
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('tabelloon', Float),
        Column('reisloon', Float),
        Column('bruto_loonbedrag', Float),
        Column('meerwerkstatus', Boolean),
        Column('soort', String))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float),
        Column('wnrloonID', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('kosten_lonen', Float),
        Column('voortgangstatus', String),
        Column('statusweek', String(6)),
        Column('begr_constr_uren', Float),
        Column('werk_constr_uren', Float),
        Column('begr_mont_uren', Float),
        Column('werk_mont_uren', Float),
        Column('begr_retourlas_uren', Float),
        Column('werk_retourlas_uren', Float),
        Column('begr_telecom_uren', Float),
        Column('werk_telecom_uren', Float),
        Column('begr_bfi_uren', Float),
        Column('werk_bfi_uren', Float),
        Column('begr_bvl_uren', Float),
        Column('werk_bvl_uren', Float),
        Column('begr_spoorleg_uren', Float),
        Column('werk_spoorleg_uren', Float),
        Column('begr_spoorlas_uren', Float),
        Column('werk_spoorlas_uren', Float),
        Column('begr_reis_uren', Float),
        Column('werk_reis_uren', Float),
        Column('meerminderwerk', Float),
        Column('begr_voeding_uren', Float),
        Column('werk_voeding_uren', Float))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('werkuur', Float),
        Column('reisuur', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selwnr = select([werknemers]).where(and_(werknemers.c.accountID==int(maccountnr),\
                     werknemers.c.loonID < 37))
    rpwnr = con.execute(selwnr).first()
    if rpwnr:
        maccountnr = int(maccountnr)
    else:
       self.urenEdit.setText('0')
       self.lblt.setStyleSheet("font: bold ; color: red")
       self.lblt.setText('Person not present in this labor pool!')
       self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
       return('', mwerknr, mboekd, m_email)
    selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
    if mwerknr and len(mwerknr)== 9  and _11check(mwerknr) and con.execute(selwerk).first():
        mwerknr = int(mwerknr)
    else:
       self.urenEdit.setText('0')
       self.lblt.setStyleSheet("font: bold ; color: red")
       self.lblt.setText('This is not a existing worknumber!')
       self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
       return(maccountnr, '', mboekd, m_email)
                
    rpwerk = con.execute(selwerk).first()
    muren = 0
    mu125 = 0
    mu150 = 0
    mu200 = 0
    mreis = 0
    mmeerw100 = 0
    mmeerw125 = 0
    mmeerw150 = 0
    mmeerw200 = 0
    mverlof = 0
    mextraverlof = 0
    mziek = 0
    mfeest = 0
    mdokter = 0
    mgverzuim = 0
    moverzuim = 0
            
    msoort = self.k0Edit.currentIndex()
    
    mboekuren = float(self.urenEdit.text())
    
    mlist = ['100%','125%','150%','200%','Travel','Leave','Extra leave','Illness',\
            'Holiday','Doctor','Allowed absence','Illegal absence']
    
    if rpwerk[2] == 'H':
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("font: bold ; color: red")
        self.lblt.setText('Work is ready and logged out!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return(maccountnr, mwerknr, mboekd, m_email)
    elif mboekuren and msoort == 0 and mstatus:
        mmeerw100 = mboekuren
    elif mboekuren and msoort == 0:
        muren = mboekuren
    elif mboekuren and msoort == 1 and mstatus:
        mmeerw125 = mboekuren
    elif mboekuren and msoort  == 1:
        mu125 = mboekuren 
    elif mboekuren and msoort == 2 and mstatus:
        mmeerw150 = mboekuren
    elif mboekuren and msoort == 2:
        mu150 = mboekuren
    elif mboekuren and msoort == 3 and mstatus:
        mmeerw200 = mboekuren
    elif mboekuren and msoort == 3:
        mu200 = mboekuren
    elif mboekuren and msoort == 4:
        mreis = mboekuren
    elif mboekuren and msoort == 5:
        mverlof = mboekuren
        upd = update(werknemers).where(werknemers.c.accountID ==\
            maccountnr).values(verlofsaldo = werknemers.c.verlofsaldo - mboekuren)
        con.execute(upd) 
    elif mboekuren and msoort == 6:
        mextraverlof = mboekuren
        upd = update(werknemers).where(werknemers.c.accountID ==\
            maccountnr).values(extraverlof = werknemers.c.extraverlof - mextraverlof)
        con.execute(upd) 
    elif mboekuren and msoort == 7:
        mziek = mboekuren
    elif mboekuren and msoort == 8:
        mfeest = mboekuren
    elif mboekuren and msoort == 9:
        mdokter = mboekuren
    elif mboekuren and msoort == 10:
        mgverzuim = mboekuren 
    elif mboekuren and msoort == 11:
        moverzuim = mboekuren  
    else:
        self.urenEdit.setText('0')
        self.lblt.setStyleSheet("font: bold;color: red")
        self.lblt.setText('No hours entered!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return(maccountnr, mwerknr, mboekd, m_email)

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    try:
        mwrkwnruren=(con.execute(select([func.max(wrkwnrln.c.wrkwnrurenID,\
            type_=Integer)])).scalar())
    except:
        mwrkwnruren = 1

    wrkgr = rpwnr[2]
    wrkgr2 = rpwnr[5]
    loonsel = select([lonen]).where(lonen.c.loonID == wrkgr)    #time loonID for works
    loonsel2 = select([lonen]).where(lonen.c.loonID == wrkgr2)  #loonID for wages
    loonres = con.execute(loonsel).first()
    loonres2 = con.execute(loonsel2).first()
    muurloon = loonres2[1]
    mwerkuur = loonres[2]
    mreisuur = loonres[3]
    mwrku125 = mwerkuur*1.25
    mwrku150 = mwerkuur*1.5
    mwrku200 = mwerkuur*2
 
    loonk = (muren*mwerkuur)+(mreis*mreisuur)+(mu125*mwrku125)+(mu150*mwrku150)+\
             (mu200*mwrku200)+(mmeerw100*mwerkuur)+(mmeerw125*mwerkuur)+(mmeerw150*\
             mwerkuur)+(mmeerw200*mwerkuur)
    meerk = (mmeerw100*mwerkuur)+(mmeerw125*mwrku125)+\
            (mmeerw150*mwrku150)+(mmeerw200*mwrku200)
    lonen = (muren*muurloon)+(mu125*muurloon*1.25)+(mu150*muurloon*1.5)+(mu200\
             *muurloon*2)+(mreis*mreisuur)+(mmeerw100*muurloon)+\
             (mmeerw125*muurloon*1.25)+(mmeerw150*muurloon*1.5)+\
             (mmeerw200*muurloon*2)+(mverlof*muurloon)+(mextraverlof*muurloon)+\
             (mziek*muurloon)+(mfeest*muurloon)+(mdokter*muurloon)+\
             (mgverzuim*muurloon)+(moverzuim*muurloon)
     
    inswrkwnrln = wrkwnrln.insert().values(
    wrkwnrurenID = mwrkwnruren+1,
    werknemerID = rpwnr[0],
    boekdatum = mboekd,
    aantaluren = muren+mu125+mu150+mu200+mreis+mmeerw100+mmeerw125+mmeerw150+\
      mmeerw200+mverlof+mextraverlof+mziek+mfeest+mdokter+mgverzuim+moverzuim,
    soort = mlist[msoort],
    werknummerID = mwerknr,
    tabelloon = muurloon,
    reisloon = mreisuur,
    bruto_loonbedrag = lonen,
    meerwerkstatus = mstatus,
    loonID = wrkgr2)
    if con.execute(inswrkwnrln):
        self.applyBtn.setStyleSheet("color: black; background-color: #00CC66")
    else:
        self.urenEdit.setText('0')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return(maccountnr, mwerknr, mboekd, m_email) 
                 
    if wrkgr < 5 and msoort < 5:
        stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
        values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_constr_uren = werken.c.werk_constr_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([werken]).where(werken.c.werknummerID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[5]))
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[4]))
        lblptext = 'Totals: Realised / Budgeted\nHours Construction'
        lbltext = 'Mutate hours (work - wages) not cumulatively'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr < 9 and msoort < 5: 
        stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_mont_uren = werken.c.werk_mont_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([werken]).where(werken.c.werknummerID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[6]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[7]))
        lblptext = 'Totals: Realised / Budgeted\nHours Assembly'
        lbltext = 'Mutate hours (work - wages) not cumulative'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr < 13 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_retourlas_uren = werken.c.werk_retourlas_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[8]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[9]))
          lblptext = 'Totals: Realised / Budgeted\nHours return welding'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    elif wrkgr < 17 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_telecom_uren = werken.c.werk_telecom_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
                meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[10]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[11]))
          lblptext = 'Totals: Realised / Budgeted\nHours Telecom'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    elif wrkgr < 21 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_bfi_uren = werken.c.werk_bfi_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[12]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[13]))
          lblptext = 'Totals: Realised / Budgeted\nHours Chief mechanic'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    elif wrkgr < 25 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_bvl_uren = werken.c.werk_bvl_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
                meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[14]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[15]))
          lblptext = 'Totals: Realised / Budgeted\nHours Catenary'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    elif wrkgr < 29 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_spoorleg_uren = werken.c.werk_spoorleg_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[16]))
          self.urentotEdit.setText('{:>12.2f}'.format(rpsel[17]))
          lblptext = 'Totals: Realised / Budgeted\nHours Track laying'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    elif wrkgr < 33 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_mont_uren = werken.c.werk_spoorlas_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[18]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[19]))
          lblptext = 'Totals: Realised / Budgeted\nHours Track welding'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    elif wrkgr < 37 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
                values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_voeding_uren = werken.c.werk_voeding_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
               meerminderwerk = werken.c.meerminderwerk + meerk)
          con.execute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[23]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[24]))
          lblptext = 'Totals: Realised / Budgeted\nHours Power-supply'
          lbltext = 'Mutate hours (work - wages) not cumulative'
          self.lblprof.setText(lblptext)
          self.lblt.setStyleSheet("color: black")
          self.lblt.setText(lbltext)
    else:
        msaldo = ''
        mboekuren = str(mboekuren)
        if msoort == 5 and wrkgr < 37:
            selsal = select([werknemers]).where(werknemers.c.accountID == maccountnr)
            rpsal = con.execute(selsal).first()
            msaldo = str(rpsal[3])
            lbltext = mboekuren+' Leave hours entered, Balance ='+msaldo+' hours.'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 6 and wrkgr < 37:
            lbltext = mboekuren+' Extra Leave Hours entered'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 7 and wrkgr < 37:
            lbltext = mboekuren+' Hours illness entered'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 8 and wrkgr < 37:
            lbltext = mboekuren+' Hours Holidays entered'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 9  and wrkgr < 37:
            lbltext = mboekuren+' Hours Doctor\'s Visit entered'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 10 and wrkgr < 37:
            lbltext = mboekuren+' Hours allowed absence entered'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 11 and wrkgr < 37:
            lbltext = mboekuren+' Hours illegal absence entered'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        else:
            self.urenEdit.setText('0')
            self.lblt.setStyleSheet("font: bold;color: red")
            self.lblt.setText('Person not in this labor pool')
            self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
            return(maccountnr, mwerknr, mboekd, m_email) 

    self.urenEdit.setText('0')
    self.k0Edit.setCurrentIndex(0)
    return(maccountnr, mwerknr, mboekd, m_email) 
    
def urenMut(maccountnr, mwerknr, mboekd, m_email):
    class Widget(QDialog):
        def __init__(self):
            super(Widget,self).__init__()
            
            self.setWindowTitle("Entering hours of external works - wages")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
               
            self.zkaccEdit = QLineEdit(str(maccountnr))
            self.zkaccEdit.setFixedWidth(150)
            self.zkaccEdit.setFont(QFont("Arial",10))
            self.zkaccEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[1]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, self.zkaccEdit)
            self.zkaccEdit.setValidator(input_validator)
            
            self.zkwerknEdit = QLineEdit(str(mwerknr))
            self.zkwerknEdit.setFixedWidth(150)
            self.zkwerknEdit.setFont(QFont("Arial",10))
            self.zkwerknEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[8]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, self.zkwerknEdit)
            self.zkwerknEdit.setValidator(input_validator)
     
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(150)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('100%')
            self.k0Edit.addItem('125%')
            self.k0Edit.addItem('150%')
            self.k0Edit.addItem('200%')
            self.k0Edit.addItem('Travel')
            self.k0Edit.addItem('Leave')
            self.k0Edit.addItem('Extra leave')
            self.k0Edit.addItem('Illness')
            self.k0Edit.addItem('Holiday')
            self.k0Edit.addItem('Doctor')
            self.k0Edit.addItem('Allowed. leave')
            self.k0Edit.addItem('Illegal leave')
  
            self.cBox = QCheckBox('More/less work')
            self.cBox.setFont(QFont("Arial",10))
            self.cBox.setStyleSheet('color: black; background-color: #F8F7EE')
                                                                     
            self.urenEdit = QLineEdit('0')
            self.urenEdit.setFixedWidth(150)
            self.urenEdit.setFont(QFont("Arial",10))
            self.urenEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.urenEdit)
            self.urenEdit.setValidator(input_validator)
            
            self.urentotEdit = QLineEdit('0')
            self.urentotEdit.setFixedWidth(150)
            self.urentotEdit.setDisabled(True)
            self.urentotEdit.setFont(QFont("Arial",10))
            self.urentotEdit.setStyleSheet("color: black")
    
            self.urenbegrEdit = QLineEdit('0')
            self.urenbegrEdit.setFixedWidth(150)
            self.urenbegrEdit.setDisabled(True)
            self.urenbegrEdit.setFont(QFont("Arial",10))
            self.urenbegrEdit.setStyleSheet("color: black")        
                                                         
            self.boekdatumEdit = QLineEdit(mboekd)
            self.boekdatumEdit.setFixedWidth(150)
            self.boekdatumEdit.setFont(QFont("Arial",10))
            self.boekdatumEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[2]{1}[0-1]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, self.boekdatumEdit)
            self.boekdatumEdit.setValidator(input_validator)
                                            
            def accChanged():
                self.zkaccEdit.setText(self.zkaccEdit.text())
            self.zkaccEdit.textChanged.connect(accChanged)
             
            def werknChanged():
                self.zkwerknEdit.setText(self.zkwerknEdit.text())
            self.zkwerknEdit.textChanged.connect(werknChanged)
             
            '''
            def k0Changed():
                self.k0Edit.setCurrentText(self.k0Edit.currentText())
            self.k0Edit.currentTextChanged.connect(k0Changed)
                        
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.activated[str].connect(k0Changed)
            '''
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
                       
            def cboxChanged():
                self.cBox.setCheckState(self.cBox.checkState())
            self.cBox.stateChanged.connect(cboxChanged)
            
            def urenChanged():
                self.urenEdit.setText(self.urenEdit.text())
            self.urenEdit.textChanged.connect(urenChanged)
            
            def boekdatumChanged():
                self.boekdatumEdit.setText(self.boekdatumEdit.text())
            self.boekdatumEdit.textChanged.connect(boekdatumChanged)
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,0 , 1)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)       

            self.lblt = QLabel('Mutate hours (work - wages) not cumulative')
            self.lblt.setStyleSheet("color: black")
            self.lblt.setFont(QFont("Arial", 10))
            grid.addWidget(self.lblt , 12, 0, 1, 4, Qt.AlignCenter)
            
            lbl1 = QLabel('Account number')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 6, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkaccEdit , 6, 2, 1, 1, Qt.AlignRight)
            
            lbl2 = QLabel('Work number')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 7, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkwerknEdit, 7, 2, 1, 1, Qt.AlignRight)
                
            lbl3 = QLabel('Type of hours')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 8, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.k0Edit, 8, 2, 1, 1, Qt.AlignRight)
                        
            grid.addWidget(self.cBox, 8, 3)
            
            self.lblprof = QLabel('Totals: Realised / Budgeted\nHours')
            self.lblprof.setFont(QFont("Arial", 10))
            self.lblprof.setFixedWidth(200)
            self.lblprof.setAlignment(Qt.AlignRight)
            grid.addWidget(self.lblprof, 9, 1, 1, 1, Qt.AlignRight | Qt.AlignTop)
            grid.addWidget(self.urentotEdit, 9, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenbegrEdit, 9, 3, 1, 1)
            
            lbl4 = QLabel('Mutate hours')
            lbl4.setFont(QFont("Arial", 10))
            grid.addWidget(lbl4, 10, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenEdit, 10, 2, 1, 1, Qt.AlignRight)

            lbl5 = QLabel('Book date')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 11, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.boekdatumEdit, 11, 2, 1, 1, Qt.AlignRight)
            
            self.applyBtn = QPushButton('Mutate')
            self.applyBtn.clicked.connect(lambda: urenBoeking(self, m_email))
               
            self.applyBtn.setFont(QFont("Arial",10))
            self.applyBtn.setFixedWidth(100)
            self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(self.applyBtn,13, 3 , 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
    
            grid.addWidget(cancelBtn, 13, 2, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
                   
            infoBtn = QPushButton('Info')
            infoBtn.clicked.connect(lambda: info()) 
    
            grid.addWidget(infoBtn, 13, 1, 1, 1, Qt.AlignRight)
            infoBtn.setFont(QFont("Arial",10))
            infoBtn.setFixedWidth(100)
            infoBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
            rightslbl = QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl')
            rightslbl.setFont(QFont("Arial", 10))
            grid.addWidget(rightslbl, 14, 1, 1, 4, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
                
    window = Widget()
    window.exec_()  