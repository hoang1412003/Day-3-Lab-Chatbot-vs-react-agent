import os
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        TODO: Implement the system prompt that instructs the agent to follow ReAct.
        Should include:
        1.  Available tools and their descriptions.
        2.  Format instructions: Thought, Action, Observation.
        """
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        return f"""
        You are an intelligent assistant. You have access to the following tools:
        {tool_descriptions}

        Use the following format:
        Thought: your line of reasoning.
        Action: tool_name(arguments)
        Observation: result of the tool call.
        ... (repeat Thought/Action/Observation if needed)
        Final Answer: your final response.
        """

    def run(self, user_input: str) -> str:
        """
        Implemented ReAct loop logic (v2 with Guardrails and Metrics).
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        current_prompt = user_input
        steps = 0
        consecutive_errors = 0
        max_retries = 3
        
        total_prompt_tokens = 0
        total_completion_tokens = 0

        while steps < self.max_steps:
            # Generate LLM response
            response = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            result = response.get('content', '')
            usage = response.get('usage', {})
            
            # Metrics aggregation
            total_prompt_tokens += usage.get('prompt_tokens', 0)
            total_completion_tokens += usage.get('completion_tokens', 0)
            
            logger.log_event("AGENT_STEP", {"step": steps, "result": result, "usage": usage})
            
            # Parse Thought/Action from result
            action_match = re.search(r"Action:\s*(.*?)\((.*?)\)", result)
            final_answer_match = re.search(r"Final Answer:\s*(.*)", result, re.DOTALL)
            
            if final_answer_match:
                final_answer = final_answer_match.group(1).strip()
                self._log_metrics(steps + 1, total_prompt_tokens, total_completion_tokens)
                logger.log_event("AGENT_END", {"steps": steps + 1, "final_answer": final_answer})
                return final_answer
                
            if action_match:
                consecutive_errors = 0 # reset on success
                tool_name = action_match.group(1).strip()
                tool_args = action_match.group(2).strip()
                
                # Check for tool hallucination natively
                valid_tools = [t['name'] for t in self.tools]
                if tool_name not in valid_tools:
                    logger.log_event("TOOL_ERROR", {"type": "hallucination", "tool": tool_name})
                    observation = f"Error: Tool '{tool_name}' does not exist. Please use one of: {', '.join(valid_tools)}."
                else:
                    observation = self._execute_tool(tool_name, tool_args)
                    
                current_prompt += f"\n{result}\nObservation: {observation}\n"
            else:
                consecutive_errors += 1
                if consecutive_errors >= max_retries:
                    error_msg = "Aborted due to repeated formatting errors."
                    self._log_metrics(steps + 1, total_prompt_tokens, total_completion_tokens)
                    logger.log_event("AGENT_END", {"steps": steps + 1, "error": error_msg})
                    return f"System Error: {error_msg}"
                    
                current_prompt += f"\n{result}\nObservation: Error - Could not parse action. You MUST use the exact format 'Action: tool_name(arguments)' or 'Final Answer: your answer'.\n"
                
            steps += 1
            
        self._log_metrics(steps, total_prompt_tokens, total_completion_tokens)
        logger.log_event("AGENT_END", {"steps": steps, "error": "Max steps reached"})
        return "I could not complete the task within the allowed steps."

    def _log_metrics(self, steps: int, prompt_tokens: int, comp_tokens: int):
        """Helper to calculate and log final metrics (Cost & Ratio)."""
        ratio = round(comp_tokens / max(1, prompt_tokens), 2)
        # Simple cost estimation (approximate gpt-4o rates)
        cost_usd = (prompt_tokens * 5 / 1000000) + (comp_tokens * 15 / 1000000)
        
        logger.log_event("LLM_METRIC", {
            "total_steps": steps,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": comp_tokens,
            "token_ratio": ratio,
            "estimated_cost_usd": round(cost_usd, 6)
        })

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Helper method to execute tools by name.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                func = tool.get('func') or tool.get('function')
                if callable(func):
                    try:
                        return str(func(args))
                    except Exception as e:
                        logger.log_event("TOOL_ERROR", {"type": "execution_error", "tool": tool_name, "error": str(e)})
                        return f"Error executing tool: {e}"
                else:
                    return f"Simulated result for {tool_name}({args})"
        return f"Tool {tool_name} not found."
