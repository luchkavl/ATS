from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ats.exceptions import CandidateNotFoundException
from ats.routers import candidates, jobs, admin, auth
from ats.middlewares import AddProcessTimeHeaderMiddleware

# 'localhost:9999/api/v1'
app = FastAPI(root_path='/api/v1', openapi_url="/api/v1/openapi.json")

app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(admin.router)

app.add_middleware(BaseHTTPMiddleware, dispatch=AddProcessTimeHeaderMiddleware())


@app.get('/')
async def root():
    return {'message': 'Applicant Tracking System by Vladyslav Luchka'}


@app.exception_handler(CandidateNotFoundException)
async def candidate_not_found_exc_handler(request: Request, exc: CandidateNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': f'Candidate with id {exc.candidate_id} not found.'}
    )
