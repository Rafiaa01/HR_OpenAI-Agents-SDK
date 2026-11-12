from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from src.routes.route import router

application = FastAPI(
    title="HR Leave Management API",
    description="HTTP API for employee leave management.",
    version="1.0.0",
)

application.include_router(router)


@application.get("/")
def home():
    return {"message": "HR Leave Management API is running."}