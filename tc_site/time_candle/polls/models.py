from peewee import *


db = PostgresqlDatabase('mydb', user='shaft', password='',
                           host='/var/run/postgresql', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Question(BaseModel):
    question_text = CharField(max_length=200)
    pub_date = DateTimeField(default=None,
                             null=True)


class Choice(BaseModel):
    question = ForeignKeyField(Question, on_delete='CASCADE')
    choice_text = CharField(max_length=200)
    votes = IntegerField(default=0)


def create_tables():
    with db:
        db.create_tables([Choice, Question])


create_tables()