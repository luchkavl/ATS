import time
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from ats.exceptions import CandidateNotFoundException
from ats.routers import candidates, jobs, admin, auth

# 'localhost:9999/api/v1'
app = FastAPI(root_path='/api/v1')
app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(admin.router)


@app.get('/')
async def root():
    return {'message': 'Applicant Tracking System by Vladyslav Luchka'}


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.exception_handler(CandidateNotFoundException)
async def candidate_not_found_exc_handler(request: Request, exc: CandidateNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': f'Candidate with id {exc.candidate_id} not found.'}
    )
