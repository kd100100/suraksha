from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, Any, Optional
import uuid
from datetime import datetime


class ScanRequest(BaseModel):
    method: str = Field(...,
                        description="HTTP method for the scan", example="GET")
    url: str = Field(..., description="URL to scan")
    url_params: Dict[str, str] = Field(
        default={}, description="URL parameters")
    headers: Dict[str, str] = Field(default={}, description="HTTP headers")
    body: Optional[Dict[str, Any]] = Field(
        default=None, description="Request body")


class ScanModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                    description="Unique identifier for the scan")
    status: str = Field(default="CREATED",
                        description="Current status of the scan")
    request: ScanRequest
    created_at: str = Field(default_factory=lambda: datetime.now(
    ).isoformat(), description="Timestamp of scan creation")
    completed_at: Optional[str] = Field(
        default=None, description="Timestamp of scan completion")

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "CREATED",
                "request": {
                    "method": "GET",
                    "url": "https://example.com",
                    "url_params": {"param1": "value1"},
                    "headers": {"Content-Type": "application/json"},
                    "body": {"key": "value"}
                },
                "created_at": "2023-06-01T12:00:00Z",
                "completed_at": None
            }
        }
