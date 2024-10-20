from typing import List, Dict, Any, Optional
from validator_interface import Validator
from models.validation_result import ValidationResult
from utils.validator_utils import validate_field_for_injection, FieldType

DEFAULT_SQL_INJECTION_PATTERNS = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' OR 1=1 --",
    "SELECT * FROM users WHERE name = 'admin' AND password = 'password';",
]
DEFAULT_EXPECTED_STATUS_CODE = 400


class SQLInjectionValidator(Validator):
    def __init__(self, sql_injection_patterns: Optional[List[str]] = None, expected_status_code: int = DEFAULT_EXPECTED_STATUS_CODE):
        self.sql_injection_patterns = sql_injection_patterns or DEFAULT_SQL_INJECTION_PATTERNS
        self.expected_status_code = expected_status_code

    def validate(self, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str]) -> List[ValidationResult]:
        results = []

        # Validate URL parameters
        for param_key, param_value in url_params.items():
            results.extend(self._validate_field(
                param_key, param_value, "URL_PARAM", method, url, url_params, req_body, headers))

        # Validate request body fields
        results.extend(self._validate_field(
            "", req_body, "REQUEST_BODY", method, url, url_params, req_body, headers))

        return results

    def _validate_field(self, field_key: str, field_value: Any, field_type: FieldType, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str]) -> List[ValidationResult]:
        return validate_field_for_injection(
            field_key, field_value, field_type, method, url, url_params, req_body, headers,
            self.sql_injection_patterns, self.expected_status_code
        )
