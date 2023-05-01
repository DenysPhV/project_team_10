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
   def read_note():
      ...

   @staticmethod
   def update_note():
      ...

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
         note_lines = "\n".join(str(record) for record in list(create_list_notes))
         return first_string + note_lines
   
   @staticmethod
   def find_by_tag_note():
      ...
   
   @staticmethod
   def find_by_name_note():
      ...

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
    - show all notes -> to show list of notes that were saved in folder;
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
   def read_note_handler():
      ...

   @command_error_handler
   def delete_note_handler(self=None):
      note = input("Enter note which want to delete it (without '.txt'): ")

      if note != "":
         return NOTES.delete_note(note)
      return "Name of note is missed. Please try again"
   
   @command_error_handler
   def find_tag_handler():
      ...  
   
   @command_error_handler
   def find_note_handler():
      ...
   
   @command_error_handler
   def show_all_handler(self=None):
      return NOTES.show_all_note()
   
   @command_error_handler
   def add_tag_handler():
      ...
   
   @command_error_handler
   def add_text_handler():
      ...
   
   @command_error_handler
   def change_tag_handler():
      ...
   
   @command_error_handler
   def change_text_handler():
      ...
   
   @command_error_handler
   def delete_tag_handler():
      ...
   
   @command_error_handler
   def delete_text_handler():
      ...

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
            return"\nThanks, see you soon!!!\n"
         
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
                print("Incorrect input.\nPlease check and enter correct command (or 'help' or 'exit').")
         
         
if __name__ == '__main__':
   CLINotes.run_notes()