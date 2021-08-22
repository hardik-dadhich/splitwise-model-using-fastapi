from app.routs.v1 import app_v1
from fastapi import FastAPI

# FastAPI route
app = FastAPI(title="SplitWise CRUD API Documentation", description="Exposed APIs for Splitwise", version="1.0.0")

# Defining v1 route for versioning the application
# So all route will start from prefix /v1/*
app.include_router(app_v1, prefix="/v1")

