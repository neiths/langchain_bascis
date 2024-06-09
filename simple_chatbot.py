import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from expert_prompt import PROMPTS
from utils import *
# Load environment variables
load_dotenv()

# database path
db_path = "db/chat_history.json"

# Function to convert a chat string to a message object to store in the chat history
def convert_chat_string_to_prompt(chat_string, type="ai"):
    if type == "user":
        return HumanMessage(content=chat_string)
    elif type == "ai":
        return AIMessage(content=chat_string)
    else:
        raise ValueError("Invalid type")

# Initialize the LLM model
def load_llm(llm_provider):
    if llm_provider == 'google':
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
    elif llm_provider == 'open_ai':
        return ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))    
    elif llm_provider == 'anyscale':
        pass
    elif llm_provider == 'local':
        # ollama, llm studio
        pass

def get_expert_prompt(user_choice):
    return PROMPTS.get(user_choice, None)

def llm_response(system_prompt, user_message, chat_history):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    try:
        llm = load_llm('google')
    except:
        print("Can't connect to LLM server")
        print("""Please choose another available servers: 
              1. openai
              2. another
              """)
        user_choice = input('--> ')
        if user_choice == '1':
            llm = load_llm('open_ai')
        else:
            return "We haven't supported LLM servers yet."
            
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    output = chain.invoke({"input": user_message, "chat_history": chat_history})
    return output

def chatbot_cli(chat_history):
    while True:
        user_choice = input("""Please choose your expert type:
                            Entern a number from list below.
                            ---------------------------------- 
                            | 1. Math Teacher                |   
                            | 2. Doctor                      |   
                            | 3. Personal Trainer            |
                            | 4. Customer Service            |   
                            | 5. Friend                      |   
                            ----------------------------------
                            ---> """)
        system_prompt = get_expert_prompt(user_choice)

        chat_history_expert = get_chat_history(user_choice, chat_history)
        
        if not system_prompt:
            print("Please choose a correct expert")
            continue
        else:
            break

    print(f'Awaiting connection to {user_choice} expert...')
    time.sleep(1)
    print('Connected')

    while True:
        user_message = input("User: ")
        if user_message.lower() == "exit":
            print("Goodbye!")
            break
        
        output = llm_response(system_prompt, user_message, chat_history_expert)

        # Add the user message to the chat history
        chat_history_expert.append(convert_chat_string_to_prompt(user_message, type="user"))
        # Add the expert message to the chat history
        chat_history_expert.append(convert_chat_string_to_prompt(output, type="ai"))

        # Add the chat history to the overall chat history
        chat_history[user_choice] = chat_history_expert

        print(f'Expert: {output}\n')
    save_chat_history(db_path, chat_history)
 
def main():

    # load chat history
    chat_history = load_chat_history(db_path)

    while True:
        if input("Do you want to chat with the chatbot? (y/n): ").lower() == "n":
            print("Goodbye!")
            break
        else: 
            chatbot_cli(chat_history)
   
if __name__ == "__main__":
    main()
