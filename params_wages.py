from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp, QSize
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon, QMovie, QColor
from PyQt5.QtWidgets import QWidget, QTableView, QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, create_engine, select, update, insert, func)

def insertReq():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Insert data is required!')
    msg.setWindowTitle('Insert parameters')
    msg.exec_()

def insertOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Inserting data was successful!')
    msg.setWindowTitle('Insert parameters')
    msg.exec_()

def errorInsert(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('An error has occurred!\n'+message)
    msg.setWindowTitle('Insert parameters')
    msg.exec_()

def closeInsert(m_email, auth_1, auth_2, auth_3, self):
    self.close()
    chooseSubMenu(m_email, auth_1, auth_2, auth_3)

def noChange(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText("An critical error has occurred: \n"+message)
    msg.setWindowTitle('Modify parameters')
    msg.exec_()

def changeOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Changes successful!')
    msg.setWindowTitle('Modify parameters')
    msg.exec_()

def refresh(m_email, auth_1, auth_2, auth_3, data, self):
    self.close()
    showParams(m_email, auth_1, auth_2, auth_3, data)

def closeSubmenu(m_email, self):
    self.close()
    hoofdMenu(m_email)

def chooseSubMenu(m_email, auth_1, auth_2, auth_3):
    # structure Menu's
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Pandora ERP Wages")
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")

            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(310)
            self.k0Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.k0Edit.setFont(QFont("Arial", 10))
            self.k0Edit.setEditable(True)
            self.k0Edit.lineEdit().setFont(QFont("Arial",10))
            self.k0Edit.addItem('Submenu Parameters Wages')
            self.k0Edit.lineEdit().setReadOnly(True)
            self.k0Edit.lineEdit().setAlignment(Qt.AlignCenter)
            self.k0Edit.setItemData(0, Qt.AlignCenter, Qt.TextAlignmentRole)
            self.k0Edit.addItem('1. View params Wages')
            self.k0Edit.addItem('2. Modify params Wages')
            self.k0Edit.addItem('3. Insert new params Wages')

            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
                self.accept()
            self.k0Edit.currentIndexChanged.connect(k0Changed)

            grid = QGridLayout()
            grid.setSpacing(20)

            lblinfo = QLabel('Parameters Wages.')
            grid.addWidget(lblinfo, 1, 0, 1, 2, Qt.AlignCenter)

            grid.addWidget(self.k0Edit, 2, 0, 1, 2, Qt.AlignCenter)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240, 80))
            movie.start()
            grid.addWidget(pyqt, 0, 0)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 0, 1, 1, 2, Qt.AlignRight)

            if auth_1 == 0:
                self.k0Edit.model().item(1).setEnabled(False)
                self.k0Edit.model().item(1).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(1).setBackground(QColor('gainsboro'))

            if auth_2 == 0:
                self.k0Edit.model().item(2).setEnabled(False)
                self.k0Edit.model().item(2).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(2).setBackground(QColor('gainsboro'))

            if auth_3 == 0:
                self.k0Edit.model().item(3).setEnabled(False)
                self.k0Edit.model().item(3).setForeground(QColor('darkgrey'))
                self.k0Edit.model().item(3).setBackground(QColor('gainsboro'))

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)

            self.setLayout(grid)
            self.setGeometry(600, 100, 150, 150)

            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: closeSubmenu(m_email, self))

            grid.addWidget(cancelBtn, 3, 0, 1, 2, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial", 10))
            cancelBtn.setFixedWidth(130)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.k0Edit.currentIndex(), ]

    window = Widget()
    data = window.getData()

    if data[0] == 1 :
        showParams(m_email, auth_1, auth_2, auth_3, data)
    if data[0] == 2:
        showParams(m_email, auth_1, auth_2, auth_3, data)
    if data[0] == 3:
        insertParams(m_email, auth_1, auth_2, auth_3, data)
    chooseSubMenu(m_email, auth_1, auth_2, auth_3)

def showParams(m_email, auth_1, auth_2, auth_3, data):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args, )
            self.setWindowTitle('View / Change parameters Wages')
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
            # table_view.clicked.connect(selectRow)
            if auth_2 == 1 and data[0] == 2:
                table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0, 1, 7)

            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 1, 6, 1, 1, Qt.AlignRight)

            freshBtn = QPushButton('Refresh')
            freshBtn.clicked.connect(lambda: refresh(m_email, auth_1, auth_2, auth_3, data, self))

            freshBtn.setFont(QFont("Arial", 10))
            freshBtn.setFixedWidth(100)
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")

            grid.addWidget(freshBtn, 1, 5, 1, 1, Qt.AlignRight | Qt.AlignBottom)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)

            closeBtn.setFont(QFont("Arial", 10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")

            grid.addWidget(closeBtn, 1, 4, 1, 1, Qt.AlignRight | Qt.AlignBottom)

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 2, 1, 1, Qt.AlignBottom)

            self.setLayout(grid)
            self.setGeometry(300, 50, 900, 900)
            self.setLayout(grid)

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

    header = ['deductionID', 'Item', 'Factor Charging', 'Amount Charging', 'Lower Limit', 'Upper Limit', 'Date']

    metadata = MetaData()
    params_wages = Table('params_wages', metadata,
       Column('deductionID', Integer(), primary_key=True),
       Column('item', String),
       Column('factor_charging', Float),
       Column('amount_charging', Integer),
       Column('lower_limit', Integer),
       Column('upper_limit', Integer),
       Column('date', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()

    sel = select([params_wages]).order_by(params_wages.c.deductionID.asc())

    rp = con.execute(sel)

    data_list = []
    for row in rp:
        data_list += [row]

    def showSelection(idx):
        wagesnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params_wages]).where(params_wages.c.deductionID == wagesnr)
            rppar = con.execute(selpar).first()
            class paramWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                        Qt.WindowMinMaxButtonsHint)

                    grid = QGridLayout()
                    grid.setSpacing(20)

                    self.setWindowTitle("Pandora Enterprise Resource Planning")
                    self.setFont(QFont('Arial', 10))

                    dt = str(datetime.datetime.now())[0:10]

                    self.Item = QLabel()
                    q0Edit = QLineEdit(str(rppar[1]))
                    q0Edit.setCursorPosition(0)
                    q0Edit.setFixedWidth(300)
                    q0Edit.setFont(QFont("Arial", 10))
                    q0Edit.textChanged.connect(self.q0Changed)
                    reg_ex = QRegExp("^.{0,30}$")
                    input_validator = QRegExpValidator(reg_ex, q0Edit)
                    q0Edit.setValidator(input_validator)

                    self.Factor = QLabel()
                    q1Edit = QLineEdit(str(round(float(rppar[2]), 2)))
                    q1Edit.setCursorPosition(0)
                    q1Edit.setFixedWidth(100)
                    q1Edit.setFont(QFont("Arial", 10))
                    q1Edit.textChanged.connect(self.q1Changed)
                    reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, q1Edit)
                    q1Edit.setValidator(input_validator)

                    self.Amount = QLabel()
                    q2Edit = QLineEdit(str(int(rppar[3])))
                    q2Edit.setCursorPosition(0)
                    q2Edit.setFixedWidth(100)
                    q2Edit.setFont(QFont("Arial", 10))
                    q2Edit.textChanged.connect(self.q2Changed)
                    reg_ex = QRegExp("^([1-9]{1}[0-9]{0,7})+$")
                    input_validator = QRegExpValidator(reg_ex, q2Edit)
                    q2Edit.setValidator(input_validator)

                    self.Lower = QLabel()
                    q3Edit = QLineEdit(str(int(rppar[4])))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setCursorPosition(0)
                    q3Edit.setFont(QFont("Arial", 10))
                    q3Edit.textChanged.connect(self.q3Changed)
                    reg_ex = QRegExp("^([1-9]{1}[0-9]{0,7})+$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)

                    self.Upper = QLabel()
                    q4Edit = QLineEdit(str(int(rppar[5])))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setCursorPosition(0)
                    q4Edit.setFont(QFont("Arial", 10))
                    q4Edit.textChanged.connect(self.q4Changed)
                    reg_ex = QRegExp("^([1-9]{1}[0-9]{0,7})+$")
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)

                    lblinfo = QLabel('Modify Parameters Wages.')
                    grid.addWidget(lblinfo, 1, 0, 1, 3, Qt.AlignCenter)

                    lbl1 = QLabel('Deduction ID')
                    grid.addWidget(lbl1, 2, 0)

                    lbl2 = QLabel(str(wagesnr))
                    grid.addWidget(lbl2, 2, 1)

                    lbl3 = QLabel('Item')
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(q0Edit, 3, 1, 1, 2)

                    lbl4 = QLabel('Factor Charging')
                    grid.addWidget(lbl4, 4, 0)
                    grid.addWidget(q1Edit, 4, 1, 1, 2)

                    lbl5 = QLabel('Amount Charging')
                    grid.addWidget(lbl5, 5, 0)
                    grid.addWidget(q2Edit, 5, 1, 1, 2)

                    lbl6 = QLabel('Lower Limit')
                    grid.addWidget(lbl6, 6, 0)
                    grid.addWidget(q3Edit, 6, 1, 1, 2)

                    lbl7 = QLabel('Upper Limit')
                    grid.addWidget(lbl7, 7, 0)
                    grid.addWidget(q4Edit, 7, 1, 1, 2)

                    lbl8 = QLabel('Modification Date')
                    grid.addWidget(lbl8, 8, 0)
                    lbl9 = QLabel(dt)
                    grid.addWidget(lbl9, 8, 1, 1, 2)

                    pyqt = QLabel()
                    movie = QMovie('./images/logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240, 80))
                    movie.start()
                    grid.addWidget(pyqt, 0, 0, 1, 2)

                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo, 0, 2, 1, 1, Qt.AlignRight)

                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 0, 1, 3,
                                   Qt.AlignCenter)

                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)

                    applyBtn = QPushButton('Insert')
                    applyBtn.clicked.connect(self.accept)

                    grid.addWidget(applyBtn, 9, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial", 10))
                    applyBtn.setFixedWidth(130)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)

                    grid.addWidget(cancelBtn, 9, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial", 10))
                    cancelBtn.setFixedWidth(130)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

                def q0Changed(self, text):
                    self.Item.setText(text)

                def q1Changed(self, text):
                    self.Factor.setText(text)

                def q2Changed(self, text):
                    self.Amount.setText(text)

                def q3Changed(self, text):
                    self.Lower.setText(text)

                def q4Changed(self, text):
                    self.Upper.setText(text)

                def returnq0(self):
                    return self.Item.text()

                def returnq1(self):
                    return self.Factor.text()

                def returnq2(self):
                    return self.Amount.text()

                def returnq3(self):
                    return self.Lower.text()

                def returnq4(self):
                    return self.Upper.text()

                @staticmethod
                def getData(parent=None):
                    dialog = paramWindow()
                    dialog.exec_()
                    return [dialog.returnq0(), dialog.returnq1(), dialog.returnq2(), dialog.returnq3(), dialog.returnq4()]

            paramWin = paramWindow()
            data = paramWin.getData()

            changeflag = 0
            for k in range(0,5):
                if data[k]:
                    changeflag = 1
            if changeflag == 0:
                return

            if data[0]:
                mf0 = data[0]
            else:
                mf0 = rppar[1]
            if data[1]:
                mf1 = str(data[1])
            else:
                mf1 = rppar[2]

            dt = str(datetime.datetime.now())[0:10]

            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            try:
                updpar = update(params_wages).where(params_wages.c.deductionID == wagesnr).values(working_period = mf0,
                                      working_hours_per_period = mf1, date = dt)
                con.execute(updpar)
                changeOK()
            except Exception as e:
                noChange(str(e))

    win = MyWindow(data_list, header)
    win.exec_()

def insertParams(m_email, auth_1, auth_2, auth_3, data):
    metadata = MetaData()
    params_wages = Table('params_wages', metadata,
         Column('deductionID', Integer(), primary_key=True),
         Column('item', String),
         Column('factor_charging', Float),
         Column('amount_charging', Float),
         Column('lower_limit', Integer),
         Column('upper_limit', Integer),
         Column('date', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    try:
       wagesnr = (con.execute(select([func.max(params_wages.c.deductionID, \
                                               type_=Integer)])).scalar())
       wagesnr += 1
    except:
       wagesnr = 1

    class parWindow(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)

            grid = QGridLayout()
            grid.setSpacing(20)

            self.setWindowTitle("Pandora Enterprise Resource Planning")
            self.setFont(QFont('Arial', 10))

            dt = str(datetime.datetime.now())[0:10]

            self.Item = QLabel()
            q0Edit = QLineEdit('')
            q0Edit.setCursorPosition(0)
            q0Edit.setFixedWidth(300)
            q0Edit.setFont(QFont("Arial", 10))
            q0Edit.textChanged.connect(self.q0Changed)
            reg_ex = QRegExp("^.{0,30}$")
            input_validator = QRegExpValidator(reg_ex, q0Edit)
            q0Edit.setValidator(input_validator)

            self.Factor = QLabel()
            q1Edit = QLineEdit('')
            q1Edit.setCursorPosition(0)
            q1Edit.setFixedWidth(100)
            q1Edit.setFont(QFont("Arial", 10))
            q1Edit.textChanged.connect(self.q1Changed)
            reg_ex = QRegExp("^[-+]?[0-9]*\\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)

            self.Amount = QLabel()
            q2Edit = QLineEdit('')
            q2Edit.setCursorPosition(0)
            q2Edit.setFixedWidth(100)
            q2Edit.setFont(QFont("Arial", 10))
            q1Edit.textChanged.connect(self.q2Changed)
            reg_ex = QRegExp("^([1-9]{1}[0-9]{0,7})+$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)

            self.Lower = QLabel()
            q3Edit = QLineEdit('')
            q3Edit.setFixedWidth(100)
            q3Edit.setCursorPosition(0)
            q3Edit.setFont(QFont("Arial", 10))
            q3Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^([1-9]{1}[0-9]{0,7})+$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)

            self.Upper = QLabel()
            q4Edit = QLineEdit('')
            q4Edit.setFixedWidth(100)
            q4Edit.setCursorPosition(0)
            q4Edit.setFont(QFont("Arial", 10))
            q4Edit.textChanged.connect(self.q3Changed)
            reg_ex = QRegExp("^([1-9]{1}[0-9]{0,7})+$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)

            lblinfo = QLabel('Insert Parameters Wages.')
            grid.addWidget(lblinfo, 1, 0, 1, 3, Qt.AlignCenter)

            lbl1 = QLabel('Deduction ID')
            grid.addWidget(lbl1, 2, 0)

            lbl2 = QLabel(str(wagesnr))
            grid.addWidget(lbl2, 2, 1)

            lbl3 = QLabel('Item')
            grid.addWidget(lbl3, 3, 0)
            grid.addWidget(q0Edit, 3, 1, 1, 2)

            lbl4 = QLabel('Factor Charging')
            grid.addWidget(lbl4, 4, 0)
            grid.addWidget(q1Edit, 4, 1, 1, 2)

            lbl5 = QLabel('Amount Charging')
            grid.addWidget(lbl5, 5, 0)
            grid.addWidget(q2Edit, 5, 1, 1, 2)

            lbl6 = QLabel('Lower Limit')
            grid.addWidget(lbl6, 6, 0)
            grid.addWidget(q3Edit, 6, 1, 1, 2)

            lbl7 = QLabel('Upper Limit')
            grid.addWidget(lbl7, 7, 0)
            grid.addWidget(q4Edit, 7, 1, 1, 2)

            lbl8 = QLabel('Modification Date')
            grid.addWidget(lbl8, 8, 0)
            lbl9 = QLabel(dt)
            grid.addWidget(lbl9, 8, 1, 1, 2)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240, 80))
            movie.start()
            grid.addWidget(pyqt, 0, 0, 1, 2)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 0, 2, 1, 1, Qt.AlignRight)

            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 10, 0, 1, 3,
                           Qt.AlignCenter)

            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)

            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(self.accept)

            grid.addWidget(applyBtn, 9, 2, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(130)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(lambda: closeInsert(m_email, auth_1, auth_2, auth_3, self))

            grid.addWidget(cancelBtn, 9, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial", 10))
            cancelBtn.setFixedWidth(130)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")

        def q0Changed(self, text):
            self.Item.setText(text)

        def q1Changed(self, text):
            self.Factor.setText(text)

        def q2Changed(self, text):
            self.Amount.setText(text)

        def q3Changed(self, text):
            self.Lower.setText(text)

        def q4Changed(self, text):
            self.Upper.setText(text)

        def returnq0(self):
            return self.Item.text()

        def returnq1(self):
            return self.Factor.text()

        def returnq2(self):
            return self.Amount.text()

        def returnq3(self):
            return self.Lower.text()

        def returnq4(self):
            return self.Upper.text()

        @staticmethod
        def getData(parent=None):
            dialog = parWindow()
            dialog.exec_()
            return [dialog.returnq0(), dialog.returnq1(), dialog.returnq2(), dialog.returnq3(), dialog.returnq4()]

    parWin = parWindow()
    data = parWin.getData()
    if data[0]:
        mf0 = data[0]
    else:
        insertReq()
        insertParams(m_email, auth_1, auth_2, auth_3, data)
    if data[1]:
        mf1 = int(data[1])
    else:
        insertReq()
        insertParams(m_email, auth_1, auth_2, auth_3, data)

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    try:
        inspar = insert(params_wages).values(periodID = wagesnr, working_period = mf0, working_hours_per_period = mf1)
        con.execute(inspar)
        insertOK()
        insertParams(m_email, auth_1, auth_2, auth_3, data)
    except Exception as e:
        errorInsert(str(e))
        insertParams(m_email, auth_1, auth_2, auth_3, data)
