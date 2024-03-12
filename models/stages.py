from typing import List
from pydantic import BaseModel

class Stage(BaseModel):
    duration: str
    target: int
class TestParams(BaseModel):
    stages: List[Stage]
    sleep: float