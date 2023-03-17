import datetime, sys
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine,\
                     Float, update
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication

def odd_even():
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Reset parameter successful!')
    msg.setWindowTitle('Reset parameter')
    msg.exec_()

metadata = MetaData()
params = Table('params', metadata,
       Column('paramID', Integer(), primary_key=True),
       Column('item', String),
       Column('tarief', Float))

engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()

mjaar = int(str(datetime.date.today())[0:4])
updeven = update(params).where(params.c.paramID == 99).values(tarief = int(mjaar%2))
con.execute(updeven)
app = QApplication(sys.argv)
app.setStyle("Windows")
sys.exit(odd_even())
app.exec_()



