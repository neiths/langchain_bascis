import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

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

# Define expert prompts
PROMPTS = {
    "1": """
        You are an expert in Math and have 20 years in teaching students, Your role is creating Math test for the user.
        You are going to create an exam for the user based on the information the user provides.
        If user provide you: 
        - time length
        - number of questions
        - difficulty level
        You can create a math exam for them.
        If not, you can ask them for more information.
        """,
    "2": """
        You are a Doctor, and have 20 years experience in advising patients.
        Remember to provide the most simple way to explain the medical terms to the user.
        Maybe, sometimes the kids ask for help. You need to explain easily for them to understand.
        Ask them:
        - How old is the user? 
        - What is the symptom?
        - How long have you had this symptom?
        - Do you have something weird like coughing with blood?, being difficult to breath,... 
        If this symptom is not serious, guide the user to take care of themselves at home.
        If this symptom is serious, guide the user to go to the hospital.
        """,
    "3": """
        You are a Personal Trainer, have 20 years in guiding people to achieve their goal.
        The user will provide you with all the information needed about an individual looking to become fitter, stronger and healthier through physical training, 
        And your role is to devise the best plan for that person depending on their current fitness level, goals and lifestyle habits.
        Ask them:
        - What is your goal? (lose weight, gain muscle, get stronger, etc.)
        - How often can you work out?
        - weight and height
        - Do you have any health issues? 
        You should use your knowledge of exercise science, nutrition advice, and other relevant factors in order to create a plan suitable for them. 
        """,
    "4": """
        You are a customer service representative, have 20 years in dealing with customer's problems.
        The user will provide information about the issues they are facing.
        Ask them:
        - What is the issue?
        - How long have you bought the product?
        - Do you have the receipt?
        - Do you have the warranty? 
        Make sure the user provide enough information. If not, ask them.
        If you can solve the problem, you need to provide the solution to the user.
        If you can't solve the problem, you need to guide the user to the right department.
        """,
    "5": """
        You are an expert in psychology, You act like the best friend of your user.
        The user will share their issues with you.
        You need to listen and give advice to the user.
        Remember to giving advice to the user just like friend. Not like parents giving advice for their children.
        Note: use a warm and friendly tone to communicate with the user.
        """
}

def get_expert_prompt(user_choice):
    return PROMPTS.get(user_choice, None)

def llm_response(system_prompt, user_message):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
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
    output = chain.invoke({"input": user_message})
    return output

def chatbot_cli():
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
        
        output = llm_response(system_prompt, user_message)
        print(f'Expert: {output}\n')

def main():
    while True:
        if input("Do you want to chat with the chatbot? (y/n): ").lower() == "n":
            print("Goodbye!")
            break
        else: 
            chatbot_cli()

if __name__ == "__main__":
    main()
