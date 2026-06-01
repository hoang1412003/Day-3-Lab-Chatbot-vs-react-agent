def web_search(query: str) -> str:
    """
    Simulates a web search for the given query.
    Returns mocked facts for lab testing.
    """
    query = query.lower()
    
    mock_db = {
        "iphone": "The iPhone 15 costs $799. Stock: 10 units available.",
        "discount": "Coupon 'WINNER' gives a 10% discount on the total price.",
        "shipping": "Shipping to Hanoi is a flat rate of $15.",
        "tax": "The current tax rate is 8%.",
        "capital": "Paris is the capital of France.",
        "weather": "Sunny and 25°C."
    }
    
    for key, info in mock_db.items():
        if key in query:
            return info
            
    return f"Search results for '{query}': No specific mocked data found. Try searching for 'iphone', 'discount', or 'shipping'."
