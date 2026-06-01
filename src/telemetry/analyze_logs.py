import os
import json
import glob
from collections import Counter

def analyze_logs(log_dir="logs"):
    if not os.path.exists(log_dir):
        print(f"Log directory '{log_dir}' does not exist.")
        return

    log_files = glob.glob(os.path.join(log_dir, "*.log"))
    if not log_files:
        print(f"No log files found in '{log_dir}'.")
        return

    total_runs = 0
    success_runs = 0
    failed_runs = 0
    parsing_errors = 0
    tool_hallucinations = 0
    total_cost = 0.0
    token_ratios = []
    
    print(f"Analyzing {len(log_files)} log file(s)...\n")

    for file_path in log_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    log_entry = json.loads(line)
                    event = log_entry.get("event")
                    data = log_entry.get("data", {})
                    
                    if event == "AGENT_START" or event == "CHATBOT_START":
                        total_runs += 1
                    
                    elif event == "AGENT_STEP":
                        result = data.get("result", "")
                        if "Action:" not in result and "Final Answer:" not in result:
                            parsing_errors += 1
                            
                    elif event == "AGENT_END":
                        if "final_answer" in data:
                            success_runs += 1
                        elif "error" in data:
                            failed_runs += 1
                            
                    elif event == "TOOL_ERROR":
                        if data.get("type") == "hallucination":
                            tool_hallucinations += 1
                            
                    elif event == "LLM_METRIC":
                        total_cost += data.get("estimated_cost_usd", 0.0)
                        if "token_ratio" in data:
                            token_ratios.append(data["token_ratio"])
                            
                except json.JSONDecodeError:
                    pass

    avg_ratio = sum(token_ratios)/len(token_ratios) if token_ratios else 0.0

    print("=== FAILURE ANALYSIS & METRICS REPORT ===")
    print(f"Total Runs (Agent/Chatbot): {total_runs}")
    print(f"Successful Runs (Final Answer): {success_runs}")
    print(f"Failed Runs (Timeout/Max Steps/Error): {failed_runs}")
    print("-" * 40)
    print(f"Parsing Errors (Format not followed): {parsing_errors}")
    print(f"Tool Hallucinations (Invalid tool called): {tool_hallucinations}")
    print("-" * 40)
    print(f"Estimated Total Cost (USD): ${total_cost:.6f}")
    print(f"Average Token Ratio (Completion/Prompt): {avg_ratio:.2f}")
    print("=========================================\n")

if __name__ == "__main__":
    # Go up one level from src/telemetry to project root, then into logs
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir_path = os.path.join(root_dir, "logs")
    analyze_logs(log_dir_path)
