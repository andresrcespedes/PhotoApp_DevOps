#!/usr/bin/env python3

from fastapi import Path, Body
from pydantic import BaseModel, Field
from typing import List
from beanie import Document, init_beanie

class Fmodel:
    uri: str

class Dname:
    STR = "The display name of the filter"
    MAX_LENGTH = 16
    PATH_PARAM = Path(..., title = STR, max_length = MAX_LENGTH)

class Fname:
    STR = "The first name of the filter"
    MAX_LENGTH = 32

class Lname:
    STR = "The last name of the filter"
    MAX_LENGTH = 32

class Interests:
    STR = "The interests of the filter"

class FilterDesc(BaseModel):
    display_name: str = Field (None, title = Dname.STR, max_length = Dname.MAX_LENGTH)
    first_name: str = Field (None, title = Fname.STR, max_length = Dname.MAX_LENGTH)
    last_name: str = Field (None, title = Lname.STR, max_length = Lname.MAX_LENGTH)
    interests: List[str] = Field (None, title = Interests.STR)

class Filter(Document, FilterDesc):
    pass

FILTER_EXAMPLE = {
    "display_name": "rdoisneau",
    "first_name": "robert",
    "last_name": "doisneau",
    "interests": ["street", "portrait"],
    }

FILTER_BODY = Body(..., example = FILTER_EXAMPLE)

class FilterDigest(BaseModel):
    display_name: str
    link: str

class Filters(BaseModel):
    items: List[FilterDigest]
    has_more: bool
