from typing import List, Dict, Any
from src.validators.validator_interface import ValidatorInterface
from src.models.validation_result import ValidationResult
from src.utils.validation_utils import validate_with_patterns
from src.config.config import config
import logging

logger = logging.getLogger(__name__)


class DOMInjectionValidator(ValidatorInterface):
    def __init__(self):
        dom_injection_config = config['validators']['domInjection']
        self.patterns = dom_injection_config['patterns']
        self.expected_status_code = dom_injection_config['expectedStatusCode']

    async def validate(self, method: str, url: str, urlParams: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], scan_id: str) -> List[ValidationResult]:
        logger.info(f"Scan ID: {scan_id} | Starting DOM injection validation")
        result = await validate_with_patterns(
            self.patterns,
            lambda field_value, pattern: field_value + pattern,
            method,
            url,
            urlParams,
            req_body,
            headers,
            self.expected_status_code,
            scan_id=scan_id,
            validator_name="DOM_INJECTION"
        )
        logger.info(f"Scan ID: {scan_id} | Completed DOM injection validation")
        return result
