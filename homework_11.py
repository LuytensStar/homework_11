from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

class Name(Field):
    pass

class Phone(Field):
    
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must be 10 digits")
        self.__value = value

class Birthday(Field):

    def __init__(self, birthday):
        self.__value = birthday

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
            self.__value = value
        except ValueError:
            raise ValueError("Birthday must be in the format dd-mm-yyyy")
        


class Record:

    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now()
            birthday_date = datetime.strptime(self.birthday.value, '%d-%m-%Y')
            print(birthday_date)
            next_birthday = datetime(now.year, birthday_date.month, birthday_date.day)
            if now > next_birthday:
                next_birthday = datetime(now.year + 1, birthday_date.month, birthday_date.day)
            return (next_birthday - now).days
        else:
            return None

    def __str__(self):
        phones = "; ".join([str(phone.value) for phone in self.phones])
        return f"Contact name: {self.name.value}, phones: {phones}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i+n]


book = AddressBook()

birthday = '15-05-1423'



john = Record('John', birthday)
print(john.days_to_birthday())

john.add_phone('1231231331')
mary = Record('Mary')
paul = Record('Paul')

book.add_record(john)
book.add_record(mary)
book.add_record(paul)

for i in book.iterator(2):
    for record in i:
        print(record)