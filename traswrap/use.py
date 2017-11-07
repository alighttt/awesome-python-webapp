import db, orm

db.create_engine()
# u = User(id=1, email='2246707520@qq.com', password='1246707520', admin=1, name='alight', image='imagecontent', created_at=1991.0201)
u = orm.User(id=1, email='1246707520@qq.com')
# print u.insert()
print u.select('id', 'name')
# print u.select('*')