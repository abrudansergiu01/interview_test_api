import requests
from pprint import pprint
from interview_test_api.config import API_BASE_URL, DATA_DIR

def start_interview(candidate_id: str, job_description: str) -> dict:
    url = f"{API_BASE_URL}/start_interview"
    payload = {
        "candidate_id": candidate_id,
        "job_description": job_description
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Error starting interview:", response.text)
        exit(1)
    return response.json()

def submit_response(candidate_id: str, question_index: int, response_text: str) -> dict:
    url = f"{API_BASE_URL}/submit_response"
    payload = {
        "candidate_id": candidate_id,
        "question_index": question_index,
        "response": response_text
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Error submitting response for question {question_index + 1}:", response.text)
        exit(1)
    return response.json()

def complete_interview(candidate_id: str) -> dict:
    url = f"{API_BASE_URL}/complete_interview"
    payload = {"candidate_id": candidate_id}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Error completing interview:", response.text)
        exit(1)
    return response.json()

def main():
    print("AI Driven Interview Client\n")
    candidate_id = input("Enter candidate ID: ").strip()
    job_description = input("Enter job description: ").strip()
    print("\nStarting interview...")
    start_data = start_interview(candidate_id, job_description)
    questions = start_data.get("questions", [])
    if not questions:
        print("No questions received. Exiting.")
        exit(1)

    print("\nInterview Questions:")
    for i, question in enumerate(questions, start=1):
        print(f"{i}. {question}")

    for i, question in enumerate(questions):
        print(f"\nQuestion {i + 1}: {question}")
        answer = input("Your answer: ").strip()
        submit_response(candidate_id, i, answer)

    print("\nAll questions answered. Completing interview and saving session...")
    summary = complete_interview(candidate_id)
    print("\nInterview Summary:")
    pprint(summary)
    print("\nInterview session completed successfully.")
    print(f'The interview result will be saved as a JSON file in path: \n{DATA_DIR}\n')


if __name__ == "__main__":
    main()
