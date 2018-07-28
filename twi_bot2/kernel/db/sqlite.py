# coding: utf-8
import sqlite3


# import logging


# log = logging.getLogger()


class DB(object):
    def __init__(self, name='db.sqlite'):
        self.conn = sqlite3.connect(name)

    def __del__(self):
        self.conn.close()

    @staticmethod
    def sql_create_table(table, fields):
        return 'CREATE TABLE IF NOT EXISTS %s (\n  %s\n);' % (table, ',\n  '.join(fields))

    @staticmethod
    def sql_primary_key(*fields):
        return 'PRIMARY KEY(%s)' % (', '.join(fields))

    @staticmethod
    def sql_foreign_key(field, table2, field2='id'):
        # todo ON DELETE
        return 'FOREIGN KEY(%s) REFERENCES %s(%s)' % (field, table2, field2)

    @staticmethod
    def sql_insert(table, fields, values):
        assert len(fields) == len(values)
        return 'INSERT INTO %s (%s) VALUES(%s)' % (table, ', '.join(fields), ', '.join(values))


db = DB()


class AbstractField(object):
    pass


class Field(AbstractField):
    sql_type = ''

    def __init__(self, pk=False, unique=False, null=False, default=None):
        self.pk = pk
        self.unique = unique
        self.null = null
        self.default = default

    def get_sql(self, name):
        result = [name, self.sql_type]
        if self.pk:
            result.append('PRIMARY KEY')
        if self.unique:
            result.append('UNIQUE')
        if not self.null:
            result.append('NOT NULL')
        if self.default:
            result.append('DEFAULT %s' % self.default)
        return [' '.join(result)]

    def to_str(self, value):
        if value is None:
            if not self.null:
                raise ValueError('Not None')
            else:
                return 'null'
        # raise NotImplementedError todo


class FieldInteger(Field):
    sql_type = 'INTEGER'

    def to_str(self, value):
        return super(FieldInteger, self).to_str(value) or '%d' % int(value)


class FieldText(Field):
    sql_type = 'TEXT'

    def to_str(self, value):
        return super(FieldText, self).to_str(value) or "'%s'" % value


class FieldBlob(Field):
    sql_type = 'BLOB'


class FieldReal(Field):
    sql_type = 'REAL'


class FieldNumeric(Field):
    # BOOLEAN, DATE, DATETIME
    sql_type = 'NUMERIC'


class FieldForeign(Field):
    sql_type = 'INTEGER'

    def __init__(self, model, **kwargs):
        self.model_name = model.__name__.lower()
        super(FieldForeign, self).__init__(**kwargs)

    def get_sql(self, name):
        s1 = super(FieldForeign, self).get_sql(name)
        s2 = DB.sql_foreign_key(name, self.model_name)
        return s1, s2


class FieldManyToMany(AbstractField):
    def __init__(self, model):
        self.model = model

    def get_sql(self, model_name2):
        model_name1 = self.model.__name__.lower()
        model_name2 = model_name2.lower()
        table = ''.join((model_name1, model_name2))
        f1, f2 = '%s_id' % model_name1, '%s_id' % model_name2
        fields = [
            ',\n  '.join(FieldInteger().get_sql(f1)),
            ',\n  '.join(FieldInteger().get_sql(f2)),
            DB.sql_primary_key(f1, f2),
            DB.sql_foreign_key(f1, model_name1),
            DB.sql_foreign_key(f2, model_name2),
        ]
        return DB.sql_create_table(table, fields)


class Manager(object):
    def __init__(self, table, fields):
        self._table = table
        self._fields = fields

    def all(self):
        result = []
        fields = self._fields.keys()
        sql = 'SELECT %s FROM %s' % (', '.join(fields), self._table)
        print(sql)

        cursor = db.conn.cursor()
        cursor.execute(sql)
        for i in cursor.fetchall():
            d = {}
            for k, v in zip(fields, i):
                d[k] = v
            result.append(d)
        cursor.close()
        return result


class FakeManager(object):
    def all(self):
        return []


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name != 'Model':
            mcs.init(attrs, name)
        return super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)

    @staticmethod
    def init(attrs, name):
        if 'id' not in attrs:
            attrs['id'] = FieldInteger(pk=True, null=True)

        fields = {}
        for k, v in attrs.items():
            if isinstance(v, AbstractField):
                fields[k] = v
        attrs['_fields'] = fields

        attrs['objects'] = Manager(name.lower(), fields)

        result, ls = [], []
        for k, v in fields.items():
            if isinstance(v, Field):
                ls.extend(v.get_sql(k))
            elif isinstance(v, FieldManyToMany):
                result.append(v.get_sql(name))
            else:
                raise NotImplementedError
        result.insert(0, DB.sql_create_table(name.lower(), ls))
        attrs['sql_create_table'] = result


class Model(object):
    __metaclass__ = ModelMetaclass
    _fields = {}
    sql_create_table = ''
    objects = FakeManager()

    def __init__(self, **kwargs):
        assert self._fields
        assert self.sql_create_table
        assert isinstance(self.objects, Manager)
        for name in self._fields.keys():
            self.__setattr__(name, None)
        for name, value in kwargs.items():
            if name not in self._fields.keys():
                raise ValueError('field %d not exist in model' % name)
            self.__setattr__(name, value)

    def save(self):
        # is_insert = self.__getattribute__('__is_insert')
        # is_update = self.__getattribute__('__is_update')
        r1, r2 = [], []
        for name, f in self._fields.items():
            value = self.__getattribute__(name)
            r1.append(name)
            r2.append(f.to_str(value))

        sql = db.sql_insert(self.__class__.__name__.lower(), r1, r2)
        print(sql)

        cursor = db.conn.cursor()
        cursor.execute(sql)  # todo parameters
        cursor.close()
        db.conn.commit()


def test():
    class Device(Model):
        name = FieldText()

    class Pattern(Model):
        name = FieldText()
        devices = FieldManyToMany(Device)

    ls = Device.objects.all()
    print(ls)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    test()
