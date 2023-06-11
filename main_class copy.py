from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def update(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return str(self.name)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def update_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.update(new_phone)
                break


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record
