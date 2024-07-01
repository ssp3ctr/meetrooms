from fastapi import APIRouter, HTTPException, Request
from app.services.rule_service import RuleService

router = APIRouter()

@router.post("/")
async def service_clarify(request: Request):
    try:
        service_data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {str(e)}")
    
    rule_service = RuleService()
    try:
        valid_document_ids = await rule_service.process_service_data(service_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"valid_document_ids": valid_document_ids, "valid_document_count": len(valid_document_ids)}
