
from fastapi import APIRouter, HTTPException

from interview_test_api.models.models import (
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitResponseRequest,
    SubmitResponseResponse,
    CompleteInterviewRequest,
    InterviewSummary,
)
from interview_test_api.services.interview_service import (
    start_interview_service,
    submit_response_service,
    complete_interview_service,
)

router = APIRouter()


@router.post("/start_interview", response_model=StartInterviewResponse)
def start_interview(req: StartInterviewRequest):
    try:
        response = start_interview_service(req)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/submit_response", response_model=SubmitResponseResponse)
async def submit_response(req: SubmitResponseRequest):
    try:
        response = await submit_response_service(req)
        return response
    except KeyError:
        raise HTTPException(status_code=404, detail="Interview session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete_interview", response_model=InterviewSummary)
async def complete_interview(req: CompleteInterviewRequest):
    try:
        summary = await complete_interview_service(req)
        return summary
    except KeyError:
        raise HTTPException(status_code=404, detail="Interview session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
