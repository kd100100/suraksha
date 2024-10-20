import pytest
from src.validators.impl.sql_injection_validator import SQLInjectionValidator
from src.validators.impl.dom_injection_validator import DOMInjectionValidator
from src.validators.impl.string_length_validator import StringLengthValidator
from src.models.validation_result import ValidationResult
from unittest.mock import patch, Mock


@pytest.fixture
def mock_make_request():
    with patch('src.utils.validator_utils.make_request') as mock:
        yield mock


@pytest.mark.asyncio
async def test_sql_injection_validator(mock_make_request):
    validator = SQLInjectionValidator()
    mock_make_request.return_value = {
        "status_code": 200, "text": "Response text"}

    results = await validator.validate(
        method="GET",
        url="http://example.com",
        url_params={"param": "' OR '1'='1"},
        req_body={},
        headers={}
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, ValidationResult) for result in results)
    assert any(not result.isValid for result in results)


@pytest.mark.asyncio
async def test_dom_injection_validator(mock_make_request):
    validator = DOMInjectionValidator()
    mock_make_request.return_value = {
        "status_code": 200, "text": "Response text"}

    results = await validator.validate(
        method="GET",
        url="http://example.com",
        url_params={"param": "<script>alert('XSS')</script>"},
        req_body={},
        headers={}
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, ValidationResult) for result in results)
    assert any(not result.isValid for result in results)


@pytest.mark.asyncio
async def test_string_length_validator(mock_make_request):
    validator = StringLengthValidator()
    mock_make_request.return_value = {
        "status_code": 400, "text": "Response text"}

    results = await validator.validate(
        method="GET",
        url="http://example.com",
        url_params={"short": "short", "long": "a" * 101},
        req_body={"nested": {"short": "short", "long": "a" * 251}},
        headers={}
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, ValidationResult) for result in results)
    # Two valid results (long params)
    assert sum(1 for result in results if result.isValid) == 2
    # Two invalid results (short params)
    assert sum(1 for result in results if not result.isValid) == 2


@pytest.mark.asyncio
async def test_validators_with_valid_input(mock_make_request):
    validators = [
        SQLInjectionValidator(),
        DOMInjectionValidator(),
        StringLengthValidator()
    ]
    mock_make_request.return_value = {
        "status_code": 200, "text": "Response text"}

    for validator in validators:
        results = await validator.validate(
            method="GET",
            url="http://example.com",
            url_params={"param": "valid_input"},
            req_body={},
            headers={}
        )

        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(result, ValidationResult) for result in results)
        assert all(not result.isValid for result in results)


@pytest.mark.asyncio
async def test_validators_with_invalid_input(mock_make_request):
    validators = [
        (SQLInjectionValidator(), "' OR '1'='1"),
        (DOMInjectionValidator(), "<script>alert('XSS')</script>"),
        (StringLengthValidator(), "a" * 501)
    ]
    mock_make_request.return_value = {
        "status_code": 400, "text": "Response text"}

    for validator, invalid_input in validators:
        results = await validator.validate(
            method="GET",
            url="http://example.com",
            url_params={"param": invalid_input},
            req_body={},
            headers={}
        )

        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(result, ValidationResult) for result in results)
        assert any(result.isValid for result in results)
