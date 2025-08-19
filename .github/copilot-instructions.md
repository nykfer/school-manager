# GitHub Copilot Integrated Instructions for FastAPI Project

## Purpose
These instructions tell Copilot how to:
1. Write **descriptive docstrings and inline comments** for every API function.
2. Use the correct **models** from `models.py`.
3. Implement **endpoint logic**.
4. **Immediately** generate full coverage tests for the endpoint using `fastapi.testclient` in the api/test folder.

---

## API Endpoint Rules

When creating an API endpoint:
- Start with a **triple-quoted docstring** describing:
  - **Purpose** of the endpoint.
  - **Parameters** (name, type, description).
  - **Return type**.
  - **Possible status codes** and when they occur.
- Use **inline comments** to explain key logic decisions.
- Always import and use:
  - `UserCreate` (request body schema)
  - `UserPublic` or `UserPublicWithSomething` (response schema)
  - `ErrorResponse` (error schema)
- Define `responses` in the FastAPI decorator with `ErrorResponse` for error codes.
- Follow **PEP8** style consistently.

**Example Endpoint:**
```python
from fastapi import APIRouter, HTTPException, Query
from models import UserCreate, UserResponse, ErrorResponse
from database import save_user, get_user_by_email
from typing import Annotated

router = APIRouter()

@router.post(
    "/users/",
    response_model=UserPublic,
    status_code=201,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def create_user(user: Annotated[UserCreate, Query()]):
    """
    Create a new user.

    Args:
        user (UserCreate): User data to create.

    Returns:
        UserResponse: Newly created user.

    Status Codes:
        201: User created successfully.
        400: Invalid request data.
        409: User already exists.
        500: Internal server error.
    """
    # Check for duplicate email before creation
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    try:
        new_user = await save_user(user)
        return UserPublic(id=new_user.id, name=new_user.name, email=new_user.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")