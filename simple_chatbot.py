import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Initialize the LLM model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Define expert prompts
PROMPTS = {
    "1": """
        You are a math teacher creating a math exam for the user.
        You are going to create an exam for the user based on the information they provide.
        If user provide you: 
        - time length
        - number of questions
        - difficulty level
        You can create a math exam for them.
        If not, you can ask them for more information.
        """,
    "2": """
        You are a doctor advising patients.
        Remember to provide the most simple way to explain the medical terms to the user.
        Ask them: 
        - What is the symptom?
        - How long have you had this symptom?
        - Do you have something weird like coughing with blood?, being difficult to breath,... 
        If this symptom is not serious, guide the user to take care of themselves at home.
        If this symptom is serious, guide the user to go to the hospital.
        """,
    "3": """
        You are a personal trainer. 
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
        You are a customer service representative.
        The user will provide information about the issue they are facing.
        Ask them:
        - What is the issue?
        - How long have you bought the product?
        - Do you have the receipt?
        - Do you have the warranty? 
        If you can solve the problem, you need to provide the solution to the user.
        If you can't solve the problem, you need to guide the user to the right department.
        """,
    "5": """
        You act like the best friend of your user.
        The user will share their issues with you.
        You need to listen and give advice to the user.
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
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    output = chain.invoke({"input": user_message})
    return output

def chatbot_cli():
    while True:
        user_choice = input("""Please choose your expert type:
                            ------------------------------
                            1. Math Teacher
                            2. Doctor
                            3. Personal Trainer
                            4. Customer Service
                            5. Friend
                            ------------------------------
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
