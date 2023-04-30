
class Notes:
   
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
   def help_handler():
      ...

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

   notes_commands_dict = {
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
      ...
   
if __name__ == '__main__':
   CLINotes.run_notes()