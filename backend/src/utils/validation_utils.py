from typing import List, Dict, Any, Callable
from src.models.validation_result import ValidationResult, Modification
from src.client.rest_request_handler import make_request
import copy
import time
import logging

logger = logging.getLogger(__name__)


async def validate_with_patterns(
    patterns: List[str],
    apply_pattern: Callable[[str, str], str],
    method: str,
    url: str,
    url_params: Dict[str, str],
    req_body: Dict[str, Any],
    headers: Dict[str, str],
    expected_status_code: int,
    validate_url_params: bool = True,
    validate_body: bool = True,
    validate_headers: bool = False,
    stop_on_first_valid: bool = False,
    scan_id: str = None,
    validator_name: str = None
) -> List[ValidationResult]:
    results = []

    if validate_url_params:
        for param_key, param_value in url_params.items():
            field_results = await _validate_field(
                param_key, param_value, "URL_PARAM", method, url, url_params, req_body, headers,
                patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name
            )
            results.extend(field_results)

    if validate_body:
        body_results = await _validate_nested_fields(
            req_body, "REQUEST_BODY", method, url, url_params, req_body, headers,
            patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name
        )
        results.extend(body_results)

    if validate_headers:
        for header_key, header_value in headers.items():
            field_results = await _validate_field(
                header_key, header_value, "HEADER", method, url, url_params, req_body, headers,
                patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name
            )
            results.extend(field_results)

    logger.info(
        f"Scan ID: {scan_id} | {validator_name} completed successfully")
    return results


async def _validate_nested_fields(
    obj: Dict[str, Any],
    field_type: str,
    method: str,
    url: str,
    url_params: Dict[str, str],
    req_body: Dict[str, Any],
    headers: Dict[str, str],
    patterns: List[str],
    apply_pattern: Callable[[str, str], str],
    expected_status_code: int,
    stop_on_first_valid: bool,
    scan_id: str,
    validator_name: str,
    prefix: str = ""
) -> List[ValidationResult]:
    results = []
    for key, value in obj.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, str):
            field_results = await _validate_field(
                full_key, value, field_type, method, url, url_params, req_body, headers,
                patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name
            )
            results.extend(field_results)
        elif isinstance(value, dict):
            nested_results = await _validate_nested_fields(
                value, field_type, method, url, url_params, req_body, headers,
                patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name, full_key
            )
            results.extend(nested_results)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str):
                    field_results = await _validate_field(
                        f"{full_key}[{i}]", item, field_type, method, url, url_params, req_body, headers,
                        patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name
                    )
                    results.extend(field_results)
                elif isinstance(item, dict):
                    nested_results = await _validate_nested_fields(
                        item, field_type, method, url, url_params, req_body, headers,
                        patterns, apply_pattern, expected_status_code, stop_on_first_valid, scan_id, validator_name, f"{full_key}[{i}]"
                    )
                    results.extend(nested_results)
    return results


async def _validate_field(
    field_key: str,
    field_value: str,
    field_type: str,
    method: str,
    url: str,
    url_params: Dict[str, str],
    req_body: Dict[str, Any],
    headers: Dict[str, str],
    patterns: List[str],
    apply_pattern: Callable[[str, str], str],
    expected_status_code: int,
    stop_on_first_valid: bool,
    scan_id: str,
    validator_name: str
) -> List[ValidationResult]:
    results = []

    for pattern in patterns:
        start_time = time.time()
        test_value = apply_pattern(field_value, pattern)

        temp_url_params = copy.deepcopy(url_params)
        temp_req_body = copy.deepcopy(req_body)
        temp_headers = copy.deepcopy(headers)

        if field_type == "URL_PARAM":
            temp_url_params[field_key] = test_value
        elif field_type == "REQUEST_BODY":
            _set_nested_value(temp_req_body, field_key.split('.'), test_value)
        elif field_type == "HEADER":
            temp_headers[field_key] = test_value

        formatted_url = url.format(**temp_url_params)
        response = await make_request(method, formatted_url, temp_req_body, temp_headers)
        end_time = time.time()
        runtime = end_time - start_time

        is_valid = response["status_code"] == expected_status_code
        results.append(ValidationResult(
            isValid=is_valid,
            modification=Modification(
                type=field_type,
                key=field_key,
                value=pattern
            ),
            request={
                "method": method,
                "url": formatted_url,
                "body": temp_req_body,
                "headers": temp_headers,
            },
            response=response,
            executionTime=runtime
        ))

        logger.info(
            f"Scan ID: {scan_id} | {validator_name} | Validated field {field_key} with pattern {pattern}. Is valid: {is_valid}")

        if stop_on_first_valid and is_valid:
            break

    return results


def _set_nested_value(obj: Dict[str, Any], keys: List[str], value: Any):
    for key in keys[:-1]:
        obj = obj.setdefault(key, {})
    obj[keys[-1]] = value
