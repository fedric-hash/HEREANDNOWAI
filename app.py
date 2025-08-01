from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
import ast # Abstract Syntax Trees for parsing Python code
import warnings

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = "gemini-2.5-flash"

@tool
def web_scrap_tool(url):
    """
    Scrapes the content from a list of URLs.
    The input should be a string representation of Python
    list of URLs,(e.g. "['https://example.com', 'https://another.com']").
    Returns the concatenated text content of all scrapped pages.
    """
    try:
        url_list = ast.literal_eval(url)
        if not isinstance(url_list, list) or not all(isinstance(url, str) for u in url_list):
            raise ValueError("Input must be a list of URLs as a strings.Example: ['https://example.com', 'https://another.com']")
    except (ValueError,SyntaxError) as e:  
        return ValueError(f"Invalid input: {e}.please provide a valid python list of URLs .")
    combined_conent = []
    for url in url_list:
        try:
            loader = WebBaseLoader(
                [url],
                requests_kwargs={"headers": {"User-Agent": "caramel AI"}}
            )
            documents = loader.load()
            for doc in documents:
                combined_conent.append(doc.page_content)
        except Exception as e:
            combined_conent.append(f"could not scrape {url}. Error {e}.") 
    return "\n".join(combined_conent)              

def run_web_scrap_agent():
    """
    Create and runs an agent that can use the web_scrap_tool.
    """
    llm = ChatGoogleGenerativeAI(model=model, api_key=api_key)
    tools = [web_scrap_tool]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
    question_about_us ="""
                        what is the conent of the 'About Us' page of hereandnowai.com?
                        The URL is https://hereandnowai.com/about-here-and-now-ai/
                        """
    response_about_us = agent_executor.invoke({"input": question_about_us}) 
    print(f"Agent response: {response_about_us['output']}")

if __name__ == "__main__":
    run_web_scrap_agent()    
