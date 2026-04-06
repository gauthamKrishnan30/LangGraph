import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def call_mode(State : MessagesState):
    response = llm.invoke(State.messages)
    return {"messages":[response ]}

graph = StateGraph(MessagesState)
graph.add_node("model", call_mode)
graph.set_entry_point(START,"model")
graph.set_finish_point("model",END)

app=graph.compile()

for chunk in app.stream({"messages":[("user","Hi,my name is Adam i am from chennai")]},stream_mode="values"):
    chunk["messages"][-1].pretty_print()

for chunk in app.stream({"messages":[("user","What is LLM?")]},stream_mode="values"):
    chunk["messages"][-1].pretty_print()

