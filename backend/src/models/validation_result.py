from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


class Modification(BaseModel):
    type: str
    key: str
    value: str


class ValidationResult(BaseModel):
    isValid: bool
    modification: Modification
    request: Dict[str, Any]
    response: Dict[str, Any]
    executionTime: float


class ValidationSummary(BaseModel):
    scanId: str
    validation: str
    apiUrl: str
    results: List[ValidationResult]
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: str = "system"

    class Config:
        schema_extra = {
            "example": {
                "scanId": "123e4567-e89b-12d3-a456-426614174000",
                "validation": "SQL_INJECTION",
                "apiUrl": "https://api.example.com/data",
                "results": [
                    {
                        "isValid": True,
                        "modification": {
                            "type": "URL_PARAM",
                            "key": "id",
                            "value": "1 OR 1=1"
                        },
                        "request": {
                            "method": "GET",
                            "url": "https://api.example.com/data?id=1 OR 1=1",
                            "headers": {"Content-Type": "application/json"}
                        },
                        "response": {
                            "status_code": 400,
                            "body": "Invalid input"
                        },
                        "executionTime": 0.5
                    }
                ],
                "createdAt": "2023-06-01T12:00:00Z",
                "createdBy": "system"
            }
        }
