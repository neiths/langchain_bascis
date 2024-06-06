import os
# load .env
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.callbacks import get_openai_callback
from langchain_community.llms import Anyscale

#llm = Anyscale(model_name='')

# initialize the LLMs model, there are many LLMs from different providers: OpenAI, Google, Microsoft, etc.
# Each model has its own API_KEY and Initial way to call the model
# Open AI
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
# output = llm.invoke("how can langsmith help with testing?")
# print(output)
# GeminiAI
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=GOOGLE_API_KEY)
# output = llm.invoke("how can langsmith help with testing?")
# print(output)
# manage prompt
system_prompt = """
        Bạn là một nhà bác sĩ bán thuốc cho bệnh nhân
        User sẽ cung cấp thông tin về triệu chứng của bệnh nhân
        Bạn cần tư vấn cho bệnh nhân cách sử dụng thuốc và liều lượng
        """

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user","{input}")
])
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
# chain = prompt | llm
output = chain.invoke({"input":"Tôi bị đau bụng và sốt cao, tôi nên dùng thuốc gì?"})

print(output)