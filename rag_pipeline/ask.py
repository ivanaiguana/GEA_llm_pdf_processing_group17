
import openai
import os

def ask_gpt(context_chunks, question, deployment="gpt-35-turbo"):
    context = "\n\n".join(context_chunks)
    prompt = f"Use the following context to answer:\n{context}\n\nQuestion: {question}"

    response = openai.ChatCompletion.create(
        engine=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=400
    )
    return response.choices[0].message["content"]
