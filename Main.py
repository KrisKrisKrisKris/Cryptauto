from openai import OpenAI
from dotenv import load_dotenv
import os 

# Load environment variables from .env
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Now you can use the OpenAI library functions
# For example, you might want to set your API key
# openai.api_key = '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'

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "say hello to hannah, write a poem pls"}],
    stream = True,
    max_tokens = 10,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


