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

    def find_name(self, strname):
        for record in self.data:
            if strname == record:
                return self.data[record]
        return Record(Name(NOT_DEFINED))

    def remove(self, name):
        self.data.pop(name)


class Record:  # responsible for the record manipulation

    def __init__(self, name):
        self.name = name  # type of Name
        self.phone = []  # list of phones
        self.email = []  # list of e-mails
        self.birthday = Birthday()
        self.add = Address()

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
            return delta.days
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

    def print_phones(self):
        # output = "Phones: "
        output = ""
        for phone in self.phone:
            output += phone.value + " "
        return output

    def print_emails(self):
        # print("Emails: ")
        output = ""
        for email in self.email:
            output += email.value + " "
        return output

    def edit_address(self, newaddress):
        self.add.update(newaddress)

    def print_address(self):
        return self.add.value

    def create_output_line(self, index):
        output = []
        if index == 0:
            output.append(self.name.value)
            if len(self.phone) > 0:
                output.append(self.phone[0].value)
            else:
                output.append("")

            if len(self.email) > 0:
                output.append(self.email[0].value)
            else:
                output.append("")

            if self.birthday.day != "":
                output.append(self.birthday.day)
            else:
                output.append("")

            if self.add.value != NOT_DEFINED:
                output.append(self.add.value)
            else:
                output.append("")
        else:
            output = [""]
            if len(self.phone) > index:
                output.append(self.phone[index].value)
            else:
                output.append("")

            if len(self.email) > index:
                output.append(self.email[index].value)
            else:
                output.append("")
            output.append("")
            output.append("")
        return output

    def print(self):
        m1 = len(self.phone)
        m2 = len(self.email)
        if m1 > m2:
            m = m1
        else:
            m = m2
        print("-" * 160)
        for i in range(m):
            output = self.create_output_line(i)
            # print(output)
            print(" {:^20} | {:^20}| {:^20} | {:^20} | {:^20} ".format(
                output[0], output[1], output[2], output[3], output[4]))

    def edit_birthday(self, new):
        self.birthday.update(new)


class Field:  # defines general fields properties TBD
    def __init__(self, value):
        self.value = value

    def update(self, newvalue):
        self.value = newvalue


class Name(Field):  # mandatory field
    def __init__(self, value):
        self.value = value


class Phone(Field):  # nonmandatory field
    def __init__(self, phone=NOT_DEFINED):
        self.__value = phone

    @ property  # define getter
    def value(self):
        return self.__value

    @ value.setter  # define setter
    def value(self, val):
        match = re.fullmatch(
            r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", val)
        if not match:
            raise ValueError(">> Phone number is not  correct.\n")
        else:
            self.__value = val


class Email(Field):  # nonmandatory field
    def __init__(self, email=NOT_DEFINED):
        self.__value = email

    @ property  # getter
    def value(self):
        return self.__value

    @ value.setter  # setter
    def value(self, val):
        match = re.fullmatch(
            r"[a-zA-Z\.\-_0-9]+@[a-zA-Z0-9]+[\.][a-zA-Z]{2}", val)
        if not match:
            raise ValueError(">> Email name is not correct. \n")
        else:
            self.__value = val


class Birthday:
    # will keep it in format yyyy/mm/dd
    def __init__(self):
        self.__birthday = ""

    @ property  # define getter
    def day(self):
        return self.__birthday

    @ day.setter  # define setter
    def day(self, val):
        match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
        if not match:
            raise ValueError(">> Date is not  correct date.\n")
        else:
            self.__birthday = val

    def update(self, newbirth):
        self.__birthday = newbirth.day


class Address(Field):
    def __init__(self, add=NOT_DEFINED):
        self.value = add


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
EDT_CMD = "edit"
RMV_CMD = "remove"
EMAIL_CMD = "email"
CONGRAT_CMD = "birthday"

COMMANDS = [HELLO_CMD, ADD_CMD, CHANGE_CMD,
            PHONE_CMD, SHOW_CMD, HLP_CMD, SRCH_CMD,
            EDT_CMD, RMV_CMD, EMAIL_CMD, CONGRAT_CMD]


def parser(line):
    return re.sub("[^0-9a-zA-Z+()-]", " ", line).split()


GREETING = "How can I help you ? For the commands description please type help"
NOTHING = "There is nothing to execute"
UNDERSTOOD = "Understood"


def wait():
    print(">> Please wait....")
    time.sleep(2)


def check_number(num):
    match = re.fullmatch("^[0-9]+$", num)
    while not match:
        print(">> Please input correct number. It should include only digits")
        num = input(">> ").lower()
        match = re.fullmatch("^[0-9]+$", num)
    return num


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
        print(">> " + "Found command change in your request. Will need name and a new phone of the contact")
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


def email_process(words):
    command = words[0]
    if len(words) == 2:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "It is all right. Will chase for the email of " + name)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command email in your request. Will need name of the contact")
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


def edit_process(words):
    command = words[0]
    if len(words) < 2:
        name = check_name("-1")
    else:
        name = check_name(words[1])
    return command + " " + name


def remove_process(words):
    command = words[0]
    if len(words) < 2:
        name = check_name("-1")
    else:
        name = check_name(words[1])
    return command + " " + name


def birthday_process(words):
    command = words[0]
    if len(words) == 2:  # all required arguments were taken
        days = check_number(words[1])  # check the name
        print(">> " + "It is all right. Will chase for the names who will have birthday in " + days + "  days")
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command birthday in your request. Will need number of days")
        days = check_number("-1")  # check the name
    return command + " " + days


PROCESS = {ADD_CMD: add_process,
           CHANGE_CMD: change_process,
           PHONE_CMD: phone_process,
           SRCH_CMD: search_process,
           EDT_CMD: edit_process,
           RMV_CMD: remove_process,
           EMAIL_CMD: email_process,
           CONGRAT_CMD: birthday_process
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


@ input_error
def add_contact(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        # print(words)
        name = words[1]
        phone = words[2]
        # will add the contact into the address book
        title = Name(name)
        person = Record(title)
        person.add_phone(Phone(phone))
        contact_book.add_record(person)
        output += name + " "
    return "Added " + output + "into the contacts"


@ input_error
def change(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        name = words[1]
        found_record = contact_book.find_name(name)
        # print(found)
        if found_record.name.value != NOT_DEFINED:
            found_record.print()
            print(">> please specify which phone you would like to change?")
            old_phone = input(">> ").lower()
            old_phone = check_phone(old_phone)
            # remove old phone
            print(">> " + contact_book.get(name).remove_phone(old_phone))
            phone = words[2]
            contact_book.get(name).add_phone(Phone(phone))  # add new phone
            found_record.print()
            output += name + " "
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Phones were modified for: " + output


@ input_error
def phone(list):  # list contains lists of possible actions to add
    # print(list)
    for record in list:
        words = record.split()
        name = words[1]
        found_record = contact_book.find_name(name)
        # print(found)
        if found_record.name.value != NOT_DEFINED:
            print(f">> {name}:" + found_record.print_phones())
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Done"


@ input_error
def email(list):  # list contains lists of possible actions to add
    # print(list)
    for record in list:
        words = record.split()
        name = words[1]
        found_record = contact_book.find_name(name)
        # print(found)
        if found_record.name.value != NOT_DEFINED:
            print(f">> {name}:" + found_record.print_emails())
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Done"


def show(list=[]):
    # print("-" * 36)
    # print("{:^36}|".format("Current list of the contacts"))
    # print("-" * 36)
    # for contact in CONTACTS:
    #    print("{:^16} | {:^16} |".format(contact, CONTACTS[contact]))
    #    print("-" * 36)
    contact_book.print()
    return "Done"


def help(list=[]):
    return """\n
* add - add a contact and a phone\n
* change - change a contact phone \n
* phone - list a phone of the contact \n
* email - list an email of the contact \n
* show all - list all the contacts \n
* remove - remove record \n
* edit - edit record (append phones, emails) \n
* search - search records according to input text \n
* help - list menu of the commands \n"""


@ input_error
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


@ input_error
def edit(list):
    for record in list:
        words = record.split()
        name = words[1]  # read name
        record = contact_book.find_name(name)
        # print(record.name)
        if record.name.value == NOT_DEFINED:
            print(">> contact " + name + " does not exist. Skip")
        else:
            record.print()
            print(">> would you like to append phone ?[y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                print(">> please input correct phone kind of +1(647)861-90-06")
                phone = input(">> ").lower()
                try:
                    newphone = Phone()
                    newphone.value = phone
                    record.add_phone(newphone)
                    wait()
                    record.print()
                except ValueError as msg:
                    print(msg)

            print(">> would you like to append email ?[y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":

                print(">> please input e-mail kind of ali-mak@gmail.ca")
                email = input(">> ").lower()
                try:
                    newemail = Email()
                    newemail.value = email
                    record.add_email(newemail)
                    wait()
                    record.print()
                except ValueError as msg:
                    print(msg)

            print(">> would you like to edit adress ?[y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                print(">> please input your full address")
                address = input(">> ").lower()
                record.edit_address(address)
                wait()
                record.print()

            print(">> would you like to input birthday? [y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                print(">> please input date kind of yyyy/mm/dd")
                birthday = input(">> ").lower()
                try:
                    newday = Birthday()
                    newday.day = birthday
                    record.edit_birthday(newday)
                    wait()
                    record.print()
                except ValueError as msg:
                    print(msg)
    return "Done"


@ input_error
def remove(list):
    for record in list:
        words = record.split()
        name = words[1]  # read name
        record = contact_book.find_name(name)
        if record.name.value == NOT_DEFINED:
            print(">> contact " + name + " does not exist. Skip")
        else:
            record.print()
            print(
                ">> are are you sure that you want to remove this record completely? [y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                contact_book.remove(name)

    return "Done"


@ input_error
def birthday(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        days = int(words[1])
        for contact in contact_book.iterator():
            contact_record = contact[0]
            name = contact_record.name.value
            # print(date.today() + timedelta(days=58))
            if contact_record.days_to_birthday() == days:
                output += name + " "
    return "birthday have: " + output


def command_parser(line):
    return re.findall("add[ ]+[a-zA-Z]+[ ]+[+][1-9][(][0-9]{3}[)][0-9]{3}-[0-9]{4}", line)


PARSER = {
    HELLO_CMD: lambda x: re.findall(HELLO_CMD, x),
    ADD_CMD: lambda x: re.findall(ADD_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*", x),
    CHANGE_CMD: lambda x: re.findall(CHANGE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*", x),
    PHONE_CMD: lambda x: re.findall(PHONE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    EMAIL_CMD: lambda x: re.findall(EMAIL_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    SHOW_CMD: lambda x: re.findall(SHOW_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    HLP_CMD: lambda x: re.findall(HLP_CMD, x),
    SRCH_CMD: lambda x: re.findall(SRCH_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    EDT_CMD: lambda x: re.findall(EDT_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    RMV_CMD: lambda x: re.findall(RMV_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    CONGRAT_CMD: lambda x: re.findall(
        CONGRAT_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x)
}

RESPONSE = {
    HELLO_CMD: greet,
    ADD_CMD: add_contact,
    CHANGE_CMD: change,
    PHONE_CMD: phone,
    EMAIL_CMD: email,
    SHOW_CMD: show,
    HLP_CMD: help,
    SRCH_CMD: search,
    EDT_CMD: edit,
    RMV_CMD: remove,
    CONGRAT_CMD: birthday
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

    contact_book = AddressBook()  # address book of contacts

    if (os.path.exists(ADRESSBOOK)):
        contact_book = contact_book.read_from_file(ADRESSBOOK)
        print(">> address book was succesfully read")

        # contact_book.print()
    else:
        print(f">> address book {ADRESSBOOK} was not found")

    main()
    print(">> address book saved to " + ADRESSBOOK)
    contact_book.save_to_file(ADRESSBOOK)
