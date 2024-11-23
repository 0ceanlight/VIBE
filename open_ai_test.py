import os

import requests

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

r = requests.get("https://www.spiegel.de/wirtschaft/elektromobilitaet-aral-setzt-auf-ladeparks-ein-modell-fuer-die-zukunft-der-tankstellen-a-923d0774-da27-40ac-8039-8817d72ecd9f")

response = client.chat.completions.create(
    model="gpt-4o",
    messages = [
        {
            "role": "system",
            "content": "Return the text of the news article in the user's html. If it's blocked by a paywall, return nothing",
        },
        {
            "role": "user",
            "content": r.content
        }
    ],
    max_tokens=100
)

text = response.choices[0].message.content

import code
code.interact(local = locals())

