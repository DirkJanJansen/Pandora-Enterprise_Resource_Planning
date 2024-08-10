from login import hoofdMenu
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QIcon 
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine, Float)
from sqlalchemy.sql import select, insert, delete, func, and_
import datetime

def jaarweek():
    dt = datetime.datetime.now()
    week = str('0'+str(dt.isocalendar()[1]))[-2:]
    jaar = str(dt.isocalendar()[0])
    jrwk = jaar+week
    return(jrwk)

def JN(m_email):
    msgBox=QMessageBox()
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Calculate Data from external Works")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Do you want to calculate this week's financials?")
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        bereken(m_email)
    else:
        hoofdMenu(m_email) 
        
def geenGegevens():
    msgBox=QMessageBox()
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Calculate financial data from external works")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText("No data available for this year!")
    msgBox.exec_()
    
def berBestaat(jrwk, m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            msg = QMessageBox()
            msg.setStyleSheet("color: black;  background-color: gainsboro")
            msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            msg.setWindowTitle("Calculation of external works")
            msg.setIcon(QMessageBox.Warning)
            msg.setText('This booking week\'s report is present\n\nDo you want to recalculate it?\n\nN.B. the existing data will be overwritten!')
            msg.setStandardButtons(QMessageBox.Yes)
            msg.addButton(QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            if(msg.exec_() == QMessageBox.Yes):
                metadata = MetaData()
                resultaten = Table('resultaten', metadata,
                   Column('resID', Integer(), primary_key=True),
                   Column('boekweek', String))  
                resultaten_status = Table('resultaten_status', metadata,
                   Column('rID', Integer(), primary_key=True),
                   Column('boekweek', String))  
                engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
                con = engine.connect()
                seldel1 = delete(resultaten).where(resultaten.c.boekweek == jrwk)
                con.execute(seldel1)
                seldel2 = delete(resultaten_status).where(resultaten_status.c.boekweek == jrwk)
                con.execute(seldel2)
                bereken(m_email)
    window = Widget()
    window.show()  
       
def berGelukt():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            msg = QMessageBox()
            msg.setStyleSheet("color: black;  background-color: gainsboro")
            msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            msg.setIcon(QMessageBox.Information)
            msg.setText('The calculation for '+jaarweek()+' is completed!')
            msg.setWindowTitle('Results')
            msg.exec_()
    window = Widget()
    window.show()    

def divBereken(row):
    jrwk = jaarweek()
    mstatuswk = row[12]
    metadata = MetaData()
    resultaten = Table('resultaten', metadata,
        Column('resID', Integer(), primary_key=True),
        Column('statusweek', String),
        Column('blonen', Float),
        Column('wlonen', Float),
        Column('bmaterialen', Float),
        Column('wmaterialen', Float),
        Column('bmaterieel', Float),
        Column('wmaterieel', Float),
        Column('binhuur', Float),
        Column('winhuur', Float),
        Column('bdiensten', Float),
        Column('wdiensten', Float),
        Column('bprojectkosten', Float),
        Column('wprojectkosten', Float),
        Column('btotaal', Float),
        Column('wtotaal', Float),
        Column('betaald_bedrag', Float),
        Column('meerminderwerk', Float),
        Column('onderhandenwerk', Float),
        Column('boekweek', String),
        Column('bruto_winst', Float),
        Column('aanneemsom', Float))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selres = select([resultaten]).where(and_(resultaten.c.statusweek == mstatuswk,\
                   resultaten.c.boekweek == jrwk))
    rpres = con.execute(selres).first()
    mstatus = row[11]
    mkosten = row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+row[17]+\
              row[18]+row[19]+row[20]
    if mstatus == 'C':
        mwinst = row[2]/3-mkosten
    elif mstatus == 'D':
        mwinst = row[2]/3-mkosten
    elif mstatus == 'E':
        mwinst = row[2]*2/3-mkosten
    elif mstatus == 'F':
        mwinst = row[2]*.8667-mkosten
    elif mstatus == 'G':
       mwinst = row[2]-mkosten
    elif mstatus == 'H':
        mwinst = row[2]+row[10]-mkosten
    else:
        mwinst = 0

    if not rpres:
        try:
            mresnr = (con.execute(select([func.max(resultaten.c.resID,\
                type_=Integer)])).scalar())
            mresnr += 1
        except:
            mresnr = 1
        insres = insert(resultaten).values(resID = mresnr, statusweek = mstatuswk,\
          blonen=round(row[28],2), wlonen=round(row[4],2),bmaterialen=round(row[27],2),\
          wmaterialen=round(row[3],2),bmaterieel=round(row[26],2), wmaterieel=round(row[5],2),\
          binhuur=round(row[21],2), winhuur=round(row[21],2),bprojectkosten=round(row[14]+\
          row[15]+row[16]+row[22],2),wprojectkosten=round(row[6]+row[7]+row[8]+row[9],2),\
          btotaal=round(row[2],2), wtotaal=round(row[3]+row[4]+row[5]+row[6]+row[7]+row[8]\
          +row[9]+row[17]+row[18]+row[19]+row[20],2),betaald_bedrag=round(row[13],2),\
          meerminderwerk=round(row[10],2), onderhandenwerk=round(row[3]+row[4]+row[5]+\
          row[6]+row[7]+row[8]+row[9]+row[10]+row[17]+row[18]+row[19]+row[20]-row[13],2),\
          bruto_winst = round(mwinst,2), boekweek = jrwk, aanneemsom = round(row[2],2))
        con.execute(insres)

def bereken(m_email):
    jrwk = jaarweek()
    jr = jrwk[0:4]
    metadata = MetaData()
    resultaten = Table('resultaten', metadata,
        Column('resID', Integer(), primary_key=True),
        Column('boekweek', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selc = select([resultaten]).where(resultaten.c.boekweek == jrwk)
    rpc = con.execute(selc).first()
    if rpc:
        berBestaat(jrwk, m_email)
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
     
    sel = select([werken]).where(werken.c.statusweek.like(jr+'%')).order_by(werken.c.statusweek)
    if con.execute(sel).first():
        rpwerken = con.execute(sel)
    else:
        geenGegevens()
        hoofdMenu(m_email)
         
    msomA,msomB,msomC,msomD,msomE,msomF,msomG,msomH,mkosttot,mbetaald,mmeerwerk = (0,)*11
    mkostB,mkostC,mkostD,mkostE,mkostF,mkostG,mkostH = (0,)*7
    mwinstC, mwinstD, mwinstE, mwinstF, mwinstG, mwinstH = (0,)*6
    mohwC, mohwD, mohwE, mohwF, mohwG, mohwH = (0,)*6
    maantA,maantB,maantC,maantD,maantE,maantF,maantG,maantH = (0,)*8
    mbetaaldB, mbetaaldC, mbetaaldD, mbetaaldE, mbetaaldF, mbetaaldG, mbetaaldH = (0,)*7
    mmeerwB, mmeerwC, mmeerwD, mmeerwE, mmeerwF, mmeerwG, mmeerwH = (0,)*7
    for row in rpwerken:
        #mwerknr = row[0]
        #mwerkomschr = row[1]
        mktotal=row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[17]+row[18]+row[19]+row[20]
        mmeerwerk = mmeerwerk+row[10]
        mkosttot = mkosttot+mktotal
        mbetaald = mbetaald+row[13]
        mvgangst = row[11]
        if mvgangst == 'A' and row[12][0:4] == jaarweek()[0:4]:
            msomA = msomA+row[2]
            maantA = maantA+1
        elif mvgangst == 'B':
            msomB = msomB+row[2]
            mkostB = mkostB+row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            maantB = maantB+1
            mbetaaldB = mbetaaldB+row[13]
            mmeerwB = mmeerwB+row[10]
        elif mvgangst == 'C' and row[12][0:4] == jaarweek()[0:4]:
            msomC = msomC+row[2]
            mkostC = mkostC+row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            maantC = maantC+1
            mbetaaldC = mbetaaldC+row[13]
            mmeerwC = mmeerwC+row[10]
            mmeerwerk = mmeerwerk+row[10]
            mwinstC = mwinstC+row[2]/3-mkostC
            mohwC =  mohwC+mkostC-mbetaaldC
        elif mvgangst == 'D' and row[12][0:4] == jaarweek()[0:4]:
            msomD = msomD+row[2]
            mkostD = row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            mkostD += mkostD
            maantD = maantD+1
            mbetaaldD += mbetaaldD+row[13]
            mmeerwD += mmeerwD+row[10]
            mwinstD = mwinstD+row[2]/3-mkostD
            mohwD =  mohwD+mkostD-mbetaaldD
        elif mvgangst == 'E' and row[12][0:4] == jaarweek()[0:4]:
            msomE = msomE+row[2]
            mkostE = mkostE+row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            maantE = maantE+1
            mbetaaldE += mbetaaldE+row[13]
            mmeerwE += mmeerwE+row[10]
            mwinstE = mwinstE+row[2]*2/3-mkostE
            mohwE =  mohwE+mkostE-mbetaaldE
        elif mvgangst == 'F' and row[12][0:4] == jaarweek()[0:4]:
            msomF = msomF+row[2]
            mkostF = mkostF+row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            maantF = maantF+1
            mbetaaldF += mbetaaldF+row[13]
            mmeerwF += mmeerwF+row[10]
            mwinstF = mwinstF+row[2]*.8666-mkostF
            mohwF =  mohwF+mkostF-mbetaaldF
        elif mvgangst == 'G' and row[12][0:4] == jaarweek()[0:4]:
            msomG = msomG+row[2]
            mkostG = mkostG+row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            maantG = maantG+1
            mbetaaldG += mbetaaldG+row[13]
            mmeerwG += mmeerwG+row[10]
            mwinstG= mwinstG+row[2]-mkostG
            mohwG =  mohwG+mkostG-mbetaaldG
        elif mvgangst == 'H' and row[12][0:4] == jaarweek()[0:4]:
            msomH = msomH+row[2]
            mkostH = mkostH+row[3]+row[4]+row[5]+row[6]+row[7]+row[8]+row[9]+row[10]+\
                row[17]+row[18]+row[19]+row[20]
            maantH = maantH+1
            mbetaaldH += mbetaaldH+row[13]
            mmeerwH = mmeerwH+row[10]
            mwinstH = mwinstH+row[2]+mmeerwH-mkostH
            mohwH =  mohwH+mkostH-mbetaaldH
            
        divBereken(row)
   
    metadata = MetaData()      
    resultaten_status = Table('resultaten_status', metadata,
        Column('rID', Integer, primary_key=True),
        Column('status', String),
        Column('aanneemsom', Float),
        Column('kosten', Float),
        Column('aantal', Integer),
        Column('boekweek', String),
        Column('betaald', Float),
        Column('meerminderwerk', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selr = select([resultaten_status]).where(resultaten_status.c.boekweek == jrwk)
    rpr = con.execute(selr).first()
    
    if not rpr: 
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
             type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'A',\
            aanneemsom = round(msomA,2), aantal = maantA, boekweek = jrwk)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
              type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'B',\
            aanneemsom = round(msomB,2), kosten = round(mkostB,2), aantal = maantB,\
            betaald = mbetaaldB, boekweek = jrwk, meerminderwerk = mmeerwB)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
               type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'C',\
            aanneemsom = round(msomC,2), kosten = round(mkostC,2), aantal = maantC,\
            betaald = mbetaaldC, boekweek = jrwk, meerminderwerk = mmeerwC)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
              type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'D',\
            aanneemsom = round(msomD,2), kosten = round(mkostD,2), aantal = maantD,\
            betaald = mbetaaldD, boekweek = jrwk, meerminderwerk = mmeerwD)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
               type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'E',\
            aanneemsom = round(msomE,2), kosten = round(mkostE,2), aantal = maantE,\
            betaald = mbetaaldE, boekweek = jrwk, meerminderwerk = mmeerwE)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
              type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'F',\
            aanneemsom = round(msomF,2), kosten = round(mkostF,2), aantal = maantF,\
            betaald = mbetaaldF, boekweek = jrwk, meerminderwerk = mmeerwF)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
               type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'G',\
            aanneemsom = round(msomG,2), kosten = round(mkostG,2), aantal = maantG,\
            betaald = mbetaaldG, boekweek = jrwk, meerminderwerk = mmeerwG)
        con.execute(insres)
        try:
            mrnr = (con.execute(select([func.max(resultaten_status.c.rID,\
               type_=Integer)])).scalar())
            mrnr += 1
        except:
            mrnr = 1
        insres = insert(resultaten_status).values(rID = mrnr, status = 'H',\
            aanneemsom = round(msomH,2), kosten = round(mkostH,2), aantal = maantH,\
            betaald = mbetaaldH, boekweek = jrwk, meerminderwerk = mmeerwH)
        con.execute(insres)
        berGelukt() 
        hoofdMenu(m_email)
