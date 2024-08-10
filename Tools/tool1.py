from sqlalchemy import (Table, Column, Integer, MetaData,\
                         create_engine, Float, select, update)
import random

# before executing this script set param 99 in table param to 1 (in this year 2020, in 2021 to 0)
# this script forces to recalculate minimum stock and order sizes from all products
# This should normally happen after starting a new year
# and distribute the groups of categories from reservation in a better way.
# if you want to switch of certain parts delete the according #
# start the script once after setting the param 99 to 1 (in 2021 param to 0)
# after this start the program Pandora.py to recalculate
# if you want to switch off certain parts delete the according # before and after the code section


metadata = MetaData()
artikelen = Table('artikelen', metadata,
    Column('artikelID', Integer(), primary_key=True),
    Column('art_min_voorraad', Float),
    Column('art_bestelgrootte', Float),
    Column('categorie', Integer),
    Column('bestelsaldo', Float),
    Column('reserveringsaldo', Float),
    Column('jaarverbruik_1', Float),
    Column('jaarverbruik_2', Float))

engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()

selart = select([artikelen]).order_by(artikelen.c.artikelID)
rpart = con.execute(selart)

count = 0
for row in rpart:
    #'''
    if row[3] == 7 :
        updart1 = update(artikelen).where(artikelen.c.artikelID == row[0]).values(categorie = random.randint(5,9))
        con.execute(updart1)
    #'''
    
    #'''
    if row[3] == 8:
        updart1 = update(artikelen).where(artikelen.c.artikelID == row[0]).values(categorie = random.randint(5,9))
        con.execute(updart1)
    #'''
    
    #'''
    updart = update(artikelen).where(artikelen.c.artikelID == row[0]).\
      values(art_min_voorraad = 0, art_bestelgrootte = 0, jaarverbruik_1 = row[7])
    con.execute(updart)
    print(row, count)
    count += 1
    #'''
