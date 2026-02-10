from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str


class ItemOut(BaseModel):
    id: int
    name: str
