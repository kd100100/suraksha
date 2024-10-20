from typing import List, Dict, Any, Optional
from src.validators.validator_interface import ValidatorInterface
from src.models.validation_result import ValidationResult, Modification
from src.utils.validator_utils import set_nested_value, FieldType
from src.client.rest_request_handler import make_request
import copy
import time
import logging

logger = logging.getLogger(__name__)

DEFAULT_LENGTH_STEPS = [100, 250, 500]
DEFAULT_EXPECTED_STATUS_CODE = 400


class StringLengthValidator(ValidatorInterface):
    def __init__(self, length_steps: Optional[List[int]] = None, expected_status_code: int = DEFAULT_EXPECTED_STATUS_CODE):
        self.length_steps = length_steps or DEFAULT_LENGTH_STEPS
        self.expected_status_code = expected_status_code

    async def validate(self, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str]) -> List[ValidationResult]:
        results = []

        # Validate URL parameters
        for param_key, param_value in url_params.items():
            if isinstance(param_value, str):
                results.extend(await self._validate_field(
                    param_key, param_value, "URL_PARAM", method, url, url_params, req_body, headers))

        # Validate request body fields
        results.extend(await self._validate_nested_fields(
            req_body, "REQUEST_BODY", method, url, url_params, req_body, headers))

        return results

    async def _validate_nested_fields(self, obj: Dict[str, Any], field_type: FieldType, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], prefix: str = "") -> List[ValidationResult]:
        results = []
        for key, value in obj.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, str):
                results.extend(await self._validate_field(
                    full_key, value, field_type, method, url, url_params, req_body, headers))
            elif isinstance(value, dict):
                results.extend(await self._validate_nested_fields(
                    value, field_type, method, url, url_params, req_body, headers, full_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        results.extend(await self._validate_field(
                            f"{full_key}[{i}]", item, field_type, method, url, url_params, req_body, headers))
                    elif isinstance(item, dict):
                        results.extend(await self._validate_nested_fields(
                            item, field_type, method, url, url_params, req_body, headers, f"{full_key}[{i}]"))
        return results

    async def _validate_field(self, field_key: str, sample_text: str, field_type: FieldType, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str]) -> List[ValidationResult]:
        results = []

        for length in self.length_steps:
            start_time = time.time()
            test_value = sample_text * (length // len(sample_text) + 1)
            test_value = test_value[:length]

            temp_url_params = copy.deepcopy(url_params)
            temp_req_body = copy.deepcopy(req_body)

            if field_type == "URL_PARAM":
                temp_url_params[field_key] = test_value
            else:  # REQUEST_BODY
                set_nested_value(
                    temp_req_body, field_key.split('.'), test_value)

            formatted_url = url.format(**temp_url_params)
            response = await make_request(
                method, formatted_url, temp_req_body, headers)
            end_time = time.time()
            runtime = end_time - start_time

            is_valid = response["status_code"] == self.expected_status_code
            results.append(ValidationResult(
                isValid=is_valid,
                modification=Modification(
                    type=field_type,
                    key=field_key,
                    value=f"{length}"
                ),
                request={
                    "method": method,
                    "url": formatted_url,
                    "body": temp_req_body,
                    "headers": headers,
                },
                response=response,
                executionTime=runtime
            ))

            logger.info(
                f"Validated field {field_key} with length {length}. Is valid: {is_valid}")

            if is_valid:
                break

        return results
