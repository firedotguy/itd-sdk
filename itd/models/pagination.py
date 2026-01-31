from pydantic import BaseModel, Field

class Pagination(BaseModel):
    page: int = 1
    limit: int = 20
    total: int | None = None
    has_more: bool = Field(True, alias='hasMore')