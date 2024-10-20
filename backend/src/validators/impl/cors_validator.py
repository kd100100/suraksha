from src.validators.validator_interface import ValidatorInterface
from src.models.validation_result import ValidationResult
from src.client.rest_request_handler import make_request
from src.config.config import config
import logging

logger = logging.getLogger(__name__)


class CORSValidator(ValidatorInterface):
    def __init__(self):
        self.cors_config = config['validators']['cors']
        self.malicious_origin = self.cors_config['maliciousOrigin']

    async def validate(self, method: str, url: str, urlParams: dict, req_body: dict, headers: dict, scan_id: str) -> list[ValidationResult]:
        logger.info(
            f"Scan ID: {scan_id} | Starting CORS validation for URL: {url}")
        results = []

        # Test for CORS misconfiguration
        cors_headers = {
            "Origin": self.malicious_origin,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "Content-Type"
        }

        # Preflight request
        options_response = await make_request("OPTIONS", url, {}, {**headers, **cors_headers})

        # Actual request
        actual_response = await make_request(method, url, req_body, {**headers, **cors_headers})

        # Check CORS headers in the responses
        is_vulnerable, vulnerability_details = self._check_cors_headers(
            options_response, actual_response, self.malicious_origin)

        results.append(ValidationResult(
            isValid=not is_vulnerable,
            modification={
                "type": "CORS",
                "key": "Origin",
                "value": self.malicious_origin
            },
            request={
                "method": method,
                "url": url,
                "headers": cors_headers
            },
            response=options_response,
            executionTime=options_response.get(
                "execution_time", 0) + actual_response.get("execution_time", 0)
        ))

        logger.info(
            f"Scan ID: {scan_id} | CORS validation completed. Vulnerable: {is_vulnerable}")
        return results

    def _check_cors_headers(self, options_response, actual_response, origin):
        vulnerability_details = []

        # Check preflight response
        allow_origin = options_response["headers"].get(
            "Access-Control-Allow-Origin")
        if allow_origin == "*":
            vulnerability_details.append(
                "Preflight response allows all origins")
        elif allow_origin == origin:
            vulnerability_details.append(
                "Preflight response allows malicious origin")

        allow_credentials = options_response["headers"].get(
            "Access-Control-Allow-Credentials")
        if allow_credentials and allow_credentials.lower() == "true":
            vulnerability_details.append(
                "Preflight response allows credentials")

        # Check actual response
        allow_origin = actual_response["headers"].get(
            "Access-Control-Allow-Origin")
        if allow_origin == "*":
            vulnerability_details.append("Actual response allows all origins")
        elif allow_origin == origin:
            vulnerability_details.append(
                "Actual response allows malicious origin")

        is_vulnerable = len(vulnerability_details) > 0
        return is_vulnerable, vulnerability_details
