from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uuid
from datetime import datetime


class ScanRequest(BaseModel):
    method: str = Field(...,
                        description="HTTP method for the scan", example="GET")
    url: str = Field(..., description="URL to scan")
    urlParams: Dict[str, str] = Field(
        default={}, description="URL parameters")
    headers: Dict[str, str] = Field(default={}, description="HTTP headers")
    body: Optional[Dict[str, Any]] = Field(
        default=None, description="Request body")


class ScanModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request: ScanRequest
    domain: str = Field(default="", description="Domain of the API")
    path: str = Field(default="", description="Path of the API")
    status: str = "CREATED"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: str = "system"
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    updatedBy: str = "system"

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "request": {
                    "method": "GET",
                    "url": "https://api.example.com/data",
                    "urlParams": {"param1": "value1"},
                    "body": {"key": "value"},
                    "headers": {"Content-Type": "application/json"}
                },
                "domain": "api.example.com",
                "path": "/data",
                "status": "CREATED",
                "createdAt": "2023-06-01T12:00:00Z",
                "createdBy": "system",
                "updatedAt": "2023-06-01T12:00:00Z",
                "updatedBy": "system"
            }
        }
