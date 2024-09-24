from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine,\
                        ForeignKey, Float, select, update, insert, func, and_, Boolean)

metadata = MetaData()
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
werken = Table('werken', metadata,
   Column('werknummerID', Integer(), primary_key=True),
   Column('begr_sleuvengraver_uren', Float),
   Column('begr_persapparaat_uren', Float),
   Column('begr_atlaskraan_uren', Float),
   Column('begr_kraan_groot_uren', Float),
   Column('begr_mainliner_uren', Float),
   Column('begr_hormachine_uren', Float),
   Column('begr_wagon_uren', Float),
   Column('begr_locomotor_uren', Float),
   Column('begr_locomotief_uren', Float),
   Column('begr_montagewagen_uren', Float),
   Column('begr_stormobiel_uren', Float),
   Column('begr_robeltrein_uren', Float))
engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()
selcal = select([calculaties]).order_by(calculaties.c.koppelnummer)
rpcal = con.execute(selcal)

for row in rpcal:
    upd = update(werken).where(werken.c.werknummerID == calculaties.c.koppelnummer).values(begr_sleuvengraver_uren = werken.c.begr_sleuvengraver_uren+calculaties.c.sleuvengraver,\
        begr_persapparaat_uren = werken.c.begr_persapparaat_uren+calculaties.c.persapparaat, begr_atlaskraan_uren=werken.c.begr_atlaskraan_uren+calculaties.c.atlaskraan,\
        begr_kraan_groot_uren= werken.c.begr_kraan_groot_uren+calculaties.c.kraan_groot, begr_mainliner_uren=werken.c.begr_mainliner_uren+calculaties.c.mainliner,\
        begr_hormachine_uren=werken.c.begr_hormachine_uren+calculaties.c.hormachine,begr_wagon_uren= werken.c.begr_wagon_uren+calculaties.c.wagon, begr_locomotor_uren=werken.c.begr_locomotor_uren+calculaties.c.locomotor,\
        begr_locomotief_uren=werken.c.begr_locomotief_uren+calculaties.c.locomotief, begr_montagewagen_uren=werken.c.begr_montagewagen_uren+calculaties.c.montagewagen,\
        begr_stormobiel_uren=werken.c.begr_stormobiel_uren+calculaties.c.stormobiel, begr_robeltrein_uren=werken.c.begr_robeltrein_uren+calculaties.c.robeltrein)
    con.execute(upd)


