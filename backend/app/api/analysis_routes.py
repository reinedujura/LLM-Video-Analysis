"""
Video analysis API endpoints.

REST endpoints for video/image upload and analysis.
"""

import time
import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from app.core.security import JWTManager
from app.exceptions import ApplicationException
from app.schemas import AnalysisResult, AnalysisType, VideoAnalysisRequest
from app.services import VideoAnalysisService
from app.utils import FileValidator, get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

jwt_manager = JWTManager()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_media(
    file: UploadFile = File(...),
    analysis_type: AnalysisType = Form(AnalysisType.COMPREHENSIVE),
    custom_prompt: str = Form(None),
    current_user: str = Depends(jwt_manager.get_current_user),
) -> AnalysisResult:
    """
    Analyze a video or image file.

    Args:
        file: Media file to analyze (image or video)
        analysis_type: Type of analysis to perform
        custom_prompt: Optional custom analysis prompt
        current_user: Authenticated user (from JWT token)

    Returns:
        AnalysisResult with analysis ID, type, and result

    Raises:
        HTTPException: If file validation or analysis fails
    """
    analysis_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Validate file
        validator = FileValidator()
        file_content = await file.read()

        mime_type = validator.validate_file(
            file.filename, len(file_content)
        )

        logger.info(
            f"Analysis initiated: user={current_user}, "
            f"file={file.filename}, type={analysis_type}"
        )

        # Perform analysis
        analysis_service = VideoAnalysisService()
        result = await analysis_service.analyze_file(
            file_content=file_content,
            mime_type=mime_type,
            analysis_type=analysis_type,
            custom_prompt=custom_prompt,
        )

        processing_time = time.time() - start_time

        logger.info(
            f"Analysis completed: id={analysis_id}, "
            f"time={processing_time:.2f}s"
        )

        return AnalysisResult(
            analysis_id=analysis_id,
            analysis_type=analysis_type,
            result=result,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            processing_time_seconds=processing_time,
        )

    except ApplicationException as exc:
        logger.error(f"Analysis failed: {exc.detail}")
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )
    except Exception as exc:
        logger.error(f"Unexpected error during analysis: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed unexpectedly",
        )
