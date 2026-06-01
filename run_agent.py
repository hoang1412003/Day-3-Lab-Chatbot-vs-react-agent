import sys
from src.core.factory import get_provider
from src.agent.agent import ReActAgent
from src.tools import get_all_tools

def main():
    print("Initializing Agent v2...")
    try:
        llm = get_provider()
    except Exception as e:
        print(f"Error initializing provider: {e}")
        sys.exit(1)
        
    tools = get_all_tools()
    agent = ReActAgent(llm=llm, tools=tools, max_steps=7)
    
    print(f"Using Model: {llm.model_name}")
    print("Available Tools:")
    for t in tools:
        print(f"  - {t['name']}: {t['description']}")
    print("\nType 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue
                
            print("\nThinking...")
            result = agent.run(user_input)
            
            print(f"\nFinal Answer: {result}\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nCritical Error: {e}")

if __name__ == "__main__":
    main()
