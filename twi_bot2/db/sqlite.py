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
    def get_sql_type(self):
        raise NotImplementedError


class FieldInteger(Field):
    """
    INT
    INTEGER
    TINYINT
    SMALLINT
    MEDIUMINT
    BIGINT
    UNSIGNED BIG INT
    INT2
    INT8
    """

    def __init__(self, pk=False):
        self.pk = pk

    def get_sql_type(self):
        result = 'INTEGER'
        if self.pk:
            result += ' PRIMARY KEY'
        return result


class FieldText(Field):
    """
    CHARACTER(20)
    VARCHAR(255)
    VARYING CHARACTER(255)
    NCHAR(55)
    NATIVE CHARACTER(70)
    NVARCHAR(100)
    TEXT
    CLOB
    """
    pass


class FieldBlob(Field):
    """
    BLOB
    """
    pass


class FieldReal(Field):
    """
    REAL
    DOUBLE
    DOUBLE PRECISION
    FLOAT
    """
    pass


class FieldNumeric(Field):
    """
    NUMERIC
    DECIMAL(10,5)
    BOOLEAN
    DATE
    DATETIME
    """
    pass


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        fields = ['%s %s' % (k, v.get_sql_type()) for k, v in attrs.items() if isinstance(v, Field)]

        def create_table():
            sql = 'CREATE TABLE %s (%s)' % (name.lower(), ', '.join(fields))
            # log.debug('%', sql)
            print(sql)
            cursor = db.conn.cursor()
            cursor.execute(sql)
            db.conn.commit()

        attrs['create_table'] = staticmethod(create_table)
        return super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)


class Model(object):
    __metaclass__ = ModelMetaclass

    @staticmethod
    def create_table():
        pass


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    class Model2(Model):
        pk = FieldInteger(pk=True)


    Model2.create_table()
