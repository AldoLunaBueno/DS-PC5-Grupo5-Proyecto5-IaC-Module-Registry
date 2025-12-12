import re
from typing import List, Optional

from pydantic import BaseModel, field_validator


class Module(BaseModel):
    id: str
    name: str
    type: str
    path: str
    version: str
    tags: List[str] = []
    quality_state: Optional[str] = None

    @field_validator("name")
    def name_must_match_regex(cls, v):
        regex = r"^[a-z0-9-]+$"
        if not re.match(regex, v):
            raise ValueError(
                "El nombre solo puede contener letras minúsculas, números y guiones."
            )
        return v
