# ResearchMind — Multi-Agent Research System

ResearchMind is a web-based research tool built with Python, LangChain, Groq, and Streamlit. It takes a research topic and processes it through four stages: searching for relevant information, reading source material, writing a report, and reviewing the final output.

The idea behind the project is to break a research task into smaller steps instead of asking a single LLM call to handle everything.

## How it works

The application follows a sequential workflow:

1. **Search Agent** — searches the web for relevant information using Tavily and returns source URLs and snippets.
2. **Reader Agent** — reads selected web pages and extracts useful information using BeautifulSoup.
3. **Writer Agent** — combines the collected information into a structured report with key findings, an introduction, a conclusion, and source URLs.
4. **Critic Agent** — reviews the generated report, identifies strengths and areas for improvement, and provides a score and verdict.

The agents run one after another, with each stage using the output of the previous stages.

## Tech stack

- **Python** — application logic and workflow
- **LangChain** — LLM integration and tool-based agents
- **Groq** — language model inference
- **Tavily** — web search
- **Requests & BeautifulSoup** — fetching and extracting webpage content
- **Streamlit** — web interface
- **python-dotenv** — loading API keys from environment variables

## Project structure

```text
Multi Agent System/
├── agents.py          # Agent and LLM configuration
├── tools.py           # Web search and webpage scraping tools
├── pipeline.py        # Research workflow
├── app.py             # Streamlit interface
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed)
├── .gitignore
└── README.md
```


No license has been added yet. If you plan to make this repository public for reuse, consider adding an appropriate open-source license.
