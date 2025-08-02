from pydantic import BaseModel, Field
from typing import Optional

class MathRequest(BaseModel):
    operation: str = Field(..., description="Operation type: pow, fibonacci, factorial")
    input_data: dict = Field(..., description="Input data for the operation")
    result: Optional[float] = Field(None, description="Result of the operation")
