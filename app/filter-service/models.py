#!/usr/bin/env python3

from pydantic import BaseModel


class PhotoModel(BaseModel):
    photographer: str
    photo_id: str
