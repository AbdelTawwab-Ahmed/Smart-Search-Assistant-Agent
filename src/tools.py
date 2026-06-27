from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain.tools import tool
from langchain_tavily import TavilySearch
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


# --- Tool 1 (Search on the web)---

search_tool = TavilySearch(max_results = 1)


# --- Tool 2 (Math Evaluation) ---

@tool
def calculate(expression: str) -> str:

    """Math evaluation, Use this tool in any mathematical expression or calculation."""

    try:
        return str(eval(expression))
    
    except Exception as e:
        return f"Error: {e}"


# --- Tool 3 (Save notes) --- 

notes = []

@tool
def save_notes(topic: str, note: str) -> str:

    """Save note in notes list, Use this tool when the user wants to save any note."""

    notes.append({"topic": topic, "content": note, "timestamp": datetime.now().strftime("%Y-%m-%d %I-%M %p")})
    return "Note saved successfully."


# --- Tool 4 (Display saved notes) ---

@tool
def get_notes(filter_topic: str="") -> str:

    """Return all notes or search for note with topic, Use this tool when the user asks to get saved note(s)."""

    if not notes:
        return "No notes saved yet."
    
    if not filter_topic:
        result = "\n === All saved notes === \n"
        for note in notes:
            result += f"\n- {note['content']} [At {note['timestamp']}]\n"
        
        return result
    
    filtered = [note for note in notes if note["topic"].lower() == filter_topic.lower()]

    if not filtered:
        return f"No notes found for topic: '{filter_topic}'"

    return "".join([f"\n- {note['content']} [At {note['timestamp']}]\n" for note in filtered])
        

# --- Tool 5 (Generate summary report) ---

def preprocess(inputs: dict) -> dict:
    inputs["topic"] = inputs["topic"].strip()
    return inputs

def postprocess(text: str) -> str:
    return text + "\n\n[Powered By Agents].\n"


prompt = ChatPromptTemplate.from_template('''Generate a concise, well-structured summary report about {topic}.
                                             Include key points and a short conclusion.''')

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0.3)

parser = StrOutputParser()

chain = RunnableLambda(preprocess) | prompt | llm | parser | RunnableLambda(postprocess)

@tool
def generate_report(topic: str) -> str:

    """Generate a structured 3-paragraph research summary report about a given topic.
       Use this when the user asks for a report, summary, or overview of a topic."""

    response =  chain.invoke({"topic":topic})

    return response


# --- Tool 6 (Analyze text & return `Sentiment & Top keywords`) ---

sentiment_chain = (
                ChatPromptTemplate.from_template("Analyze this text and determine its sentiment. Return only one word (positive | negative | neutral). {text}")
                | llm 
                | parser
)

keywords_chain = (
                ChatPromptTemplate.from_template("Analyze this text and extract Top 3 keywords from it as comma-separated list. {text}")
                | llm 
                | parser
)

parallel_chain = RunnableParallel({

    "sentiment": sentiment_chain,
    "keywords": keywords_chain
})

@tool
def analyze_text(text: str) -> str:

    """Analyze text and define the sentiment and top 3 keywords of it."""

    response = parallel_chain.invoke({"text":text})
    return f"Sentiment: {response['sentiment']} || Keywords: {response['keywords']}"