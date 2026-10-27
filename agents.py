
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=2048
)

# 1. Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a web research search agent. "
            "Use only the provided web_search tool. "
            "Never call web_open, browser_search, or any "
            "tool that has not been provided. "
            "Search for relevant information and preserve "
            "the source URLs returned by the tool."
        )
    )


# 2. Reader Agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a research reader agent. "
            "Use only the provided scrape_url tool to read "
            "webpages. Never invent URLs or call tools that "
            "have not been provided. Extract relevant facts "
            "and preserve source URLs where available."
        )
    )


# 3. Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. "
        "Write clear, structured, factual reports. "
        "Use the supplied research and do not invent sources."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list URLs present in the supplied research)

Be detailed, factual and professional.
Clearly identify limitations or conflicting evidence."""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# 4. Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. "
        "Evaluate factual support, source quality, clarity, "
        "completeness and unsupported claims."
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
