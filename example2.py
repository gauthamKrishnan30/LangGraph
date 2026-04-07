from asyncio import tools
import os
from datetime import datetime
from xml.parsers.expat import model
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, ChatGoogleGenerativeAlI
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, EN
from langgraph.graph.message import add_messages
from geopy.geocoders import Nominatim #pip install geopy
import requests

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

class AgentState (TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

geolocator = Nominatim(user_agent="langgraph-weather")

@tool
def get_weather(location: str):
    """Get current weather for the provided city"""
    loc = geolocator.geocode("Hyderabad")
    if not loc: 
        return "Location not found"

    resp = requests.get(f"")

    data=resp.json()

    return f"Temperature in {location}: {data['current']['temperature']}°C"

tools=[get_weather]
model=llm.bing_tools(tools)
tools_by_name = {t.name: t for t in tools}

def call_model (state: AgentState):
    return {"messages": [model.invoke(state["messages"])]}


def call_tools (state: AgentState):
    outputs=[]
    for t in state ["messages"] [-1].tool_calls:
        tool_result = tools_by_name[t["name"]].invoke(t["args"])
        outputs.append(ToolMessage(content=tool_result, name=t["name"], tool_call_id=t["id"]))

graph=StateGraph (AgentState)
graph.add_node("model", call_model)
graph.add_node("tools", call_tools)
graph.set_entry_point("model")
graph.add_conditional_edges("model")
graph.add_edge("tools", "models")

app=graph.create_app()
result = app.invoke({"messages": [HumanMessage(content="What is the weather in Chennai?")]})
result["messages"][-1].pretty_print()