# May the force be with you
import functools
import os
from pathlib import Path


class Notes:
   
   @staticmethod
   def add_note():
      ...

   def read_note():
      ...

   def update_note():
      ...

   def delete_note():
      ...

   def show_all_note():
      ...

   def find_by_tag_note():
      ...

   def find_by_name_note():
      ...

class CLINotes:
   

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

   def add_note_handler():
      ...

   def read_note_handler():
      ...

   def delete_note_handler():
      ...  

   def find_tag_handler():
      ...  

   def find_note_handler():
      ...

   def show_all_handler():
      ...

   def add_tag_handler():
      ...

   def add_text_handler():
      ...

   def change_tag_handler():
      ...

   def change_text_handler():
      ...

   def delete_tag_handler():
      ...

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