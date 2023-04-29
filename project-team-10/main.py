import time
import sys
from collections import UserDict
from datetime import date, timedelta
import re
import pickle
import os


NOT_DEFINED = "not defined"
ADRESSBOOK = "book.bin"


class AddressBook(UserDict):

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value

    def save_to_file(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

    def read_from_file(self, filename):
        with open(filename, "rb") as fh:
            read = pickle.load(fh)
        return read

    def iterator(self, n=1):  # n indicates number of record to take for each iteration
        recorded = 0
        output = []
        for record in self.data:
            if (recorded < n):
                output.append(self.data[record])
                recorded += 1
            else:  # recorded == n
                yield output
                recorded = 1
                output = [self.data[record]]
        yield output

    def add_record(self, record):  # adding record type Record into the dictionary
        self.data[record.name.value] = record

    def print(self):
        for name in self.data:
            self.data[name].print()


class Record:  # responsible for the record manipulation

    def __init__(self, name):
        self.name = name  # type of Name
        self.phone = []
        self.email = []
        self.birthday = Birthday()

    def set_birthday(self, s):
        self.birthday.day = check_birthday(s)

    def days_to_birthday(self):
        today = date.today()
        result = self.birthday.day
        if result != "":
            inputdate = result.split("/")
            birthday = date(year=int(inputdate[0]), month=int(
                inputdate[1]), day=int(inputdate[2]))
            thisbirthday = date(
                year=today.year, month=birthday.month, day=birthday.day)
            if today.month > birthday.month:  # birthday has passed
                nextbirthday = date(year=today.year + 1,
                                    month=birthday.month, day=birthday.day)
            else:  # still will be
                nextbirthday = date(
                    year=today.year, month=birthday.month, day=birthday.day)
            delta = nextbirthday - today
            return (f"Days left: {delta.days}")
        else:
            return "No date of birth defined yet"

    def add_phone(self, phone):
        self.phone.append(phone)
        return (f"add phone: {phone.value} for {self.name.value}")

    def find_phone(self, phone):
        for ph in self.phone:
            if ph.value == phone:
                return ph
        return Phone()

    def find_email(self, email):
        for ph in self.email:
            if ph.value == email:
                return ph
        return Email()

    def remove_phone(self, strphone):
        try:
            phone = self.find_phone(strphone)
            self.phone.remove(phone)
            return f"{phone.value} removed"
        except ValueError:
            return f"can not remove phone {strphone}: does not exist"

    def edit_phone(phone):  # to be defined in next H/W
        pass

    def add_email(self, email):
        self.email.append(email)
        return (f"add email: {email.value}")

    def remove_email(self, stremail):
        try:
            email = self.find_email(stremail)
            self.email.remove(email)
            return f"{email.value} removed"
        except ValueError:
            return f"can not remove email {stremail}: does not exist"

    def edit_email(email):  # to be defined in next H/W
        pass

    def print_phones(self):
        print("Phones: ")
        for phone in self.phone:
            print(phone.value)

    def print_emails(self):
        print("Emails: ")
        for email in self.email:
            print(email.value)

    def print(self):
        print("Name: " + self.name.value)
        self.print_phones()
        self.print_emails()


class Field:  # defines general fields properties TBD
    def __init__(self, value):
        self.value = value


class Name(Field):  # mandatory field
    def __init__(self, value):
        self.value = value


class Phone(Field):  # nonmandatory field
    def __init__(self, phone=NOT_DEFINED):
        self.__value = phone

    @property  # define getter
    def value(self):
        return self.__value

    @value.setter  # define setter
    def value(self, val):
        match = re.fullmatch(
            r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", val)
        if not match:
            raise ValueError(">> Phone number is not  correct.\n")
        else:
            self.__value = val


class Email(Field):  # nonmandatory field
    def __init__(self, email=NOT_DEFINED):
        self.value = email


class Birthday:
    # will keep it in format yyyy/mm/dd
    def __init__(self):
        self.__birthday = ""

    @property  # define getter
    def day(self):
        return self.__birthday

    @day.setter  # define setter
    def day(self, val):
        match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
        if not match:
            raise ValueError(">> Date is not  correct date.\n")
        else:
            self.__birthday = val


def do_something():
    output = """ here we created the following classes:\n 
    - AdressBook \n 
    - Record \n 
    - Field \n 
    - Name \n 
    - Phone \n 
    - Email \n
    and added some functionality which will be developed in the next H/Ws"""
    print(output)


def output(list):  # list of records
    s = ""
    for record in list:
        s += record.name.value + " "
    return s


def check_birthday(val):
    match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
    while not match:
        print(">> Please input correct date. Typically it is yyyy/mm/dd")
        val = input(">> ").lower()
        match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
    return val


exit_list = ["good bye", "close", "exit", "close"]


# list of commands to use

HELLO_CMD = "hello"
ADD_CMD = "add"
CHANGE_CMD = "change"
PHONE_CMD = "phone"
SHOW_CMD = "show all"
HLP_CMD = "help"
SRCH_CMD = "search"

COMMANDS = [HELLO_CMD, ADD_CMD, CHANGE_CMD,
            PHONE_CMD, SHOW_CMD, HLP_CMD, SRCH_CMD]


def parser(line):
    return re.sub("[^0-9a-zA-Z+()-]", " ", line).split()


GREETING = "How can I help you ? For the commands description please type help"
NOTHING = "There is nothing to execute"
UNDERSTOOD = "Understood"


def wait():
    print(">> Please wait....")
    time.sleep(2)


def check_name(name):
    match = re.fullmatch("[a-zA-Z]+", name)
    while not match:
        print(">> Please input correct name. It should include only letters")
        name = input(">> ").lower()
        match = re.fullmatch("[a-zA-Z]+", name)
    return name


def check_phone(phone):
    match = re.fullmatch(
        r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", phone)
    while not match:
        print(">> Please input correct phone. Typically it is +1(647)861-9006 or similar")
        phone = input(">> ").lower()
        match = re.fullmatch(
            r"[+]?[0-9]{1,2}(\([0-9]{3}\)|[0-9]{3})[0-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", phone)
    return phone


def add_process(words):
    command = words[0]
    if len(words) == 3:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "Check phone info for " + name)
        wait()
        phone = check_phone(words[2])  # check the phone
        print(">> " + "It is all right. Will add " + name + " " + phone)
        wait()
    elif len(words) == 2:  # one argument is missing - phone
        name = check_name(words[1])  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
        print(">> " + "It is all right. Will add " + name + " " + phone)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command add in your request. Will need a name and a phone of the contact")
        name = check_name("-1")  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
    return command + " " + name + " " + phone


def change_process(words):
    command = words[0]
    if len(words) == 3:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "Check phone info for " + name)
        wait()
        phone = check_phone(words[2])  # check the phone
        print(">> " + "It is all right. Will change " + name + " " + phone)
        wait()
    elif len(words) == 2:  # one argument is missing - phone
        name = check_name(words[1])  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
        print(">> " + "It is all right. Will change " + name + " " + phone)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command change in your request. Will need name and phone of the contact")
        name = check_name("-1")  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
    return command + " " + name + " " + phone


def phone_process(words):
    command = words[0]
    if len(words) == 2:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "It is all right. Will chase for the phone of " + name)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command phone in your request. Will need name of the contact")
        name = check_name("-1")  # check the name
    return command + " " + name


def search_process(words):
    command = words[0]
    if len(words) < 2:
        what = ""
        while len(what) == 0:
            print(">> would you please enter what you looking for ?")
            what = input(">> ").lower()
    else:
        what = words[1]
    return command + " " + what


PROCESS = {ADD_CMD: add_process,
           CHANGE_CMD: change_process,
           PHONE_CMD: phone_process,
           SRCH_CMD: search_process
           }


def input_error(command_func):
    def inner(list):
        corrected_list = []
        for record in list:  # list of commands extracted from the user input
            # print(record)
            words = record.split()  # split the possible action
            command = words[0]  # it is always command
            corrected_list.append(PROCESS[command](words))
            # 33 print(corrected_list)
        return command_func(corrected_list)
    return inner


def nothing():
    return NOTHING


def greet(list=[]):
    return GREETING


@input_error
def add_contact(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        # print(words)
        name = words[1]
        phone = words[2]
        CONTACTS[name] = phone
        # will add the contact into the address book
        title = Name(name)
        person = Record(title)
        person.add_phone(Phone(phone))
        contact_book.add_record(person)
        output += name + " "
    return "Added " + output + "into the contacts"


@input_error
def change(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        name = words[1]
        found = CONTACTS.get(name, 0)
        # print(found)
        if found:
            old_phone = CONTACTS[name]
            contact_book.get(name).remove_phone(old_phone)  # remove old phone
            phone = words[2]
            contact_book.get(name).add_phone(Phone(phone))  # add new phone
            CONTACTS[name] = phone
            output += name + " "
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Phones were modified for: " + output


@input_error
def phone(list):  # list contains lists of possible actions to add
    # print(list)
    print("-" * 36)
    print("{:^36}|".format("Current list of the contacts"))
    print("-" * 36)
    for record in list:
        words = record.split()
        name = words[1]
        found = CONTACTS.get(name, 0)
        # print(found)
        if found:
            print("{:^16} | {:^16} |".format(name, CONTACTS[name]))
            print("-" * 36)
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Done"


def show(list=[]):
    print("-" * 36)
    print("{:^36}|".format("Current list of the contacts"))
    print("-" * 36)
    for contact in CONTACTS:
        print("{:^16} | {:^16} |".format(contact, CONTACTS[contact]))
        print("-" * 36)
    return "Done"


def help(list=[]):
    return """\n
* add - add a contact and a phone\n  
* change - change a contact phone \n
* phone - list a phone of the contact \n
* show all - list all the contacts \n
* help - list menu of the commands \n"""


@input_error
def search(list):
    users = ""
    for record in list:
        words = record.split()
        what = words[1]
        for contact in contact_book.iterator():
            contact_record = contact[0]
            name = contact_record.name.value
            x = name.find(what)
            if x >= 0:
                users += name + " "
            else:
                for phone in contact_record.phone:
                    x = phone.value.find(what)
                    if x >= 0:
                        users += name + " "
        if len(users) == 0:
            return "nothing was found"
        else:
            return "users found: " + users


def command_parser(line):
    return re.findall("add[ ]+[a-zA-Z]+[ ]+[+][1-9][(][0-9]{3}[)][0-9]{3}-[0-9]{4}", line)


PARSER = {
    HELLO_CMD: lambda x: re.findall(HELLO_CMD, x),
    ADD_CMD: lambda x: re.findall(ADD_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*", x),
    CHANGE_CMD: lambda x: re.findall(CHANGE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*", x),
    PHONE_CMD: lambda x: re.findall(PHONE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    SHOW_CMD: lambda x: re.findall(SHOW_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    HLP_CMD: lambda x: re.findall(HLP_CMD, x),
    SRCH_CMD: lambda x: re.findall(SRCH_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x)
}

RESPONSE = {
    HELLO_CMD: greet,
    ADD_CMD: add_contact,
    CHANGE_CMD: change,
    PHONE_CMD: phone,
    SHOW_CMD: show,
    HLP_CMD: help,
    SRCH_CMD: search
}


def main():
    while True:
        line = input(">> ").lower()
        if line in exit_list:
            print(">> Good bye!")
            break
        else:
            for word in COMMANDS:
                command_list = PARSER[word](line)
                if len(command_list):
                    handler = RESPONSE[word]
                    print(">> " + str(handler(command_list)))


def restore_contacts():
    for record in contact_book.iterator():
        CONTACTS[record[0].name.value] = record[0].phone[0].value


# print(check_phone("+386478617006"))
# print(check_name("+1(647)861 wrwf"))
# line = "add Alisa +16478617006 show all"
# command_line = PARSER["add"](line)
# handler = RESPONSE["add"]
# print(handler(command_line))
# 3command_line = PARSER["show"](line)
# handler = RESPONSE["show"]
# print(handler(command_line))
# wait()
if __name__ == "__main__":

    CONTACTS = {}  # dictionary of the contacts
    contact_book = AddressBook()  # address book of contacts

    if (os.path.exists(ADRESSBOOK)):
        contact_book = contact_book.read_from_file(ADRESSBOOK)
        restore_contacts()
        print(">> address book was succesfully read")
        # contact_book.print()
    else:
        print(f">> address book {ADRESSBOOK} was not found")

    main()
    print(">> address book saved to " + ADRESSBOOK)
    contact_book.save_to_file(ADRESSBOOK)