from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import pathlib
import uuid
import json


app = Flask(__name__)
thisdir = pathlib.Path(__file__).parent.absolute() # path to directory of this file


# Function to load and save the mail to/from the json file


def load_mail() -> List[Dict[str, str]]:
   """
   Loads the mail from the json file
   Returns:
       list: A list of dictionaries representing the mail entries
   """
   try:
       return json.loads(thisdir.joinpath('mail_db.json').read_text())
   except FileNotFoundError:
       return []


def save_mail(mail: List[Dict[str, str]]) -> None:
   """TODO: fill out this docstring (using the load_mail docstring as a guide)
   Saves the mail from the json file.
   Args:
      mail (List[Dict[str,str]]): The mail to be saved.
   Returns: 
      nothing
   """
   thisdir.joinpath('mail_db.json').write_text(json.dumps(mail, indent=4))


def add_mail(mail_entry: Dict[str, str]) -> str:
   """TODO: fill out this docstring (using the load_mail docstring as a guide)
   Adds a mail to the mail list. 
   Args:
      mail_entry (Dict[str,str]): Mail entry to be added.
   Returns:
      mail_entry: A string of the mail id. 
   """
   mail = load_mail()
   mail.append(mail_entry)
   mail_entry['id'] = str(uuid.uuid4()) # generate a unique id for the mail entry
   save_mail(mail)
   return mail_entry['id']


def delete_mail(mail_id: str) -> bool:
   """TODO: fill out this docstring (using the load_mail docstring as a guide)
   Checks if a mail_entry is part of the list and deletes it.
   Arg:
      mail_id (str): ID for mail within mail.
   Returns:
      bool: True if the mail entry is in the list and is deleted, false if it isn’t. 
   """
   mail = load_mail()
   for i, entry in enumerate(mail):
       if entry['id'] == mail_id:
           mail.pop(i)
           save_mail(mail)
           return True


   return False


def get_mail(mail_id: str) -> Optional[Dict[str, str]]:
   """TODO: fill out this docstring (using the load_mail docstring as a guide)
   Retrieves the mail entry.
   Args:
   mail_id (str): ID from mail. 
   Returns:
      entry: Returns the mail entry if it exists.
   """
   mail = load_mail()
   for entry in mail:
       if entry['id'] == mail_id:
           return entry


   return None


def get_inbox(recipient: str) -> List[Dict[str, str]]:
   """TODO: fill out this docstring (using the load_mail docstring as a guide)
   Retrieves the inbox for a given recipient.
   Args:
      recipient (str): Name of the recipient of mail.
   Returns: 
      inbox: List of all mail entries from recipient
   """
   mail = load_mail()
   inbox = []
   for entry in mail:
       if entry['recipient'] == recipient:
           inbox.append(entry)


   return inbox


def get_sent(sender: str) -> List[Dict[str, str]]:
   """TODO: fill out this docstring (using the load_mail docstring as a guide)
   Retrieves all mail sent to a given sender.
   Args:
      sender(str): name of a specific sender. 
   Returns:
      sent: A list of mail entries sent by a given sender.
   """
   mail = load_mail()
   sent = []
   for entry in mail:
       if entry['sender'] == sender:
           sent.append(entry)


   return sent


# API routes - these are the endpoints that the client can use to interact with the server
@app.route('/mail', methods=['POST'])
def add_mail_route():
   """
   Summary: Adds a new mail entry to the json file
   Returns:
       str: The id of the new mail entry
   """
   mail_entry = request.get_json()
   mail_id = add_mail(mail_entry)
   res = jsonify({'id': mail_id})
   res.status_code = 201 # Status code for "created"
   return res


@app.route('/mail/<mail_id>', methods=['DELETE'])
def delete_mail_route(mail_id: str):
   """
   Summary: Deletes a mail entry from the json file
   Args:
       mail_id (str): The id of the mail entry to delete
   Returns:
       bool: True if the mail was deleted, False otherwise
   """
   # TODO: implement this function
   res = jsonify(delete_mail(mail_id))
   res.status_code = 200 # Status code for “OK”
   return res


@app.route('/mail/<mail_id>', methods=['GET'])
def get_mail_route(mail_id: str):
   """
   Summary: Gets a mail entry from the json file
   Args:
       mail_id (str): The id of the mail entry to get
   Returns:
       dict: A dictionary representing the mail entry if it exists, None otherwise
   """
   res = jsonify(get_mail(mail_id))
   res.status_code = 200 # Status code for "ok"
   return res


@app.route('/mail/inbox/<recipient>', methods=['GET'])
def get_inbox_route(recipient: str):
   """
   Summary: Gets all mail entries for a recipient from the json file
   Args:
       recipient (str): The recipient of the mail
   Returns:
       list: A list of dictionaries representing the mail entries
   """
   res = jsonify(get_inbox(recipient))
   res.status_code = 200
   return res


# TODO: implement a route to get all mail entries for a sender
# HINT: start with something like this:
#   @app.route('/mail/sent/<sender>', ...)
@app.route('/mail/sent/<sender>', methods=['GET'])
def get_sent_route(sender: str):
   """
   Summary: Gets all mail entries from a sender from the json file
   Args:
       recipient (str): The sender of the mail
   Returns:
       list: A list of dictionaries representing the mail entries
   """


   res = jsonify(get_sent(sender))
   res.status_code = 200 # Status code for “OK”
   return res


if __name__ == '__main__':
   app.run(port=5000, debug=True)

