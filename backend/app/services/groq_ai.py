from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please create a .env file with your API key.")

client = Groq(api_key=api_key)

def get_ai_suggestions(prompt: str) -> list[str]:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You provide resume improvement advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content
        
        if not content:
            return ["Unable to generate suggestions. Please try again."]

        return [
            line.strip("-• ").strip()
            for line in content.split("\n")
            if line.strip()
        ]
    except Exception as e:
        return [f"Error: {str(e)}"]