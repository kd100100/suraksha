from typing import List, Dict, Any, Literal, Union
from src.models.validation_result import ValidationResult, Modification
from src.client.rest_request_handler import make_request
import copy
import time

FieldType = Literal["URL_PARAM", "REQUEST_BODY"]


async def validate_field_for_injection(field_key: str, field_value: Any, field_type: FieldType, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], injection_patterns: List[str], expected_status_code: int) -> List[ValidationResult]:
    """Validate a field for vulnerabilities."""
    results = []

    if field_type == "REQUEST_BODY" and field_key == "":
        # Handle the entire request body
        for pattern in injection_patterns:
            results.extend(await validate_request_body(pattern, method, url, url_params, req_body, headers, expected_status_code))
    elif isinstance(field_value, str):
        results.extend(await validate_string_field_for_injection(field_key, field_value, field_type, method, url, url_params, req_body, headers, injection_patterns, expected_status_code))
    elif isinstance(field_value, dict):
        for inner_key, inner_value in field_value.items():
            results.extend(await validate_field_for_injection(
                f"{field_key}.{inner_key}", inner_value, field_type, method, url, url_params, req_body, headers, injection_patterns, expected_status_code))
    elif isinstance(field_value, list):
        for index, value in enumerate(field_value):
            results.extend(await validate_field_for_injection(
                f"{field_key}[{index}]", value, field_type, method, url, url_params, req_body, headers, injection_patterns, expected_status_code))

    return results


async def validate_request_body(pattern: str, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], expected_status_code: int) -> List[ValidationResult]:
    """Validate the entire request body for vulnerabilities."""
    start_time = time.time()
    temp_req_body = copy.deepcopy(req_body)

    # Inject the pattern into all string values in the request body
    inject_pattern_into_dict(temp_req_body, pattern)

    formatted_url = url.format(**url_params)
    response = await make_request(method, formatted_url, temp_req_body, headers)
    end_time = time.time()
    runtime = end_time - start_time

    return [ValidationResult(
        isValid=response["status_code"] == expected_status_code,
        modification=Modification(
            type="REQUEST_BODY",
            key="",
            value=pattern
        ),
        request={
            "method": method,
            "url": formatted_url,
            "body": temp_req_body,
            "headers": headers,
        },
        response=response,
        executionTime=runtime
    )]


def inject_pattern_into_dict(d: Dict[str, Any], pattern: str):
    """Recursively inject a pattern into all string values in a dictionary."""
    for key, value in d.items():
        if isinstance(value, str):
            d[key] = value + pattern
        elif isinstance(value, dict):
            inject_pattern_into_dict(value, pattern)
        elif isinstance(value, list):
            d[key] = [
                item + pattern if isinstance(item, str) else item for item in value]


async def validate_string_field_for_injection(field_key: str, field_value: str, field_type: FieldType, method: str, url: str, url_params: Dict[str, str], req_body: Dict[str, Any], headers: Dict[str, str], injection_patterns: List[str], expected_status_code: int) -> List[ValidationResult]:
    """Validate a string field for vulnerabilities."""
    results = []
    for pattern in injection_patterns:
        start_time = time.time()
        temp_url_params = copy.deepcopy(url_params)
        temp_req_body = copy.deepcopy(req_body)

        if field_type == "URL_PARAM":
            set_nested_value(temp_url_params, field_key, field_value + pattern)
        else:
            set_nested_value(temp_req_body, field_key, field_value + pattern)

        formatted_url = url.format(**temp_url_params)

        response = await make_request(method, formatted_url, temp_req_body, headers)
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
                "headers": headers,
            },
            response=response,
            executionTime=runtime
        ))
    return results


def set_nested_value(obj: Dict[str, Any], key: Union[str, List[str]], value: Any):
    """Set a value in a nested dictionary using a dot-separated key or a list of keys."""
    if isinstance(key, str):
        keys = key.split('.')
    else:
        keys = key

    if keys[0] == '':  # Handle keys starting with a dot
        keys = keys[1:]

    for k in keys[:-1]:
        obj = obj.setdefault(k, {})
    obj[keys[-1]] = value
