import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID


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


def display_search_results(query):
    """
    Display search results for a given query.

    Parameters:
        query (str): The search query.
    """
    results = search_web(query)
    if results:
        print(f"\nSearch Results for '{query}':")
        for i, result in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}\n")
    else:
        print("No results to display.")


def main():
    """
    Main function to handle user input and perform web search.
    """
    print("Welcome to Aura's Web Browsing Module!")
    while True:
        user_query = input("\nEnter your search query (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            print("Exiting the Web Browsing Module.")
            break
        display_search_results(user_query)


if __name__ == "__main__":
    main()
