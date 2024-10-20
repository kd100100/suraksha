from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.models.validation_result import ValidationResult


class ValidatorInterface(ABC):
    @abstractmethod
    async def validate(self, method: str, url: str, url_params: Dict[str, str], body: Dict[str, Any], headers: Dict[str, str]) -> List[ValidationResult]:
        pass
