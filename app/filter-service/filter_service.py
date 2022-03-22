#!/usr/bin/env python3

import uvicorn

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseSettings
from models import PhotoModel
import requests
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
from PIL import Image
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)


class Settings(BaseSettings):
    photo_host: str = "photo-service"
    photo_port: str = "80"


settings = Settings()

photo_service = 'http://' + settings.photo_host + ':' + settings.photo_port

app = FastAPI(title="Filter Service")

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

FILTERS = {
    'blur': BLUR,
    'contour': CONTOUR,
    'detail': DETAIL,
    'edge_enhance': EDGE_ENHANCE,
    'edge_enhance_more': EDGE_ENHANCE_MORE,
    'emboss': EMBOSS,
    'find_edges': FIND_EDGES,
    'smooth': SMOOTH,
    'smooth_more': SMOOTH_MORE,
    'sharpen': SHARPEN,
}

REQUEST_TIMEOUT = 5

# FastAPI logging
# gunicorn_logger = logging.getLogger('gunicorn.error')
# logger.handlers = gunicorn_logger.handlers


@app.get("/filters", status_code=200)
async def get_filters():
    return list(FILTERS.keys())


@app.post("/filter", status_code=201)
async def filter_(response: Response,
                  body: PhotoModel,
                  type: str = Query(..., regex='|'.join(FILTERS.keys()))):

    display_name = body.photographer
    photo_id = body.photo_id

    photo = requests.get(f'{photo_service}/photo/{display_name}/{photo_id}',
                         timeout=REQUEST_TIMEOUT)
    if photo.status_code != requests.codes.ok:
        return JSONResponse(
            status_code=503,
            content={
                "message": "Could not get original photo",
                "photo_service_status_code": photo.status_code,
                "photo_service_response_body": photo.content,
            },
        )

    # save original as file
    with open('tmp_original.jpeg', 'wb') as fp:
        fp.write(photo.content)

    # filter the obtained image and save
    Image.open('tmp_original.jpeg') \
         .filter(FILTERS[type]) \
         .save('tmp_filtered.jpeg')

    # its missing information about the filter applied and original photo
    photo_response = requests.post(f'{photo_service}/gallery/{display_name}',
                                   files={'file': open('tmp_filtered.jpeg',
                                                       'rb')},
                                   timeout=REQUEST_TIMEOUT)
    if photo_response.status_code == requests.codes.created:
        filtered_uri = photo_response.headers['Location']
        response.headers['Location'] = photo_service + filtered_uri
    else:
        return JSONResponse(
            status_code=503,
            content={
                "message": "Could not upload filtered photo",
                "photo_service_status_code": photo_response.status_code,
                "photo_service_response_body": photo_response.content,
            },
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    # logger.setLevel(logging.DEBUG)
else:
    # logger.setLevel(gunicorn_logger.level)
    pass
