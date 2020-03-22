import barcode
from barcode.writer import ImageWriter #for barcode as png
from sqlalchemy import (Table, Column, String, Integer, MetaData,\
                         create_engine, select, update)

metadata = MetaData()
artikelen = Table('artikelen', metadata,
    Column('artikelID', Integer(), primary_key=True),
    Column('barcode', String(13))) 

engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()
selart = select([artikelen]).order_by(artikelen.c.artikelID)
rpart = con.execute(selart)

x = 1
for row in rpart:
    ean = barcode.get('ean13', '800'+str(row[0]), writer=ImageWriter()) # for barcode as png
    barc = ean.get_fullcode()  
    print(barc) # follow the writing
    
    if x < 11:
       filename = ean.save(str(row[0])) # save 10 barcodes for the time being
    x += 1
    
    # filename = ean.save(str(row[0])) 
    # save the barcodes with the <name of artikelID>.svg
    # if started outside the if clause these are 3775 pictures!!! 
     
    upd = update(artikelen).where(artikelen.c.artikelID == row[0]).values(barcode = ean.get_fullcode())
    con.execute(upd)
    
    # here the 3775 numbers are written as barcode eancode 13 to the fields barcode in artikelen

