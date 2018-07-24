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

    def get_sql(self, name):
        return '%s %s' % (name, self.sql_type)


class FieldInteger(Field):
    def __init__(self, pk=False):
        self.pk = pk

    @property
    def sql_type(self):
        result = 'INTEGER'
        if self.pk:
            result += ' PRIMARY KEY'
        return result


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
    def __init__(self, model):
        self.model_name = model.__name__.lower()

    def get_sql(self, name):
        return '%s INTEGER,\n  FOREIGN KEY(%s) REFERENCES %s(%s)' % (name, name, self.model_name, 'id')


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name != 'Model':
            attrs['id'] = FieldInteger(pk=True)
            fields = [v.get_sql(k) for k, v in attrs.items() if isinstance(v, Field)]
            sql = 'CREATE TABLE %s (\n  %s\n);' % (name.lower(), ',\n  '.join(fields))
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
        dev = FieldText()

    class Pattern(Model):
        dev = FieldForeign(Device)


    cursor = db.conn.cursor()
    cursor.execute(Device.sql_create_table)
    cursor.execute(Pattern.sql_create_table)
    db.conn.commit()
