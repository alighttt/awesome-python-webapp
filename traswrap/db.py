# from __main__ import traceback
import MySQLdb

class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect()
    
engine = None


def create_engine(user='root', passwd='123456', db='test', host='localhost', port=3306):
    connectfunc = lambda :MySQLdb.connect(user=user, passwd=passwd, db=db, host=host, port=port)
    engine = _Engine(connectfunc)
    
create_engine()
cur = engine.connect().cursor()
cur.execute('select * from testtable')
for row in cur.fetchall():
    print row
cur.close()
print "aa"


# class _DbCtx(threading.local):
#     def __init__(self):
#         self.connection = None
#         self.transactions = 0
#         
#     def is_init(self):
#         return not self.connection is None
#     
#     def init(self):
#         self.connection = _LasyConnection()
#         self.transactions = 0
#         
#     def cleanup(self):
#         self.connection.cleanup()
#         self.connection = None
#         
#     def cursor(self):
#         return self.connection.cursor()
#     
# _db_ctx = _DbCtx()
# 
# 
# class _ConnectionCtr(object):
#     def __enter__(self):
#         global _db_ctx
#         self.should_cleanup = False
#         if not _db_ctx.is_init():
#             _db_ctx.init()
#             self.should_cleanup = True
#         return self
#     
#     def __exit__(self, exctype, excvalue, traceback):
#         global _db_ctx
#         if self.should_cleanup:
#             _db_ctx.cleanup()
# 
#  
# def connection():
#     return _ConnectionCtr()
# 
# 
# @with_connection
# def select(sql, *args):
#     pass
#     
#       
# @with_connection
# def update(sql, *args):
#     pass
# 
# 
# class _TransactionCtx(object):
#     def __enter__(self):
#         global _db_ctx
#         self.should_close_conn = False
#         if not _db_ctx.is_init():
#             _db_ctx.init()
#             self.should_close_conn = True
#         _db_ctx.transactions = _db_ctx.transactions + 1
#         return self
# 
#     def __exit__(self, exctype, excvalue, traceback):
#         global _db_ctx
#         _db_ctx.transactions = _db_ctx.transactions - 1
#         try:
#             if _db_ctx.transactions == 0:
#                 if exctype is None:
#                     self.commit()
#                 else:
#                     self.rollback()
#         finally:
#             if self.should_close_conn:
#                 _db_ctx.cleanup()
# 
#     def commit(self):
#         global _db_ctx
#         try:
#             _db_ctx.connection.commit()
#         except:
#             _db_ctx.connection.rollback()
#             raise
# 
#     def rollback(self):
#         global _db_ctx
#         _db_ctx.connection.rollback()
#          
