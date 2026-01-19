from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class DateFilterRequest(BaseModel):    
    start_date: datetime = Field(
        ..., 
        description="Начальная дата в формате YYYY-MM-DDTHH:MM:SS"
    )
    end_date: datetime = Field(
        ..., 
        description="Конечная дата в формате YYYY-MM-DDTHH:MM:SS"
    )
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError("end_date must be greater than or equal to start_date")
        return v