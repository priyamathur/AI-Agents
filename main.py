# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import Tool, DuckDuckGoSearchResults
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    load_dotenv()
    ddg_search = DuckDuckGoSearchResults()
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
    }

    def parse_html(content) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        text_content_with_links = soup.get_text()
        return text_content_with_links

    def fetch_web_page(url: str) -> str:
        response = requests.get(url, headers=HEADERS)
        return parse_html(response.content)

    web_fetch_tool = Tool.from_function(
        func=fetch_web_page,
        name="WebFetcher",
        description="Fetches the content of a web page"
    )
    prompt_template = "Summarize the following content: {content}"
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )
    summarize_tool = Tool.from_function(
        func=llm_chain.run,
        name="Summarizer",
        description="Summarizes a web page"
    )
    tools = [ddg_search, web_fetch_tool, summarize_tool]

    agent = initialize_agent(
        tools=tools,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=llm,
        verbose=True,
        handle_parsing_errors=True,
    )
    prompt = "Research how to use the requests library in Python. Use your tools to search and summarize content into a guide on how to use the requests library."

    print(agent.run(prompt))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/