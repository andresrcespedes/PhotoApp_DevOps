#!/usr/bin/env python3

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import Response
from fastapi.logger import logger

from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel,BaseSettings
from typing import List
import pymongo
import requests
from models import Fmodel

from beanie import Document, init_beanie
import asyncio, motor

import re

from typing import Literal
from filters import blur, sharpen, contour

class Settings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: str = "27017"
    mongo_user: str = ""
    mongo_password: str = ""
    database_name: str = "filters"

    photo_host: str = "photo-service"
    photo_port: str = "80"

settings = Settings()

photo_service = 'http://' + settings.photo_host + ':' + settings.photo_port

app = FastAPI(title = "Filter Service")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FILTERS = [
    'blur',
    'sharpen',
    'contour',
]

# FastAPI logging
#gunicorn_logger = logging.getLogger('gunicorn.error')
#logger.handlers = gunicorn_logger.handlers

@app.on_event("startup")
async def startup_event():
    conn = f"mongodb://"
    if settings.mongo_user:
        conn += f"{settings.mongo_user}:{settings.mongo_password}@"
    conn += f"{settings.mongo_host}:{settings.mongo_port}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn)
    await init_beanie(database=client['filters'], document_models=[Filter])

    # connect("devops-s21-00-filter-db",
    #         username="devops-s21-00-user",
    #         password="***",
    #         host="mongo.cloud.rennes.enst-bretagne.fr")

@app.get("/filters", response_model = Filters, status_code = 200)    
async def get_filters():
    return FILTERS

@app.post("/filter", status_code = 201)
async def filter_(type: Literal['blur', 'sharpen', 'contour'], body: Fmodel):

    photo_uri = body.uri

    try:
        photo = requests.get(f'{photo_service}/{photo_uri}',
                             timeout=REQUEST_TIMEOUT)
        if photo.status_code == requests.codes.ok:
            # we need to open the file so that we can filter
            # we need to ask how to get the bytes and open it in the ImageFilter lib
            # Image.open(filename)
            image = ''
        elif photo.status_code == requests.codes.unavailable:
            raise HTTPException(status_code = 503, detail = "Mongo unavailable")
        elif photo.status_code == requests.codes.not_found:
            raise HTTPException(status_code = 404, detail = "Photo Not Found")
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        raise HTTPException(status_code = 503, detail = "Mongo unavailable")

    if type == 'blur':
        blur(image)
    elif type == 'sharpen':
        sharpen(image)
    elif type == 'contour':
        contour(image)

@app.get("/filter/{display_name}", response_model = FilterDesc, status_code = 200)    
async def get_filter(display_name: str = Dname.PATH_PARAM):

    try:
        filter = await Filter.find_one(Filter.display_name == display_name)    
        if filter is not None:
            return filter
        else:
            raise HTTPException(status_code = 404, detail = "Filter does not exist")
    except:
        raise HTTPException(status_code=503, detail="Mongo unavailable")


@app.put("/filter/{display_name}", status_code = 200)
async def update_filter(display_name: str = Dname.PATH_PARAM,
                        filter: FilterDesc = FILTER_BODY):
    try:
        found = await Filter.find_one(Filter.display_name == display_name)    
        if found is None:
            raise HTTPException(status_code = 503, detail = "Not Found")
        else:
            await found.set(dict(filter))
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")


@app.delete("/filter/{display_name}", status_code = 200)
async def delete_filter(display_name: str = Dname.PATH_PARAM):
    try:
        found = await Filter.find_one(Filter.display_name == display_name)    
        if found is None:
            raise HTTPException(status_code = 404, detail = "Not Found")
        else:
            await found.delete()
    except pymongo.errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Mongo unavailable")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    #logger.setLevel(logging.DEBUG)
else:
    #logger.setLevel(gunicorn_logger.level)
    pass
