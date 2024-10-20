from typing import List, Dict, Any
from src.validators.validator_interface import ValidatorInterface
from src.models.validation_result import ValidationResult
from src.utils.validation_utils import validate_with_patterns
from src.config.config import config
import logging
import traceback

logger = logging.getLogger(__name__)


class StringLengthValidator(ValidatorInterface):
    def __init__(self):
        string_length_config = config['validators']['stringLength']
        self.length_steps = string_length_config['lengthSteps']
        self.expected_status_code = string_length_config['expectedStatusCode']

    async def validate(self, method: str, url: str, urlParams: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], scan_id: str) -> List[ValidationResult]:
        try:
            result = await validate_with_patterns(
                [str(step) for step in self.length_steps],
                self._apply_length_pattern,
                method,
                url,
                urlParams,
                req_body,
                headers,
                self.expected_status_code,
                stop_on_first_valid=True,
                scan_id=scan_id,
                validator_name="STRING_LENGTH"
            )
            return result
        except Exception as e:
            logger.error(
                f"Scan ID: {scan_id} | Error in StringLengthValidator.validate: {str(e)}")
            logger.error(
                f"Scan ID: {scan_id} | Traceback: {traceback.format_exc()}")
            raise

    def _apply_length_pattern(self, field_value: str, pattern: str) -> str:
        try:
            target_length = int(pattern)
            if not isinstance(field_value, str):
                field_value = str(field_value)
            if len(field_value) >= target_length:
                result = field_value[:target_length]
            else:
                result = (field_value * (target_length //
                          len(field_value) + 1))[:target_length]
            return result
        except Exception as e:
            logger.error(f"Error in _apply_length_pattern: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
