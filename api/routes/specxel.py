from fastapi import APIRouter, HTTPException
from api.schemas import ClassifyRequest, ClassifyResponse
from specxel.pipeline import classify_image
from core.logging import get_logger

logger = get_logger("specxel")
router = APIRouter()

@router.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    try:
        is_pixelart, confidence = classify_image(req.image_url)
        logger.info(f"[{req.sprite_id}] is_pixelart={is_pixelart} confidence={confidence:.4f}")
        return ClassifyResponse(
            sprite_id=req.sprite_id,
            is_pixelart=is_pixelart,
            confidence=confidence,
        )
    except Exception as e:
        logger.error(f"Classify failed for {req.sprite_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))