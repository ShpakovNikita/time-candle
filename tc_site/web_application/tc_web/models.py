from peewee import *


db = PostgresqlDatabase('mydb', user='shaft', password='',
                        host='/var/run/postgresql', port=5432)
