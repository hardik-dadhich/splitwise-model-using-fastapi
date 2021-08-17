from typing import Optional

from fastapi import FastAPI

app = FastAPI(title="SplitWise Api Documentation", description="Various CURD API Docs for Splitwise", version="1.0.0")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

