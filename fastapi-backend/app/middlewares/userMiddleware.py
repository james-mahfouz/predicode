from fastapi import HTTPException
from app.models.userModel import User
from configs.config import SECRET_KEY
import jwt


async def auth_middleware(request, call_next):
    try:
        token = request.headers.get("Authorization", "").split(" ")[1]

        if not token:
            raise HTTPException(status_code=403, detail="Unauthenticated")

        decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
        user = await User.get(id=decoded['id'])

        request.state.user = user

        response = await call_next(request)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")