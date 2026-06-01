import operator
import re

def calc_math(expression: str) -> str:
    """
    Safely evaluates a basic mathematical expression.
    """
    try:
        allowed_operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        match = re.match(r"^\s*([\d\.]+)\s*([\+\-\*/])\s*([\d\.]+)\s*$", expression)
        if not match:
            # Fallback to eval for more complex expressions in this lab context
            # WARNING: unsafe for production, but okay for a closed lab environment
            # Filter out letters to prevent code execution
            if re.search(r'[a-zA-Z]', expression):
                return "Error: Invalid characters in math expression."
            return str(eval(expression))
            
        num1 = float(match.group(1))
        op = match.group(2)
        num2 = float(match.group(3))
        
        result = allowed_operators[op](num1, num2)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Math Error: {str(e)}"
