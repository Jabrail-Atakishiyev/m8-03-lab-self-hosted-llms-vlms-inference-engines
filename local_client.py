"""
Task 2 — Hit the local Ollama endpoint from Python.

WHY THIS IS "THE SAME SHAPE" AS A HOSTED GEMINI CALL:
-------------------------------------------------------
When you call Gemini (or OpenAI, or any hosted LLM), you're sending an
HTTP POST request to a remote server with a JSON body containing your
messages, and you get back a JSON response with the model's reply.

Ollama does the EXACT same thing — just on your own machine at localhost.
The request format, the response structure, even the field names
(model, messages, choices, content) are identical. The *only* difference
is the URL: "https://generativelanguage.googleapis.com/..." vs
"http://localhost:11434/v1/...". The LLM doesn't care where it runs —
it's all just HTTP + JSON. This is why the openai SDK works against
Ollama unchanged: swap base_url, and the rest is copy-paste.

Run Ollama first (it starts a server automatically when you `ollama run`
or `ollama serve`), then:

    pip install -r requirements.txt
    python local_client.py
"""

from openai import OpenAI

# Point the OpenAI client at your LOCAL Ollama server instead of the cloud.
# This is the whole insight of the lab: "calling an LLM" is just an HTTP
# request to an inference server — wherever that server happens to run.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required by the client library, but ignored by Ollama
)

MODEL = "llama3.2:3b"  # change to any model you pulled with `ollama pull`
PROMPT = "In one sentence, what is an inference engine?"


def main() -> None:
    print(f"Sending prompt to local Ollama ({MODEL})...\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user",   "content": PROMPT},
        ],
    )

    answer = response.choices[0].message.content
    print(f"Model response:\n{answer}\n")

    # --- Reflection ---
    # This call looks identical to a Gemini or OpenAI call because it IS
    # structurally identical. We build a list of {role, content} messages,
    # POST them to an inference server, and read back choices[0].message.content.
    # Ollama simply runs that inference server locally instead of in the cloud.
    # Change base_url to a hosted endpoint and the rest of this script works
    # unchanged — proof that "calling an LLM" is just HTTP to a server.
    print("(Reflection) Same shape as a hosted API call — only base_url differs.")


if __name__ == "__main__":
    main()
