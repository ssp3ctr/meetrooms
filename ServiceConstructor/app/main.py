from fastapi import FastAPI
from app.api.endpoints.service_clarify import router as service_clarify_router

app = FastAPI()

app.include_router(service_clarify_router, prefix="/service_clarify")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
