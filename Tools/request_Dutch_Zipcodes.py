
import sys
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import  QDialog, QTableView, QWidget, QVBoxLayout, QApplication
from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, Boolean, MetaData, select, and_

def zipcode():
    metadata = MetaData()
    postcodes = Table('postcodes', metadata,
       Column('postcode', String),
       Column('soort', Boolean),
       Column('van', Integer),
       Column('tem', Integer),
       Column('straatID', None, ForeignKey('straat.straatID')))
    plaats = Table('plaats', MetaData(),
       Column('plaatsID', Integer, primary_key=True),
       Column('c_plaats', String))
    straat = Table('straat', MetaData(),
       Column('straatID', Integer, primary_key=True),
       Column('c_straat', String),
       Column('plaatsID', None, ForeignKey('plaats.plaatsID')))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selzip= select(postcodes.c.postcode, straat.c.c_straat,postcodes.c.van,postcodes.c.tem, plaats.c.c_plaats)\
        .where(and_(postcodes.c.straatID == straat.c.straatID, straat.c.plaatsID == plaats.c.plaatsID))
    rpzip = con.execute(selzip)

    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args, )
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Request own sales company')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setColumnWidth(0, 100)
            table_view.setColumnWidth(1, 300)
            table_view.setColumnWidth(4, 300)
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header

        def rowCount(self, parent):
            return len(self.mylist)

        def columnCount(self, parent):
           return len(self.mylist[0])

        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld

        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None

    header = ['Zipcode', 'Streetname','Lowernr', 'Uppernr', 'Residence']

    data_list = []
    for row in rpzip:
        data_list += [row]

    win = MyWindow(data_list, header)
    win.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    zipcode()
    app.exec_()
    sys.exit()