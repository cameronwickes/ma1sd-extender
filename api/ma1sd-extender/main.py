import uvicorn
from fastapi import FastAPI, Request, Body, Response, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.memory import CACHE_KEY, InMemoryCacheBackend
from json import loads
import asyncio
import search
import models

description="""
The `ma1sd_extender` API allows Matrix user directories to be federated for corporate use.

All federation servers must have compatible ma1sd versions and run the `ma1sd_extender` API for user directories to sync.
"""

app = FastAPI(title="ma1sd-extender",
    description=description,
    version="0.0.1",
    contact={
        "name": "Cameron Wickes",
        "url": "https://cameronwickes.co.uk",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def cache():
    return caches.get(CACHE_KEY)

@app.on_event('startup')
async def onStartup():
    rc = InMemoryCacheBackend()
    caches.set(CACHE_KEY, rc)

@app.on_event('shutdown')
async def onShutdown():
    await close_caches()

@app.get("/", summary="Check MA1SD extender is running", response_model = models.RootResponse)
async def root():
    """
    Endpoint for determining if API is functioning correctly. Should return 'MA1SD Extender' if API is up.
    """
    return {"message": "MA1SD Extender"}

@app.post("/_matrix/client/r0/user_directory/search", summary="Recursively search for Matrix users", response_model = models.UserDirectoryResponse)
async def userDirectory(request: Request, cache: InMemoryCacheBackend = Depends(cache), access_token: str | None = None, requestBody: models.UserDirectoryBody = Body(..., example={"search_term": "johndoe@example.org", "no_recursion": True})):
    """
    Endpoint that attempts to compile a list of all potential users a client could be referring to. Recursively searches federation servers for users within their own user directories.

    **Request Body**

    The request body has one required field and one optional field:

    - search_term: str - The term to search for (required)
    - no_recursion : bool = false - Whether to recursively check federation servers (optional)

    **Response Body**

    The response body has 4 fields:

    - limited: bool - Whether the search has been limited
    - results: list - List of gathered users (contains display_name and user_id)
    - display_name: str - Display name of each gathered user
    - user_id : str - Matrix ID of each gathered user
    """
    response = await search.findUsers(request, cache)
    return response
