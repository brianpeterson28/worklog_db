from peewee import *
import datetime

from models.employee import Employee

db = SqliteDatabase('time_entries.db')


class Time_Entry(Model):
    employee_name = ForeignKeyField(Employee, backref='time_entries')
    date = DateField(formats='%d/%m/%Y')
    title = TextField()
    time_spent = IntegerField()
    notes = TextField()

    class Meta:
        database = db


if __name__ == '__main__':
    pass
