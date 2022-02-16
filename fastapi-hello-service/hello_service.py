#!/usr/bin/env python3

import uvicorn

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi import Path

app = FastAPI()

@app.get("/hello", status_code=200)
def say_hello():
    return {'message': 'hello'}

@app.get("/hello/{firstname}", status_code=200)
def read_item(firstname, q: Optional[str] = None):
    if q:
        return {"nice to meet you": firstname}
    return {"hello": firstname}

if __name__ == "__main__":
    uvicorn.run(app, log_level="info")

