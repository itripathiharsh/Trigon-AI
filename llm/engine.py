import os
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self):
        # Load working Groq keys from .env
        self.groq_keys = [k for k in [os.getenv("GROQ_API_KEY_1"), os.getenv("GROQ_API_KEY_2")] if k]
        if not self.groq_keys:
            print("⚠️ Warning: No Groq API keys found in .env")

    def request(self, prompt, system_prompt, is_json=False):
        """
        Handles requests to Groq models with optional JSON mode.
        """
        # Models are tried in order of capability
        for model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]:
            try:
                client = Groq(api_key=random.choice(self.groq_keys))
                
                # Groq strictly requires the word 'json' in the prompt for json_object mode
                response_format = {"type": "json_object"} if is_json else None
                
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model=model,
                    response_format=response_format
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"[*] Groq {model} failed: {e}")
        
        # Final fallback if all Groq calls fail
        return '{"status": "FAIL", "retry_instruction": "API Error: All Groq models failed or rate-limited."}'