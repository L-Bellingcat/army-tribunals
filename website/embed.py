import os

import openai
import tiktoken
from dotenv import load_dotenv

enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4")

load_dotenv()
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_TOKENS = 8191
ENCODING = tiktoken.get_encoding("cl100k_base")


def trim_text(text: str, max_tokens: int = MAX_TOKENS):
    tokens = ENCODING.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return ENCODING.decode(tokens)


def embed_text(text: str):
    text = trim_text(text)

    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
