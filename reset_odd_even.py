import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine,\
                     Float, update

metadata = MetaData()
params = Table('params', metadata,
       Column('paramID', Integer(), primary_key=True),
       Column('item', String),
       Column('tarief', Float))

engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()

mjaar = int(str(datetime.date.today())[0:4])
updeven = update(params).where(params.c.paramID == 99).values(tarief = int(mjaar%2))
con.execute(updeven)
