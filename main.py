import asyncio, uvicorn, importlib.util

from dotenv import load_dotenv
load_dotenv()

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union

from dependencies import getTokenHeader
from modules.logger import configureModuleLogger
from modules.pusher import pusher
#

app = FastAPI(dependencies=[Depends(getTokenHeader)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"], # GET, POST, PUT, DELETE
    allow_headers=["X-API-KEY", "Content-Type"],
)
#

@app.get("/")
async def root():
    return {"message": "Hello World .."}
#

class RequestModel(BaseModel):
    package: str
    logger: Optional[bool] = False
    args: Union[dict, None] = {}

@app.post("/run")
async def run(r: RequestModel, backgroundTasks: BackgroundTasks):
    package = f"packages.{r.package.replace('/', '.')}"
    try:
        module = importlib.import_module(package)
        
        configureModuleLogger(module, r.package, r.logger)
        setattr(module, 'pusher', pusher)

        if hasattr(module, "run"):
            func = module.run
            if asyncio.iscoroutinefunction(func):
                backgroundTasks.add_task(func, r.args)
                return {
                    "status": "success",
                    "message": "Async task started in the background."
                }
            else:
                result = func(r.args)
                return {"status": "success", "result": result}
        else:
            raise HTTPException(
                status_code=400,
                detail="The module does not have a 'run' function.")
    except ModuleNotFoundError:
        raise HTTPException(status_code=404,
                            detail=f"Module '{package}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
