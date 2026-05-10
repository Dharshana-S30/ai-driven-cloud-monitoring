import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_log(log_text):

    prompt = f"""
    Analyze this Kubernetes/cloud log.

    Explain:
    1. What happened
    2. Possible issue
    3. Suggested fix

    Log:
    {log_text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return result


sample_log = """
Error: Pod restarting repeatedly.
CPU usage above 90%.
Possible memory leak.
"""

analysis = analyze_log(sample_log)

print("\n===== AI ANALYSIS =====\n")
print(analysis)