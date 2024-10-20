from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.models.scan import ScanRequest, ScanModel
from src.config.database import get_database
from src.services.scan_service import process_scan
import logging
from bson import ObjectId

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scan", response_model=dict, status_code=202)
async def create_scan(scan_request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Create a new scan and start processing it asynchronously.

    - **scan_request**: The details of the scan to be performed
    - **returns**: A message confirming the scan creation and the scan ID
    """
    try:
        db = get_database()

        # Create a new ScanModel instance
        scan_model = ScanModel(request=scan_request)

        # Insert the document
        result = await db.scans.insert_one(scan_model.dict())

        if scan_model.id:
            # Add the scan processing to background tasks
            background_tasks.add_task(process_scan, str(scan_model.id))

            logger.info(
                f"Scan ID: {scan_model.id} | Scan created successfully and processing started")
            # Return the created scan's ID
            return {"message": "Scan created successfully and processing started", "scan_id": str(scan_model.id)}
        else:
            logger.error("Failed to create scan: No ID generated")
            raise HTTPException(
                status_code=500, detail="Failed to create scan")
    except Exception as e:
        logger.error(f"Error in create_scan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/scan/{scan_id}", response_model=dict)
async def get_scan_results(scan_id: str):
    """
    Retrieve the results of a specific scan.

    - **scan_id**: The ID of the scan to retrieve results for
    - **returns**: The scan details and validation results
    """
    try:
        db = get_database()

        # Retrieve the scan
        scan = await db.scans.find_one({"id": scan_id})
        if not scan:
            logger.warning(f"Scan ID: {scan_id} | Scan not found")
            raise HTTPException(status_code=404, detail="Scan not found")

        # Retrieve the validation results
        validation_results = await db.validation_results.find({"scanId": scan_id}).to_list(None)

        # Convert ObjectId to string for JSON serialization
        def convert_objectid(obj):
            if isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid(item) for item in obj]
            elif isinstance(obj, ObjectId):
                return str(obj)
            return obj

        scan = convert_objectid(scan)
        validation_results = convert_objectid(validation_results)

        logger.info(
            f"Scan ID: {scan_id} | Retrieved scan results successfully")
        return {
            "scan": scan,
            "validation_results": validation_results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Scan ID: {scan_id} | Error in get_scan_results: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
