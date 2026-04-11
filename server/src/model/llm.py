import os
from dotenv import load_dotenv
from openai import OpenAI

# Initialize the client

load_dotenv()

# Access variables
openrouter_key = os.getenv("OPENROUTER_API_KEY")
congress_key = os.getenv("CONGRESS_API_KEY")

print("Initializing OpenAI client with key:", openrouter_key)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key,
)


# Make a request
completion = client.chat.completions.create(
    model="openai/gpt-5-nano",
    messages=[
        {"role": "user", "content": "Hi, how are you?"}
    ]
)

print(completion.choices[0].message.content)
