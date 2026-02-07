from pydantic import BaseModel

class Pin(BaseModel):
    slug: str
    name: str
    description: str