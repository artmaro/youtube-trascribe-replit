import os

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def send_openai_request(prompt: str) -> str:
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=1000
    )
    content = completion.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned an empty response.")
    return content
