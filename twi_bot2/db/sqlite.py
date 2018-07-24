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
        return 'CREATE TABLE IF NOT EXISTS %s (\n  %s\n);' % (table.lower(), ',\n  '.join(fields))

    @staticmethod
    def sql_primary_key(*fields):
        return 'PRIMARY KEY(%s)' % (', '.join(fields))

    @staticmethod
    def sql_foreign_key(field, table2, field2='id'):
        # todo ON DELETE
        return 'FOREIGN KEY(%s) REFERENCES %s(%s)' % (field, table2, field2)


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
    sql_type = 'INTEGER'

    def __init__(self, model, **kwargs):
        self.model_name = model.__name__.lower()
        super(FieldForeign, self).__init__(**kwargs)

    def get_sql(self, name):
        result = super(FieldForeign, self).get_sql(name)
        sql = DB.sql_foreign_key(name, self.model_name)
        return result, sql


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


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name != 'Model':
            sql = []
            fields = []
            attrs['id'] = FieldInteger(pk=True)
            for k, v in attrs.items():
                if not isinstance(v, AbstractField):
                    continue
                if isinstance(v, Field):
                    fields.extend(v.get_sql(k))
                elif isinstance(v, FieldManyToMany):
                    sql.append(v.get_sql(name))
                else:
                    raise NotImplementedError

            sql.insert(0, DB.sql_create_table(name, fields))
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
        name = FieldText()
        devices = FieldManyToMany(Device)


    cursor = db.conn.cursor()
    for ls in Device.sql_create_table, Pattern.sql_create_table:
        for sql in ls:
            print(sql)
            cursor.execute(sql)
    db.conn.commit()
