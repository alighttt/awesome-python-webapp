# from __main__ import traceback
import threading
import MySQLdb

name = 'db_name'

class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect()
    
engine = None


def create_engine(user='root', passwd='123456', db='awesome', host='localhost', port=3306):
    connectfunc = lambda :MySQLdb.connect(user=user, passwd=passwd, db=db, host=host, port=port)
    global engine
    engine = _Engine(connectfunc)


class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0
         
    def is_init(self):
        return not self.connection is None
     
    def init(self):
        global engine
        self.connection = engine.connect()
        self.transactions = 0
         
    def cleanup(self):
        self.connection.close()
        self.connection = None
         
    def cursor(self):
        return self.connection.cursor()
     
_db_ctx = _DbCtx()
 
 
class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self
     
    def __exit__(self):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()
 

def with_connection(func):
    def wrapper(*args, **kw):
        connectionctx = _ConnectionCtx()
        connectionctx.__enter__()
        rs = func(*args, **kw)
        connectionctx.__exit__()
        return rs
    return wrapper

@with_connection
def select(sql, *args):
    global _db_ctx
    cur = _db_ctx.cursor()
    cur.execute(sql)
    rs = []
    for row in cur.fetchall():
        rs.append(row)
    return rs

@with_connection
def update(sql, *args):
    global _db_ctx
    cur = _db_ctx.cursor()
    cur.execute(sql)
    rowcount = cur.rowcount
    _db_ctx.connection.commit()
    return rowcount

    

class _TransactionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        return self
 
    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()
 
    def commit(self):
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            _db_ctx.connection.rollback()
            raise
 
    def rollback(self):
        global _db_ctx
        _db_ctx.connection.rollback()
          
