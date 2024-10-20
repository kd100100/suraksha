import pytest
from unittest.mock import Mock, patch
from src.services.scan_service import process_scan, run_validation, save_results
from src.models.scan import ScanRequest, ScanModel
from src.models.validation_result import ValidationResult, ValidationSummary, Modification


@pytest.fixture
def mock_db():
    with patch('src.services.scan_service.get_database') as mock:
        yield mock.return_value


@pytest.fixture
def mock_validators():
    with patch('src.services.scan_service.VALIDATORS') as mock:
        yield mock


@pytest.fixture
def sample_scan_request():
    return ScanRequest(
        method="GET",
        url="http://test.com",
        url_params={},
        headers={},
        body={}
    )


@pytest.mark.asyncio
async def test_process_scan_success(mock_db, mock_validators, sample_scan_request):
    mock_db.scans.find_one.return_value = {
        "id": "test_id", "request": sample_scan_request.dict()}
    mock_validators.__iter__.return_value = [("MOCK_VALIDATOR", Mock())]
    mock_validators[0][1].validate.return_value = [
        ValidationResult(
            isValid=True,
            modification=Modification(type="TEST", key="test", value="test"),
            request={},
            response={},
            executionTime=0.1
        )
    ]

    await process_scan("test_id")

    mock_db.scans.update_one.assert_called()
    mock_db.validation_results.insert_many.assert_called()


@pytest.mark.asyncio
async def test_process_scan_not_found(mock_db, mock_validators):
    mock_db.scans.find_one.return_value = None

    await process_scan("test_id")

    mock_db.scans.update_one.assert_not_called()
    mock_db.validation_results.insert_many.assert_not_called()


@pytest.mark.asyncio
async def test_run_validation_success(mock_validators, sample_scan_request):
    mock_validator = Mock()
    mock_validator.validate.return_value = [
        ValidationResult(
            isValid=True,
            modification=Modification(type="TEST", key="test", value="test"),
            request={},
            response={},
            executionTime=0.1
        )
    ]
    mock_validators.__iter__.return_value = [
        ("MOCK_VALIDATOR", mock_validator)]

    results = await run_validation("test_id", sample_scan_request)

    assert len(results) == 1
    assert isinstance(results[0], ValidationSummary)
    assert results[0].scanId == "test_id"
    assert results[0].validation == "MOCK_VALIDATOR"
    assert len(results[0].results) == 1


@pytest.mark.asyncio
async def test_run_validation_exception(mock_validators, sample_scan_request):
    mock_validator = Mock()
    mock_validator.validate.side_effect = Exception("Test exception")
    mock_validators.__iter__.return_value = [
        ("MOCK_VALIDATOR", mock_validator)]

    results = await run_validation("test_id", sample_scan_request)

    assert len(results) == 0


@pytest.mark.asyncio
async def test_save_results_success(mock_db):
    validation_summaries = [
        ValidationSummary(
            scanId="test_id",
            validation="TEST",
            apiUrl="http://test.com",
            results=[]
        )
    ]

    await save_results(validation_summaries)

    mock_db.validation_results.insert_many.assert_called_once()


@pytest.mark.asyncio
async def test_save_results_empty(mock_db):
    await save_results([])

    mock_db.validation_results.insert_many.assert_not_called()


@pytest.mark.asyncio
async def test_save_results_exception(mock_db):
    mock_db.validation_results.insert_many.side_effect = Exception(
        "Test exception")
    validation_summaries = [
        ValidationSummary(
            scanId="test_id",
            validation="TEST",
            apiUrl="http://test.com",
            results=[]
        )
    ]

    await save_results(validation_summaries)

    mock_db.validation_results.insert_many.assert_called_once()
