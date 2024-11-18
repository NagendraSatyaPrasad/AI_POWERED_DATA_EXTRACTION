import requests

def google_search(query, api_key, cse_id, num_results=3):
    """
    Perform a Google search and return top results.
    """
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("items", [])
        return [(item["title"], item["link"], item["snippet"]) for item in results]
    else:
        return []
