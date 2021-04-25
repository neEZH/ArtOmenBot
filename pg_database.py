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
    login = CharField(column_name='login', null=False, max_length=50, unique=True)
    lastWork = CharField(column_name='lastWork', null=True, max_length=255)
    lastThumb = CharField(column_name='lastThumb', null=True, max_length=255)
    lastPost = DateTimeField(column_name='lastPost', null=True)

    def upd(self, work=None, thumb=None, post=None):
        self.lastWork = work if work is not None else self.lastWork
        self.lastThumb = thumb if thumb is not None else self.lastThumb
        self.lastPost = post if post is not None else self.lastPost


class User(AOB):
    class Meta:
        table_name = 'Users'

    id = DoubleField(column_name='tg_id', null=False, primary_key=True)
    username = CharField(column_name='username', null=True, max_length=255)
    name = CharField(column_name='name', null=False, max_length=255)
    lastName = CharField(column_name='Last_name', null=True, max_length=255)


class Subscribe(AOB):
    class Meta:
        table_name = 'Subscribes'
    id = BigAutoField(column_name='id', null=False,)
    userID = ForeignKeyField(User, backref='tg_id', column_name='user_TG_ID', null=True)
    artistID = ForeignKeyField(Artist, backref='id', column_name='artist_id', null=True)
    isActive = BooleanField(column_name='isActive', null=False, default=True)


def createDB():
    try:
        conn.connect()
        conn.create_tables([Artist, User, Subscribe])

    except Exception as e:
        print(e)
    # cursor = conn.cursor()
    conn.close()
