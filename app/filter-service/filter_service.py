#!/usr/bin/env python3

import uvicorn

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseSettings
from models import Fmodel
import requests
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware

from filters import blur, sharpen, contour

from io import BytesIO


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
    'blur': blur,
    'sharpen': sharpen,
    'contour': contour,
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
                  body: Fmodel,
                  type: str = Query(..., regex="blur|sharpen|contour")):

    photo_uri = body.uri
    _, display_name, photo_id = photo_uri.split('/')

    photo = requests.get(f'{photo_service}/{photo_uri}',
                         timeout=REQUEST_TIMEOUT)
    if photo.status_code == requests.codes.ok:
        # options
        # write the bytes in a temp file (last resort)
        # use Image.frombytes

        with open('tmp.jpeg', 'wb') as fp:
            fp.write(photo.content)
    elif photo.status_code == requests.codes.unavailable:
        raise HTTPException(status_code=503, detail="Mongo unavailable")
    elif photo.status_code == requests.codes.not_found:
        raise HTTPException(status_code=404, detail="Photo Not Found")

    # filter the obtained image
    filtered = FILTERS[type](photo.content)

    bytes_out = filtered.tobytes()

    # its missing information about the filter applied and original photo
    photo_response = requests.post(f'{photo_service}/gallery/{display_name}',
                                   files={'upload_file': BytesIO(bytes_out)},
                                   timeout=REQUEST_TIMEOUT)
    if photo_response.status_code == requests.codes.ok:
        filtered_uri = photo_response.headers['Location']
        response.headers['Location'] = photo_service + filtered_uri
    else:
        print(photo_response.status_code)
        print(photo_response.content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    # logger.setLevel(logging.DEBUG)
else:
    # logger.setLevel(gunicorn_logger.level)
    pass
