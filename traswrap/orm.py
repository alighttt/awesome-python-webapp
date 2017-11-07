import db

class Field(object):
    def __init__(self, column_type):
        self.column_type = column_type
    def __str__(self):
        return '<%s>' % (self.__class__.__name__)

class StringField(Field):
    def __init__(self):
        super(StringField, self).__init__('varchar(100)')
        
class TextField(Field):
    def __init__(self):
        super(TextField, self).__init__('text')

class BooleanField(Field):
    def __init__(self):
        super(BooleanField, self).__init__('tinyint(1)')
        
class IntegerField(Field):
    def __init__(self):
        super(IntegerField, self).__init__('bigint')

class FloatField(Field):
    def __init__(self):
        super(FloatField, self).__init__('numeric(15,3)')
        
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __metaclass__ = ModelMetaclass
    def insert(self):
        fields = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(k)
            args.append('"' + str(self.get(k)) + '"')
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args))
        return db.update(sql)
    def select(self, *key):
        args = []
        for k, v in self.__mappings__.iteritems():
            if not self.get(k) is None :
                args.append(str(k) + '="' + str(self.get(k)) + '"')
        sql = 'select %s from %s where %s' % (','.join(key), self.__table__, ' and '.join(args))
        d = db.select(sql)
        return d if d else None

    
class User(Model):
    __table__ = 'users'
    id = StringField()
    email = StringField()
    password = StringField()
    admin = BooleanField()
    name = StringField()
    image = StringField()
    created_at = FloatField()

 
class Blog(Model):
    __table__ = 'blogs'
    id = StringField()
    user_id = StringField()
    user_name = StringField()
    user_image = StringField()
    name = StringField()
    summary = StringField()
    content = TextField()
    created_at = FloatField()
 
class Comment(Model):
    __table__ = 'comments'
    id = StringField()
    blog_id = StringField()
    user_id = StringField()
    user_name = StringField()
    user_image = StringField()
    content = TextField()
    created_at = FloatField()
