from pydantic import BaseModel
from typing import List

class UserDirectoryBody(BaseModel):
    search_term: str
    no_recursion: bool | None = None

class UserDirectoryResult(BaseModel):
    display_name: str = "John Doe"
    user_id: str = "@jdoe:example.org"

class UserDirectoryResponse(BaseModel):
    limited: bool = False
    results: List[UserDirectoryResult]

class RootResponse(BaseModel):
    message: str = "MA1SD Extender"
