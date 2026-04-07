import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, ChatGoogleGenerativeAl
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent, create_react_egent
from langchain_core.messages import HumanMessage

load_dotenv()

llm=ChatGoogleGenerativeAI (model="gemini-2.5-flash", temperature=0)

@tool
def add(a: int, b:int)->int:
    return a+b

@tool
def multiply(a:int,b:int) -> int:
    return ab

tools=[add, multiply]
agent=create_react_agent(llm, tools)

result=agent.invoke({"messages": [HumanMessage(content="What is 25*4-10?")]})
result["messages"] [-1].pretty_print()