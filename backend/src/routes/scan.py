from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.models.scan import ScanRequest, ScanModel
from src.config.database import get_database
from src.services.scan_service import process_scan, create_scan_model, get_scan_results
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

        # Create a new ScanModel instance using the service function
        scan_model = create_scan_model(scan_request)

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
async def get_scan_results_route(scan_id: str):
    """
    Retrieve the results of a specific scan.

    - **scan_id**: The ID of the scan to retrieve results for
    - **returns**: The scan details, validation results, and trend data
    """
    try:
        results = await get_scan_results(scan_id)
        if not results:
            logger.warning(f"Scan ID: {scan_id} | Scan not found")
            raise HTTPException(status_code=404, detail="Scan not found")

        # Convert ObjectId to string for JSON serialization
        def convert_objectid(obj):
            if isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid(item) for item in obj]
            elif isinstance(obj, ObjectId):
                return str(obj)
            return obj

        results = convert_objectid(results)

        logger.info(
            f"Scan ID: {scan_id} | Retrieved scan results and trend data successfully")
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Scan ID: {scan_id} | Error in get_scan_results: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
