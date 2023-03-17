import os, sys
from math import sqrt
import datetime
from PyQt5.QtWidgets import QApplication
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, create_engine,\
    insert, select, update, func, Boolean

# set lock for up to 1 session per PC

home = os.path.expanduser("~")
if os.path.isfile(str(home)+'/.pandora_lock'):
    sys.exit()
else:
    open(str(home)+'/.pandora_lock', 'w')
    
# following rules for annual consumption of items even/odd year per year
# and calculate warehouse inventory value for charts per month

metadata = MetaData()
artikelen = Table('artikelen', metadata,
    Column('artikelID', Integer(), primary_key=True),
    Column('artikelprijs', Float),
    Column('art_voorraad', Float),
    Column('mutatiedatum', String),
    Column('jaarverbruik_1', Float),
    Column('jaarverbruik_2', Float),
    Column('art_min_voorraad', Float),
    Column('bestelsaldo', Float),
    Column('bestelstatus', Boolean),
    Column('reserveringsaldo', Float),
    Column('categorie', Integer),
    Column('art_bestelgrootte', Float))
params = Table('params', metadata,
    Column('paramID', Integer, primary_key=True),
    Column('tarief', Float))
magazijnvoorraad = Table('magazijnvoorraad', metadata,\
    Column('jaarmaand', String, primary_key=True),
    Column('totaal', Float),
    Column('courant', Float),                     
    Column('incourant', Float))
          
engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()

mjaar = int(str(datetime.date.today())[0:4])
selpar = select([params]).where(params.c.paramID == 99)
rppar = con.execute(selpar).first()
updeven = update(params).where(params.c.paramID == 99).values(tarief = int(mjaar%2))
con.execute(updeven)

selpar = select([params]).where(params.c.paramID == 99)
rppar = con.execute(selpar).first()

if mjaar%2 == 1 and int(rppar[1]) == 0:
    updpar = update(params).where(params.c.paramID == 99).values(tarief = 1)
    con.execute(updpar)
    selpar2 = select([params]).where(params.c.paramID == 101)
    rppar2 = con.execute(selpar2).first()
    selart = select([artikelen]).order_by(artikelen.c.artikelID)
    rpartikel = con.execute(selart)
    selpar1 = select([params]).where(params.c.paramID == 6)
    rppar1 = con.execute(selpar1).first()
            
    for row in rpartikel:
        mjaar = int(str(datetime.datetime.now())[0:4])
        mbestgr = round(sqrt(2*row[5]*rppar2[1])/(row[1]*rppar[1]),0)
        mjrverbr = row[4]
        if row[10] == 1 or row[10] == 5:
            minvrd = round(mjrverbr*1/17, 0) # < 3 weeks delivery time
        elif row[10] == 2 or row[10] == 6 or row[10] == 7 :
            minvrd = round(mjrverbr*4/17, 0) # < 12 weeks delivery time
        elif row[10] == 3 or row[10] == 8:
            minvrd = round(mjrverbr*8/17, 0) # < 26 weeks delivery time
        elif row[10] == 4 or row[10] == 9: 
            minvrd = round(mjrverbr*16/17,0) # < 52 weeks delivery time
        updart = update(artikelen).where(artikelen.c.artikelID == row[0]).\
            values(jaarverbruik_2 = 0, art_min_voorraad = minvrd, art_bestelgrootte = mbestgr)
        con.execute(updart)
elif mjaar%2 == 0 and int(rppar[1]) == 1:
    updpar = update(params).where(params.c.paramID == 99).values(tarief = 0)
    con.execute(updpar)
    selpar2 = select([params]).where(params.c.paramID == 101)
    rppar2 = con.execute(selpar2).first()
    selart = select([artikelen]).order_by(artikelen.c.artikelID)
    rpartikel = con.execute(selart)
    selpar1 = select([params]).where(params.c.paramID == 6)
    rppar1 = con.execute(selpar1).first()

    for row in rpartikel:
        mjaar = int(str(datetime.datetime.now())[0:4])
        mbestgr = round(sqrt(2*row[4]*rppar2[1])/(row[1]*rppar1[1]),0)
        mjrverbr = row[5]
        mjrverbr = 0
        if row[10] == 1 or row[10] == 5:
            minvrd = round(mjrverbr*1/17, 0) # < 3 weeks delivery time
        elif row[10] == 2 or row[10] == 6 or row[10] == 7 :
            minvrd = round(mjrverbr*4/17, 0) # < 12 weeks delivery time
        elif row[10] == 3 or row[10] == 8: 
            minvrd = round(mjrverbr*8/17, 0) # < 26 weeks delivery time
        elif row[10] == 4 or row[10] == 9: 
            minvrd = round(mjrverbr*16/17,0) # < 52 weeks delivery time
       
        updart = update(artikelen).where(artikelen.c.artikelID == row[0]).\
            values(jaarverbruik_1 = 0, art_min_voorraad = minvrd, art_bestelgrootte = mbestgr)
        con.execute(updart)
    
mhjrmnd = str(datetime.date.today())[0:7]                                                  #(this year year-month) yyyy-mm
mvjrmnd = int(str(int(str(datetime.date.today())[0:4])-1)+str(datetime.date.today())[5:7]) #(last year yearmonth) yyyymm
mdbjrmnd = (con.execute(select([func.max(magazijnvoorraad.c.jaarmaand,\
                    type_=Integer)])).scalar())     #(last stored year-month) yyyy-mm
if mhjrmnd != mdbjrmnd:
    insdb = insert(magazijnvoorraad).values(jaarmaand = mhjrmnd)
    con.execute(insdb)
    selart = select([artikelen])
    rpart = con.execute(selart)
    mtotaal = 0
    mcourant = 0
    mincourant = 0
    for row in rpart:      
        mtotaal = mtotaal + row[1]*row[2]                       # total value of stock
        if mvjrmnd < int(str(row[3][0:4])+str(row[3])[5:7]):    # see if last transaction less than a year ago
            mcourant = mcourant + row[1]*row[2]
        else:
            mincourant = mincourant + row[1]*row[2]             # last transaction more than a year ago
    updmvrd = update(magazijnvoorraad).where(magazijnvoorraad.c.jaarmaand == mhjrmnd)\
          .values(totaal = int(mtotaal), courant = int(mcourant), incourant = int(mincourant)) 
    # write totals in present year-month
    con.execute(updmvrd)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    if sys.platform == "linux":
        os.system("../.usbkbd.sh")
    from login import inlog
    inlog()
    app.exec_()