from fastapi import FastAPI

from routers import api_router
from subscriber import kafka_router

app = FastAPI()
app.include_router(api_router)
app.include_router(kafka_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)