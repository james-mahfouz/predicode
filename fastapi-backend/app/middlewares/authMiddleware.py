from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from bson.objectid import ObjectId


from models.userModel import User
from configs.config import SECRET_KEY

security = HTTPBearer()


# async def auth_middleware(request: Request, call_next):
#     try:
#         # token = request.headers.get("Authorization", "").split(" ")[1]
#         # if not token:
#         #     raise HTTPException(status_code=403, detail="Unauthenticated")
#         # decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
#         # user = await User.get(id=decoded['id'])
#         #
#         # request.state.user = user
#         #
#         # response = await call_next(request)
#         #
#         # return response
#         token = request.headers.get('Authorization').split(' ')[1]
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         request.state.user = User.objects(_id=decoded_token.get('id')).first
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Server error")
#
#     response = await call_next(request)
#     return response

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload["id"])
        user_id = payload["id"]
        print(user_id)
        user = User.objects.get(id=ObjectId(user_id))
        print(user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
