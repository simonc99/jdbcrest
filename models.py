from pydantic import BaseModel, Field
from datetime import date
import re

ALLOWED_STATUS = {
    "NEW",
    "PENDING",
    "COMPLETE",
    "FAILED"
}

class QueryRequest(BaseModel):
    filter_value: str = Field(
        min_length=1,
        max_length=50
    )

class InsertRequest(BaseModel):

    reference_number: str = Field(
        min_length=1,
        max_length=30
    )

    entry_date: date

    marker: str = Field(
        min_length=1,
        max_length=20
    )

    status: str

    @classmethod
    def validate_status(cls, value):

        if value not in ALLOWED_STATUS:
            raise ValueError(
                "Invalid status"
            )

        return value
