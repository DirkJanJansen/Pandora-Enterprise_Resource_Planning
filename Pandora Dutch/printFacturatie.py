from login import hoofdMenu
import datetime, os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine, Float, select)

def jaarweek():
    dt = datetime.datetime.now()
    week = ('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)
    
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Printen Facturen')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()

def printGeg(m_email, filename):
    from sys import platform
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Printlijst te factureren werken")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Wilt U de lijst van nog te factureren\nbedragen externe werken uitprinten?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        if platform == 'win32':
            os.startfile(filename, "print")
        else:
            os.system("lpr "+filename)
        printing()
        hoofdMenu(m_email)
    else:
        hoofdMenu(m_email)

def maakLijst(m_email):
    from sys import platform
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True),
        Column('werkomschrijving', String),
        Column('aanneemsom', Float),
        Column('kosten_materialen', Float),
        Column('kosten_lonen', Float),
        Column('kosten_materieel', Float),
        Column('kosten_leiding', Float),
        Column('kosten_huisv', Float),
        Column('kosten_overig', Float),
        Column('kosten_vervoer', Float),
        Column('meerminderwerk', Float),
        Column('voortgangstatus', String),
        Column('statusweek',  String),
        Column('betaald_bedrag', Float),
        Column('begr_huisv', Float),
        Column('begr_leiding', Float),
        Column('begr_overig', Float),
        Column('kosten_inhuur', Float),
        Column('beton_bvl', Float),
        Column('kabelwerk', Float),
        Column('grondverzet', Float),
        Column('begr_inhuur', Float),
        Column('begr_vervoer', Float),
        Column('begr_beton_bvl', Float),
        Column('begr_kabelwerk', Float),
        Column('begr_grondverzet', Float),
        Column('begr_materieel',Float),
        Column('begr_materialen', Float),
        Column('begr_lonen', Float),
        Column('startweek', String))
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    sel = select([werken]).order_by(werken.c.werknummerID)
    rpwerken = con.execute(sel)
    rgl = 0
    mblad = 0
    for row in rpwerken:
        msom = row[2]
        mktotal=row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[17]\
         +row[18]+row[19]+row[20]
        mbetaald = row[13]
        mvgangst = row[11]
        mstatwk = row[12]
        mfact = 0
        mwerknr = row[0]
        mmeerwerk = float(row[10])
        if mvgangst == 'A':
            if mktotal > 0:
                mvgangst = 'B'
                mstatwk = jaarweek()
        elif mvgangst == 'B':      
            if mktotal > msom/3:
                mvgangst = 'C'
                mstatwk = jaarweek()
        elif mvgangst == 'C':
            if mktotal > msom/2:
                mvgangst = 'D'
                mstatwk = jaarweek()
            mfact = msom/3-mbetaald
        elif mvgangst == 'D':
            if mktotal > msom/1.5:
                mvgangst = 'E'
                mstatwk = jaarweek()
        elif mvgangst == 'E':
            if mktotal >= msom:
                mvgangst = 'F'
                mstatwk = jaarweek()
            mfact = msom/1.5-mbetaald
        elif mvgangst == 'F':
            mfact = msom-mbetaald*0.9
        elif mvgangst == 'G':
            mfact = msom+mmeerwerk-mbetaald 
        if mfact > 1:
            if rgl == 0 or rgl%57 == 0:
                mblad += 1
                if platform == 'win32':
                    filename = '.\\forms\\Facturen_Werken\\Factuur-Werken_'+str(datetime.datetime.now())[0:10]+'.txt'
                else:
                    filename = './forms/Facturen_Werken/Factuur-Werken_'+str(datetime.datetime.now())[0:10]+'.txt'
                kop =\
            ('Facturen Externe werken Datum: '+str(datetime.datetime.now())[0:10]+' Pagina '+str(mblad)+'\n'+
            "==============================================================================================\n"+
            "Werknummer      Omschrijving    Status   Aanneemsom nog-Factureren  reeds-Betaald     Meerwerk\n"+
            "==============================================================================================\n")
                if rgl == 0:
                    open(filename, 'w').write(kop)
                elif rgl%57 == 0:
                    open(filename, 'a').write(kop)
                
            gegevens = str(mwerknr)+' '+"{:18s}".format(str(row[1])[0:18])+'  '\
                 +str(mvgangst)+' '+str(mstatwk)+' '+"{:>12.2f}"\
                 .format(msom)+'   '+"{:>12.2f}".format(mfact)+'   '+"{:>12.2f}".format(mbetaald)\
                 +' '+"{:>12.2f}".format(mmeerwerk)
            open(filename,'a').write (gegevens+'\n') 
            rgl += 1
    printGeg(m_email, filename)    
        