from typing import List, Dict, Any
from src.validators.validator_interface import ValidatorInterface
from src.models.validation_result import ValidationResult
from src.utils.validation_utils import validate_with_patterns
import logging

logger = logging.getLogger(__name__)

DEFAULT_SQL_INJECTION_PATTERNS = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' OR 1=1 --",
    "SELECT * FROM users WHERE name = 'admin' AND password = 'password';",
]
DEFAULT_EXPECTED_STATUS_CODE = 400


class SQLInjectionValidator(ValidatorInterface):
    def __init__(self, patterns: List[str] = DEFAULT_SQL_INJECTION_PATTERNS, expected_status_code: int = DEFAULT_EXPECTED_STATUS_CODE):
        self.patterns = patterns
        self.expected_status_code = expected_status_code

    async def validate(self, method: str, url: str, urlParams: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], scan_id: str) -> List[ValidationResult]:
        return await validate_with_patterns(
            self.patterns,
            lambda field_value, pattern: field_value + pattern,
            method,
            url,
            urlParams,
            req_body,
            headers,
            self.expected_status_code,
            scan_id=scan_id,
            validator_name="SQL_INJECTION"
        )
