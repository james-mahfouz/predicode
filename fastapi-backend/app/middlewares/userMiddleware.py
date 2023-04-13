from fastapi import Header, HTTPException


async def user_middleware(request, call_next):
    response = await call_next(request)

    return response