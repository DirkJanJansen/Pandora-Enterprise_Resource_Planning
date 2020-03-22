from login import hoofdMenu
import  datetime
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        MetaData, create_engine, ForeignKey, select, update)

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def invoerOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Wijzigen van verkoop_uurtarieven gelukt!')
    msg.setWindowTitle('UURTARIEVEN')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
      
def winKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            msg = QMessageBox.question(self, 'Verkoop-uurtarieven aanpassen',\
             "Verkoop-uurtarieven aanpassen?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.No:
                windowSluit(self, m_email)
                winKeuze(m_email)
            metadata = MetaData()  
            params = Table('params', metadata,
                Column('paramID', Integer(), primary_key=True),
                Column('item', String),
                Column('tarief', Float),
                Column('verrekening', String),
                Column('ondergrens', Float),
                Column('bovengrens', Float),
                Column('datum', String),
                Column('lock', Boolean),
                Column('loonID', None, ForeignKey('lonen.loonID')),
                Column('reisuur', Float),
                Column('tarieffactor', Float))
            lonen = Table('lonen', metadata,
                Column('loonID', Integer(), primary_key=True),
                Column('tabelloon', Float),
                Column('werkuur',Float),
                Column('reisuur', Float),
                Column('direct', Boolean),
                Column('maandloon', Float),
                Column('functieomschr', String),
                Column('boekdatum', String))
                                  
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params,lonen]).where(params.c.loonID == lonen.c.loonID).order_by(lonen.c.loonID)
            rppar = con.execute(selpar)
            mboekd = str(datetime.datetime.now())[0:10] 
            for row in rppar:
                updpar = update(params).where(params.c.loonID == row[8]).values(tarief = row[12]*row[10],\
                          datum = mboekd, reisuur = row[12]/3)
                con.execute(updpar)
                updlon = update(lonen).where(lonen.c.loonID == row[11]).values(werkuur = row[2])
                con.execute(updlon)
                updlon = update(lonen).where(lonen.c.loonID == row[11]-1).values(werkuur = row[2])
                con.execute(updlon)
                updlon = update(lonen).where(lonen.c.loonID == row[11]-2).values(werkuur = row[2])
                con.execute(updlon)
                if row[0] < 37:
                    updlon = update(lonen).where(lonen.c.loonID == row[11]-3).values(werkuur = row[2])
                    con.execute(updlon) 
            invoerOK()
            windowSluit(self, m_email)
    window = Widget()
    window.show()   
