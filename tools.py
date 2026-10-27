
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web and return concise results with source URLs."""
    results = tavily.search(query=query, max_results=3)

    output = []

    for result in results.get("results", []):
        output.append(
            f"Title: {result.get('title', '')[:120]}\n"
            f"URL: {result.get('url', '')}\n"
            f"Snippet: {result.get('content', '')[:180]}"
        )

    return "\n---\n".join(output)[:1800]


@tool
def scrape_url(url: str) -> str:
    """Extract relevant text from a webpage URL."""
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script", "style", "nav", "footer",
            "header", "aside", "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:2000]

    except requests.RequestException as exc:
        return f"Could not scrape URL: {exc}"
