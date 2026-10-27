
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)
import re


def run_research_pipeline(topic: str) -> dict:
    state = {}

    print("\n" + "=" * 50)
    print("Step 1 - Search Agent")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            ("user",
             f"Search for reliable sources about: {topic}. "
             "Use the web_search tool once. Return concise "
             "findings and preserve the exact source URLs.")
        ]
    })

    state["search_results"] = search_result["messages"][-1].content
    print("\nSearch results:\n", state["search_results"])

    print("\n" + "=" * 50)
    print("Step 2 - Reader Agent")
    print("=" * 50)

    # Extract URLs from the search output.
    urls = re.findall(
        r"https?://[^\s<>\])\"']+",
        state["search_results"]
    )
    urls = list(dict.fromkeys(urls))[:3]

    if urls:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [
                ("user",
                 f"Research topic: {topic}\n"
                 f"Available URLs:\n"
                 + "\n".join(urls)
                 + "\nChoose one relevant URL from this list and "
                   "use scrape_url to read it. Do not invent "
                   "URLs or use any other tools.")
            ]
        })
        state["scraped_content"] = (
            reader_result["messages"][-1].content
        )
    else:
        state["scraped_content"] = (
            "No valid source URLs were found in the search output."
        )

    print("\nScraped content:\n", state["scraped_content"])

    print("\n" + "=" * 50)
    print("Step 3 - Writer")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results'][:1800]}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content'][:2500]}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print("\nFinal report:\n", state["report"])

    print("\n" + "=" * 50)
    print("Step 4 - Critic")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"][:5000]
    })

    print("\nCritic feedback:\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip()

    if topic:
        run_research_pipeline(topic)
    else:
        print("Please enter a research topic.")
