from fastapi import Request, Header
from fastapi.responses import JSONResponse
from os import getenv
from requests import get, post
from json import loads
from itertools import chain
import asyncio


async def findUsers(request: Request):
    # Declare constants
    MA1SD_EXTENDER_USERNAME, MA1SD_EXTENDER_PASSWORD, MA1SD_EXTENDER_FEDERATED_DOMAINS, MA1SD_EXTENDER_MATRIX_DOMAIN = getenv("MA1SD_EXTENDER_USERNAME", ""), getenv("MA1SD_EXTENDER_PASSWORD", ""), loads(getenv("MA1SD_EXTENDER_FEDERATED_DOMAINS", "[]").replace('\'', '"')), getenv("MA1SD_EXTENDER_MATRIX_DOMAIN", "")
    MA1SD_EXTENDER_ACCESS_TOKEN = getAccessToken(MA1SD_EXTENDER_MATRIX_DOMAIN, MA1SD_EXTENDER_USERNAME, MA1SD_EXTENDER_PASSWORD)

    # Return bad response if credentials are wrong.
    if MA1SD_EXTENDER_ACCESS_TOKEN == "M_FORBIDDEN":
        return JSONResponse(status_code=400, content={'errcode': 'M_UNKNOWN', 'error': 'wrong credentials specified for ma1sd_extender', 'success': False})

    # Grab body and headers.
    body = await request.body()
    headers = request.headers

    # Extract the search term from the request body or return 400 client error.
    parsedBody = ""
    try:
        parsedBody = loads(body)
    except:
        return JSONResponse(status_code=400, content={'errcode': 'M_UNKNOWN', 'error': 'search_term` is required field', 'success': False})

    # Check access token is valid with a federation domain.
    validAccessToken = any([checkAccessToken(domain, headers) for domain in chain(MA1SD_EXTENDER_FEDERATED_DOMAINS, [f"{MA1SD_EXTENDER_MATRIX_DOMAIN}:4343"])])

    # Return if the access token provided is not valid for any federation domain.
    if not validAccessToken:
        return JSONResponse(status_code=400, content={"errcode": "M_UNKNOWN_TOKEN", "error": "Invalid macaroon passed.", "soft_logout": False})

    # Retrieve local results.
    localDirectoryListings = [getDirectorySearch('http', 'localhost:8090', f"Bearer {MA1SD_EXTENDER_ACCESS_TOKEN}", parsedBody)]

    # Do recursive directory listing if requested.
    if "no_recursion" not in parsedBody.keys():
        parsedBody["no_recursion"] = True
        remoteDirectoryListings = [getDirectorySearch('https', domain, headers["authorization"], parsedBody) for domain in MA1SD_EXTENDER_FEDERATED_DOMAINS]

    # Get final response and return it.
    return JSONResponse(status_code=200, content=parseDirectoryListings(chain(localDirectoryListings, remoteDirectoryListings)))


async def getAccessToken(domain, username, password):
    try:
        # Gain access token.and make request.
        url, body = f"https://{domain}:4343/_matrix/client/r0/login", {"type": "m.login.password", "identifier": {"type": "m.id.user", "user": f"{username}"}, "password": f"{password}"}
        return post(url, json=body).json()["access_token"]
    except:
        return "M_FORBIDDEN"

async def checkAccessToken(domain, headers):
    try:
        # Validate access token.
        url, headers = f"https://{domain}/_matrix/client/r0/account/3pid", {"Authorization": headers["authorization"]}
        return get(url, headers=headers).status_code == 200
    except:
        return False


async def getDirectorySearch(https, domain, token, body):
    try:
        # Set headers.
        url, headers = f"{https}://{domain}/_matrix/client/r0/user_directory/search", {"Authorization": token}
        response = post(url, json=body, headers=headers)

        if response.status_code == 200 and "error" not in response.json().keys():
            return response.json()
        return []
    except:
        return []


async def parseDirectoryListings(directoryListings):
    try:
        return {"limited": any([x["limited"] for x in directoryListings]), "results": chain(*[x["results"] for x in directoryListings])}
    except:
        return {"limited": False, "results": []}
