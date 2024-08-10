import datetime, sys
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine,\
                     Float, update
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication

def odd_even(message):
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle('Reset parameter')
    msg.exec_()

try:
    metadata = MetaData()
    params_system = Table('params_system', metadata,
           Column('systemID', Integer(), primary_key=True),
           Column('item', String),
           Column('system_value', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    mjaar = int(str(datetime.date.today())[0:4])
    updeven = update(params_system).where(params_system.c.systemID == 3).values(system_value = int(mjaar%2))
    con.execute(updeven)
    message = "Reset parameter successful!"
except Exception as e:
    message = "Reset parameter failed!\n"+str(e)
app = QApplication(sys.argv)
app.setStyle("Windows")
sys.exit(odd_even(message))
app.exec_()



