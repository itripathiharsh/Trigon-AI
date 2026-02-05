import json
import streamlit as st
from llm.engine import LLMEngine
from llm.prompts import PLANNER_SYSTEM_PROMPT

class PlannerAgent:
    def __init__(self):
        self.engine = LLMEngine()

    def create_plan(self, user_prompt: str):
        """
        Sends the user prompt to Groq to generate a structured execution plan.
        """
        # Ensure 'json' is in the prompt for Groq JSON mode
        response = self.engine.request(
            prompt=user_prompt,
            system_prompt=PLANNER_SYSTEM_PROMPT,
            is_json=True
        )
        
        try:
            # Clean response if LLM adds markdown backticks
            clean_res = response.strip()
            if clean_res.startswith("```json"):
                clean_res = clean_res.replace("```json", "").replace("```", "").strip()
            
            plan = json.loads(clean_res)
            return plan
        except Exception as e:
            st.error(f"Planner failed to parse JSON: {e}")
            # Fallback empty plan
            return {"plan": []}