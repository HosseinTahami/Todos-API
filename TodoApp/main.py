from fastapi import FastAPI, status
from .database import engine
from .models import Base
from .routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy", status_code=status.HTTP_200_OK)
def health_check():
    return {
        'status':'Healthy'
    }

app.include_router(router=auth.router)
app.include_router(router=todos.router)
app.include_router(router=admin.router)
app.include_router(router=users.router)