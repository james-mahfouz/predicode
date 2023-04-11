from fastapi import FastAPI
import uvicorn
import multiprocessing
import os
from starlette.middleware.cors import CORSMiddleware

# from routes.auth_routes import router as auth_router
# from routes.user_routes import router as user_router
# from routes.admin_routes import router as admin_router
# from middlewares.auth_middleware import auth_middleware
# from middlewares.admin_middleware import admin_middleware
from configs.db.config import connect_to_mongo

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_router, prefix='/auth')
# app.include_router(user_router, prefix='/user',
#                    dependencies=[Depends(auth_middleware)])
# app.include_router(admin_router, prefix='/admin',
#                    dependencies=[Depends(auth_middleware), Depends(admin_middleware)])

if __name__ == '__main__':
    num_workers = multiprocessing.cpu_count()
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port, workers=num_workers)
    connect_to_mongo()
