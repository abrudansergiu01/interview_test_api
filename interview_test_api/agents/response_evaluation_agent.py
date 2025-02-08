import requests
import json
from interview_test_api.config import LM_STUDIO_API_URL, HEADERS


def evaluate_response(response: str, question: str) -> dict:
    # lower temperature for deterministic results
    temperature = 0.25
    max_tokens = 250
    top_p = 0.75
    # penalty for repetition of words
    frequency_penalty = 0.65
    presence_penalty = 0.8
    stop_sequences = ["\n\n", "###"]

    DATA = {
        "model": "mistral-7b-instruct-v0.3",
        "messages": [
            {
                "role": "user",
                "content": (
                        "You are an expert evaluator with a keen eye for detail. Your task is to evaluate the answer provided below, "
                        "focusing on accuracy, clarity, completeness, relevance, and especially the richness of details. Evaluate the answer "
                        "using the following guidelines:\n"
                        "1. Assess the answer on the above criteria.\n"
                        "2. If the answer is vague, generic, or lacks specific examples and supporting details, assign a low score (between 1.0 and 5.0).\n"
                        "3. If the answer is detailed, specific, and provides ample evidence or examples, assign a high score (between 5.5 and 10.0).\n"
                        "4. Briefly explain your score in your feedback, focusing on whether the answer meets the expected level of detail.\n"
                        "5. Return only a valid JSON object with exactly two keys: 'score' (a decimal number between 1.0 and 10.0) and 'feedback' (a concise comment). "
                        "Do not include any extra text, markdown formatting, code blocks, or commentary.\n\n"
                        "Note: Any lines intended for internal guidance (such as example outputs) should be ignored in your final output.\n\n"
                        "Question: \"" + question + "\"\n"
                        "Response: \"" + response + "\""
                )
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stop": stop_sequences
    }

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
    return data
