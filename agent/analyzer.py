import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_security_threat(
    file_name,
    log_info
):

    prompt = f"""
    Analyze this suspicious activity
    detected inside a Kubernetes
    cloud application.

    File:
    {file_name}

    Log Information:
    {log_info}

    Explain:
    1. Possible threat
    2. Severity
    3. Possible impact
    4. Recommended actions
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

    result = (
        response
        .choices[0]
        .message
        .content
    )

    return result