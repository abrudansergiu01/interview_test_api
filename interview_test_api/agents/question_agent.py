import requests
import json
from interview_test_api.config import LM_STUDIO_API_URL, HEADERS


# The agent that generates the interview questions
def generate_questions(job_description: str) -> list:
    # I chose to use a higher temperature for better creativity for the generated questions
    temperature = 0.9
    max_tokens = 200

    # data payload for the request
    DATA = {
        "model": "mistral-7b-instruct-v0.3",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Generate three interview questions for the role of **{job_description}**.\n\n"
                    "### Return the questions in **valid JSON format** with no additional text.\n"
                    "The response should strictly follow this structure:\n"
                    "{ \"questions\": [ \"First question\", \"Second question\", \"Third question\" ] }\n\n"
                    "**Make sure the questions are clear, relevant, and well-structured.**"
                )
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stop": ["\n\n", "###"]
    }

    # Send request to LM Studio
    response = requests.post(LM_STUDIO_API_URL, headers=HEADERS, data=json.dumps(DATA))
    if response.status_code == 200:
        result = response.json()
        response_text = result["choices"][0]["message"]["content"]
        try:
            data = eval(response_text)
        except Exception as e:
            print("Error parsing response:", e)
            print("Raw response:", response_text)
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return [q for q in data["questions"][:3]]

