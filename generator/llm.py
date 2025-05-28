from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.environ.get('GROQ_API_KEY')
client=Groq(api_key=api_key)
def ask_llm(prompt, context="", model="gemma2-9b-it"):
    """
    Sends a prompt and context to the Groq LLM and returns the response.
    """
    message = [
        {"role": "system", "content": "You are a helpful assistant.Also answer which part of the context you used to answer the query "},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=0.7,
        max_tokens=512
    )

    return completion.choices[0].message.content.strip()

