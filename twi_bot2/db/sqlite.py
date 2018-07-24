# coding: utf-8
import sqlite3


# import logging


# log = logging.getLogger()


class DB(object):
    def __init__(self, name='db.sqlite'):
        self.conn = sqlite3.connect(name)

    def __del__(self):
        self.conn.close()


db = DB()


class Field(object):
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
        return ' '.join(result)


class FieldInteger(Field):
    sql_type = 'INTEGER'


class FieldText(Field):
    sql_type = 'TEXT'


class FieldBlob(Field):
    sql_type = 'BLOB'


class FieldReal(Field):
    sql_type = 'REAL'


class FieldNumeric(Field):
    # BOOLEAN, DATE, DATETIME
    sql_type = 'NUMERIC'


class FieldForeign(Field):
    sql_type = 'INTEGER'  # ?

    def __init__(self, model, **kwargs):
        self.model_name = model.__name__.lower()
        super(FieldForeign, self).__init__(**kwargs)

    def get_sql(self, name):
        result = super(FieldForeign, self).get_sql(name)
        sql = 'FOREIGN KEY(%s) REFERENCES %s(%s)' % (name, self.model_name, 'id')
        return ',\n  '.join((result, sql))


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name != 'Model':
            attrs['id'] = FieldInteger(pk=True)
            fields = [v.get_sql(k) for k, v in attrs.items() if isinstance(v, Field)]
            sql = 'CREATE TABLE IF NOT EXISTS %s (\n  %s\n);' % (name.lower(), ',\n  '.join(fields))
            print(sql)
            attrs['sql_create_table'] = sql
            # todo replace fields
        return super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)


class Model(object):
    __metaclass__ = ModelMetaclass
    sql_create_table = ''


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    class Device(Model):
        name = FieldText()

    class Pattern(Model):
        dev = FieldForeign(Device, null=False)


    cursor = db.conn.cursor()
    cursor.execute(Device.sql_create_table)
    cursor.execute(Pattern.sql_create_table)
    db.conn.commit()
