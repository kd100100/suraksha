from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import uuid


class Modification(BaseModel):
    type: str
    key: str
    value: str


class ValidationResult(BaseModel):
    isValid: bool
    modification: Modification
    request: Dict[str, Any]
    response: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    executionTime: float

    @classmethod
    def create(cls, is_valid: bool, modification: Modification, request: Dict[str, Any], response: Dict[str, Any], execution_time: float):
        return cls(
            isValid=is_valid,
            modification=modification,
            request=request,
            response=response,
            executionTime=execution_time
        )


class ValidationSummary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scanId: str
    validation: str
    apiUrl: str
    results: List[ValidationResult]

    @classmethod
    def create(cls, scan_id: str, validation: str, api_url: str, results: List[ValidationResult]):
        return cls(
            scanId=scan_id,
            validation=validation,
            apiUrl=api_url,
            results=results,
        )
