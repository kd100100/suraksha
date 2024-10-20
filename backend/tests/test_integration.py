import pytest
from httpx import AsyncClient
from main import app
from src.config.database import get_database
from unittest.mock import patch


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_db():
    with patch('src.config.database.get_database') as mock:
        yield mock.return_value


@pytest.mark.asyncio
async def test_create_scan_integration(async_client, mock_db):
    mock_db.scans.insert_one.return_value.inserted_id = "test_id"

    response = await async_client.post(
        "/api/scan",
        json={
            "method": "GET",
            "url": "http://test.com",
            "url_params": {},
            "headers": {},
            "body": {}
        }
    )

    assert response.status_code == 200
    assert "scan_id" in response.json()


@pytest.mark.asyncio
async def test_get_scan_results_integration(async_client, mock_db):
    mock_db.scans.find_one.return_value = {
        "id": "test_id",
        "status": "COMPLETED",
        "request": {
            "method": "GET",
            "url": "http://test.com",
            "url_params": {},
            "headers": {},
            "body": {}
        }
    }
    mock_db.validation_results.find.return_value = [
        {
            "_id": "result_id",
            "scanId": "test_id",
            "validation": "TEST_VALIDATION",
            "apiUrl": "http://test.com",
            "results": []
        }
    ]

    response = await async_client.get("/api/scan/test_id")

    assert response.status_code == 200
    assert "scan" in response.json()
    assert "validation_results" in response.json()


@pytest.mark.asyncio
async def test_create_scan_invalid_input(async_client, mock_db):
    response = await async_client.post(
        "/api/scan",
        json={
            "invalid_field": "invalid_value"
        }
    )

    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_get_scan_results_not_found(async_client, mock_db):
    mock_db.scans.find_one.return_value = None

    response = await async_client.get("/api/scan/nonexistent_id")

    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_scan_with_validation_results(async_client, mock_db):
    mock_db.scans.insert_one.return_value.inserted_id = "test_id"
    mock_db.scans.find_one.return_value = {
        "id": "test_id",
        "status": "COMPLETED",
        "request": {
            "method": "GET",
            "url": "http://test.com",
            "url_params": {"param": "test_value"},
            "headers": {},
            "body": {}
        }
    }
    mock_db.validation_results.find.return_value = [
        {
            "_id": "result_id",
            "scanId": "test_id",
            "validation": "STRING_LENGTH",
            "apiUrl": "http://test.com",
            "results": [
                {
                    "isValid": True,
                    "modification": {
                        "type": "URL_PARAM",
                        "key": "param",
                        "value": "100"
                    },
                    "request": {
                        "method": "GET",
                        "url": "http://test.com",
                        "body": {},
                        "headers": {}
                    },
                    "response": {
                        "status_code": 200,
                        "text": "Response text"
                    },
                    "executionTime": 0.1
                }
            ]
        }
    ]

    # Create a scan
    create_response = await async_client.post(
        "/api/scan",
        json={
            "method": "GET",
            "url": "http://test.com",
            "url_params": {"param": "test_value"},
            "headers": {},
            "body": {}
        }
    )

    assert create_response.status_code == 200
    scan_id = create_response.json()["scan_id"]

    # Get scan results
    get_response = await async_client.get(f"/api/scan/{scan_id}")

    assert get_response.status_code == 200
    assert "scan" in get_response.json()
    assert "validation_results" in get_response.json()

    validation_results = get_response.json()["validation_results"]
    assert len(validation_results) == 1
    assert validation_results[0]["validation"] == "STRING_LENGTH"
    assert len(validation_results[0]["results"]) == 1
    assert validation_results[0]["results"][0]["isValid"] == True
    assert validation_results[0]["results"][0]["modification"]["value"] == "100"
