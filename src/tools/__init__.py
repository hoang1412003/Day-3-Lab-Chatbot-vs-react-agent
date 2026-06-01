from .calculator import calc_math
from .search import web_search

def get_all_tools():
    """
    Returns the tool specifications required by the ReAct agent.
    """
    return [
        {
            "name": "calc_math",
            "description": "Evaluates mathematical expressions like '5 + 3', '10 / 2', or '799 * 2 * 0.9'. Pass the math string as argument.",
            "function": calc_math
        },
        {
            "name": "web_search",
            "description": "Searches the web for product prices, discounts, shipping info, and general facts. Pass the search query as argument.",
            "function": web_search
        }
    ]
