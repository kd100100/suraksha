from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class Modification:
    type: str
    key: str
    value: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationResult:
    is_valid: bool
    modification: Modification
    request: Dict[str, Any]
    response: Dict[str, Any]
    timestamp: str
    runtime: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "modification": self.modification.to_dict(),
            "request": self.request,
            "response": self.response,
            "timestamp": self.timestamp,
            "runtime": self.runtime
        }

    @classmethod
    def create(cls, is_valid: bool, modification: Modification, request: Dict[str, Any], response: Dict[str, Any], runtime: float):
        return cls(
            is_valid=is_valid,
            modification=modification,
            request=request,
            response=response,
            timestamp=datetime.now().isoformat(),
            runtime=runtime
        )


@dataclass
class ValidationSummary:
    type: str
    api_url: str
    results: List[ValidationResult]
    overall_result: bool
    total_runtime: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "api_url": self.api_url,
            "results": [result.to_dict() for result in self.results],
            "overall_result": self.overall_result,
            "total_runtime": self.total_runtime,
            "timestamp": self.timestamp
        }

    @classmethod
    def create(cls, type: str, api_url: str, results: List[ValidationResult]):
        overall_result = all(result.is_valid for result in results)
        total_runtime = sum(result.runtime for result in results)
        return cls(
            type=type,
            api_url=api_url,
            results=results,
            overall_result=overall_result,
            total_runtime=total_runtime
        )
