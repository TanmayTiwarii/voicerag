from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_openai import ChatOpenAI
from app.rag.retriever import get_retriever
from app.rag.prompts import QA_PROMPT
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_rag_agent():
    """Initializes and returns the LangChain ReAct agent."""
    if not settings.XAI_API_KEY:
        logger.warning("XAI_API_KEY is not set. The agent will fail if called.")
        
    # Initialize the LLM for reasoning (using Grok via OpenAI compatible endpoint)
    llm = ChatOpenAI(
        model="grok-2-latest", 
        temperature=0,
        api_key=settings.XAI_API_KEY,
        base_url="https://api.x.ai/v1"
    )
    
    # Initialize retriever
    retriever = get_retriever()
    
    def retrieve_context(query: str) -> str:
        """Helper function for the retriever tool."""
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])
    
    # Define tools for the agent
    tools = [
        Tool(
            name="SearchTranscripts",
            func=retrieve_context,
            description="Use this tool to search through call transcripts to find context to answer user questions. Input should be a specific search query."
        )
    ]
    
    # Create the ReAct agent
    agent = create_react_agent(llm, tools, QA_PROMPT)
    
    # Create Agent Executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor

def query_agent(question: str) -> str:
    """Entry point to query the agent."""
    agent_executor = get_rag_agent()
    
    try:
        response = agent_executor.invoke({
            "input": question,
            "chat_history": "" # Can be expanded to include history later
        })
        return response.get("output", "Sorry, I could not generate a response.")
    except Exception as e:
        logger.error(f"Error querying agent: {e}")
        return f"An error occurred: {str(e)}"
