import json
from llm.engine import LLMEngine
from llm.prompts import VERIFIER_SYSTEM_PROMPT

class VerifierAgent:
    def __init__(self):
        self.engine = LLMEngine()

    def verify_and_format(self, user_prompt, executor_report):
        """
        Audits tool results and converts them into user-friendly Markdown.
        """
        print("[*] Verifier auditing results...")
        
        # Prepare the context for the LLM to audit
        context = f"User Request: {user_prompt}\n\nTool Results Data: {json.dumps(executor_report)}"
        
        # We set is_json=False because we want a Markdown string for the UI, 
        # but the prompt tells it to use JSON if it needs to trigger a retry.
        raw_output = self.engine.request(
            prompt=context,
            system_prompt=VERIFIER_SYSTEM_PROMPT,
            is_json=False
        )

        # Check if the Verifier wants to trigger a retry loop
        if '"status": "FAIL"' in raw_output or '"status":"FAIL"' in raw_output:
            try:
                # Extract JSON even if there's surrounding text
                start = raw_output.find('{')
                end = raw_output.rfind('}') + 1
                data = json.loads(raw_output[start:end])
                return {"status": "FAIL", "instruction": data.get("retry_instruction")}
            except:
                pass # If parsing fails, fall back to showing the raw output

        return {"status": "SUCCESS", "content": raw_output}