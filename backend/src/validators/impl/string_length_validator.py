from typing import List, Dict, Any
from src.validators.validator_interface import ValidatorInterface
from src.models.validation_result import ValidationResult
from src.utils.validation_utils import validate_with_patterns
import logging
import traceback

logger = logging.getLogger(__name__)

DEFAULT_LENGTH_STEPS = [100, 250, 500]
DEFAULT_EXPECTED_STATUS_CODE = 400


class StringLengthValidator(ValidatorInterface):
    def __init__(self, length_steps: List[int] = DEFAULT_LENGTH_STEPS, expected_status_code: int = DEFAULT_EXPECTED_STATUS_CODE):
        self.length_steps = length_steps
        self.expected_status_code = expected_status_code

    async def validate(self, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], scan_id: str) -> List[ValidationResult]:
        try:
            result = await validate_with_patterns(
                [str(step) for step in self.length_steps],
                self._apply_length_pattern,
                method,
                url,
                url_params,
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
