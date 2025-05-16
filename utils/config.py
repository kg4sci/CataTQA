from openai import OpenAI

API_KEY = 'YOUR_API_KEY'
MODEL = 'YOUR_MODEL_NAME'

# Matadata Path
TABLE_PAR_PATH = '../../metadata/parameters.json'
TABLE_PATH = '../../processing/output/'

class LLMClient:
    @staticmethod
    def query(prompt: str) -> str:
        client = OpenAI(
            api_key=API_KEY
        )
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content

