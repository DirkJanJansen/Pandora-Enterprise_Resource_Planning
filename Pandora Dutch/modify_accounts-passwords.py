from sqlalchemy import (Table, Column, Integer, String, MetaData,
                        create_engine, select, update)

metadata = MetaData()
accounts = Table('accounts', metadata,
   Column('accountID', Integer(), primary_key=True),
   Column('email', String, nullable=False),
   Column('password', String, nullable=False))
engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
conn = engine.connect()
sel = select([accounts]).order_by(accounts.c.accountID)
rpaccount = conn.execute(sel)

plist = \
['$argon2id$v=19$m=65536,t=3,p=4$xUBFjNimSrn324RHtLtevg$fW7HS5uQfvyFvxPhxE6R9OzkN0OA6YhLrSoQq79phEU',
 '$argon2id$v=19$m=65536,t=3,p=4$7UbdLSI1mBAn/vN37aC+JA$mAMHtsYLNOQU52OjzqFljfJPXc1Y1V9BScUqc1byAt8',
 '$argon2id$v=19$m=65536,t=3,p=4$CVrbj4oI+H0AblVcZwcz7w$jFlv06Z/vaZ9kxAstrkcKJNpXngRv+6SD3Khmdetbg4',
 '$argon2id$v=19$m=65536,t=3,p=4$pL9M8Zng14EInZVrfOebGA$mfHdWzV79l8/sg6fo8fG8YSB/RPs1seScm030keWf2k',
 '$argon2id$v=19$m=65536,t=3,p=4$IM/hspCPgb8JPBvfhuXioQ$2GlujthcUGsbeXuJqrJA7JRgIkWnXN1CVdej0R/BNiQ',
 '$argon2id$v=19$m=65536,t=3,p=4$n7sbjGA/9kDCVKE3sEAmxg$5v9SOE9OIMVwR5MWeF+PyTzBuoROoOQQJwTlvGYVlkc',
 '$argon2id$v=19$m=65536,t=3,p=4$JbxhhvWkrc/jEr6OKfPXjg$MufWpeLiDTizdSkKc1DKbl4jX4GLOwEPX00/ewgwbbE',
 '$argon2id$v=19$m=65536,t=3,p=4$9AlvMHjozjPmzVQ+Z3Bi7g$AiDBmaQBcrUBZK2ghnUNukgtSj2wkhmBPx5NWEk43Gg',
 '$argon2id$v=19$m=65536,t=3,p=4$3pVyeOE0CdMAv0gdEBBkTw$T3qh5NUSJf4hI8zz5zEsSOiVOm3vlnGIp/9rh27E+s4',
 '$argon2id$v=19$m=65536,t=3,p=4$N0AvJ0wqMnUVEvk3iESDgg$kjt/9/FnKLSxROBrghLiUlLqbGjInE7G7yCMD6HkgKg',
 '$argon2id$v=19$m=65536,t=3,p=4$tknUnBeP2yPjvjVpomzQ0w$uuC+fxF0uZmCV8/TX733JcCug+nlWE4Bm9ZBEOxo/mY',
 '$argon2id$v=19$m=65536,t=3,p=4$O6Z8rzR93w8rWWFZg0jMxA$geil+9br29RhsiDfxCY4WB0d1MJ4kUV9aU+j/r6bg48',
 '$argon2id$v=19$m=65536,t=3,p=4$Qr31n1Y6hlUqqkUTmQyJ1w$0EgAIseLgWEQ7NoD0rd4OTOBK3bBNalbvISI1hjix2E',
 '$argon2id$v=19$m=65536,t=3,p=4$EcwYl341eSQLC1EQcGnUVQ$rBaNzMwWp6WyGqlEfdDRZVZiyeljq/+87sBDQaSz81U',
 '$argon2id$v=19$m=65536,t=3,p=4$dBnPtHkSHx1751ejAARoyA$u4Q7SkXtHZEcqw/fkyXoXKaMZV1wT0ilWiHIByPzGXs']

x = 0
for records in rpaccount:
    passwd = plist[x]
    upd = update(accounts).where(accounts.c.accountID==records[0]).values(password=passwd)
    conn.execute(upd)
    print(records[0],plist[x])
    x += 1



