from pydantic import BaseModel
from typing import Optional

class Example(BaseModel):
    table_id: Optional[int]
    example_str: str
    example_int: int
    example_not_required: str
