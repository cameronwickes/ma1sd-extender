from fastapi import Request, Header
from fastapi.responses import JSONResponse
import requests
import os
import asyncio
import json


async def findUsers(request: Request):
    # Declare constants
    MA1SD_EXTENDER_USERNAME = os.getenv("MA1SD_EXTENDER_USERNAME", "")
    MA1SD_EXTENDER_PASSWORD = os.getenv("MA1SD_EXTENDER_PASSWORD", "")
    MA1SD_EXTENDER_FEDERATED_DOMAINS = json.loads(os.getenv("MA1SD_EXTENDER_FEDERATED_DOMAINS", "[]").replace('\'', '"'))
    MA1SD_EXTENDER_MATRIX_DOMAIN = os.getenv("MA1SD_EXTENDER_MATRIX_DOMAIN", "")
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
        parsedBody = json.loads(body)
        searchTerm = parsedBody["search_term"]
    except:
        return JSONResponse(status_code=400, content={'errcode': 'M_UNKNOWN', 'error': 'search_term` is required field', 'success': False})

    # Check if to recurse or not.
    recurse = True
    if "no_recursion" in parsedBody.keys():
        recurse = False

    # Check access token is valid with a federation domain.
    validAccessToken = False
    for domain in MA1SD_EXTENDER_FEDERATED_DOMAINS:
        if checkAccessToken(domain, headers):
            validAccessToken = True
    if checkAccessToken(MA1SD_EXTENDER_MATRIX_DOMAIN + ':4343', headers):
        validAccessToken = True

    # Return if the access token provided is not valid for any federation domain.
    if not validAccessToken:
        return JSONResponse(status_code=400, content={"errcode": "M_UNKNOWN_TOKEN", "error": "Invalid macaroon passed.", "soft_logout": False})

    directoryListings = []

    # Add the local directory listing.
    directoryListings.append(getDirectorySearch('http', 'localhost:8090', f"Bearer {MA1SD_EXTENDER_ACCESS_TOKEN}", parsedBody))

    # Do recursive directory listing if requested.
    if recurse:
        parsedBody["no_recursion"] = True
        for domain in MA1SD_EXTENDER_FEDERATED_DOMAINS:
            directoryListings.append(getDirectorySearch('https', domain, headers["authorization"], parsedBody))

    # Get final response and return it.
    response = parseDirectoryListings(directoryListings)
    return JSONResponse(status_code=200, content=response)


def getAccessToken(domain, username, password):
    try:
        # Gain access token.
        url = f"https://{domain}:4343/_matrix/client/r0/login"
        body = {"type": "m.login.password", "identifier": {"type": "m.id.user", "user": f"{username}"}, "password": f"{password}"}

        # Make request.
        response = requests.post(url, json=body)
        # Return result.
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            return "M_FORBIDDEN"
    except:
        return "M_FORBIDDEN"


def checkAccessToken(domain, headers):
    try:
        # Validate access token.
        url = f"https://{domain}/_matrix/client/r0/account/3pid"
        headers = {"Authorization": headers["authorization"]}
        print(url)
        print(headers)
        response = requests.get(url, headers=headers)
        print(response)

        # Return result.
        if response.status_code == 200:
            return True

        # Return false if no OK status code.
        return False
    except:
        return False


def getDirectorySearch(https, domain, token, body):
    try:
        # Set headers.
        url = f"{https}://{domain}/_matrix/client/r0/user_directory/search"
        headers = {"Authorization": token}
        print(url, headers)

        # Get response and return it.
        response = requests.post(url, json=body, headers=headers)
        print(response.json())
        if response.status_code == 200 and "error" not in response.json().keys():
            return response.json()
        return []
    except:
        return []


def parseDirectoryListings(directoryListings):
    directory = {"limited": False, "results": []}
    try:
        for dir in directoryListings:
            # Set limited to true if one is true.
            print(dir)
            if dir["limited"] == True:
                directory["limited"] = True
            # Append the results together.
            directory["results"] += dir["results"]

        return directory
    except:
        return directory
