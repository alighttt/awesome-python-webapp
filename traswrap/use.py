import db

db.create_engine()

print db.update("insert into testtable (name, sex, birthday) values ('xiaoguang', 'm', '2017-01-20')")

for row in db.select("select * from testtable"):
    print row

# cur = db.engine.connect().cursor()
# cur.execute('select * from testtable')
# for row in cur.fetchall():
#     print row
# cur.close()
# print "aa"