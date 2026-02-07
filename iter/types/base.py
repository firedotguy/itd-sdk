from datetime import datetime
from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict, BeforeValidator, model_validator
from pydantic.alias_generators import to_camel

def validate_datetime(v: Any):
    if isinstance(v, str) and "+" in v:
        parts = v.split("+")
        if len(parts[-1]) <= 2:
            v = f"{parts[0]}+{parts[-1].zfill(2)}:00"
    return v

PostgresDateTime = Annotated[datetime, BeforeValidator(validate_datetime)]

class IterBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @model_validator(mode='before')
    @classmethod
    def unwrap_data_envelope(cls, data: Any) -> Any:
        if isinstance(data, dict) and "data" in data and len(data) == 1:
            return data["data"]
        return data