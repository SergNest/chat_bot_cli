from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

STOP_WORDS = ["good bye", "close", "exit"]

address_book = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input"
        except IndexError:
            return "Insufficient arguments"
    return inner

def hello(*args):
    return "How can I help you?"

@input_error
def add(*args):
    name, *phones = args[0][1:]
    record = Record(name)
    for phone in phones:
        record.add_phone(Phone(phone))
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
        if record.phone:
            return record.phone.value
        else:
            return 'No phone number found for this contact'
    else:
        return 'Contact not found'

@input_error
def show_all(*args):
    if address_book.data:
        result = ''
        for name, record in address_book.data.items():
            phones = [phone.value for phone in record.phones]
            result += f'{name.title()}: {", ".join(phones)}\n'
        return result
    else:
        return 'No contacts found'


def close(word):
    return word in STOP_WORDS

OPERATIONS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show_all': show_all    
}

def get_handler(operator):
    return OPERATIONS.get(operator, lambda x: "I don't know such a command")

def input_text():
    return input('Input some command: ').lower().split(' ')

def main():
    while True:
        user_input = input_text()
        if len(user_input) > 0:
            command = user_input[0]
            if close(command):
                print("Good bye!")
                break
            else:
                handler = OPERATIONS.get(command, lambda x: "I don't know such a command")
                print(handler(user_input))

if __name__ == '__main__':
    main()