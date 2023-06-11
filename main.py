
STOP_WORDS = ["good bye", "close", "exit"]

contacts = {}

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
    name, phone = args[0][1], args[0][2]
    contacts[name] = phone
    return 'Contact added successfully'

@input_error
def change(*args):
    name, phone = args[0][1], args[0][2]
    if name in contacts:
        contacts[name] = phone
        return 'Phone number updated successfully'
    else:
        return 'Contact not found'

@input_error
def phone(*args):
    name = args[0][1]
    return contacts[name]

@input_error
def show_all(*args):
    if contacts:
        result = ''
        for name, phone in contacts.items():
            titel_name = name
            result += f'{titel_name.title()}: {phone}\n'
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
  
      
        

