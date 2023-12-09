from login import hoofdMenu
from postcode import checkpostcode
import os, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import  QDialog, QWidget, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine,\
                        Float, ForeignKey, select, and_)

def geenBest(m_email):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Nog geen facturen aanwezig voor deze klant!')
    msg.setWindowTitle('Facturen printen')
    msg.exec_()
    hoofdMenu(m_email)

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Webverkooporders printen')
    msg.exec_()
    
def printGeg(filename, movbestnr):
    from sys import platform
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msgBox.setWindowTitle("Printen orderfactuur")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Wilt U factuur van ordernummer "+str(movbestnr)+" uitprinten?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        if platform == 'win32':
            os.startfile(filename, "print")
        else:
            os.system("lpr "+filename)
        printing()
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def kiesOrder(m_email):
    metadata = MetaData()
    orders_verkoop = Table('orders_verkoop', metadata,
        Column('ovbestelID', Integer, primary_key=True),
        Column('klantID', None, ForeignKey('klanten.klantID')),
        Column('ovbesteldatum', String),
        Column('datum_betaald', String),
        Column('datum_geleverd', String),
        Column('bedrag', Float))
    klanten = Table('klanten', metadata,
        Column('klantID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('rekening', String))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('aanhef', String),
        Column('voornaam', String), 
        Column('tussenvoegsel', String),
        Column('achternaam', String),
        Column('postcode', String),       
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('email', String),
        Column('telnr', String)) 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selord = select([orders_verkoop, klanten, accounts]).where(and_(orders_verkoop.c.klantID == klanten.c.klantID,\
                klanten.c.accountID == accounts.c.accountID, accounts.c.email == m_email))
    rpc = con.execute(selord).fetchone()
    if rpc:
        rpord = con.execute(selord)
    else:
        geenBest(m_email)
    
    mpostcode = rpc[14]
    mhuisnr = int(rpc[15])
    madres = checkpostcode(mpostcode,mhuisnr)
    mstraat = madres[0]
    mplaats = madres[1]
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 900, 900)
            self.setWindowTitle('Printen orderfacturen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.setColumnHidden(1,True)
            table_view.setColumnHidden(6,True)
            table_view.setColumnHidden(9,True)
            table_view.setColumnHidden(10,True)
            table_view.setColumnHidden(11,True)
            table_view.setColumnHidden(12,True)
            table_view.setColumnHidden(13,True)
            table_view.setColumnHidden(14,True)
            table_view.setColumnHidden(15,True)
            table_view.setColumnHidden(16,True)
            table_view.setColumnHidden(17,True)
            table_view.setColumnHidden(18,True)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(printFactuur)
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
            if not index.isValid():
                return None
            elif role != Qt.DisplayRole:
               return None
            veld = self.mylist[index.row()][index.column()]
            if type(veld) == float:
                return '{:>12.2f}'.format(round(veld,2))
            elif type(veld) == int:
                return '{:>9d}'.format(veld)
            else:
                return str(veld)
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
      
    header = ['Bestelnummer','','Besteldatum','Betaaldatum', 'Leverdatum','Totaalbedrag','', 'Accountnr',\
              'Rekeningnr','','','','','','','','','','']
    
    data_list=[]
    for row in rpord:
        data_list += [(row)]
        
    def Heading(movbestnr, mblad):
        kop=\
            ('Ordernummer: '+ str(movbestnr)+'          Datum: '+str(datetime.datetime.now())[0:10]+'      Besteldatum: '+str(rpc[2])+' Blad : '+str(mblad)+'\n'+
            '==============================================================================================\n'+
            'Artikelnr  Omschrijving                        Eenheid Aantal     Prijs   Subtotaal       BTW \n'+
            '==============================================================================================\n')
        return(kop)
        
    def printFactuur(idx):
        from sys import platform
        movbestnr = idx.data()
        if idx.column() == 0:
            metadata = MetaData()
            orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
                Column('ovaID', Integer, primary_key=True),
                Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
                Column('artikelID', None, ForeignKey('artikelen.artikelID')),
                Column('ovaantal', Integer),
                Column('ovleverdatum', String),
                Column('verkoopprijs', Float),
                Column('regel', Integer),
                Column('retour', Float),
                Column('betaaldatum', String),
                Column('leveringsdatum', String))
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer(), primary_key=True),
                Column('artikelomschrijving', String),
                Column('artikelprijs', Float),
                Column('art_voorraad', Float),
                Column('art_eenheid', String),
                Column('locatie_magazijn', String))
                
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selova = select([orders_verkoop_artikelen,artikelen]).where(and_(\
              orders_verkoop_artikelen.c.ovbestelID == movbestnr, orders_verkoop_artikelen\
              .c.artikelID == artikelen.c.artikelID)).order_by(orders_verkoop_artikelen.c.ovaID)
            rpova = con.execute(selova)
                
            mblad = 1
            rgl = 0
            if platform == 'win32':
                filename = '.\\forms\\Weborders_Facturen\\Weborder-factuur_'+str(rpc[0])+'.txt'
            else:
                filename = './forms/Weborders_Facturen/Weborder-factuur_'+str(rpc[0])+'.txt' 
            adreskop=\
            ('\n\n\n\n\n\n\nFACTUUR\n\n'+rpc[10]+' '+rpc[11]+' '+rpc[12]+' '+rpc[13]+',\n'+\
             mstraat+' '+rpc[15]+rpc[16]+',\n'+\
             rpc[14]+' '+mplaats+'.\n\n\n\n\n')
            open(filename,'w').write(adreskop)
            mtotaal = 0
            
            for row in rpova:
                if rgl == 0:
                    kop =  Heading(movbestnr, mblad)
                    open(filename, 'a').write(kop)
                    rgl = 16
                elif rgl%57 == 0:
                    mblad += 1
                    kop =  Heading(movbestnr, mblad)
                    open(filename, 'a').write(kop)
                msub = row[3]*row[5]
                open(filename,'a').write('{:<11d}'.format(row[2])+'{:<37.35s}'.format(row[11])+\
                 '{:>6s}'.format(row[14])+' '+'{:>6.2f}'.format(row[3])+'{:>10.2f}'.format(row[5])+\
                 ' '+'{:>10.2f}'.format(msub)+' '+'{:>10.2f}'.format(msub*21/121)+'\n')
                mtotaal = mtotaal+msub
                rgl += 1
           
            tail =(\
                   
            '----------------------------------------------------------------------------------------------\n'+
            'Totaal factuurbedrag inclusief 21% BTW                                  '+'{:10.2f}'.format(mtotaal)+' \n'+
            '==============================================================================================\n')    
            open(filename,'a').write(tail)
        printGeg(filename, movbestnr)
            
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)