from pydantic import BaseModel
from datetime import datetime

class SummaryCreate(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    id: int
    input_text: str
    summary_text: str
    created_at: datetime

    class Config:
        orm_mode = True
