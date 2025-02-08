
from interview_test_api.models.models import (
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitResponseRequest,
    SubmitResponseResponse,
    CompleteInterviewRequest,
    InterviewSummary,
)
from interview_test_api.session import session_context
from interview_test_api.config import DATA_DIR

from interview_test_api.agents.question_agent import generate_questions
from interview_test_api.agents.response_evaluation_agent import evaluate_response
import os
import json
import datetime
import aiofiles
import asyncio
from fastapi.concurrency import run_in_threadpool


async def evaluate_response_async(response: str, question: str, candidate_id: str, question_index: int):
    # Run the blocking evaluation in a thread pool
    result = await run_in_threadpool(evaluate_response, response, question)
    # Store the result once it's available
    session_context[candidate_id]["evaluations"][f"evaluation_{question_index}"] = result
    return result

def start_interview_service(req: StartInterviewRequest) -> StartInterviewResponse:
    candidate_id = req.candidate_id
    job_description = req.job_description
    # generate the questions
    questions = generate_questions(job_description)
    # initialize the dictionaries for the questions, responses and evaluations
    questions_dict = {f"question_{questions.index(question)+1}": question for question in questions}
    responses_dict = {f"response_{questions.index(question)+1}": None for question in questions}
    evaluations_dict = {f"evaluation_{questions.index(question)+1}": None for question in questions}
    # add session context for the current candidate.
    session_context[candidate_id] = {
        "job_description": job_description,
        "questions": questions_dict,
        "responses": responses_dict,
        "evaluations": evaluations_dict,
        "evaluation_tasks": {}
    }

    return StartInterviewResponse(candidate_id=candidate_id, questions=questions)



async def submit_response_service(req: SubmitResponseRequest) -> SubmitResponseResponse:
    candidate_id = req.candidate_id
    # we are adding +1 to the question_index, so the key will match with 'question_1', 'question_2', etc.
    question_index = req.question_index + 1
    candidate_response = req.response
    session = session_context[candidate_id]
    question = session["questions"][f'question_{question_index}']
    # Save the response immediately.
    session["responses"][f'response_{question_index}'] = candidate_response

    # Ensure there's a place to store evaluation tasks
    if "evaluation_tasks" not in session:
        session["evaluation_tasks"] = {}
    # this inner async function will perform the evaluation. So we won't have to wait for the evaluation
    async def evaluate_and_store():
        evaluation = await run_in_threadpool(evaluate_response, candidate_response, question)
        session["evaluations"][f'evaluation_{question_index}'] = evaluation

    task = asyncio.create_task(evaluate_and_store())
    session["evaluation_tasks"][f'evaluation_{question_index}'] = task

    return SubmitResponseResponse(
        candidate_id=candidate_id,
        question=question,
        response=candidate_response,
        evaluation={"status": "pending"}
    )


async def complete_interview_service(req: CompleteInterviewRequest) -> InterviewSummary:
    candidate_id = req.candidate_id
    session = session_context[candidate_id]
    job_description = session["job_description"]

    # If there is any pending evaluation task, the API will wait for it's completion.
    if "evaluation_tasks" in session:
        tasks = list(session["evaluation_tasks"].values())
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    print(f"Evaluation task error for candidate {candidate_id}: {res}")
                    # Optionally handle or log the error.

    # define summary dictionary
    summary = {
        "candidate_id": candidate_id,
        "job_description": job_description,
        "questions": session["questions"],
        "responses": session["responses"],
        "evaluations": session["evaluations"],
    }
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{candidate_id}_{job_description}_{timestamp}.json"
    file_path = os.path.join(DATA_DIR, filename)

    async with aiofiles.open(file_path, mode="w") as f:
        await f.write(json.dumps(summary))
    del session_context[candidate_id]

    return InterviewSummary(**summary)
