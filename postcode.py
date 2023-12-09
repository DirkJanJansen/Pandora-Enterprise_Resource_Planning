def checkpostcode(mpostcode,mhuisnr): 
      from sqlalchemy import create_engine, Table, Column, ForeignKey
      from sqlalchemy import Integer, String, Boolean, MetaData, and_
      from sqlalchemy.sql import select 
      postcodes = Table('postcodes', MetaData(),
             Column('van', Integer),
             Column('tem', Integer),
             Column('postcode', String),
             Column('straatID', None, ForeignKey('straat.straatID')),
             Column('soort', Boolean))
      plaats = Table('plaats', MetaData(),
             Column('plaatsID', Integer, primary_key=True),
             Column('c_plaats', String))
      straat = Table('straat', MetaData(),
             Column('straatID', Integer, primary_key=True),
             Column('c_straat', String),
             Column('plaatsID', None, ForeignKey('plaats.plaatsID')))
      engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
      con = engine.connect()
      s = select(['*']).\
                where(and_(postcodes.c.straatID == straat.c.straatID,
                straat.c.plaatsID == plaats.c.plaatsID,     
                postcodes.c.postcode.like(mpostcode),
                (postcodes.c.van <= mhuisnr) & (postcodes.c.tem >= mhuisnr),
                postcodes.c.soort != mhuisnr%2))
      result = con.execute(s).first()
      if result:
           mstraat = str(result[6])
           mplaats = str(result[8])
           con.close()
           return (mstraat, mplaats)
      else:
           con.close()
           return('','')

