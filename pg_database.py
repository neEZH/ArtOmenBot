import os
from peewee import *
from playhouse.db_url import connect
import logging


logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = conn


class AOB(BaseModel):
    class Meta:
        schema = 'aob'


class Artist(AOB):
    class Meta:
        table_name = 'Artists'

    id = BigAutoField(column_name='id', null=False, primary_key=True)
    login = CharField(column_name='login', null=False, max_length=50)
    lastWork = CharField(column_name='lastWork', null=True, max_length=255)
    lastThumb = CharField(column_name='lastThumb', null=True, max_length=255)
    lastPost = DateTimeField(column_name='lastPost', null=True)


class User(AOB):
    class Meta:
        table_name = 'Users'

    id = DoubleField(column_name='tg_id', null=False, primary_key=True)
    username = DoubleField(column_name='username', null=True)
    name = CharField(column_name='name', null=False)
    lastName = CharField(column_name='Last_name', null=True)
    chatID = DoubleField(column_name='chat_id', null=False)


def createDB():
    try:
        conn.connect()
        conn.create_tables([Artist, User])

    except Exception as e:
        print(e)
    # cursor = conn.cursor()
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
