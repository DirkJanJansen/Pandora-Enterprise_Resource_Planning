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
        checkdigit = total % 11
    if checkdigit == 10:
        checkdigit = 0
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
            self.setWindowTitle("Informatie ERP Systeem Pandora")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Informatie ERP Pandora')
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
                                        Informatie over te muteren uren.  
                                         
        De module start met de volgende variabele gegevens:
        Accountnummer: leeg veld in te vullen met accountnummer van de werknemer.
        Werknummer: leeg veld in te vullen met het werknummer, waarvoor wordt gewerkt.
        Aanwezig/Afwezig: kies hier de soort uren, waarvoor de boeking moet worden gedaan,
        bv. 100% reguliere uren, 125% overwerk, 150% overwerk, 200% overwerk, 
        of een van de diverse genoemde afwezigheidsuren voor verlof ziekte enz.
        Aantal uren: Uren die zijn gewerkt op de dag van de werkzaamheden.
        Bij het label voor de werkelijke totaaluren wordt de vakdiscipline aangegeven,
        waarvoor de uren zijn geboekt.
        Datum werkzaamheden:  datum van de huidige dag in het formaat jjjj-mm-dd
        Button 'Muteren' Standaard button met tekst 'Muteren'
        Bij het aanpassen of invullen van de velden 'Accountnummer', 'Werknummer' en
        'Datum werkzaamheden', zal het systeem bij opkomen van de velden de laatst
        ingetoetste gegevens onthouden, zodat een snelle invoer mogelijk is.
        De keuze Aanwezig/Afwezig zal standaard ingevuld worden met 100% uren,
        omdat dit de meest voorkomende keuze zal zijn.
        Bij het intoetsen van de gegevens zal  bij een juiste invoer de knop
        'Muteren' groen kleuren. Bij een foutieve of niet gelukte invoer zal de 
        knop 'Muteren' rood kleuren, in dit geval dient een korrektie te worden 
        gemaakt, omdat de invoer niet is geboekt!
        In het statusveld onder de invulvelden, wordt de status en informatie
        van de afwezigheidsuren getoond, b.v. bij verlofuren het verlofsaldo.
        Tevens worden in dit statusveld de foutmeldingen weergegeven, bij een
        ongeldige invoer.
   
     ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Sluiten')
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
       self.lblt.setText('Persoon niet in deze arbeidspool!')
       self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
       return('', mwerknr, mboekd, m_email)
    if mwerknr and len(mwerknr)== 9  and _11check(mwerknr):
        mwerknr = int(mwerknr)
    else:
       self.urenEdit.setText('0')
       self.lblt.setText('Dit is geen geldig werknummer!')
       self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
       return(maccountnr, '', mboekd, m_email)
                
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selwerk = select([werken]).where(werken.c.werknummerID == mwerknr)
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
    
    mlist = ['100%','125%','150%','200%','Reis','Verlof','Extra verlof','Ziekte',\
            'Feestdag','Dokter','Geoorl. verzuim','Ong. verzuim']
    
    if rpwerk[2] == 'H':
        self.urenEdit.setText('0')
        self.lblt.setText('Werk is gereed en afgemeld!')
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
        self.lblt.setText('Geen uren ingevoerd!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return(maccountnr, mwerknr, mboekd, m_email)
            
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    mwrkwnruren=(con.execute(select([func.max(wrkwnrln.c.wrkwnrurenID, type_=Integer)\
                           .label('mwrkwnruren')])).scalar())

    wrkgr = rpwnr[2]
    wrkgr2 = rpwnr[5]
    loonsel = select([lonen]).where(lonen.c.loonID == wrkgr)    #tijd loonID voor werken
    loonsel2 = select([lonen]).where(lonen.c.loonID == wrkgr2)  #loonID voor lonen
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
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Constructie'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
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
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Montage'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
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
          lblptext = 'Totalen: Werkelijk / Begroot\nUren Retourlas'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
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
          lblptext = 'Totalen: Werkelijk / Begroot\nUren Telecom'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
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
          lblptext = 'Totalen: Werkelijk / Begroot\nUren BFI'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
          self.lblt.setText(lbltext)
    elif wrkgr < 25 and msoort < 5:
          stmt = update(werken).where(werken.c.werknummerID == mwerknr).\
              values(kosten_lonen = werken.c.kosten_lonen+loonk,
               werk_bvl_uren = werken.c.werk_bvl_uren+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = werken.c.werk_reis_uren+mreis,\
                meerminderwerk = werken.c.meerminderwerk + meerk)
          con.xecute(stmt)
          sel = select([werken]).where(werken.c.werknummerID == mwerknr)
          rpsel = con.execute(sel).first()
          self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[14]))
          self.urentotEdit.setText('{:<12.2f}'.format(rpsel[15]))
          lblptext = 'Totalen: Werkelijk / Begroot\nUren Bovenleiding'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
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
          lblptext = 'Totalen: Werkelijk / Begroot\nUren Spoorleg'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
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
          lblptext = 'Totalen: Werkelijk / Begroot\nUren Spoorlas'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
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
          lblptext = 'Totalen: Werkelijk / Begroot\nUren Voeding'
          lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
          self.lblprof.setText(lblptext)
          self.lblt.setText(lbltext)
    else:
        msaldo = ''
        mboekuren = str(mboekuren)
        if msoort == 5 and wrkgr < 37:
            selsal = select([werknemers]).where(werknemers.c.accountID == maccountnr)
            rpsal = con.execute(selsal).first()
            msaldo = str(rpsal[3])
            lbltext = mboekuren+' Verlofuren ingevoerd, Saldo = '+msaldo+' uren.'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 6 and wrkgr < 37:
            lbltext = mboekuren+' Extra verlofuren ingevoerd'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 7 and wrkgr < 37:
            lbltext = mboekuren+' Uren ziekte ingevoerd'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 8 and wrkgr < 37:
            lbltext = mboekuren+' Uren feestdagen ingevoerd'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 9  and wrkgr < 37:
            lbltext = mboekuren+' Uren dokterbezoek ingevoerd'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 10 and wrkgr < 37:
            lbltext = mboekuren+' Uren geoorloofd verzuim ingevoerd'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 11 and wrkgr < 37:
            lbltext = mboekuren+' Uren ongeoorloofd verzuim ingevoerd'
            lblptext = 'Totaaluren\n'
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        else:
            self.urenEdit.setText('0')
            self.lblt.setText('Persoon niet in deze arbeidspool!')
            self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
            return(maccountnr, mwerknr, mboekd, m_email) 
        
    self.urenEdit.setText('0')
    self.k0Edit.setCurrentIndex(0)
    return(maccountnr, mwerknr, mboekd, m_email) 
    
def urenMut(maccountnr, mwerknr, mboekd, m_email):
    class Widget(QDialog):
        def __init__(self):
            super(Widget,self).__init__()
            
            self.setWindowTitle("Uren invoeren externe werken - lonen")
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
            self.k0Edit.addItem('Reis')
            self.k0Edit.addItem('Verlof')
            self.k0Edit.addItem('Extra verlof')
            self.k0Edit.addItem('Ziekte')
            self.k0Edit.addItem('Feestdag')
            self.k0Edit.addItem('Dokter')
            self.k0Edit.addItem('Geoorl. verzuim')
            self.k0Edit.addItem('Ong. verzuim')
  
            self.cBox = QCheckBox('Meerwerk')
            self.cBox.setFont(QFont("Arial",10))
            self.cBox.setStyleSheet('color: black; background-color: #F8F7EE')
                                                                     
            self.urenEdit = QLineEdit('0')
            self.urenEdit.setFixedWidth(150)
            self.urenEdit.setFont(QFont("Arial",10))
            self.urenEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
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

            self.lblt = QLabel('Muteren uren (werken - lonen) niet cumulatief')
            self.lblt.setFont(QFont("Arial", 10))
            grid.addWidget(self.lblt , 12, 0, 1, 4, Qt.AlignCenter)
            
            lbl1 = QLabel('Accountnummer')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 6, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkaccEdit , 6, 2, 1, 1, Qt.AlignRight)
            
            lbl2 = QLabel('Werknummer')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 7, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkwerknEdit, 7, 2, 1, 1, Qt.AlignRight)
                
            lbl3 = QLabel('Soort Uren')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 8, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.k0Edit, 8, 2, 1, 1, Qt.AlignRight)
                        
            grid.addWidget(self.cBox, 8, 3)
            
            self.lblprof = QLabel('Totalen: Werkelijk / Begroot\nUren')
            self.lblprof.setFont(QFont("Arial", 10))
            self.lblprof.setFixedWidth(200)
            self.lblprof.setAlignment(Qt.AlignRight)
            grid.addWidget(self.lblprof, 9, 1, 1, 1, Qt.AlignRight | Qt.AlignTop)
            grid.addWidget(self.urentotEdit, 9, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenbegrEdit, 9, 3, 1, 1)
            
            lbl4 = QLabel('Urenmutatie')
            lbl4.setFont(QFont("Arial", 10))
            grid.addWidget(lbl4, 10, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.urenEdit, 10, 2, 1, 1, Qt.AlignRight)
                                       
            lbl5 = QLabel('Boekdatum')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 11, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.boekdatumEdit, 11, 2, 1, 1, Qt.AlignRight)
            
            self.applyBtn = QPushButton('Muteren')
            self.applyBtn.clicked.connect(lambda: urenBoeking(self, m_email))
               
            self.applyBtn.setFont(QFont("Arial",10))
            self.applyBtn.setFixedWidth(100)
            self.applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(self.applyBtn,13, 3 , 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
    
            grid.addWidget(cancelBtn, 13, 2, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
                   
            infoBtn = QPushButton('Informatie')
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