#!/usr/bin/env python3

import uvicorn

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.requests import Request
from mongoengine import connect
from pydantic import BaseSettings
from fastapi.logger import logger
import logging
from photo import Photo
from photo_const import (REQUEST_TIMEOUT,
                         PhotoAttributesNoTags,
                         PhotoAttributes,
                         Photos)
from photo_mongo_wrapper import (mongo_allocate_photo_id,
                                 mongo_get_photo_by_name_and_id,
                                 mongo_get_photos_by_name,
                                 mongo_save_photo,
                                 mongo_set_photo_attributes)
import pymongo
import requests
import tags_pb2
from tags import TagsClient

photo_all_attributes = ["title", "comment", "location", "author"]


class Settings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: str = "27017"
    mongo_user: str = ""
    mongo_password: str = ""
    database_name: str = "photos"
    auth_database_name: str = "photographers"

    tags_host: str = "tags-service"
    tags_port: str = "50051"

    photographer_host: str = "photographer-service"
    photographer_port: str = "80"


settings = Settings()

photographer_service = \
    f'http://{settings.photographer_host}:{settings.photographer_port}/'

app = FastAPI(title="Photo Service")

# FastAPI logging
gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers

tags_client = TagsClient()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):

    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    # or logger.error(f'{exc}')
    print(request, exc_str)
    # logger.error(request, exc_str)
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.on_event("startup")
def startup_event():
    conn = "mongodb://"
    if settings.mongo_user:
        conn += f"{settings.mongo_user}:{settings.mongo_password}@"
    conn += f"{settings.mongo_host}:{settings.mongo_port}"
    conn += \
        f"/{settings.database_name}?authSource={settings.auth_database_name}"
    connect(settings.database_name, host=conn)
    tags_client.connect(settings.tags_host + ":" + settings.tags_port)


@app.post("/gallery/{display_name}", status_code=201)
def upload_photo(response: Response,
                 display_name: str,
                 file: UploadFile = File(...)):
    logger.info("Uploading a new image ...")
    try:
        photographer = requests.get(
            photographer_service + "photographer/" + display_name,
            timeout=REQUEST_TIMEOUT,
        )
        if photographer.status_code == requests.codes.ok:
            id = mongo_allocate_photo_id(display_name)
            photo_tags = tags_client.stub.getTags(
                tags_pb2.ImageRequest(file=file.file.read())
            )

            # We save the photo
            if mongo_save_photo(file.file, display_name, id):
                response.headers["Location"] = f'/photo/{display_name}/{id}'
                logger.info("A new image has been uploaded ...")
            else:
                raise HTTPException(status_code=503,
                                    detail="Mongo unavailable")
            # We save the tags
            mongo_set_photo_attributes(display_name,
                                       id,
                                       {"tags": list(photo_tags.tags)},
                                       photo_all_attributes)
        elif photographer.status_code == requests.codes.unavailable:
            raise HTTPException(status_code=503, detail="Mongo unavailable")
        elif photographer.status_code == requests.codes.not_found:
            raise HTTPException(status_code=404,
                                detail="Photographer Not Found")
    except (
        pymongo.errors.AutoReconnect,
        pymongo.errors.ServerSelectionTimeoutError,
        pymongo.errors.NetworkTimeout,
    ) as e:
        raise HTTPException(status_code=503, detail="Mongo unavailable") from e


@app.get("/photo/{display_name}/{photo_id}", status_code=200)
def get_photo(display_name: str, photo_id: int):
    logger.info("Get one photo ...")
    try:
        ph = mongo_get_photo_by_name_and_id(display_name, photo_id)
        return Response(content=ph.image_file.read(), media_type="image/jpeg")
    except (
        pymongo.errors.AutoReconnect,
        pymongo.errors.ServerSelectionTimeoutError,
        pymongo.errors.NetworkTimeout,
    ) as e:
        raise HTTPException(status_code=503, detail="Mongo unavailable") from e
    except (Photo.DoesNotExist) as e:
        raise HTTPException(status_code=404, detail="Not Found") from e
    except (Photo.MultipleObjectsReturned) as e:
        raise HTTPException(status_code=500, detail="Internal Error") from e


@app.put("/photo/{display_name}/{photo_id}/attributes", status_code=200)
def set_photo_attributes(
    display_name: str, photo_id: int, attributes: PhotoAttributesNoTags
):
    try:
        qs = mongo_set_photo_attributes(
            display_name, photo_id, vars(attributes), photo_all_attributes
        )
        if not qs:
            raise HTTPException(status_code=404, detail="Not Found")
    except (
        pymongo.errors.AutoReconnect,
        pymongo.errors.ServerSelectionTimeoutError,
        pymongo.errors.NetworkTimeout,
    ) as e:
        raise HTTPException(status_code=503, detail="Mongo unavailable") from e
    except (Photo.DoesNotExist) as e:
        raise HTTPException(status_code=404, detail="Not Found") from e
    except (Photo.MultipleObjectsReturned) as e:
        raise HTTPException(status_code=500, detail="Internal Error") from e


@app.get(
    "/photo/{display_name}/{photo_id}/attributes",
    response_model=PhotoAttributes,
    status_code=200,
)
def get_photo_attributes(display_name: str, photo_id: int):
    try:
        ph = mongo_get_photo_by_name_and_id(display_name, photo_id)
        return ph._data
    except (
        pymongo.errors.AutoReconnect,
        pymongo.errors.ServerSelectionTimeoutError,
        pymongo.errors.NetworkTimeout,
    ) as e:
        raise HTTPException(status_code=503, detail="Mongo unavailable") from e
    except (Photo.DoesNotExist) as e:
        raise HTTPException(status_code=404, detail="Not Found") from e
    except (Photo.MultipleObjectsReturned) as e:
        raise HTTPException(status_code=500, detail="Internal Error") from e


@app.get("/gallery/{display_name}", response_model=Photos, status_code=200)
def get_photos(request: Request,
               display_name: str,
               offset: int = 0,
               limit: int = 10):
    logger.info("Getting photos ...")
    list_of_photos = list()
    try:
        photographer = requests.get(
            photographer_service + "photographer/" + display_name,
            timeout=REQUEST_TIMEOUT,
        )
        if photographer.status_code == requests.codes.ok:
            try:
                (has_more, photos) = mongo_get_photos_by_name(
                    display_name, offset, limit
                )
                if not photos:
                    raise HTTPException(status_code=204, detail="No Photos")
                else:
                    for ph in photos:
                        ph._data.pop("id")
                        ph._data.pop("image_file")
                        ph._data.pop("display_name")
                        ph._data.pop("title")
                        ph._data.pop("comment")
                        ph._data.pop("author")
                        ph._data.pop("location")
                        ph._data.pop("tags")
                        # host_part = re.match(
                        #     "http://([^/]*)/", str(request.url)
                        # ).group()
                        # ph._data['link'] = host_part +
                        # "photo/" + display_name + "/" + str(ph.photo_id)
                        ph._data["link"] = (
                            "/photo/" + display_name + "/" + str(ph.photo_id)
                        )
                        list_of_photos.append(ph._data)
            except (
                pymongo.errors.AutoReconnect,
                pymongo.errors.ServerSelectionTimeoutError,
                pymongo.errors.NetworkTimeout,
            ) as e:
                raise HTTPException(status_code=503,
                                    detail="Mongo unavailable") from e
        elif photographer.status_code == requests.codes.unavailable:
            raise HTTPException(
                status_code=503, detail="Photographer Service Unavailable"
            )
        elif photographer.status_code == requests.codes.not_found:
            raise HTTPException(status_code=404, detail="Not Found")
        else:
            # Calling raise_for_status() will
            # raise an exception in case of error code
            photographer.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503,
                            detail="Photographer Service Unavailable") from e
    return {"items": list_of_photos, "has_more": has_more}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
    # logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(gunicorn_logger.level)
