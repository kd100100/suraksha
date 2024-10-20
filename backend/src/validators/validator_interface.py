from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.models.validation_result import ValidationResult


class ValidatorInterface(ABC):
    @abstractmethod
    async def validate(self, method: str, url: str, urlParams: Dict[str, str], body: Dict[str, Any], headers: Dict[str, str], scan_id: str) -> List[ValidationResult]:
        pass
