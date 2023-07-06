from datetime import datetime
from collections import UserDict
import pickle, os
from termcolor import colored, cprint

class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def write_data(self):   
        with open(path_to_db, 'wb') as file: 
            pickle.dump(self.data, file)
    
    def read_data(self):        
        with open(path_to_db, 'rb') as file:
            self.data = pickle.load(file)
    
    def find(self, word_input):        
        rset = set()
        for k, v in self.data.items():
            if k == word_input:
                rset.add(k)
                continue
            elif v.phones[0].value == word_input:
                 rset.add(k)
        return list(rset)
        
    def __iter__(self):
        return self.iterator()

    def iterator(self, batch_size=1):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0

        while current_index < total_records:
            yield records[current_index:current_index + batch_size]
            current_index += batch_size

    def __next__(self):
        raise StopIteration

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()                            
            next_birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y").replace(year=today.year).date()
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 12:
            raise ValueError("Phone number must be '380XXXXXXXXX'")

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format")


STOP_WORDS = ["good bye", "close", "exit"]
path_to_db = 'db.bin'
address_book = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Insufficient arguments"
    return inner

def hello(*args):
    return "How can I help you?"

@input_error
def add(*args):
    name, *phones = args[0][1:]
    record = Record(name)
    for item in phones:
        if item.startswith("birth="):
            birthday_value = item.split("=")[1]
            record.birthday = Birthday(birthday_value)
        else:
            record.add_phone(Phone(item))
    address_book.add_record(record)
    return 'Contact added successfully'

@input_error
def change(*args):
    name, *phones = args[0][1:]
    if name in address_book.data:
        record = address_book.data[name]
        for i, phone in enumerate(phones):
            record.edit_phone(record.phones[i], Phone(phone))
        return 'Contact updated successfully'
    else:
        return 'Contact not found'

@input_error
def phone(*args):
    name = args[0][1]
    if name in address_book.data:
        record = address_book.data[name]
        if record.phones:
            return ", ".join([phone.value for phone in record.phones])
        else:
            return 'No phone number found for this contact'
    else:
        return 'Contact not found'

@input_error
def show_all(*args):
    if address_book.data:
        batch_size = 2  # count on page
        iterator = address_book.iterator(batch_size)

        try:
            while True:
                batch = next(iterator)
                for record in batch:
                    phones = [phone.value for phone in record.phones]
                    result = f'{record.name.value.title()}, days to birthday = {record.days_to_birthday()}: {", ".join(phones)}'
                    print(result)
                print("---")

                # Check enter
                choice = input("Press Enter to view the next page, or 'q' to exit: ")
                if choice.lower() == 'q':
                    break
        except StopIteration:
            pass
    else:
        return 'No contacts found'


def close(word):
    return word in STOP_WORDS

def find(word):
    lfind = address_book.find(word[1])
    return lfind if lfind else 'nothing found'
     
OPERATIONS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show_all': show_all,
    'find': find     
}

def get_handler(operator):
    return OPERATIONS.get(operator, lambda x: "I don't know such a command")


def input_text():
    text = 'Input some command: ' 
    return input(text).lower().split(' ')

def main():

    if os.path.exists(path_to_db):        
            address_book.read_data() 

    greeting_text = '----------------------- \n \
    List of commands: \n \
    "hello"\n \
    "add"\n \
    "change"\n \
    "phone"\n \
    "show_all"\n \
    New command "Find" if you want to find some records'

    cprint(greeting_text, 'blue')

    while True:
        user_input = input_text()
        if len(user_input) > 0:
            command = user_input[0]
            if close(command):                
                address_book.write_data()               
                cprint("Good bye!", 'blue')
                break
            else:
                handler = OPERATIONS.get(command, lambda x: "I don't know such a command")
                cprint(handler(user_input), 'green')

if __name__ == '__main__':
    main()






