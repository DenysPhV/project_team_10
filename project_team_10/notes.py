# May the force be with you
import functools
import os
from pathlib import Path


class Notes:

    @staticmethod
    def add_note(note, tag, text):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)
        create_dict_note = {
            "note": note,
            "tag": tag,
            "text": "\n"+text
        }

        if not os.path.isfile(full_path):

            with open(full_path, 'w', encoding="utf8") as file:
                for k, v in create_dict_note.items():
                    file.writelines(f"{k}: {v}\n")
                    print(file)
            return f"Your new note with name '{note}' is created in folder 'notes'"

        return f"Note with name '{note}' is already exist in folder 'notes'"

    @staticmethod
    def read_note(note):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)
        note = ""
        tag = ""
        text = ""

        if os.path.isfile(full_path):
            with open(full_path, 'r', encoding="utf8") as file:
                note_data = file.readlines()
                for i, l in enumerate(note_data):
                    if i == 0:
                        note = l.replace('\n', '')
                    elif i == 1:
                        tag = l.replace('\n', '')
                    else:
                        text += l
            return f"{note}\n{tag}\n{text.strip()}"
        return f"Note with name '{note}' was not found in folder 'notes'"

    @staticmethod
    def update_note(note, tag, text):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)

        if os.path.isfile(full_path):
            with open(full_path, "w", encoding='utf8') as file:
                file.writelines(f"note: {note}\n")
                file.writelines(f"{tag}\n")
                file.writelines(text)
            return f"Note '{note}' was updated successfully!"

        return f"Note with name '{note}' was not found in folder 'notes'"

    @staticmethod
    def delete_note(note):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)

        if os.path.isfile(full_path):
            os.remove(full_path)
            return f"Your note with name '{note}' was deleted from folder 'notes'"
        else:
            return f"Note with name '{note}' was not found in folder 'notes'"

    @staticmethod
    def show_all_note():
        folder = os.path.join(Path().resolve(), "notes")
        create_list_notes = []

        for filename in os.listdir(folder):
            create_list_notes.append(filename)

        if len(create_list_notes) == 0:
            return f"Your notebook is still empty.\nPlease add your first note"
        else:
            first_string = "Your notebook has the following notes:\n"
            note_lines = "\n".join(str(record)
                                   for record in list(create_list_notes))
            return first_string + note_lines

    @staticmethod
    def find_by_tag_note(tag):
        folder = os.path.join(Path().resolve(), "notes")
        create_list_notes = []

        for filename in os.listdir(folder):
            note_to_do = Notes.read_note(filename.split('.')[0])
            tags = note_to_do.split('\n')[1].split()
            if tag in tags:
                create_list_notes.append(filename)

        if len(create_list_notes) == 0:
            return f"I can't find any note by this tag.\nPlease enter a valid note's tag for search."

        first_string = "I found the following notes by your tag:\n"
        note_names = "\n".join(str(record)
                               for record in list(create_list_notes))
        return first_string + note_names

    @staticmethod
    def find_by_name_note(note):
        folder = os.path.join(Path().resolve(), "notes")
        create_list_notes = []

        for filename in os.listdir(folder):
            if note in filename.split('.')[0]:
                create_list_notes.append(filename)

        if len(create_list_notes) == 0:
            return f"I can't find any note that contain this name.\nPlease enter a valid note's name for search."

        first_string = "I found  the following notes by searching name:\n"
        note_names = "\n".join(str(record)
                               for record in list(create_list_notes))
        return first_string + note_names


# >>>>> here start class CLI <<<<<
NOTES = Notes()


def is_exist(note):
    filename = note + ".txt"
    full_path = os.path.join(Path().resolve(), "notes", filename)
    if os.path.exists(full_path):
        return True
    return False


def command_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            return func(*args)
        except (ValueError, KeyError, Exception) as err:
            return str(err)

    return wrapper


class CLINotes:

    @staticmethod
    def help_handler():
        return ("""
    You can use the following commands for your notebook:
    - add note -> to create new note and save into folder 'notes';
    - read note -> to open indicated note and read text inside;
    - delete note -> to delete indicated note from the folder;
    - find by tag -> to find all notes that are matched with this tag;
    - find by name -> to find notes that are matched with this name;
    - show all -> to show list of notes that were saved in folder;
    - add tag -> to include additional tag to existing note;
    - add text -> to include additional text to existing note;
    - change tag -> to change existing tag in note (recommend to read note first);
    - change text -> to change existing text in note (recommend to read note first);
    - delete tag -> to delete existing tag in note (recommend to read note first);
    - delete text -> to delete existing text in note (recommend to read note first);
    """)

    @command_error_handler
    def add_note_handler(self=None):
        note = input("Enter note: ")
        if note == "":
            return f"You haven't enter, try again please"

        elif is_exist(note):
            return f"Note with name '{note}' is already exist in folder 'notes'"

        else:
            tag = input("Please enter tags (start with #, space to divide): ")
            text = input("Please enter text for note: ")
            return NOTES.add_note(note, tag, text)

    @command_error_handler
    def read_note_handler(self=None):
        note = input(
            "Please enter note which want to you read (without '.txt'): ")

        if note != "":
            return NOTES.read_note(note)
        return "Note is missed. Please try again"

    @command_error_handler
    def delete_note_handler(self=None):
        note = input("Enter note which want to delete it (without '.txt'): ")

        if note != "":
            return NOTES.delete_note(note)
        return "Name of note is missed. Please try again"

    @command_error_handler
    def find_tag_handler(self=None):
        tag = input("Please enter 1 tag to find notes (start with #): ")

        if tag != "":
            return NOTES.find_by_tag_note(tag)
        return "Tag for search is missed. Please try again"

    @command_error_handler
    def find_note_handler(self=None):

        note = input("To find note (without '.txt'): ")
        if note != "":
            return NOTES.find_by_name_note(note)

        return "Search is missed. Please try again"

    @command_error_handler
    def show_all_handler(self=None):
        return NOTES.show_all_note()

    @command_error_handler
    def add_tag_handler(self=None):
        note = input("Note to update info (without '.txt'): ")

        if is_exist(note):
            tag = input(
                "Please use first tag to add to this note (start with #): ")
            note_to_read = NOTES.read_note(note)
            old_tag = ""
            old_text = ""

            for i, item in enumerate(note_to_read.split('\n'), start=0):
                if i == 1:
                    old_tag = item + " "

            for i, item in enumerate(note_to_read.split('\n')[2:], start=0):
                old_text += item + '\n'

            return NOTES.update_note(note, old_tag + tag, old_text)
        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def add_text_handler(self=None):
        note = input("Enter note to update info (without '.txt'): ")

        if is_exist(note):
            text = input("Please write text to add to the current note: ")
            note_to_do = NOTES.read_note(note)
            old_tag = ''
            old_text = ''

            for i, item in enumerate(note_to_do.split('\n'), start=0):
                if i == 1:
                    old_tag = item

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                old_text += item + '\n'

            return NOTES.update_note(note, old_tag, old_text + text)
        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def change_tag_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            tag_list = note_to_do.split('\n')[1]
            new_tag = ''
            new_text = ''

            for i, item in enumerate(tag_list.split(), start=0):
                print(i, item)
            tag_index = int(
                input("Please enter index of tag that you want to change: "))
            tag = input(
                "Please write new tag to add instead old to the current note: ")

            for i, item in enumerate(tag_list.split(), start=0):
                if i == tag_index:
                    item = tag
                new_tag += item + ' '

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                new_text += item + '\n'

            return NOTES.update_note(note, new_tag, new_text)

        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def change_text_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            new_tag = ''
            new_text = ''

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                print(i, item)

            text_index = int(
                input("Please enter index of text that you want to change: "))
            text = input(
                "Please write new text to add instead old to the current note: ")

            for i, item in enumerate(note_to_do.split('\n'), start=0):
                if i == 1:
                    new_tag = item

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):

                if i == text_index:
                    item = text
                new_text += item + '\n'

                return NOTES.update_note(note, new_tag, new_text)

            raise ValueError(
                f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def delete_tag_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            tag_list = note_to_do.split('\n')[1]
            new_tag = ''
            new_text = ''

            for i, item in enumerate(tag_list.split(), start=0):
                print(i, item)
            tag_index = int(
                input("Please enter index of tag that you want to delete: "))

            for i, item in enumerate(tag_list.split(), start=0):
                if i == tag_index:
                    item = ""
                new_tag += item + ' '

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                new_text += item + '\n'

            return NOTES.update_note(note, new_tag.strip(), new_text)

        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def delete_text_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            tag_list = note_to_do.split('\n')[1]
            new_tag = ''
            new_text = ''

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                print(i, item)
            text_index = int(
                input("Please enter index of text that you want to delete: "))

            for i, item in enumerate(tag_list.split('\n'), start=0):
                if i == 0:
                    new_tag = item

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                if i == text_index:
                    item = ''
                new_text += item + '\n'

            return NOTES.update_note(note, new_tag, new_text.strip())

        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    commands_dict = {
        "help": help_handler,

        "add note": add_note_handler,
        "read note": read_note_handler,
        "delete note": delete_note_handler,

        "find by tag": find_tag_handler,
        "find by name": find_note_handler,
        "show all": show_all_handler,

        "add tag": add_tag_handler,
        "add text": add_text_handler,
        "change tag": change_tag_handler,
        "change text": change_text_handler,
        "delete tag": delete_tag_handler,
        "delete text": delete_text_handler,
    }

    @staticmethod
    def run_notes():
        folder = os.path.join(Path().resolve(), "notes")

        if not os.path.exists(folder):
            os.mkdir(folder)

        print("Hello! I'm here to assist you with your notes in your notebook.")
        print("You could enter exact commands if you already know them.\n"
              "Or please use:\n"
              "  help -> to see whole list of commands\n"
              "  exit -> to finish work with your notebook")

        while True:
            command = input("You haven't entered command: ").lower().strip()

            if command == "exit":
                return "\nThanks, see you soon!!!\n"

            if command in CLINotes.commands_dict.keys():
                handler = CLINotes.commands_dict[command]
                answer = handler()
                print(answer)

            else:
                commands_list = []
                for k in CLINotes.commands_dict.keys():
                    for item in k.split():
                        if command in item:
                            commands_list.append(k)
                            break

                if commands_list:
                    print("What you have mean entered these commands: ")
                    print(*commands_list, sep=", ")
                else:
                    print(
                        "Incorrect input.\nPlease check and enter correct command (or 'help' or 'exit').")


if __name__ == '__main__':
    CLINotes.run_notes()
