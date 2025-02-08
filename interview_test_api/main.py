from fastapi import FastAPI
from interview_test_api.routes import router
import uvicorn

interview_test_api = FastAPI(title="Interview Quiz API")

# Include our routes
interview_test_api.include_router(router)

if __name__ == "__main__":
    uvicorn.run("interview_test_api.main:interview_test_api", host="127.0.0.1", port=8000, reload=True)
