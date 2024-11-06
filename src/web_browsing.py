import requests
import webbrowser
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID, GEMINI_API_KEY
import google.generativeai as genai


# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def search_web(query, num_results=5):
    """
    Perform a web search using Google Custom Search API.

    Parameters:
        query (str): The search query.
        num_results (int): Number of results to return (default is 5).

    Returns:
        list: A list of dictionaries containing titles, links, and snippets of search results.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an error for unsuccessful status codes
        results = response.json()

        if "items" not in results:
            print("No results found.")
            return []

        search_results = []
        for item in results["items"]:
            search_results.append({
                "title": item["title"],
                "link": item["link"],
                "snippet": item.get("snippet", "No description available.")
            })

        return search_results
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while performing the search: {e}")
        return []


def display_results(results):
    """
    Displays search results in a readable format.

    Parameters:
        results (list): List of search results.
    """
    print("\nSearch Results:")
    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Snippet: {result['snippet']}\n")


def summarize_results_with_gemini(results):
    """
    Summarizes the snippets from search results using Gemini API.

    Parameters:
        results (list): List of search results.

    Returns:
        str: Summarized text of search result snippets.
    """
    snippets = " ".join([result["snippet"] for result in results])

    if snippets:
        # Send the snippets to Gemini for summarization
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Summarize the following text: " + snippets)
        return response.text
    return "No content available for summarization."


def open_link(results):
    """
    Allows the user to choose and open a link from the search results.

    Parameters:
        results (list): List of search results.
    """
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['title']} - {result['link']}")
    choice = input("\nEnter the number of the result to open (or type 'exit' to skip): ")
    if choice.isdigit() and 1 <= int(choice) <= len(results):
        webbrowser.open(results[int(choice) - 1]["link"])
        print(f"Opening link: {results[int(choice) - 1]['link']}")
    else:
        print("No link selected.")


def main():
    """
    Main function to handle user interaction, allowing them to search, display results,
    summarize, and open links.
    """
    print("Welcome to Aura's Web Browsing Module!")
    while True:
        query = input("\nEnter your search query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("Exiting the Web Browsing Module.")
            break

        # Fetch search results
        results = search_web(query)

        # Display results
        display_results(results)

        # Summarize results with Gemini
        summary = summarize_results_with_gemini(results)
        print("\nSummary of Search Results:\n", summary)

        # Allow the user to open a link
        open_link(results)


if __name__ == "__main__":
    main()
