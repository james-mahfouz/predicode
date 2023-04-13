from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from bson.objectid import ObjectId


from models.userModel import User
from configs.config import SECRET_KEY

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["id"]
        user = User.objects.get(id=ObjectId(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHANTICATED,
                detail="Invalid authentication credentials",
            )
        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid role"
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
