from pydantic import BaseModel
from typing import List, Any, Dict

class StartInterviewRequest(BaseModel):
    candidate_id: str
    job_description: str

class StartInterviewResponse(BaseModel):
    candidate_id: str
    questions: List[str]

class SubmitResponseRequest(BaseModel):
    candidate_id: str
    question_index: int
    response: str

class SubmitResponseResponse(BaseModel):
    candidate_id: str
    question: str
    response: str
    evaluation: Dict

class CompleteInterviewRequest(BaseModel):
    candidate_id: str
class InterviewSummary(BaseModel):
    candidate_id: str
    job_description: str
    questions: Dict[str, str]
    responses: Dict[str, str]
    evaluations: Dict[str, Dict[str, Any]]