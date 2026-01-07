import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph,END,add_messages
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
os.environ["GOOGLE_API_KEY"] =API_KEY # Add your API key here
model=init_chat_model("google_genai:gemini-2.5-flash-lite")
class MyState(TypedDict) :
  messages:Annotated[list,add_messages]
graph =StateGraph(MyState)
memory=MemorySaver()
def chat_node(state:MyState):
  print(f"inside chart_model {state}")
  responce=model.invoke(state["messages"])
  return {"messages":[responce]}

graph.add_node('Chart',chat_node)
graph.set_entry_point('Chart')
graph.add_edge('Chart',END)
agent=graph.compile(checkpointer=memory)
configuration ={
    "configurable":{
        "thread_id":1
    }
}
ans= agent.invoke({"messages":[HumanMessage(content="What is Binary search give detail")]},config=configuration)
print(ans["messages"][1].content)
