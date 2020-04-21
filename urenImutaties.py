from login import hoofdMenu
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton,\
     QLineEdit, QGridLayout, QDialog, QCheckBox, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, \
                            ForeignKey, create_engine, Boolean)
from sqlalchemy.sql import select, update, func, and_
         
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
        Werkodernummer: leeg veld in te vullen met het werkordernummer, waarvoor 
        wordt gewerkt.
        Aanwezig/Afwezig: kies hier de soort uren, waarvoor de boeking moet worden gedaan,
        bv. 100% reguliere uren, 125% overwerk, 150% overwerk, 200% overwerk, 
        of een van de diverse genoemde afwezigheidsuren voor verlof ziekte enz.
        Aantal uren: Uren die zijn gewerkt op de dag van de werkzaamheden.
        Bij het label voor de werkelijke totaaluren wordt de vakdiscipline aangegeven,
        waarvoor de uren zijn geboekt.
        Datum werkzaamheden:  datum van de huidige dag in het formaat jjjj-mm-dd
        Button 'Muteren' Standaard button met tekst 'Muteren'
        Bij het aanpassen of invullen van de velden 'Accountnummer', 'Werkordernummer'
        en 'Datum werkzaamheden', zal het systeem bij opkomen van de velden de laatst
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
        Column('werknummerID', Integer),
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
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer(), primary_key=True),
        Column('werkomschrijving', String),
        Column('voortgangstatus', String),
        Column('statusweek', String),
        Column('boekdatum', String),
        Column('begroot_totaal', Float),
        Column('werk_totaal', Float),
        Column('begr_materialen', Float),
        Column('werk_materialen', Float),
        Column('begr_lonen', Float),
        Column('werk_lonen', Float),
        Column('bzagen', Float),
        Column('wzagen', Float),
        Column('bschaven', Float),
        Column('wschaven', Float),
        Column('bsteken', Float),
        Column('wsteken', Float),
        Column('bboren', Float),
        Column('wboren', Float),
        Column('bfrezen', Float),
        Column('wfrezen', Float),
        Column('bdraaien_klein', Float),
        Column('wdraaien_klein', Float),
        Column('bdraaien_groot', Float),
        Column('wdraaien_groot', Float),
        Column('btappen', Float),
        Column('wtappen', Float),
        Column('bnube_draaien', Float),
        Column('wnube_draaien', Float),
        Column('bnube_bewerken', Float),
        Column('wnube_bewerken', Float),
        Column('bknippen', Float),
        Column('wknippen', Float),
        Column('bkanten', Float),
        Column('wkanten', Float),
        Column('bstansen', Float),
        Column('wstansen', Float),
        Column('blassen_co2', Float),
        Column('wlassen_co2', Float),
        Column('blassen_hand', Float),
        Column('wlassen_hand', Float),
        Column('bverpakken', Float),
        Column('wverpakken', Float),
        Column('bverzinken', Float),
        Column('wverzinken', Float),
        Column('bmoffelen', Float),
        Column('wmoffelen', Float),
        Column('bschilderen', Float),
        Column('wschilderen', Float),
        Column('bspuiten', Float),
        Column('wspuiten', Float),
        Column('bponsen', Float),
        Column('wponsen', Float),
        Column('bpersen', Float),
        Column('wpersen', Float),
        Column('bgritstralen', Float),
        Column('wgritstralen', Float),
        Column('bmontage', Float),
        Column('wmontage', Float),
        Column('werk_reis_uren', Float),
        Column('meerminderwerk', Float))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('werkuur', Float),
        Column('reisuur', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selwnr = select([werknemers]).where(and_(werknemers.c.accountID==int(maccountnr),\
                    werknemers.c.loonID > 52))
    rpwnr = con.execute(selwnr).first()
    if rpwnr:
        maccountnr = int(maccountnr)
    else:
       self.urenEdit.setText('0')
       self.lblt.setStyleSheet("font: bold; color: red")
       self.lblt.setText('Persoon niet in deze arbeidspool!')
       self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
       return('', mwerknr, mboekd, m_email)
    if mwerknr and len(mwerknr)== 9  and _11check(mwerknr):
        mwerknr = int(mwerknr)
    else:
       self.urenEdit.setText('0')
       self.lblt.setStyleSheet("font: bold; color: red")
       self.lblt.setText('Dit is geen geldig werkordernummer!')
       self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
       return(maccountnr, '', mboekd, m_email)
                
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selwerk = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
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
        self.lblt.setStyleSheet("font: bold; color: red")
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
        self.lblt.setStyleSheet("font: bold;color: red")
        self.lblt.setText('Geen uren ingevoerd!')
        self.applyBtn.setStyleSheet("color: black; background-color: #FF3333")
        return(maccountnr, mwerknr, mboekd, m_email)
            
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    mwrkwnruren=(con.execute(select([func.max(wrkwnrln.c.wrkwnrurenID, type_=Integer)\
                                   .label('mwrkwnruren')])).scalar())
    wrkgr = rpwnr[2]
    wrkgr2 = rpwnr[5]
    loonsel = select([lonen]).where(lonen.c.loonID == wrkgr)    #loonID
    loonsel2 = select([lonen]).where(lonen.c.loonID == wrkgr2)
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
                
    if wrkgr > 52 and wrkgr < 56 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
               values(werk_lonen = orders_intern.c.werk_lonen+loonk,
               wzagen = orders_intern.c.wzagen+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
               meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[11]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[12]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Zagen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 55 and wrkgr < 59 and msoort < 5:   
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wschaven = orders_intern.c.wschaven+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[13]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[14]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Schaven'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 58 and wrkgr < 62 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
           values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wsteken = orders_intern.c.wsteken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[15]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[16]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Steken'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 61 and wrkgr < 65 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
          values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wboren = orders_intern.c.wboren+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
            meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[17]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[18]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Boren'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 64 and wrkgr < 68 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
          values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wfrezen = orders_intern.c.wfrezen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[19]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[20]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Frezen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 67 and wrkgr < 71 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
          values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wdraaien_klein = orders_intern.c.wdraaien_klein+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
            meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[21]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[22]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Draaien klein'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 70 and wrkgr < 74 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
           values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wdraaien_groot = orders_intern.c.wdraaien_groot+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[23]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[24]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Draaien groot'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 73 and wrkgr < 77 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
           values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wtappen = orders_intern.c.wtappen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[25]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[26]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Tappen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 76 and wrkgr < 80 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wnube_draaien = orders_intern.c.wnube_draaien+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[27]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[28]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Nubé draaien'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 79 and wrkgr < 83 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wnube_bewerken = orders_intern.c.wnube_bewerken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[29]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[30]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Nubé bewerken'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 72 and wrkgr < 86 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wknippen = orders_intern.c.wknippen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[31]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[32]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Knippen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 75 and wrkgr < 89 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wkanten = orders_intern.c.wkanten+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[33]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[34]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Kanten'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 88 and wrkgr < 92 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wstansen = orders_intern.c.wstansen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[35]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[36]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Stanzen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 91 and wrkgr < 95 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
           values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wlassen_co2 = orders_intern.c.wlassen_co2+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[37]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[38]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Lassen co2'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 94 and wrkgr < 98 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wlassen_hand = orders_intern.c.wlassen_hand+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[39]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[40]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Lassen hand'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 97 and wrkgr < 101 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wverpakken = orders_intern.c.wverpakken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[41]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[42]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Verpakken'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 100 and wrkgr < 104 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wverzinken = orders_intern.c.wverzinken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[43]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[44]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Verzinken'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 103 and wrkgr < 107 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wmoffelen = orders_intern.c.wmoffelen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[45]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[46]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Moffelen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 106 and wrkgr < 110 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wschilderen = orders_intern.c.wschilderen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[47]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[48]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Schilderen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 109 and wrkgr < 113 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wspuiten = orders_intern.c.wspuiten+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[49]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[50]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Spuiten'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 112 and wrkgr < 116 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wponsen = orders_intern.c.wponsen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[51]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[52]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Ponsen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 115 and wrkgr < 119 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wpersen = orders_intern.c.wpersen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[53]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[54]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Persen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 118 and wrkgr < 122 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
           values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wgritstralen = orders_intern.c.wgritstralen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[55]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[56]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Gritstralen'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    elif wrkgr > 121 and wrkgr < 125 and msoort < 5:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
            values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wmontage = orders_intern.c.wmontage+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
        sel = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
        rpsel = con.execute(sel).first()
        self.urenbegrEdit.setText('{:<12.2f}'.format(rpsel[57]))
        self.urentotEdit.setText('{:<12.2f}'.format(rpsel[58]))
        lblptext = 'Totalen: Werkelijk / Begroot\nUren Montage'
        lbltext = 'Muteren uren (werken - lonen) niet cumulatief'
        self.lblprof.setText(lblptext)
        self.lblt.setStyleSheet("color: black")
        self.lblt.setText(lbltext)
    else:
        msaldo = ''
        mboekuren = str(mboekuren)
        if msoort == 5 and wrkgr > 52:
            selsal = select([werknemers]).where(werknemers.c.accountID == maccountnr)
            rpsal = con.execute(selsal).first()
            msaldo = str(rpsal[3])
            lbltext = mboekuren+' Verlofuren ingevoerd, Saldo = '+msaldo+' uren.'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 6 and wrkgr > 52:
            lbltext = mboekuren+' Extra verlofuren ingevoerd'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 7 and wrkgr > 52:
            lbltext = mboekuren+' Uren ziekte ingevoerd'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 8 and wrkgr > 52:
            lbltext = mboekuren+' Uren feestdagen ingevoerd'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 9 and wrkgr > 52:
            lbltext = mboekuren+' Uren dokterbezoek ingevoerd'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 10 and wrkgr > 52:
            lbltext = mboekuren+' Uren geoorloofd verzuim ingevoerd'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        elif msoort == 11 and wrkgr > 52:
            lbltext = mboekuren+' Uren ongeoorloofd verzuim ingevoerd'
            lblptext = '\n'
            self.lblt.setStyleSheet("color: navy")
            self.lblt.setText(lbltext)
            self.lblprof.setText(lblptext)
        else:
            self.urenEdit.setText('0')
            self.lblt.setStyleSheet("font: bold;color: red")
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
            
            self.setWindowTitle("Uren invoeren interne werken - lonen")
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
            reg_ex = QRegExp("^[7]{1}[0-9]{8}$")
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
                        
            def  cboxChanged():
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
            self.lblt.setStyleSheet("color: black")
            self.lblt.setFont(QFont("Arial", 10))
            grid.addWidget(self.lblt , 12, 0, 1, 4, Qt.AlignCenter)
            
            lbl1 = QLabel('Accountnummer')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 6, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.zkaccEdit , 6, 2, 1, 1, Qt.AlignRight)
            
            lbl2 = QLabel('Werkordernummer')
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