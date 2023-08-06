import functools
import logging

from easyorm.db_pool import DbPool
from easyorm.page import Page

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        logging.debug('method=[{0}], sql=[{1}], args=[{2}]'.format(func.__name__, args[0], args[1]))
        r = func(*args, **kw)
        return r

    return wrapper


def create_pool(**kw):
    logging.info('create db connection pool...')
    global __pool
    __pool = DbPool(
        host=kw.get('host'),
        port=kw.get('port', 3306),
        username=kw.get('username'),
        password=kw.get('password'),
        database=kw.get('database'))


@log
def select(sql, args=None):
    global __pool
    if args is None:
        args = []
    conn = __pool.get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql.replace('?', '%s'), args)
        return cur.fetchall()
    except Exception as e:
        logging.error('execute sql ({0}) error {1}'.format(sql, e))
        raise e
    finally:
        __pool.put_conn(conn)


@log
def execute(sql, args=None):
    global __pool
    if args is None:
        args = []
    affect_row = 0
    conn = __pool.get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql.replace('?', '%s'), args)
        affect_row = cur.rowcount
        conn.commit()
    except Exception as e:
        logging.error('execute sql ({0}) error {1}'.format(sql, e))
        conn.rollback()
    finally:
        __pool.put_conn(conn)
    return affect_row


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


class ModelMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)
        table_name = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, table_name))
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primary_key:
                        raise Exception('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise Exception('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primary_key, ', '.join(escaped_fields), table_name)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            table_name, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (table_name, primary_key)
        return type.__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    def assemble_sql(cls, where, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        order_by = kw.get('orderBy', None)
        if order_by:
            sql.append('order by')
            sql.append(order_by)
        return sql

    @classmethod
    def page(cls, where=None, args=None, page=Page(1, 10), **kw):
        c = cls.count(where, args)
        page.total = c
        sql = cls.assemble_sql(where, **kw)
        if args is None:
            args = []
        current = page.current
        size = page.size
        limit_start = (current - 1) * size
        sql.append('limit ?, ?')
        args.extend((limit_start, size))
        rs = select(' '.join(sql), args)
        data = [cls(**r) for r in rs]
        page.data = data
        return page

    @classmethod
    def find_all(cls, where=None, args=None, **kw):
        """ find objects by where clause. """
        if args is None:
            args = []
        sql = cls.assemble_sql(where, **kw)
        rs = select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    def count(cls, where=None, args=None):
        sql = ['select count(*) c from `%s`' % cls.__table__]
        if where:
            sql.append('where')
            sql.append(where)
        rs = select(' '.join(sql), args)
        return rs[0]['c']

    @classmethod
    def find_number(cls, select_field, where=None, args=None):
        """ find number by select and where. """
        sql = ['select %s _num_ from `%s`' % (select_field, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = select(' '.join(sql), args)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    def find(cls, pk):
        """ find object by primary key. """
        rs = select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk])
        if len(rs) == 0:
            return None
        return cls(**rs[0])


    def save(self):
        args = list(map(self.get_value_or_default, self.__fields__))
        args.append(self.get_value_or_default(self.__primary_key__))
        rows = execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    def update_(self):
        args = list(map(self.get_value, self.__fields__))
        args.append(self.get_value(self.__primary_key__))
        rows = execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    def remove(self):
        args = [self.get_value(self.__primary_key__)]
        rows = execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
