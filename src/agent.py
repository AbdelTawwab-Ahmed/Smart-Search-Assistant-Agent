from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7
from dotenv import load_dotenv

from tools import search_tool, calculate, save_notes, get_notes, generate_report, analyze_text

load_dotenv()


# --- Agent Setup ---

tools = [search_tool, calculate, save_notes, get_notes, generate_report, analyze_text]

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0)

checkpointer = InMemorySaver()


# --- Build Agent ---

system_prompt = '''You are a Smart Research Assistant.
                   You help users research topics, save notes, do calculations,
                   and generate structured reports. Always use tools when relevant.
                   When saving research findings, use save_notes to preserve them.
                   When asked for a summary or report, use generate_report.'''

agent = create_agent(

    model = llm,
    tools = tools,
    system_prompt = system_prompt,
    checkpointer = checkpointer
)


# --- Run Agent ---

thread_id = str(uuid7())

config = {"configurable":{"thread_id":thread_id}}

print("\n ~~~~~ Hi, How can I help you? ~~~~~ \n")

while True:

    user_input = input("Human: ")

    if user_input.lower() == "quit":
        break

    response = agent.invoke(

        {"messages":[{"role":"user", "content":user_input}]},
        config = config
    )

    print("\nBot: ", response["messages"][-1].content)