from pydantic import BaseModel
from typing import Optional


class ComparisonRequest(BaseModel):
    word_1: Optional[str] = None
    word_2: Optional[str] = None


class ComparisonResult(BaseModel):
    distance: int
    similarity: float
    is_sim: bool
