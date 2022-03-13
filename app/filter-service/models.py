#!/usr/bin/env python3

from pydantic import BaseModel

class Fmodel(BaseModel):
    uri: str
