from enum import Enum


class PersonType(Enum):
    UNDEFINED = 0,
    STUDENT = 1,
    TEACHER = 2


class Person:
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.id = kwargs.get('id', -1)
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.middle_name = kwargs.get('middle_name', '')
        self.group = kwargs.get('group', '')
        self.type = kwargs.get('ptype', PersonType.UNDEFINED)

    def valid(self):
        return len(self.username) > 0

    def certname(self):
        return self.username

    def __str__(self):
        string = str()
        string += {PersonType.STUDENT: "Студент",
                   PersonType.TEACHER: "Преподаватель"}[self.type] + '\n'
        string += f'ID: {self.id}\n'
        string += f'NAME: {self.last_name} {self.first_name} {self.middle_name}\n'
        string += f'GROUP: {self.group}'
        return string
