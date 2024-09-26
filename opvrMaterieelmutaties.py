from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QVBoxLayout, \
    QComboBox, QDialog, QLineEdit, QMessageBox, QTableView
from sqlalchemy import (Table, Column, Integer, Boolean,  Float, String, MetaData, ForeignKey, \
                        create_engine, select, and_)

metadata = MetaData()
materieelmutaties = Table('materieelmutaties', metadata,
    Column('mutatieID', Integer(), primary_key=True),
    Column('werknummerID', None, ForeignKey('werken.werknummerID')),
    Column('servicesID', None, ForeignKey('params_services.servicesID')),
    Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
    Column('orderinkoopID', None, ForeignKey('orders_inkoop_materieel.orderinkoopID')),
    Column('order_inkoop_materieelID', None, ForeignKey('orders_inkoop_materieel.order_inkoop_materieelID')),
    Column('uren_geboekt', Float),
    Column('boekbedrag', Float),
    Column('boekdatum', String),
    Column('meerwerkstatus', Boolean))
orders_inkoop_materieel = Table('orders_inkoop_materieel', metadata,
    Column('order_inkoop_materieelID', Integer, primary_key=True),
    Column('werknummerID', None, ForeignKey('werken.werknummerID')),
    Column('servicesID', None, ForeignKey('params_services.servicesID')),
    Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
    Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
    Column('uren_opdracht', Float))
werken = Table('werken', metadata,
    Column('werknummerID', Integer(), primary_key=True),
    Column('werkomschrijving', String(50)))
orders_inkoop = Table('orders_inkoop', metadata,
   Column('orderinkoopID', Integer, primary_key=True),
   Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')))
leveranciers = Table('leveranciers', metadata,
  Column('leverancierID', Integer, primary_key=True),
  Column('bedrijfsnaam', String),
  Column('rechtsvorm', String))
params_services = Table('params_services', metadata,
    Column('servicesID', Integer(), primary_key=True),
    Column('hourly_tariff', Float),
    Column('overhead_factor', Float),
    Column('item', String))

engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
conn = engine.connect()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record found\ncreate another selection please!')
    msg.setWindowTitle('Request services / Equipment')
    msg.exec_()

def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Please re-enter incorrect input\nsearch term!')
    msg.setWindowTitle('Request services / Equipment')
    msg.exec_()


def mutatieKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Search term request equipment hours mutations")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))

            self.setFont(QFont('Arial', 10))

            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(230)
            k0Edit.setFont(QFont("Arial", 10))
            k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            k0Edit.addItem('      Search sort key')
            k0Edit.addItem('1. All mutations')
            k0Edit.addItem('2. By work number')
            k0Edit.addItem('3. By work description')
            k0Edit.addItem('4. By supplier number')
            k0Edit.addItem('5. By supplier name')
            k0Edit.addItem('6. By purchase order')
            k0Edit.addItem('7. By equipment type (1-12)')
            k0Edit.addItem('8. By booking date yyyy(-mm(-dd))')
            k0Edit.activated[str].connect(self.k0Changed)

            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(230)
            zktermEdit.setFont(QFont("Arial", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)

            grid = QGridLayout()
            grid.setSpacing(20)

            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0, 1, 2)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 0, 1, 1, 1, Qt.AlignRight)

            grid.addWidget(k0Edit, 1, 1)
            lbl1 = QLabel('Search term')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)

            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)

            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(self.accept)

            grid.addWidget(applyBtn, 3, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))

            grid.addWidget(cancelBtn, 3, 1)
            cancelBtn.setFont(QFont("Arial", 10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

        def k0Changed(self, text):
            self.Keuze.setText(text)

        def zktermChanged(self, text):
            self.Zoekterm.setText(text)

        def returnk0(self):
            return self.Keuze.text()

        def returnzkterm(self):
            return self.Zoekterm.text()

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnzkterm()]

    window = Widget()
    data = window.getData()
    if data[0]:
        keuze = int(data[0][0])
    else:
        ongInvoer()
        mutatieKeuze(m_email)
    if data[1]:
        zoekterm = data[1]
    else:
        zoekterm = ''
    toonMutaties(keuze, zoekterm, m_email)

def toonMutaties(keuze, zoekterm, m_email):
    import validZt
    if keuze == 1:
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID)) \
            .order_by(werken.c.werknummerID)
    elif keuze == 2 and validZt.zt(zoekterm, 8):
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        werken.c.werknummerID == int(zoekterm)))
    elif keuze == 3:
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        werken.c.werkomschrijving.ilike('%' + zoekterm + '%'))) \
            .order_by(werken.c.werknummerID)
    elif keuze == 4 and validZt.zt(zoekterm, 3):
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        leveranciers.c.leverancierID == int(zoekterm)))
    elif keuze == 5:
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        leveranciers.c.bedrijfsnaam.ilike('%' + zoekterm + '%')))
    elif keuze == 6 and validZt.zt(zoekterm, 5):
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        orders_inkoop.c.orderinkoopID == int(zoekterm)))
    elif keuze == 7 and validZt.zt(zoekterm, 16):
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        materieelmutaties.c.servicesID == int(zoekterm))).order_by(materieelmutaties.c.servicesID)
    elif keuze == 8 and validZt.zt(zoekterm, 10):
        sel = select([materieelmutaties, orders_inkoop_materieel, werken, leveranciers]) \
            .where(and_(werken.c.werknummerID == materieelmutaties.c.werknummerID, \
                        leveranciers.c.leverancierID == materieelmutaties.c.leverancierID, \
                        orders_inkoop_materieel.c.orderinkoopID == materieelmutaties.c.orderinkoopID, \
                        materieelmutaties.c.boekdatum.ilike(zoekterm + '%'))).order_by(materieelmutaties.c.boekdatum)
    else:
        ongInvoer()
        mutatieKeuze(m_email)

    try:
        rp = conn.execute(sel)
    except Exception as e:
        geenRecord()
        mutatieKeuze(m_email)

    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args, )
            self.setGeometry(10, 50, 1900, 900)
            self.setWindowTitle('Request equipment mutations')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setColumnHidden(1, True)
            table_view.setColumnHidden(5, True)
            table_view.setColumnHidden(10, True)
            table_view.setColumnHidden(11, True)
            table_view.setColumnHidden(12, True)
            table_view.setColumnHidden(13, True)
            table_view.setColumnHidden(14, True)
            #table_view.clicked.connect(showAccount)
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
            try:
                return len(self.mylist[0])
            except:
                return 0

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

    eqlist = ['Trench machine','Pressing machine','Atlas crane','Crane big','Main liner','Ballast scraper',\
             'Wagon','Loco motor','Locomotive','Assemble Trolley','Stor mobile','Robel train']

    header = ['MutationID', '', 'EquipmentID', 'Equipment name', 'OrderPurchaseID', '','Booked hours', 'Amount booking',\
              'Booking date', 'More/less work','', '','', '', '', 'Assignment hours','Work number', 'Work description',\
              'SupplierID', 'Company name', 'Legal status']

    data_list = []
    for row in rp:
        data_list += [(row[0],row[1],row[2],eqlist[row[2]],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],\
                       row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20])]

    win = MyWindow(data_list, header)
    win.exec_()

    mutatieKeuze(m_email)