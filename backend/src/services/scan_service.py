from src.models.scan import ScanModel, ScanRequest
from src.models.validation_result import ValidationResult, ValidationSummary, Modification
from src.config.database import get_database
from src.validators.impl.sql_injection_validator import SQLInjectionValidator
from src.validators.impl.dom_injection_validator import DOMInjectionValidator
from src.validators.impl.string_length_validator import StringLengthValidator
import logging
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

# List of validators to run
VALIDATORS = [
    ("SQL_INJECTION", SQLInjectionValidator()),
    ("DOM_INJECTION", DOMInjectionValidator()),
    ("STRING_LENGTH", StringLengthValidator()),
]


async def process_scan(scan_id: str):
    try:
        logger.info(f"Scan ID: {scan_id} | Starting scan process")
        db = get_database()

        # Update scan status to "PROCESSING"
        await db.scans.update_one(
            {"id": scan_id}, {"$set": {"status": "PROCESSING"}})
        logger.info(f"Scan ID: {scan_id} | Updated scan status to PROCESSING")

        # Retrieve the scan
        scan_data = await db.scans.find_one({"id": scan_id})
        if not scan_data:
            logger.error(f"Scan ID: {scan_id} | Scan not found")
            return

        scan = ScanModel(**scan_data)

        # Run validations
        validation_summaries = await run_validation(scan_id, scan.request)

        # Save results
        await save_results(scan_id, validation_summaries)

        # Update scan status to "COMPLETED"
        await db.scans.update_one(
            {"id": scan_id},
            {
                "$set": {
                    "status": "COMPLETED",
                    "completed_at": datetime.now().isoformat()
                }
            }
        )

        logger.info(
            f"Scan ID: {scan_id} | Scan process completed successfully")
    except Exception as e:
        logger.error(f"Scan ID: {scan_id} | Error processing scan: {str(e)}")
        await db.scans.update_one({"id": scan_id}, {"$set": {"status": "FAILED"}})


async def run_validation(scan_id: str, api_spec: ScanRequest) -> List[ValidationSummary]:
    validation_summaries = []

    for validator_name, validator in VALIDATORS:
        try:
            logger.info(
                f"Scan ID: {scan_id} | Starting {validator_name} validation")
            results = await validator.validate(
                api_spec.method,
                api_spec.url,
                api_spec.url_params,
                api_spec.body or {},
                api_spec.headers,
                scan_id
            )

            summary = ValidationSummary(
                scanId=scan_id,
                validation=validator_name,
                apiUrl=api_spec.url,
                results=results
            )
            validation_summaries.append(summary)

            logger.info(
                f"Scan ID: {scan_id} | {validator_name} validation completed successfully")
        except Exception as e:
            logger.error(
                f"Scan ID: {scan_id} | Error running {validator_name} validator: {str(e)}")

    return validation_summaries


async def save_results(scan_id: str, validation_summaries: List[ValidationSummary]):
    """Save validation summaries to the database using insert_many."""
    db = get_database()
    if validation_summaries:
        try:
            documents = [summary.model_dump()
                         for summary in validation_summaries]
            await db.validation_results.insert_many(documents)
            logger.info(
                f"Scan ID: {scan_id} | Saved {len(validation_summaries)} validation summaries")
        except Exception as e:
            logger.error(
                f"Scan ID: {scan_id} | Error saving validation results: {str(e)}")
    else:
        logger.warning(f"Scan ID: {scan_id} | No validation summaries to save")
