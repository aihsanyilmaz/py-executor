import os
from typing import Annotated

from fastapi import Header, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

apiKeyHeader = APIKeyHeader(name="X-API-KEY")

async def get_token_header(apiKey: Annotated[str, Header(alias="X-API-KEY")]):
    if apiKey != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Api Key",
            headers={"WWW-Authenticate": "API-KEY"},
        )
    return True
