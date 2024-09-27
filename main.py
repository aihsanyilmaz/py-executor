import os

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from dependencies import getTokenHeader
from process import getFilePath, runFile

#

app = FastAPI(dependencies=[Depends(getTokenHeader)])

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://127.0.0.1:8000", "https://blabla.domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#

@app.get("/")
async def root():
    return {"message": "Hello World .."}
#

class RunRequest(BaseModel):
    processId: str
    package: str
    args: dict | None = []

@app.post("/run")
async def run(r: RunRequest, background_tasks: BackgroundTasks):
    if not os.path.exists(getFilePath(r.package)):
        raise HTTPException(status_code=404, detail=f"Package '{r.package}.py' not found")
    
    background_tasks.add_task(runFile, r.processId, r.package, r.args, r.kwargs)

    return {"status": "started"}
#

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
