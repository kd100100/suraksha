from fastapi import APIRouter, HTTPException, BackgroundTasks, Path, Query
from src.models.scan import ScanRequest, ScanModel
from src.config.database import get_database
from src.services.scan_service import process_scan
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scan", response_model=dict, status_code=202)
async def create_scan(
    scan_request: ScanRequest,
    background_tasks: BackgroundTasks
):
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

            # Return the created scan's ID
            return {"message": "Scan created successfully and processing started", "scan_id": str(scan_model.id)}
        else:
            raise HTTPException(
                status_code=500, detail="Failed to create scan")
    except Exception as e:
        logger.error(f"Error in create_scan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/scan/{scan_id}", response_model=dict)
async def get_scan_results(
    scan_id: str = Path(..., title="The ID of the scan to retrieve",
                        min_length=24, max_length=24)
):
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
            raise HTTPException(status_code=404, detail="Scan not found")

        # Retrieve the validation results
        validation_results = await db.validation_results.find({"scanId": scan_id}).to_list(None)

        # Convert ObjectId to string for JSON serialization
        for result in validation_results:
            result["_id"] = str(result["_id"])

        return {
            "scan": scan,
            "validation_results": validation_results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_scan_results: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/scans", response_model=list)
async def list_scans(
    limit: int = Query(
        10, ge=1, le=100, description="Number of scans to return"),
    offset: int = Query(0, ge=0, description="Number of scans to skip")
):
    """
    List all scans with pagination.

    - **limit**: Number of scans to return (default: 10, max: 100)
    - **offset**: Number of scans to skip (default: 0)
    - **returns**: A list of scans
    """
    try:
        db = get_database()

        # Retrieve the scans
        scans = await db.scans.find().skip(offset).limit(limit).to_list(None)

        # Convert ObjectId to string for JSON serialization
        for scan in scans:
            scan["_id"] = str(scan["_id"])

        return scans
    except Exception as e:
        logger.error(f"Error in list_scans: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
