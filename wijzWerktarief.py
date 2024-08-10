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
    msg.setText('Change sales hourly rates succeeded!')
    msg.setWindowTitle('Hourly rates')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
      
def winKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            msg = QMessageBox.question(self, 'Change sales hourly rates',\
             "Modify sales hourly rates?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.No:
                windowSluit(self, m_email)
                winKeuze(m_email)
            metadata = MetaData()
            params_hours = Table('params_hours', metadata,
                Column('rateID', Integer(), primary_key=True),
                Column('item', String),
                Column('hourly_tariff', Float),
                Column('wageID', None, ForeignKey('lonen.loonID')),
                Column('travel_time', Float),
                Column('overhead_factor', Float),
                Column('date', String))
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
            selpar = select([params_hours,lonen]).where(params_hours.c.rateID == lonen.c.loonID).order_by(lonen.c.loonID)
            rppar = con.execute(selpar)
            mboekd = str(datetime.datetime.now())[0:10]
            for row in rppar:
                updpar = update(params_hours).where(params_hours.c.rateID == row[3]).values(hourly_tariff = row[8]*row[5],\
                          date = mboekd, travel_time = row[8]/3)
                con.execute(updpar)
                updlon = update(lonen).where(lonen.c.loonID == row[7]).values(werkuur = row[2])
                con.execute(updlon)
                updlon = update(lonen).where(lonen.c.loonID == row[7]-1).values(werkuur = row[2])
                con.execute(updlon)
                updlon = update(lonen).where(lonen.c.loonID == row[7]-2).values(werkuur = row[2])
                con.execute(updlon)
                if row[0] < 37:
                    updlon = update(lonen).where(lonen.c.loonID == row[7]-3).values(werkuur = row[2])
                    con.execute(updlon) 
            invoerOK()
            windowSluit(self, m_email)

    window = Widget()
    window.show()   
