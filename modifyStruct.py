from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QMovie
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QDialog, QGridLayout,\
      QMessageBox, QTableView, QVBoxLayout, QLineEdit
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine, select, update, insert, func)

def insertReq():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Insert data is required!')
    msg.setWindowTitle('Insert Menu Structures')
    msg.exec_()

def insertOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Inserting data was successful!')
    msg.setWindowTitle('Insert Menu Structures')
    msg.exec_()

def errorInsert(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('An error has occurred!\n'+message)
    msg.setWindowTitle('Insert Menu Structures')
    msg.exec_()

def noRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('No record present, first insert record(s)!')
    msg.setWindowTitle('Insert Menu Structures')
    msg.exec_()

def closeInsert(sector, m_email, self):
    self.close()
    hoofdMenu(m_email)

def noChange():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Critical)
    msg.setText('An error has occurred, no changes are processed!')
    msg.setWindowTitle('Modify Menu Structures')
    msg.exec_()

def changeOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Information)
    msg.setText('Changes are successful!')
    msg.setWindowTitle('Modify Menu Structures')
    msg.exec_()

def refresh(m_email, self):
    self.close()
    menuStructure(m_email, self)

def selectRow(index):
    print('Recordnumber: ', index.row())

def menuStructure(sector, m_email):
    metadata = MetaData()
    cluster_structure_external = Table('cluster_structure_external', metadata,
       Column('structID', Integer(), primary_key=True),
       Column('overall_heading', String),
       Column('heading_level1', String),
       Column('line_level0', String),
       Column('line1', String),
       Column('line2', String),
       Column('line3', String),
       Column('line4', String),
       Column('line5', String),
       Column('line6', String),
       Column('line7', String),
       Column('line8', String),
       Column('line9', String),
       Column('line10', String),
       Column('line11', String),
       Column('line12', String),
       Column('line13', String),
       Column('line14', String),
       Column('line15', String))

    cluster_structure_internal = Table('cluster_structure_internal', metadata,
       Column('structID', Integer(), primary_key=True),
       Column('overall_heading', String),
       Column('heading_level1', String),
       Column('line_level0', String),
       Column('line1', String),
       Column('line2', String),
       Column('line3', String),
       Column('line4', String),
       Column('line5', String),
       Column('line6', String),
       Column('line7', String),
       Column('line8', String),
       Column('line9', String),
       Column('line10', String),
       Column('line11', String),
       Column('line12', String),
       Column('line13', String),
       Column('line14', String),
       Column('line15', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    if sector == 'external':
        con = engine.connect()
        sel = select([cluster_structure_external]).order_by(cluster_structure_external.c.line_level0)
        rpa = con.execute(sel)
    else:
        con = engine.connect()
        sel = select([cluster_structure_internal]).order_by(cluster_structure_internal.c.line_level0)
        rpa = con.execute(sel)
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args, )
            self.setGeometry(50, 50, 1700, 900)
            self.setWindowTitle('Request Menu Structure Clusters')
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
            table_view.clicked.connect(showSelection)
            # table_view.clicked.connect(selectRow)
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
                noRecord()
                hoofdMenu(m_email)
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

    header = ['StructureID', 'Toplevel', 'Heading Level 1', 'Line_level0', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5',\
              'Line 6', 'Line 7', 'Line 8', 'Line 9', 'Line 10', 'Line 11', 'Line 12', 'Line 13', 'Line 14', 'Line 15']

    data_list = []
    for row in rpa:
        data_list += [row]

    def showSelection(idx):
        if idx.column() == 0:
            structnr = idx.data()
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            if sector == 'external':
                selstruct = select([cluster_structure_external]).where(cluster_structure_external.c.structID == structnr)
                rpselstruct = con.execute(selstruct).first()
            else:
                selstruct = select([cluster_structure_internal]).where(cluster_structure_internal.c.structID == structnr)
                rpselstruct = con.execute(selstruct).first()
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)

                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Modify Structure Menus Clusters")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                        Qt.WindowMinMaxButtonsHint)
                    self.setFont(QFont('Arial', 10))

                    lbl1 = QLabel('Cluster Menu Structure  ID')
                    q1Edit = QLineEdit(str(rpselstruct[0]))
                    q1Edit.setFont(QFont("Arial", 10))
                    q1Edit.setFixedWidth(310)
                    q1Edit.setDisabled(True)
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1, 1)

                    self.q2 = QLabel()
                    lbl2 = QLabel('Overall heading')
                    q2Edit = QLineEdit(rpselstruct[1])
                    q2Edit.setFixedWidth(320)
                    q2Edit.setFont(QFont("Arial", 10))
                    q2Edit.textChanged.connect(self.q2Changed)
                    lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(q2Edit, 2, 1)

                    self.q3 = QLabel()
                    lbl3 = QLabel('Heading level 1')
                    q3Edit = QLineEdit(rpselstruct[2])
                    q3Edit.setFixedWidth(320)
                    q3Edit.setFont(QFont("Arial", 10))
                    q3Edit.textChanged.connect(self.q3Changed)
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(q3Edit, 3, 1)

                    self.q4 = QLabel()
                    lbl4 = QLabel('Line level 0')
                    q4Edit = QLineEdit(rpselstruct[3])
                    q4Edit.setFixedWidth(320)
                    q4Edit.setFont(QFont("Arial", 10))
                    q4Edit.textChanged.connect(self.q4Changed)
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 4, 0)
                    grid.addWidget(q4Edit, 4, 1)

                    self.q5 = QLabel()
                    lbl5 = QLabel('Line 1')
                    q5Edit = QLineEdit(rpselstruct[4])
                    q5Edit.setFixedWidth(320)
                    q5Edit.setFont(QFont("Arial", 10))
                    q5Edit.textChanged.connect(self.q5Changed)
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 5, 0)
                    grid.addWidget(q5Edit, 5, 1)

                    self.q7 = QLabel()
                    lbl7 = QLabel('Line 2')
                    q7Edit = QLineEdit(rpselstruct[5])
                    q7Edit.setFixedWidth(320)
                    q7Edit.setFont(QFont("Arial", 10))
                    q7Edit.textChanged.connect(self.q7Changed)
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 6, 0)
                    grid.addWidget(q7Edit, 6, 1)

                    self.q8 = QLabel()
                    lbl8 = QLabel('Line 3')
                    q8Edit = QLineEdit(rpselstruct[6])
                    q8Edit.setFixedWidth(320)
                    q8Edit.setFont(QFont("Arial", 10))
                    q8Edit.textChanged.connect(self.q8Changed)
                    lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl8, 7, 0)
                    grid.addWidget(q8Edit, 7, 1)

                    self.q9 = QLabel()
                    lbl9 = QLabel('Line 4')
                    q9Edit = QLineEdit(rpselstruct[7])
                    q9Edit.setFixedWidth(320)
                    q9Edit.setFont(QFont("Arial", 10))
                    q9Edit.textChanged.connect(self.q9Changed)
                    lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl9, 8, 0)
                    grid.addWidget(q9Edit, 8, 1)

                    self.q10 = QLabel()
                    lbl10 = QLabel('Line 5')
                    q10Edit = QLineEdit(rpselstruct[8])
                    q10Edit.setFixedWidth(320)
                    q10Edit.setFont(QFont("Arial", 10))
                    q10Edit.textChanged.connect(self.q10Changed)
                    lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl10, 9, 0)
                    grid.addWidget(q10Edit, 9, 1)

                    self.q20 = QLabel()
                    lbl20 = QLabel('Line 6')
                    q20Edit = QLineEdit(rpselstruct[9])
                    q20Edit.setFixedWidth(320)
                    q20Edit.setFont(QFont("Arial", 10))
                    q20Edit.textChanged.connect(self.q20Changed)
                    lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl20, 10, 0)
                    grid.addWidget(q20Edit, 10, 1)

                    self.q21 = QLabel()
                    lbl21 = QLabel('Line 7')
                    q21Edit = QLineEdit(rpselstruct[10])
                    q21Edit.setFixedWidth(320)
                    q21Edit.setFont(QFont("Arial", 10))
                    q21Edit.textChanged.connect(self.q21Changed)
                    lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl21, 11, 0)
                    grid.addWidget(q21Edit, 11, 1)

                    self.q22 = QLabel()
                    lbl22 = QLabel('Line 8')
                    q22Edit = QLineEdit(rpselstruct[11])
                    q22Edit.setFixedWidth(320)
                    q22Edit.setFont(QFont("Arial", 10))
                    q22Edit.textChanged.connect(self.q22Changed)
                    lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl22, 3, 2)
                    grid.addWidget(q22Edit, 3, 3)

                    self.q23 = QLabel()
                    lbl23 = QLabel('Line 9')
                    q23Edit = QLineEdit(rpselstruct[12])
                    q23Edit.setFixedWidth(320)
                    q23Edit.setFont(QFont("Arial", 10))
                    q23Edit.textChanged.connect(self.q23Changed)
                    lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl23, 4, 2)
                    grid.addWidget(q23Edit, 4, 3)

                    self.q24 = QLabel()
                    lbl24 = QLabel('Line 10')
                    q24Edit = QLineEdit(rpselstruct[13])
                    q24Edit.setFixedWidth(320)
                    q24Edit.setFont(QFont("Arial", 10))
                    q24Edit.textChanged.connect(self.q24Changed)
                    lbl24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl24, 5, 2)
                    grid.addWidget(q24Edit, 5, 3)

                    self.q25 = QLabel()
                    lbl25 = QLabel('Line 11')
                    q25Edit = QLineEdit(rpselstruct[14])
                    q25Edit.setFixedWidth(320)
                    q25Edit.setFont(QFont("Arial", 10))
                    q25Edit.textChanged.connect(self.q25Changed)
                    lbl25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl25, 6, 2)
                    grid.addWidget(q25Edit, 6, 3)

                    self.q26 = QLabel()
                    lbl26 = QLabel('Line 12')
                    q26Edit = QLineEdit(rpselstruct[15])
                    q26Edit.setFixedWidth(320)
                    q26Edit.setFont(QFont("Arial", 10))
                    q26Edit.textChanged.connect(self.q26Changed)
                    lbl26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl26, 7, 2)
                    grid.addWidget(q26Edit, 7, 3)

                    self.q27 = QLabel()
                    lbl27 = QLabel('Line 13')
                    q27Edit = QLineEdit(rpselstruct[16])
                    q27Edit.setFixedWidth(320)
                    q27Edit.setFont(QFont("Arial", 10))
                    q27Edit.textChanged.connect(self.q27Changed)
                    lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl27, 8, 2)
                    grid.addWidget(q27Edit, 8, 3)

                    self.q28 = QLabel()
                    lbl28 = QLabel('Line 14')
                    q28Edit = QLineEdit(rpselstruct[17])
                    q28Edit.setFixedWidth(320)
                    q28Edit.setFont(QFont("Arial", 10))
                    q28Edit.textChanged.connect(self.q28Changed)
                    lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl28, 9, 2)
                    grid.addWidget(q28Edit, 9, 3)

                    self.q29 = QLabel()
                    lbl29 = QLabel('Line 15')
                    q29Edit = QLineEdit(rpselstruct[18])
                    q29Edit.setFixedWidth(320)
                    q29Edit.setFont(QFont("Arial", 10))
                    q29Edit.textChanged.connect(self.q29Changed)
                    lbl29.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl29, 10, 2)
                    grid.addWidget(q29Edit, 10, 3)

                    pyqt = QLabel()
                    movie = QMovie('./images/logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240, 80))
                    movie.start()
                    grid.addWidget(pyqt, 0, 0, 1, 2)

                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo, 0, 3, 1, 1, Qt.AlignRight)

                    grid.addWidget(QLabel('Modify Structure Menus of Clusters from '+sector+' Works'), 0, 1, 1, 4, Qt.AlignCenter)

                    applyBtn = QPushButton('Modify')
                    applyBtn.clicked.connect(self.accept)

                    grid.addWidget(applyBtn, 21, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial", 10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)

                    grid.addWidget(closeBtn, 21, 3, 1, 1, Qt.AlignCenter)
                    closeBtn.setFont(QFont("Arial", 10))
                    closeBtn.setFixedWidth(100)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")

                    grid.addWidget(QLabel('                         \u00A9 2017 all rights reserved dj.jansen@casema.nl'), 22, 1, 1, 3)

                    self.setLayout(grid)
                    self.setGeometry(400, 50, 150, 150)

                def q2Changed(self, text):
                    self.q2.setText(text)

                def q3Changed(self, text):
                    self.q3.setText(text)

                def q4Changed(self, text):
                    self.q4.setText(text)

                def q5Changed(self, text):
                    self.q5.setText(text)

                def q7Changed(self, text):
                    self.q7.setText(text)

                def q8Changed(self, text):
                    self.q8.setText(text)

                def q9Changed(self, text):
                    self.q9.setText(text)

                def q10Changed(self, text):
                    self.q10.setText(text)

                def q20Changed(self, text):
                    self.q20.setText(text)

                def q21Changed(self, text):
                    self.q21.setText(text)

                def q22Changed(self, text):
                    self.q22.setText(text)

                def q23Changed(self, text):
                    self.q23.setText(text)

                def q24Changed(self, text):
                    self.q24.setText(text)

                def q25Changed(self, text):
                    self.q25.setText(text)

                def q26Changed(self, text):
                    self.q26.setText(text)

                def q27Changed(self, text):
                    self.q27.setText(text)

                def q28Changed(self, text):
                    self.q28.setText(text)

                def q29Changed(self, text):
                    self.q29.setText(text)

                def returnq2(self):
                    return self.q2.text()

                def returnq3(self):
                    return self.q3.text()

                def returnq4(self):
                    return self.q4.text()

                def returnq5(self):
                    return self.q5.text()

                def returnq7(self):
                    return self.q7.text()

                def returnq8(self):
                    return self.q8.text()

                def returnq9(self):
                    return self.q9.text()

                def returnq10(self):
                    return self.q10.text()

                def returnq20(self):
                    return self.q20.text()

                def returnq21(self):
                    return self.q21.text()

                def returnq22(self):
                    return self.q22.text()

                def returnq23(self):
                    return self.q23.text()

                def returnq24(self):
                    return self.q24.text()

                def returnq25(self):
                    return self.q25.text()

                def returnq26(self):
                    return self.q26.text()

                def returnq27(self):
                    return self.q27.text()

                def returnq28(self):
                    return self.q28.text()

                def returnq29(self):
                    return self.q29.text()

                @staticmethod
                def getData(parent=None):
                    dialog = MainWindow()
                    dialog.exec_()
                    return [dialog.returnq2(), dialog.returnq3(), dialog.returnq4(), dialog.returnq5(), dialog.returnq7(),\
                            dialog.returnq8(), dialog.returnq9(), dialog.returnq10(), dialog.returnq20(), dialog.returnq21(),\
                            dialog.returnq22(), dialog.returnq23(), dialog.returnq24(), dialog.returnq25(), dialog.returnq26(),\
                            dialog.returnq27(), dialog.returnq28(), dialog.returnq29()]

            mainWin = MainWindow()
            data = mainWin.getData()

            changeflag = 0
            for k in range(0, 18):
                if data[k]:
                    changeflag = 1
            if changeflag == 0:
                return

            if data[0]:
                q2 = data[0]
            else:
                q2 = rpselstruct[1]
            if data[1]:
                q3 =data[1]
            else:
                q3 = rpselstruct[2]
            if data[2]:
                q4 = data[2]
            else:
                q4 = rpselstruct[3]
            if data[3]:
                q5 = data[3]
            else:
                q5 = rpselstruct[4]
            if data[4]:
                q7 = data[4]
            else:
                q7 = rpselstruct[5]
            if data[5]:
                q8 = data[5]
            else:
                q8 = rpselstruct[6]
            if data[6]:
                q9 = data[6]
            else:
                q9 = rpselstruct[7]
            if data[7]:
                q10 = data[7]
            else:
                q10 = rpselstruct[8]
            if data[8]:
                q20 = data[8]
            else:
                q20 = rpselstruct[9]
            if data[9]:
                q21 = data[9]
            else:
                q21 = rpselstruct[10]
            if data[10]:
                q22 = data[10]
            else:
                q22 = rpselstruct[11]
            if data[11]:
                q23 = data[11]
            else:
                q23 = rpselstruct[12]
            if data[12]:
                q24 = data[12]
            else:
                q24 = rpselstruct[13]
            if data[13]:
                q25 = data[13]
            else:
                q25 = rpselstruct[14]
            if data[14]:
                q26 = data[14]
            else:
                q26 = rpselstruct[15]
            if data[15]:
                q27 = data[15]
            else:
                q27 = rpselstruct[16]
            if data[16]:
                q28 = data[16]
            else:
                q28 = rpselstruct[17]
            if data[17]:
                q29 = data[17]
            else:
                q29 = rpselstruct[18]

            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            try:
                if sector == 'external':
                    updstruct = update(cluster_structure_external).where(cluster_structure_external.c.structID == structnr). \
                        values(overall_heading=q2, heading_level1=q3, line_level0=q4, line1=q5, line2=q7, line3=q8, line4=q9, line5=q10, \
                         line6=q20, line7=q21, line8=q22, line9=q23, line10=q24, line11=q25, line12=q26, line13=q27, line14=q28, line15=q29)
                    con.execute(updstruct)
                else:
                    updstruct = update(cluster_structure_internal).where(cluster_structure_internal.c.structID == structnr). \
                        values(overall_heading=q2, heading_level1=q3, line_level0=q4, line1=q5, line2=q7, line3=q8,line4=q9, line5=q10, \
                         line6=q20, line7=q21, line8=q22, line9=q23, line10=q24, line11=q25, line12=q26, line13=q27, line14=q28, line15=q29)
                    con.execute(updstruct)
            except Exception:
                noChange()

    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)

def insertStruct(sector, m_email):
    metadata = MetaData()
    cluster_structure_external = Table('cluster_structure_external', metadata,
           Column('structID', Integer(), primary_key=True),
           Column('overall_heading', String),
           Column('heading_level1', String),
           Column('line_level0', String),
           Column('line1', String),
           Column('line2', String),
           Column('line3', String),
           Column('line4', String),
           Column('line5', String),
           Column('line6', String),
           Column('line7', String),
           Column('line8', String),
           Column('line9', String),
           Column('line10', String),
           Column('line11', String),
           Column('line12', String),
           Column('line13', String),
           Column('line14', String),
           Column('line15', String))

    cluster_structure_internal = Table('cluster_structure_internal', metadata,
           Column('structID', Integer(), primary_key=True),
           Column('overall_heading', String),
           Column('heading_level1', String),
           Column('line_level0', String),
           Column('line1', String),
           Column('line2', String),
           Column('line3', String),
           Column('line4', String),
           Column('line5', String),
           Column('line6', String),
           Column('line7', String),
           Column('line8', String),
           Column('line9', String),
           Column('line10', String),
           Column('line11', String),
           Column('line12', String),
           Column('line13', String),
           Column('line14', String),
           Column('line15', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()

    if sector == 'external':
        try:
            structnr = (con.execute(select([func.max(cluster_structure_external.c.structID, \
                                                       type_=Integer)])).scalar())
            structnr += 1
        except:
            structnr = 1
    if sector == 'internal':
        try:
            structnr = (con.execute(select([func.max(cluster_structure_internal.c.structID, \
                                                 type_=Integer)])).scalar())
            structnr += 1
        except:
            structnr = 1
    class insWindow(QDialog):
        def __init__(self, *args):
            QWidget.__init__(self, *args, )
            self.setGeometry(50, 50, 1700, 900)
            self.setWindowTitle('Request account information')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)

            grid = QGridLayout()
            grid.setSpacing(20)
            self.setWindowTitle("Insert Structure Menus Clusters")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))

            lbl1 = QLabel('Cluster Menu Structure  ID')
            q1Edit = QLineEdit(str(structnr))
            q1Edit.setFont(QFont("Arial", 10))
            q1Edit.setFixedWidth(310)
            q1Edit.setDisabled(True)
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            grid.addWidget(q1Edit, 1, 1)

            self.q2 = QLabel()
            lbl2 = QLabel('Overall heading')
            q2Edit = QLineEdit('')
            q2Edit.setFixedWidth(320)
            q2Edit.setFont(QFont("Arial", 10))
            q2Edit.textChanged.connect(self.q2Changed)
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 2, 0)
            grid.addWidget(q2Edit, 2, 1)

            self.q3 = QLabel()
            lbl3 = QLabel('Heading level 1')
            q3Edit = QLineEdit('')
            q3Edit.setFixedWidth(320)
            q3Edit.setFont(QFont("Arial", 10))
            q3Edit.textChanged.connect(self.q3Changed)
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 3, 0)
            grid.addWidget(q3Edit, 3, 1)

            self.q4 = QLabel()
            lbl4 = QLabel('Line level 0')
            q4Edit = QLineEdit('')
            q4Edit.setFixedWidth(320)
            q4Edit.setFont(QFont("Arial", 10))
            q4Edit.textChanged.connect(self.q4Changed)
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 4, 0)
            grid.addWidget(q4Edit, 4, 1)

            self.q5 = QLabel()
            lbl5 = QLabel('Line 1')
            q5Edit = QLineEdit('')
            q5Edit.setFixedWidth(320)
            q5Edit.setFont(QFont("Arial", 10))
            q5Edit.textChanged.connect(self.q5Changed)
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 5, 0)
            grid.addWidget(q5Edit, 5, 1)

            self.q7 = QLabel()
            lbl7 = QLabel('Line 2')
            q7Edit = QLineEdit('')
            q7Edit.setFixedWidth(320)
            q7Edit.setFont(QFont("Arial", 10))
            q7Edit.textChanged.connect(self.q7Changed)
            lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl7, 6, 0)
            grid.addWidget(q7Edit, 6, 1)

            self.q8 = QLabel()
            lbl8 = QLabel('Line 3')
            q8Edit = QLineEdit('')
            q8Edit.setFixedWidth(320)
            q8Edit.setFont(QFont("Arial", 10))
            q8Edit.textChanged.connect(self.q8Changed)
            lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl8, 7, 0)
            grid.addWidget(q8Edit, 7, 1)

            self.q9 = QLabel()
            lbl9 = QLabel('Line 4')
            q9Edit = QLineEdit('')
            q9Edit.setFixedWidth(320)
            q9Edit.setFont(QFont("Arial", 10))
            q9Edit.textChanged.connect(self.q9Changed)
            lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl9, 8, 0)
            grid.addWidget(q9Edit, 8, 1)

            self.q10 = QLabel()
            lbl10 = QLabel('Line 5')
            q10Edit = QLineEdit('')
            q10Edit.setFixedWidth(320)
            q10Edit.setFont(QFont("Arial", 10))
            q10Edit.textChanged.connect(self.q10Changed)
            lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl10, 9, 0)
            grid.addWidget(q10Edit, 9, 1)

            self.q20 = QLabel()
            lbl20 = QLabel('Line 6')
            q20Edit = QLineEdit('')
            q20Edit.setFixedWidth(320)
            q20Edit.setFont(QFont("Arial", 10))
            q20Edit.textChanged.connect(self.q20Changed)
            lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl20, 10, 0)
            grid.addWidget(q20Edit, 10, 1)

            self.q21 = QLabel()
            lbl21 = QLabel('Line 7')
            q21Edit = QLineEdit('')
            q21Edit.setFixedWidth(320)
            q21Edit.setFont(QFont("Arial", 10))
            q21Edit.textChanged.connect(self.q21Changed)
            lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl21, 11, 0)
            grid.addWidget(q21Edit, 11, 1)

            self.q22 = QLabel()
            lbl22 = QLabel('Line 8')
            q22Edit = QLineEdit('')
            q22Edit.setFixedWidth(320)
            q22Edit.setFont(QFont("Arial", 10))
            q22Edit.textChanged.connect(self.q22Changed)
            lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl22, 3, 2)
            grid.addWidget(q22Edit, 3, 3)

            self.q23 = QLabel()
            lbl23 = QLabel('Line 9')
            q23Edit = QLineEdit('')
            q23Edit.setFixedWidth(320)
            q23Edit.setFont(QFont("Arial", 10))
            q23Edit.textChanged.connect(self.q23Changed)
            lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl23, 4, 2)
            grid.addWidget(q23Edit, 4, 3)

            self.q24 = QLabel()
            lbl24 = QLabel('Line 10')
            q24Edit = QLineEdit('')
            q24Edit.setFixedWidth(320)
            q24Edit.setFont(QFont("Arial", 10))
            q24Edit.textChanged.connect(self.q24Changed)
            lbl24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl24, 5, 2)
            grid.addWidget(q24Edit, 5, 3)

            self.q25 = QLabel()
            lbl25 = QLabel('Line 11')
            q25Edit = QLineEdit('')
            q25Edit.setFixedWidth(320)
            q25Edit.setFont(QFont("Arial", 10))
            q25Edit.textChanged.connect(self.q25Changed)
            lbl25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl25, 6, 2)
            grid.addWidget(q25Edit, 6, 3)

            self.q26 = QLabel()
            lbl26 = QLabel('Line 12')
            q26Edit = QLineEdit('')
            q26Edit.setFixedWidth(320)
            q26Edit.setFont(QFont("Arial", 10))
            q26Edit.textChanged.connect(self.q26Changed)
            lbl26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl26, 7, 2)
            grid.addWidget(q26Edit, 7, 3)

            self.q27 = QLabel()
            lbl27 = QLabel('Line 13')
            q27Edit = QLineEdit('')
            q27Edit.setFixedWidth(320)
            q27Edit.setFont(QFont("Arial", 10))
            q27Edit.textChanged.connect(self.q27Changed)
            lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl27, 8, 2)
            grid.addWidget(q27Edit, 8, 3)

            self.q28 = QLabel()
            lbl28 = QLabel('Line 14')
            q28Edit = QLineEdit('')
            q28Edit.setFixedWidth(320)
            q28Edit.setFont(QFont("Arial", 10))
            q28Edit.textChanged.connect(self.q28Changed)
            lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl28, 9, 2)
            grid.addWidget(q28Edit, 9, 3)

            self.q29 = QLabel()
            lbl29 = QLabel('Line 15')
            q29Edit = QLineEdit('')
            q29Edit.setFixedWidth(320)
            q29Edit.setFont(QFont("Arial", 10))
            q29Edit.textChanged.connect(self.q29Changed)
            lbl29.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl29, 10, 2)
            grid.addWidget(q29Edit, 10, 3)

            pyqt = QLabel()
            movie = QMovie('./images/logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240, 80))
            movie.start()
            grid.addWidget(pyqt, 0, 0, 1, 2)

            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo, 0, 3, 1, 1, Qt.AlignRight)

            grid.addWidget(QLabel('Insert Structure Menus of Clusters from '+sector+' Works'), 0, 1, 1, 4, Qt.AlignCenter)

            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(self.accept)

            grid.addWidget(applyBtn, 21, 3, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(lambda: closeInsert(sector, m_email, self))

            grid.addWidget(closeBtn, 21, 3, 1, 1, Qt.AlignCenter)
            closeBtn.setFont(QFont("Arial", 10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")

            grid.addWidget(QLabel('                         \u00A9 2017 all rights reserved dj.jansen@casema.nl'), 22, 1, 1, 3)

            self.setLayout(grid)
            self.setGeometry(400, 50, 150, 150)


        def q2Changed(self, text):
            self.q2.setText(text)

        def q3Changed(self, text):
            self.q3.setText(text)

        def q4Changed(self, text):
            self.q4.setText(text)

        def q5Changed(self, text):
            self.q5.setText(text)

        def q7Changed(self, text):
            self.q7.setText(text)

        def q8Changed(self, text):
            self.q8.setText(text)

        def q9Changed(self, text):
            self.q9.setText(text)

        def q10Changed(self, text):
            self.q10.setText(text)

        def q20Changed(self, text):
            self.q20.setText(text)

        def q21Changed(self, text):
            self.q21.setText(text)

        def q22Changed(self, text):
            self.q22.setText(text)

        def q23Changed(self, text):
            self.q23.setText(text)

        def q24Changed(self, text):
            self.q24.setText(text)

        def q25Changed(self, text):
            self.q25.setText(text)

        def q26Changed(self, text):
            self.q26.setText(text)

        def q27Changed(self, text):
            self.q27.setText(text)

        def q28Changed(self, text):
            self.q28.setText(text)

        def q29Changed(self, text):
            self.q29.setText(text)

        def returnq2(self):
            return self.q2.text()

        def returnq3(self):
            return self.q3.text()

        def returnq4(self):
            return self.q4.text()

        def returnq5(self):
            return self.q5.text()

        def returnq7(self):
            return self.q7.text()

        def returnq8(self):
            return self.q8.text()

        def returnq9(self):
            return self.q9.text()

        def returnq10(self):
            return self.q10.text()

        def returnq20(self):
            return self.q20.text()

        def returnq21(self):
            return self.q21.text()

        def returnq22(self):
            return self.q22.text()

        def returnq23(self):
            return self.q23.text()

        def returnq24(self):
            return self.q24.text()

        def returnq25(self):
            return self.q25.text()

        def returnq26(self):
            return self.q26.text()

        def returnq27(self):
            return self.q27.text()

        def returnq28(self):
            return self.q28.text()

        def returnq29(self):
            return self.q29.text()

        @staticmethod
        def getData(parent=None):
            dialog = insWindow()
            dialog.exec_()
            return [dialog.returnq2(), dialog.returnq3(), dialog.returnq4(), dialog.returnq5(), dialog.returnq7(),\
                    dialog.returnq8(), dialog.returnq9(), dialog.returnq10(), dialog.returnq20(), dialog.returnq21(),\
                    dialog.returnq22(), dialog.returnq23(), dialog.returnq24(), dialog.returnq25(), dialog.returnq26(),\
                    dialog.returnq27(), dialog.returnq28(), dialog.returnq29()]

    insWin = insWindow()
    data = insWin.getData()

    if data[0]:
        q2 = data[0]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[1]:
        q3 =data[1]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[2]:
        q4 = data[2]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[3]:
        q5 = data[3]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[4]:
        q7 = data[4]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[5]:
        q8 = data[5]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[6]:
        q9 = data[6]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[7]:
        q10 = data[7]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[8]:
        q20 = data[8]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[9]:
        q21 = data[9]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[10]:
        q22 = data[10]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[11]:
        q23 = data[11]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[12]:
        q24 = data[12]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[13]:
        q25 = data[13]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[14]:
        q26 = data[14]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[15]:
        q27 = data[15]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[16]:
        q28 = data[16]
    else:
        insertReq()
        insertStruct(sector, m_email)
    if data[17]:
        q29 = data[17]
    else:
        insertReq()
        insertStruct(sector, m_email)

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    try:
        if sector == 'external':
            instruct = insert(cluster_structure_external).values(structID = structnr, overall_heading=q2, heading_level1=q3,\
                            line_level0=q4, line1=q5, line2=q7, line3=q8, line4=q9, line5=q10, line6=q20, line7=q21,\
                            line8=q22, line9=q23, line10=q24, line11=q25, line12=q26, line13=q27, line14=q28, line15=q29)
            con.execute(instruct)
            insertOK()
            insertStruct(sector, m_email)
        else:
            instruct = insert(cluster_structure_internal).values(structID = structnr, overall_heading=q2, heading_level1=q3,\
                            line_level0=q4, line1=q5, line2=q7, line3=q8, line4=q9, line5=q10, line6=q20, line7=q21,\
                            line8=q22, line9=q23, line10=q24, line11=q25, line12=q26, line13=q27, line14=q28, line15=q29)
            con.execute(instruct)
            insertOK()
            insertStruct(sector, m_email)
    except Exception as e:
        errorInsert(str(e))
        insertStruct(sector, m_email)