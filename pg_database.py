import os
from peewee import *

conn = PostgresqlDatabase(os.environ['DATABASE_URL'])
class BaseModel(Model):
    class Meta:
        database = conn


class Artist(BaseModel):
    id = BigAutoField(column_name='id', null=False, primary_key=True)
    login = CharField(column_name='login', max_length=50)


def dbCheck():
    print('\nDB started')
    print(os.environ['DATABASE_URL'])

    print(conn)
    print('After classes')
    try:
        conn.connect()
        conn.create_tables([Artist])
    except Exception as e:
        print(e)
    # cursor = conn.cursor()

    print('closed\n')
    conn.close()


'''
    HERE IS GOING SQLAlchemy shit 
'''
# import os
# from sqlalchemy import *
# from sqlalchemy.dialects.postgresql.base import *
# import psycopg2
#
# engine = create_engine(os.environ['DATABASE_URL'], echo=True)
#
#
# class BaseModel(base):
#     __abstract__ = True
#
#     id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     created_at = Column(TIMESTAMP, nullable=False)
#     updated_at = Column(TIMESTAMP, nullable=False)
#
#     def __repr__(self):
#         return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
#
#
# class Artist(BaseModel):
#     __tablename__ = 'artists'
#
#     tg_id = Column(DOUBLE_PRECISION(), nullable=False, primary_key=True)
#     username = Column(VARCHAR(255), nullable=True)
#     first_name = Column(VARCHAR(255), nullable=True)
#     last_name = Column(VARCHAR(255), nullable=True)
#     chat_id = Column(DOUBLE_PRECISION(), nullable=True)
