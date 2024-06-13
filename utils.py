import json
from langchain.load import dumps, loads


# Function to get the chat history for a specific expert
def get_chat_history(expert_name, chat_history):
    if expert_name not in chat_history:
        chat_history[expert_name] = []
    return chat_history[expert_name]

# Function to save the chat history to a JSON file
def save_chat_history(filename, chat_history):
    #with open(filename, 'w') as file:
        #dumps(chat_history, file)
    with open(filename, "w") as fh:
        fh.write(dumps(chat_history))    

# Function to load the chat history from a JSON file
def load_chat_history(filename):
    try:
        with open(filename) as file:
            chat_history = loads(file.read())
            return chat_history
    except FileNotFoundError:
        chat_history = {}
        return chat_history



