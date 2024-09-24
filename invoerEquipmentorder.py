from login import hoofdMenu
import datetime, os
from PyQt5.QtWidgets import (QLabel, QLineEdit, QGridLayout, QPushButton,
                QDialog, QMessageBox ,QComboBox, QTableView, QWidget)
from PyQt5.QtGui import (QRegExpValidator, QFont, QPixmap, QIcon, QColor, QMovie)
from PyQt5.QtCore import (Qt, QRegExp, QAbstractTableModel, QSize)
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey,
                        MetaData, create_engine, select, update, insert, and_, func)

metadata = MetaData()
orders_inkoop = Table('orders_inkoop', metadata,
    Column('orderinkoopID', Integer, primary_key=True),
    Column('besteldatum', String),
    Column('goedgekeurd', String),
    Column('afgemeld', String),
    Column('betaald', String),
    Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
    Column('status', Integer),
    Column('betaald_bedrag', Float))
orders_inkoop_materieel = Table('orders_inkoop_materieel', metadata,
    Column('order_inkoop_materieelID', Integer, primary_key=True),
    Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
    Column('werknummerID', None, ForeignKey('werken.werknummerID')),
    Column('werk_omschr', String),
    Column('uren_opdracht', Float),
    Column('uurtarief', Float),
    Column('bedrag_opdracht', Float),
    Column('plan_start', String),
    Column('werk_start', String),
    Column('plan_gereed', String),
    Column('werk_gereed', String),
    Column('status', Integer),
    Column('servicesID', None, ForeignKey('params_services.serviceID')),
    Column('services_omschr', String),
    Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
    Column('datum_opdracht', String))
calculaties = Table('calculaties', metadata,
    Column('sleuvengraver', Float),
    Column('persapparaat', Float),
    Column('atlaskraan', Float),
    Column('kraan_groot', Float),
    Column('mainliner', Float),
    Column('hormachine', Float),
    Column('wagon', Float),
    Column('locomotor', Float),
    Column('locomotief', Float),
    Column('montagewagen', Float),
    Column('stormobiel', Float),
    Column('robeltrein', Float),
    Column('calcID', Integer(), primary_key=True),
    Column('koppelnummer', Integer),
    Column('verwerkt', Integer),
    Column('omschrijving', String),
    Column('werkomschrijving', String),
    Column('hoeveelheid', Float),
    Column('clusterID', Integer),
    Column('eenheid', String))
params_services = Table('params_services', metadata,
    Column('servicesID', Integer, primary_key=True),
    Column('hourly_tariff', Float),
    Column('item', String))
werken = Table('werken', metadata,
    Column('werknummerID', Integer(), primary_key=True),
    Column('werkomschrijving', String(50)),
    Column('voortgangstatus', String(1)),
    Column('statusweek', String(6)),
    Column('aanneemsom', Float),
    Column('begr_materialen', Float),
    Column('begr_materieel', Float),
    Column('kosten_materieel', Float),
    Column('startweek', String),
    Column('betaald_bedrag', Float),
    Column('meerminderwerk', Float),
    Column('opdracht_datum', String),
    Column('werk_sleuvengraver_uren', Float),
    Column('werk_persapparaat_uren', Float),
    Column('werk_atlaskraan_uren', Float),
    Column('werk_kraan_groot_uren', Float),
    Column('werk_mainliner_uren', Float),
    Column('werk_hormachine_uren', Float),
    Column('werk_wagon_uren', Float),
    Column('werk_locomotor_uren', Float),
    Column('werk_locomotief_uren', Float),
    Column('werk_montagewagen_uren', Float),
    Column('werk_stormobiel_uren',Float),
    Column('werk_robeltrein_uren', Float))
leveranciers = Table('leveranciers', metadata,
    Column('leverancierID', Integer(), primary_key=True),
    Column('bedrijfsnaam', String),
    Column('rechtsvorm', String),
    Column('btwnummer', String),
    Column('kvknummer', String),
    Column('telnr', String),
    Column('postcode', String),
    Column('huisnummer', String),
    Column('toevoeging', String))

def _11check(mwerknr):
    number = str(mwerknr)
    total = 0
    fullnumber = number
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total % 11 % 10
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def noRecords():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No items found for the given selection!')
    msg.setWindowTitle('Purchase orders equipment')
    msg.exec_()

def foutInvoer():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No required input. Re-enter data!')
    msg.setWindowTitle('Purchase orders equipment')
    msg.exec_()

def foutWerknr():
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Incorrect worknumber!')
    msg.setWindowTitle('Purchase orders equipment')
    msg.exec_()

def  reservDone(message):
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle('Order-reservations for equipment')
    msg.exec_()

def wijzigOK(ordernr):
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Changing order '+str(ordernr)+' was successful!')
    msg.setWindowTitle('Order-reservations for equipment')
    msg.exec_()

def orderingOK(message):
    msg = QMessageBox()
    msg.setFont(QFont("Arial", 10))
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle('Ordering equipment')
    msg.exec_()

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Wait printing starts')
    msg.setWindowTitle('Print Equipment orders')
    msg.exec_()

def printOrder(ordernr):
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selprint = select([orders_inkoop_materieel, leveranciers]).where(orders_inkoop_materieel.c.orderinkoopID == ordernr, \
                                    leveranciers.c.leverancierID == orders_inkoop_materieel.c.leverancierID)
    rpprint = con.execute(selprint).first()
    from postcode import checkpostcode
    street, residence = checkpostcode(rpprint[22], int(rpprint[23]))
    rgl = 0
    kop=\
     ('Order number: '+ str(rpprint[1])+'          Order date: '+str(rpprint[15])+'\n'+
     '==============================================================================================\n'+
     'Ordernumber Equipment      Worknr.   Description work        Hours  Rate Start      Finish    \n'+
     '==============================================================================================\n')
    from sys import platform
    if platform == 'win32':
        filename = '.\\forms\\Equipment_Orders\\EquipmentOrder_' + str(rpprint[1]) + '.txt'
    else:
        filename = './forms/Equipment_Orders/EquipmentOrder_' + str(rpprint[1]) + '.txt'
    adreskop = \
        ('\n\n\n\n\n\n\nOrder\n\n' + rpprint[17] + ' ' + rpprint[18] + ',\n' + \
         street + ' ' + rpprint[23] + rpprint[24] + ',\n' + \
         rpprint[22] + ' ' + residence + '.\n\n\n\n\n')
    open(filename, 'w').write(adreskop)
    mtotaal = 0
    if rgl == 0:
        rgl = 16
    open(filename, 'a').write(kop)

    msub = rpprint[4] * rpprint[5]
    open(filename, 'a').write('{:<12d}'.format(rpprint[1]) + '{:<2d}'.format(rpprint[12]) + '{:<12s}'.format(rpprint[13]) + ' ' +  '{:<10d}'.format(rpprint[2]) + '{:<20s}'.format(rpprint[3]) + \
    ' ' + '{:>8.2f}'.format(rpprint[4]) + ' ' + '{:>3.2f}'.format(rpprint[5]) + ' ' + '{:<6s}'.format(rpprint[7])+' '+'{:>6s}'.format(rpprint[9]) + '\n')
    mtotaal = mtotaal + msub
    rgl += 1

    tail = ( \
       '----------------------------------------------------------------------------------------------\n' +
       'Total  order assignment excluding VAT :' + '{:10.2f}'.format(mtotaal) + ' \n' +
       '==============================================================================================\n')
    open(filename, 'a').write(tail)

    from sys import platform
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr " + filename)
    printing()

def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11 % 10
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def calKeuze(m_email, auth1, auth2, auth3):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Purchase orders equipment")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))

            self.setFont(QFont('Arial', 10))

            grid = QGridLayout()
            grid.setSpacing(20)

            # Choice
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(380)
            self.k0Edit.setFont(QFont("Arial", 10))
            self.k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k0Edit.setCurrentIndex(0)
            self.k0Edit.addItem('  Choose   ')
            self.k0Edit.setEditable(True)
            self.k0Edit.lineEdit().setFont(QFont("Arial", 10))
            self.k0Edit.lineEdit().setReadOnly(True)
            self.k0Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k0Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k0Edit.addItem('1. Reservation orders')
            self.k0Edit.addItem('2. Ordering / Modify orders')
            self.k0Edit.addItem('3. Request reserved orders by worknumber')
            self.k0Edit.addItem('4. Request ordered orders by worknumber')
            self.k0Edit.addItem('5. Request ready orders by worknumber')
            self.k0Edit.addItem('6. Request payed orders by worknumber')
            self.k0Edit.addItem('7. Request closed orders by worknumber')
            self.k0Edit.addItem('8. Request all orders sorted by worknumber')

            if auth1:
                self.k0Edit.model().item(1).setEnabled(True)
                self.k0Edit.model().item(2).setEnabled(True)
                self.k0Edit.model().item(3).setEnabled(True)
                self.k0Edit.model().item(4).setEnabled(True)
                self.k0Edit.model().item(5).setEnabled(True)
                self.k0Edit.model().item(6).setEnabled(True)
                self.k0Edit.model().item(7).setEnabled(True)
                self.k0Edit.model().item(8).setEnabled(True)
            elif auth2:
                self.k0Edit.model().item(1).setEnabled(False)
                self.k0Edit.model().item(1).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(1).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(2).setEnabled(True)
                self.k0Edit.model().item(3).setEnabled(True)
                self.k0Edit.model().item(4).setEnabled(True)
                self.k0Edit.model().item(5).setEnabled(True)
                self.k0Edit.model().item(6).setEnabled(True)
                self.k0Edit.model().item(7).setEnabled(True)
                self.k0Edit.model().item(8).setEnabled(True)
            elif auth3:
                self.k0Edit.model().item(1).setEnabled(False)
                self.k0Edit.model().item(1).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(1).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(2).setEnabled(False)
                self.k0Edit.model().item(2).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(2).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(3).setEnabled(True)
                self.k0Edit.model().item(4).setEnabled(True)
                self.k0Edit.model().item(5).setEnabled(True)
                self.k0Edit.model().item(6).setEnabled(True)
                self.k0Edit.model().item(7).setEnabled(True)
                self.k0Edit.model().item(8).setEnabled(True)
            else:
                self.k0Edit.model().item(1).setEnabled(False)
                self.k0Edit.model().item(1).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(1).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(2).setEnabled(False)
                self.k0Edit.model().item(2).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(2).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(3).setEnabled(False)
                self.k0Edit.model().item(3).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(3).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(4).setEnabled(False)
                self.k0Edit.model().item(4).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(4).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(5).setEnabled(False)
                self.k0Edit.model().item(5).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(5).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(6).setEnabled(False)
                self.k0Edit.model().item(6).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(6).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(7).setEnabled(False)
                self.k0Edit.model().item(7).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(7).setBackground(QColor('gainsboro'))
                self.k0Edit.model().item(8).setEnabled(False)
                self.k0Edit.model().item(8).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(8).setBackground(QColor('gainsboro'))

            # Worknumber
            self.werknrEdit = QLineEdit('8')
            self.werknrEdit.setFixedWidth(100)
            self.werknrEdit.setFont(QFont("Arial", 10))
            self.werknrEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[8]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, self.werknrEdit)
            self.werknrEdit.setValidator(input_validator)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(180, 60))
            movie.start()
            grid.addWidget(pyqt, 1, 0, 1, 2)

            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)

            def werknrChanged():
                self.werknrEdit.setText(self.werknrEdit.text())
            self.werknrEdit.textChanged.connect(werknrChanged)

            grid.addWidget(self.k0Edit, 2, 1)
            lbl1 = QLabel('Worknumber')
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(self.werknrEdit, 3, 1)

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 7, 0, 1, 2, Qt.AlignCenter)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 1, 1, 1, 1, Qt.AlignRight)

            applyBtn = QPushButton('Search')
            applyBtn.clicked.connect(lambda: bepaalMatch(m_email, self.k0Edit.currentIndex(), self.werknrEdit.text(), auth1, auth2, auth3))

            grid.addWidget(applyBtn, 6, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))

            grid.addWidget(cancelBtn, 6, 1, 1, 1, Qt.AlignCenter)
            cancelBtn.setFont(QFont("Arial", 10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

            self.setLayout(grid)
            self.setGeometry(600, 300, 150, 150)

    window = Widget()
    window.exec_()

def bepaalMatch(m_email, mchoice, mwerknr, auth1, auth2, auth3):
    if (len(str(mwerknr)) < 9 or  _11check(mwerknr) == False) :
        foutWerknr()
        return
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    selpar = select([params_services]).order_by(params_services.c.servicesID)
    rppar = conn.execute(selpar).fetchall()

    selcal1 = select([calculaties.c.verwerkt]).where(calculaties.c.koppelnummer==mwerknr)
    rpcal1 = conn.execute(selcal1).first()
    mstat = rpcal1[0]

    if mchoice == 1:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 1))
        rpcal = conn.execute(selcal)
    elif mchoice == 2:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 2))
        rpcal = conn.execute(selcal)
    elif mchoice == 3:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 3))
        rpcal = conn.execute(selcal)
    elif mchoice == 4:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 4))
        rpcal = conn.execute(selcal)
    elif mchoice == 5:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 5))
        rpcal = conn.execute(selcal)
    elif mchoice == 6:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 6))
        rpcal = conn.execute(selcal)
    elif mchoice == 7:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt == 7))
        rpcal = conn.execute(selcal)
    elif mchoice == 8:
        selcal = select([calculaties]).where(and_(calculaties.c.koppelnummer == mwerknr, calculaties.c.verwerkt > 0))
        rpcal = conn.execute(selcal)
    else:
        foutInvoer()
        return

    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args, )
            self.setWindowTitle('Reservation / Order / View Equipment')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)

            self.setFont(QFont('Arial', 10))

            grid = QGridLayout()
            grid.setSpacing(20)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240, 80))
            movie.start()
            grid.addWidget(pyqt, 1, 0, 1, 2)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 1, 9, 1, 1, Qt.AlignRight)

            if mchoice == 1:
                orderBtn = QPushButton('Reservation orders')
                orderBtn.clicked.connect(lambda: insertOrders(m_email, mchoice, mwerknr, nlist, auth1, auth2, auth3, self))
            elif mchoice == 2:
                orderBtn = QPushButton('Ordering / Modify Orders')
                orderBtn.setDisabled(True)
                modifyOrders(m_email, mchoice, mwerknr, nlist, auth1, auth2, auth3, self)
                self.close()
                calKeuze(m_email, auth1, auth2, auth3)
            else:
                if mstat == 1:
                    orderBtn = QPushButton('Reservation orders')
                    orderBtn.setDisabled(True)
                elif mstat > 1:
                    orderBtn = QPushButton('Ordering / Modify Orders')
                    orderBtn.setDisabled(True)
                    modifyOrders(m_email, mchoice, mwerknr, nlist, auth1, auth2, auth3, self)
                    self.close()
                    calKeuze(m_email, auth1, auth2, auth3)

            orderBtn.setFont(QFont("Arial", 10))
            orderBtn.setFixedWidth(220)

            grid.addWidget(orderBtn, 1, 7, 1, 3,  Qt.AlignBottom)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)

            closeBtn.setFont(QFont("Arial", 10))
            closeBtn.setFixedWidth(100)

            grid.addWidget(closeBtn, 1, 6, 1, 1, Qt.AlignRight | Qt.AlignBottom)
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 5, 1, 1, Qt.AlignCenter | Qt.AlignBottom)

            self.setLayout(grid)
            self.setGeometry(50, 50, 1600, 900)

            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            grid.addWidget(table_view, 0, 0, 1, 10)

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

    header = ['Work number','Work Description', 'ClusterID', 'Cluster Description', 'Unit', 'Number', 'Services number',
          'Service Description', 'Hours to order', 'Hourly Tariff', 'Amount', 'Order Status']

    data_list = []
    nlist = []
    for row in rpcal:
        mkopnr = row[13]
        mstatus = row[14]
        omschr = row[15]
        werk = row[16]
        hoev = row[17]
        clusternr = row[18]
        eenheid = row[19]
        for rowidx in range(0, 12):
            if int(row[rowidx]) > 0 :
                servicenr = rppar[rowidx][0]
                serviceDescr = rppar[rowidx][2]
                amount_hours = round(row[rowidx],2)
                hour_tariff = round(rppar[rowidx][1],2)
                amount = round(row[rowidx] * rppar[rowidx][1],2)
                data_list += [(mkopnr, werk, clusternr, omschr, eenheid, hoev, servicenr, serviceDescr,
                             amount_hours, hour_tariff, amount, mstatus)]
                nlist += [[servicenr, serviceDescr, mkopnr, werk, amount_hours, hour_tariff, amount, mstatus]]

    win = Widget(data_list, header)
    win.exec_()

def insertOrders(m_email, mchoice, mwerknr, nlist, auth1, auth2, auth3, self):
    nlist = sorted(nlist)
    size = len(nlist)
    for size in range(-len(nlist), -1):
        if nlist[size][0] == nlist[size + 1][0]:
            nlist[size + 1][4] = round(nlist[size][4] + nlist[size + 1][4], 2)
            nlist[size + 1][6] = round(nlist[size + 1][6] + nlist[size][6], 2)
            del nlist[size]
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    # next loop of compressed nlist
    # produce an order for each row
    matname = ''
    for item in nlist:
        if item[7] == 1:
            try:
                matnr = (con.execute(select([func.max(orders_inkoop_materieel.c.order_inkoop_materieelID, type_=Integer)])).scalar())
                matnr += 1
            except:
                matnr = 1
            try:
                ordnr = (con.execute(select([func.max(orders_inkoop.c.orderinkoopID, type_=Integer)])).scalar())
                ordnr = int(maak11proef(ordnr))
            except:
                ordnr = 400000003
            try:
                upd = update(calculaties).where(calculaties.c.koppelnummer == mwerknr).values(verwerkt = 2)
                con.execute(upd)
                ins_inkoop = insert(orders_inkoop).values(orderinkoopID = ordnr, status = 2)
                con.execute(ins_inkoop)
                insertres = insert(orders_inkoop_materieel).values(order_inkoop_materieelID = matnr, orderinkoopID = ordnr,
                    servicesID = item[0], services_omschr = item[1], werknummerID = item[2], werk_omschr = item[3],
                    uren_opdracht = item[4], uurtarief = item[5], bedrag_opdracht = item[6], status = 2)
                con.execute(insertres)
                matname = matname+'Order: '+str(ordnr)+', Equipment: '+str(matnr)+' , '+str(item[0])+' , '+str(item[1])+('\n')
            except Exception as e:
                noRecords()
                return

    message = 'Reservations are done for: \n'+matname
    reservDone(message)
    self.close()
    calKeuze(m_email, auth1,auth2,auth3)

def modifyOrders(m_email, mchoice, mwerknr, nlist, auth1, auth2, auth3, self):
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()

    try:
        if mchoice < 3 or mchoice == 8:
            selord = (select([orders_inkoop_materieel.c.orderinkoopID,orders_inkoop_materieel.c.servicesID,
              orders_inkoop_materieel.c.services_omschr, orders_inkoop_materieel.c.werknummerID,orders_inkoop_materieel.c.werk_omschr,
              orders_inkoop_materieel.c.uren_opdracht,orders_inkoop_materieel.c.uurtarief, orders_inkoop_materieel.c.bedrag_opdracht,
              orders_inkoop_materieel.c.status]).where(orders_inkoop_materieel.c.werknummerID == mwerknr)
              .order_by(orders_inkoop_materieel.c.servicesID))
        elif mchoice == 3:
            selord = (select([orders_inkoop_materieel.c.orderinkoopID, orders_inkoop_materieel.c.servicesID,
              orders_inkoop_materieel.c.services_omschr, orders_inkoop_materieel.c.werknummerID,
              orders_inkoop_materieel.c.werk_omschr, orders_inkoop_materieel.c.uren_opdracht,
              orders_inkoop_materieel.c.uurtarief,orders_inkoop_materieel.c.bedrag_opdracht, orders_inkoop_materieel.c.status]).
              where(and_(orders_inkoop_materieel.c.werknummerID == mwerknr, orders_inkoop_materieel.c.status == 2))
              .order_by(orders_inkoop_materieel.c.servicesID))
        elif mchoice == 4:
            selord = (select([orders_inkoop_materieel.c.orderinkoopID, orders_inkoop_materieel.c.servicesID,
                  orders_inkoop_materieel.c.services_omschr, orders_inkoop_materieel.c.werknummerID,
                  orders_inkoop_materieel.c.werk_omschr, orders_inkoop_materieel.c.uren_opdracht,
                  orders_inkoop_materieel.c.uurtarief, orders_inkoop_materieel.c.bedrag_opdracht,
                  orders_inkoop_materieel.c.status]).where(and_(orders_inkoop_materieel.c.werknummerID == mwerknr,
                  orders_inkoop_materieel.c.status == 3)).order_by(orders_inkoop_materieel.c.servicesID))
        elif mchoice == 5:
            selord = (select([orders_inkoop_materieel.c.orderinkoopID, orders_inkoop_materieel.c.servicesID,
               orders_inkoop_materieel.c.services_omschr, orders_inkoop_materieel.c.werknummerID,
               orders_inkoop_materieel.c.werk_omschr, orders_inkoop_materieel.c.uren_opdracht, orders_inkoop_materieel.c.uurtarief,
               orders_inkoop_materieel.c.bedrag_opdracht,orders_inkoop_materieel.c.status]).
               where(and_(orders_inkoop_materieel.c.werknummerID == mwerknr, orders_inkoop_materieel.c.status == 4))
              .order_by(orders_inkoop_materieel.c.servicesID))
        elif mchoice == 6:
            selord = (select([orders_inkoop_materieel.c.orderinkoopID, orders_inkoop_materieel.c.servicesID,
              orders_inkoop_materieel.c.services_omschr, orders_inkoop_materieel.c.werknummerID,
              orders_inkoop_materieel.c.werk_omschr, orders_inkoop_materieel.c.uren_opdracht,orders_inkoop_materieel.c.uurtarief,
              orders_inkoop_materieel.c.bedrag_opdracht, orders_inkoop_materieel.c.status]).
              where(and_(orders_inkoop_materieel.c.werknummerID == mwerknr, orders_inkoop_materieel.c.status == 5))
              .order_by(orders_inkoop_materieel.c.servicesID))
        elif mchoice == 7:
            selord = (select([orders_inkoop_materieel.c.orderinkoopID, orders_inkoop_materieel.c.servicesID,
              orders_inkoop_materieel.c.services_omschr, orders_inkoop_materieel.c.werknummerID,
              orders_inkoop_materieel.c.werk_omschr, orders_inkoop_materieel.c.uren_opdracht,
              orders_inkoop_materieel.c.uurtarief, orders_inkoop_materieel.c.bedrag_opdracht, orders_inkoop_materieel.c.status]).
              where(and_(orders_inkoop_materieel.c.werknummerID == mwerknr, orders_inkoop_materieel.c.status == 6)).
              order_by(orders_inkoop_materieel.c.servicesID))
        rpord = con.execute(selord)
    except Exception as e:
        print(str(e))
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args, )
            self.setWindowTitle('Ordering / Modify orders')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)

            self.setFont(QFont('Arial', 10))

            grid = QGridLayout()
            grid.setSpacing(20)

            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(chooseInkooporder)
            grid.addWidget(table_view, 0, 0, 1, 10)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240, 80))
            movie.start()
            grid.addWidget(pyqt, 1, 0, 1, 2)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 1, 9, 1, 1, Qt.AlignRight)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)

            closeBtn.setFont(QFont("Arial", 10))
            closeBtn.setFixedWidth(100)

            grid.addWidget(closeBtn, 1, 8, 1, 1)

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 5, 1, 1,
                           Qt.AlignCenter | Qt.AlignBottom)

            self.setLayout(grid)
            self.setGeometry(50, 50, 1200, 900)

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

    header = ['Order number', 'EquipmentID', 'Equipment description', 'Work number', 'Work Description', 'Budgeted hours', 'Hourly tariff',
              'Sum subtotal', 'Order Status', 'OrderPurchaseID']

    data_list = []
    for row in rpord:
        data_list += [(row)]

    def chooseInkooporder(idx):
        ordernr = idx.data()
        if idx.column() == 0:
            try:
                selorder = select([orders_inkoop_materieel, orders_inkoop]).where(and_(orders_inkoop.c.orderinkoopID ==
                             ordernr, orders_inkoop_materieel.c.orderinkoopID == orders_inkoop.c.orderinkoopID))
                rporder = con.execute(selorder).first()
            except Exception as e:
                print(str(e))
                noRecords()
                return
            try:
                sellev = select([leveranciers.c.leverancierID, leveranciers.c.bedrijfsnaam, leveranciers.c.rechtsvorm,
                            leveranciers.c.postcode, leveranciers.c.huisnummer]).order_by(leveranciers.c.bedrijfsnaam)
                rplev = con.execute(sellev)
            except:
                noRecords()
                return

            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Ordering Modify Equipment for "+mwerknr)
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))

                    self.setFont(QFont('Arial', 10))

                    #Purchase order
                    inkorderEdit = QLineEdit(str(ordernr))
                    inkorderEdit.setDisabled(True)
                    inkorderEdit.setAlignment(Qt.AlignRight)
                    inkorderEdit.setFixedWidth(100)
                    inkorderEdit.setFont(QFont("Arial", 10))

                    # Work number
                    werknrEdit = QLineEdit(str(mwerknr))
                    werknrEdit.setFixedWidth(100)
                    werknrEdit.setAlignment(Qt.AlignRight)
                    werknrEdit.setDisabled(True)
                    werknrEdit.setFont(QFont("Arial", 10))

                    # Start planned
                    self.q3Edit = QLineEdit(rporder[7])
                    self.q3Edit.setCursorPosition(0)
                    self.q3Edit.setFixedWidth(130)
                    self.q3Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, self.q3Edit)
                    self.q3Edit.setValidator(input_validator)

                    # Finish planned
                    self.q4Edit = QLineEdit(rporder[9])
                    self.q4Edit.setCursorPosition(0)
                    self.q4Edit.setFixedWidth(130)
                    self.q4Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex,self.q4Edit)
                    self.q4Edit.setValidator(input_validator)

                    # Supplier
                    self.k0Edit = QComboBox()
                    self.k0Edit.setFixedWidth(400)
                    self.k0Edit.setFont(QFont("Arial", 10))
                    self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.k0Edit.setMaxVisibleItems(15)
                    self.k0Edit.addItem('                      Choose Supplier')
                    k = 0
                    slist = []
                    for row in rplev:
                        slist += [(row)]
                        self.k0Edit.addItem(str(slist[k][0])+' '+slist[k][1]+' '+slist[k][2])
                        k += 1

                    grid = QGridLayout()
                    grid.setSpacing(20)

                    lblord = QLabel('              Ordering / View Equipment    ')
                    lblord.setStyleSheet("font: 18pt Comic Sans MS; color: black ; background-color: #D9E1DF")
                    grid.addWidget(lblord, 1, 0, 1, 4, Qt.AlignCenter)

                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl, 1, 0)

                    self.setFont(QFont('Arial', 10))

                    lbl1 = QLabel('Order number')
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 5, 0)
                    grid.addWidget(inkorderEdit, 5, 1)

                    grid.addWidget(QLabel('Work number'), 6, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(werknrEdit, 6, 1)

                    grid.addWidget(self.k0Edit, 7, 1, 1, 3)
                    grid.addWidget(QLabel('*'), 7, 0, Qt.AlignRight)

                    mstatus = rporder[11]
                    if mstatus == 0:
                        strstatus = 'calculation'
                    elif mstatus == 1:
                        strstatus = 'work linked'
                    elif mstatus == 2:
                        strstatus = 'reserved'
                    elif mstatus == 3:
                        strstatus = 'ordered'
                    elif mstatus == 4:
                        strstatus = 'ready'
                    elif mstatus == 5:
                        strstatus = 'paid'
                    else:
                        strstatus = 'closed'

                    orderdate = ''
                    if mstatus > 2:
                        sellev1 = select([leveranciers]).where(and_(leveranciers.c.leverancierID == orders_inkoop.c.leverancierID,
                                orders_inkoop.c.orderinkoopID == ordernr))
                        rplev1 = con.execute(sellev1).first()
                        orderdate = rporder[15]
                        lbl3 = QLabel('Equipment: ' + str(rporder[12]) + '  ' + rporder[13])
                        grid.addWidget(lbl3, 6, 2, 1, 2)
                        lbl4 = QLabel('Supplier   : ' + str(rplev1[0])+'\n'+rplev1[1]+' '+rplev1[2])
                        grid.addWidget(lbl4, 9, 2, 1, 2)
                        lbl6 = QLabel('Budgeted hours : ' + str(round(rporder[4], 2)) + '\nHourly tariff       :   ' + str(round(rporder[5], 2)))
                        grid.addWidget(lbl6, 8, 2, 1, 2)
                        lbl7 = QLabel('Total cost : ')
                        grid.addWidget(lbl7, 11, 0)
                        grid.addWidget(QLabel(str(round(rporder[6], 2))), 11, 1)

                    lbl5 = QLabel('Order status: '+strstatus+'\n'+'Order date  : '+orderdate)
                    if orderdate == '':
                        lbl5 = QLabel('Order status: '+strstatus)
                    grid.addWidget(lbl5, 5, 2, 1, 2)

                    lbl6 = QLabel('Planned start             *')
                    grid.addWidget(lbl6, 8, 0)
                    grid.addWidget(self.q3Edit, 8, 1)

                    lbl7 = QLabel('Planned ready           *')
                    grid.addWidget(lbl7, 9, 0)
                    grid.addWidget(self.q4Edit, 9, 1)
                    grid.addWidget(QLabel('* Required'), 7, 0)

                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo, 1, 3, 1, 1, Qt.AlignRight)

                    self.setLayout(grid)
                    self.setGeometry(600, 150, 150, 150)

                    orderBtn = QPushButton('Order')
                    orderBtn.clicked.connect(lambda: showResults(self))

                    grid.addWidget(orderBtn, 12, 3, 1, 1, Qt.AlignRight)
                    orderBtn.setFont(QFont("Arial", 10))
                    orderBtn.setFixedWidth(100)
                    orderBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    printBtn = QPushButton('Print order')
                    printBtn.clicked.connect(lambda: printOrder(ordernr))

                    grid.addWidget(printBtn, 12, 2, 1, 1, Qt.AlignRight)
                    printBtn.setFont(QFont("Arial", 10))
                    printBtn.setFixedWidth(100)
                    printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                    if auth1 and mchoice == 2 and mstatus == 2:      # insert   reservation/insert   reserved
                        orderBtn.setEnabled(True)
                        printBtn.setEnabled(False)
                        self.q3Edit.setEnabled(True)
                        self.q4Edit.setEnabled(True)
                        self.k0Edit.setEnabled(True)
                    elif auth1 and mchoice == 2 and mstatus > 2:     # insert  reservation/insert  ordered
                        orderBtn.setEnabled(False)
                        printBtn.setEnabled(True)
                        self.q3Edit.setEnabled(False)
                        self.q4Edit.setEnabled(False)
                        self.k0Edit.setEnabled(False)
                    elif auth1 and mchoice == 3:                     # insert ordered
                        printBtn.setEnabled(False)
                        orderBtn.setEnabled(False)
                        self.q3Edit.setEnabled(False)
                        self.q4Edit.setEnabled(False)
                        self.k0Edit.setEnabled(False)
                    elif auth2:                                      #modify
                        orderBtn.setEnabled(False)
                        printBtn.setEnabled(False)
                        self.q3Edit.setEnabled(False)
                        self.q4Edit.setEnabled(False)
                        self.k0Edit.setEnabled(False)
                    else:                                            # query
                        orderBtn.setEnabled(False)
                        printBtn.setEnabled(False)
                        self.q3Edit.setEnabled(False)
                        self.q4Edit.setEnabled(False)
                        self.k0Edit.setEnabled(False)

                    def q3Changed():
                        self.q3Edit.setText(self.q3Edit.text())
                    self.q3Edit.textChanged.connect(q3Changed)

                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)

                    def k0Changed():
                        self.k0Edit.setCurrentText(self.k0Edit.currentText())
                        self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
                    self.k0Edit.activated.connect(k0Changed)

                    def showResults(self):
                        leverancier = self.k0Edit.currentText()
                        leverancier_index = self.k0Edit.currentIndex()-1
                        startdate = self.q3Edit.text()
                        finishdate = self.q4Edit.text()
                        if len(startdate) < 10 or len(finishdate) < 10 or self.k0Edit.currentIndex() == 0:
                            foutInvoer()
                            return
                        leverancierlist = slist[leverancier_index]
                        dt = str(datetime.datetime.now())[0:10]
                        updord = update(orders_inkoop).where(orders_inkoop.c.orderinkoopID == ordernr)\
                            .values(besteldatum = dt, leverancierID = leverancierlist[0], status = 3)
                        con.execute(updord)
                        updmatord = update(orders_inkoop_materieel).where(orders_inkoop_materieel.c.orderinkoopID == ordernr)\
                           .values(leverancierID = leverancierlist[0], datum_opdracht = dt, plan_start = startdate,\
                            plan_gereed = finishdate, status = 3)
                        con.execute(updmatord)
                        orderingOK('Ordering of '+str(ordernr)+' is successful' + '\nYou can now print the order!')
                        orderBtn.setDisabled(True)
                        printBtn.setEnabled(True)
                        # self.close()

                    selwerk = select([werken]).where(and_(werken.c.werknummerID == mwerknr, orders_inkoop_materieel.c.werknummerID == werken.c.werknummerID))
                    rpwerk = con.execute(selwerk).first()

                    real_equipment_hours = rpwerk[rporder[12]+11]

                    lblmod = QLabel('                  Modify / View Equipment                 ')
                    lblmod.setStyleSheet("font: 18pt Comic Sans MS; color: black ; background-color: #D9E1DF")
                    grid.addWidget(lblmod, 13, 0 , 1, 4, Qt.AlignCenter)

                    # Actual start
                    self.q1Edit = QLineEdit(rporder[8])
                    self.q1Edit.setCursorPosition(0)
                    self.q1Edit.setFixedWidth(130)
                    self.q1Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, self.q1Edit)
                    self.q1Edit.setValidator(input_validator)

                    # Actual finish
                    self.q6Edit = QLineEdit(rporder[10])
                    self.q6Edit.setCursorPosition(0)
                    self.q6Edit.setFixedWidth(130)
                    self.q6Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, self.q6Edit)
                    self.q6Edit.setValidator(input_validator)

                    # Actual hours by work number and equipment
                    self.q9Edit = QLineEdit(str(round(real_equipment_hours, 2)))
                    self.q9Edit.setCursorPosition(0)
                    self.q9Edit.setFixedWidth(130)
                    self.q9Edit.setDisabled(True)
                    self.q9Edit.setFont(QFont("Arial", 10))

                    # Order approved date
                    self.q8Edit = QLineEdit(rporder[18])
                    self.q8Edit.setCursorPosition(0)
                    self.q8Edit.setFixedWidth(130)
                    self.q8Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, self.q8Edit)
                    self.q8Edit.setValidator(input_validator)

                    # Order paid date
                    self.q7Edit = QLineEdit(rporder[20])
                    self.q7Edit.setCursorPosition(0)
                    self.q7Edit.setFixedWidth(130)
                    self.q7Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, self.q7Edit)
                    self.q7Edit.setValidator(input_validator)

                    # order closed
                    self.q2Edit = QLineEdit(rporder[19])
                    self.q2Edit.setCursorPosition(0)
                    self.q2Edit.setFixedWidth(130)
                    self.q2Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)

                    # Invoice
                    self.q5Edit = QLineEdit('0')
                    self.q5Edit.setCursorPosition(0)
                    self.q5Edit.setFixedWidth(130)
                    self.q5Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q5Edit)
                    self.q5Edit.setValidator(input_validator)

                    # Amount paid
                    self.q10Edit = QLineEdit(str(float(round(rporder[23], 2))))
                    self.q10Edit.setCursorPosition(0)
                    self.q10Edit.setDisabled(True)
                    self.q10Edit.setFixedWidth(130)
                    self.q10Edit.setFont(QFont("Arial", 10))

                    lbl10 = QLabel('Start work date')
                    grid.addWidget(lbl10, 14, 0)
                    grid.addWidget(self.q1Edit, 14, 1)

                    lbl11 = QLabel('Finish work date')
                    grid.addWidget(lbl11, 14, 2)
                    grid.addWidget(self.q6Edit, 14, 3)

                    lbl12 = QLabel('Actual hours')
                    grid.addWidget(lbl12, 15, 0)
                    grid.addWidget(self.q9Edit, 15, 1)

                    lbl14 = QLabel('Approved work date')
                    grid.addWidget(lbl14, 15, 2)
                    grid.addWidget(self.q8Edit, 15, 3)

                    lbl15 = QLabel('Total paid date')
                    grid.addWidget(lbl15, 16, 0)
                    grid.addWidget(self.q7Edit, 16, 1)

                    lbl16 = QLabel('Closed order date')
                    grid.addWidget(lbl16, 16, 2)
                    grid.addWidget(self.q2Edit, 16, 3)

                    lbl17 = QLabel('Invoice amount to pay')
                    grid.addWidget(lbl17, 17, 0)
                    grid.addWidget(self.q5Edit, 17,1)

                    lbl18 = QLabel('Total amount paid')
                    grid.addWidget(lbl18, 17, 2)
                    grid.addWidget(self.q10Edit, 17, 3)

                    modifyBtn = QPushButton('Modify')
                    modifyBtn.clicked.connect(lambda: saveModified(self, mstatus))

                    grid.addWidget(modifyBtn, 18, 3, Qt.AlignRight)
                    modifyBtn.setFont(QFont("Arial", 10))
                    modifyBtn.setFixedWidth(100)
                    modifyBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    if ((mchoice == 1 or mchoice == 2) and (mstatus < 3)) or mchoice > 2 or mstatus == 6:
                        self.q1Edit.setDisabled(True)
                        self.q2Edit.setDisabled(True)
                        self.q5Edit.setDisabled(True)
                        self.q6Edit.setDisabled(True)
                        self.q7Edit.setDisabled(True)
                        self.q8Edit.setDisabled(True)
                        modifyBtn.setDisabled(True)

                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)

                    grid.addWidget(closeBtn, 18, 2, Qt.AlignRight)
                    closeBtn.setFont(QFont("Arial", 10))
                    closeBtn.setFixedWidth(100)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 19, 0, 1, 4,
                                   Qt.AlignCenter)

                    def q1Changed():
                        self.q1Edit.setText(self.q1Edit.text())
                    self.q3Edit.textChanged.connect(q1Changed)

                    def q6Changed():
                        self.q6Edit.setText(self.q6Edit.text())
                    self.q6Edit.textChanged.connect(q6Changed)

                    def q8Changed():
                        self.q8Edit.setText(self.q8Edit.text())
                    self.q8Edit.textChanged.connect(q8Changed)

                    def q7Changed():
                        self.q7Edit.setText(self.q7Edit.text())
                    self.q7Edit.textChanged.connect(q7Changed)

                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q3Edit.textChanged.connect(q2Changed)

                    def saveModified(self,mstatus):
                        start = self.q1Edit.text()       # date
                        finish = self.q6Edit.text()      # date
                        if len(finish) == 10:
                            mstatus = 4
                        approved = self.q8Edit.text()    # date
                        paid = self.q7Edit.text()        # date
                        if len(paid) == 10:
                            mstatus = 5
                        closed = self.q2Edit.text()      # date
                        if len(closed) == 10:
                            mstatus = 6
                        invoice = round(float(self.q5Edit.text()), 2)

                        if not((len(start) == 0 or len(start) == 10) and (len(finish) == 0 or len(finish) == 10) and (len(approved) == 0\
                              or len(approved) == 10) and  (len(paid) == 0 or len(approved) == 10) and (len(closed) == 0 or len(closed) == 10)):
                            foutInvoer()
                            return
                        else:
                            self.q5Edit.setText('0')
                            selval = select([orders_inkoop]).where(orders_inkoop.c.orderinkoopID == ordernr)
                            rpval = con.execute(selval).first()
                            self.q10Edit.setText(str(float(round(rpval[7]+invoice, 2))))
                            grid.addWidget(self.q10Edit, 17, 3)
                            wijzigOK(ordernr)

                        updmatord = update(orders_inkoop_materieel).where(orders_inkoop_materieel.c.orderinkoopID == ordernr)\
                        .values(werk_start = start, werk_gereed = finish, status = mstatus)
                        con.execute(updmatord)
                        updord = update(orders_inkoop).where(orders_inkoop.c.orderinkoopID == ordernr)\
                            .values(goedgekeurd = approved, betaald = paid, afgemeld = closed,\
                            betaald_bedrag = orders_inkoop.c.betaald_bedrag + invoice, status = mstatus)
                        con.execute(updord)
                        updcal = update(calculaties).where(calculaties.c.koppelnummer == mwerknr).values(verwerkt = mstatus)
                        con.execute(updcal)

            window = Widget()
            window.exec_()

    win = Widget(data_list, header)
    win.exec_()