import sys
from src.core.factory import get_provider
from src.telemetry.logger import logger

def main():
    """
    Baseline Chatbot without ReAct logic.
    Used for evaluation and comparison against the Agent.
    """
    print("Initializing Chatbot Baseline...")
    try:
        llm = get_provider()
    except Exception as e:
        print(f"Error initializing provider: {e}")
        sys.exit(1)
        
    print(f"Using Model: {llm.model_name}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue
                
            logger.log_event("CHATBOT_START", {"input": user_input, "model": llm.model_name})
            
            print("Chatbot: ", end="", flush=True)
            full_response = ""
            
            # Using streaming for better UX
            for chunk in llm.stream(user_input):
                print(chunk, end="", flush=True)
                full_response += chunk
            print("\n")
            
            logger.log_event("CHATBOT_END", {"response_length": len(full_response)})

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            logger.log_event("CHATBOT_ERROR", {"error": str(e)})

if __name__ == "__main__":
    main()
