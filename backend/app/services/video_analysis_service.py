"""
Video analysis service using Google Gemini AI.

Implements the service layer pattern for video/image analysis.
Single responsibility: handles all analysis logic.
"""

import base64
import io
import tempfile
import time
from typing import Optional
import logging

from google import genai
from google.genai import types as genai_types
from app.core.config import get_settings
from app.exceptions import ExternalServiceException, ValidationException
from app.schemas import AnalysisType
from app.utils import get_logger

logger = get_logger(__name__)


class VideoAnalysisService:
    """
    Video and image analysis using Google Gemini AI.

    Follows single responsibility principle - only handles analysis logic.
    Uses dependency injection for settings.
    """

    def __init__(self, settings=None):
        """
        Initialize video analysis service.

        Args:
            settings: Application settings (defaults to get_settings())
        """
        self.settings = settings or get_settings()
        self._client = None

    @property
    def client(self) -> genai.Client:
        """
        Get or create Gemini API client.

        Uses lazy initialization pattern.

        Returns:
            Google Genai client instance
        """
        if self._client is None:
            api_key = self.settings.GEMINI_API_KEY
            logger.info(f"Initializing Gemini client with API key: {api_key[:20]}...")
            self._client = genai.Client(
                api_key=api_key
            )
        return self._client

    def _create_analysis_prompt(
        self,
        analysis_type: AnalysisType,
        custom_prompt: Optional[str] = None,
    ) -> str:
        """
        Create analysis prompt based on analysis type.

        Args:
            analysis_type: Type of analysis to perform
            custom_prompt: Optional custom analysis prompt

        Returns:
            Analysis prompt string
        """
        if custom_prompt:
            return custom_prompt

        prompts = {
            AnalysisType.COMPREHENSIVE: (
                "Provide a comprehensive analysis of this video/image. "
                "Include: main subjects, key events, important details, "
                "visual elements, and any text visible."
            ),
            AnalysisType.BULLETS: (
                "Analyze this video/image and provide key points in "
                "bullet-point format."
            ),
            AnalysisType.DETAILED: (
                "Provide a detailed, thorough analysis of this video/image. "
                "Cover all observable elements, context, and implications."
            ),
            AnalysisType.PARAGRAPHS_TIMECODE: (
                "Analyze this video and provide analysis in paragraphs with "
                "timecode references where applicable."
            ),
            AnalysisType.QA: (
                "Analyze this video/image and provide key questions "
                "and answers about its content."
            ),
            AnalysisType.TRANSCRIPTION: (
                "Transcribe all spoken content in this video/audio. "
                "Include speaker identification if possible."
            ),
        }

        return prompts.get(
            analysis_type,
            prompts[AnalysisType.COMPREHENSIVE],
        )

    async def analyze_file(
        self,
        file_content: bytes,
        mime_type: str,
        analysis_type: AnalysisType = AnalysisType.COMPREHENSIVE,
        custom_prompt: Optional[str] = None,
    ) -> str:
        """
        Analyze a media file (image or video).

        Args:
            file_content: Raw file content as bytes
            mime_type: MIME type of the file
            analysis_type: Type of analysis to perform
            custom_prompt: Optional custom analysis prompt

        Returns:
            Analysis result as string

        Raises:
            ExternalServiceException: If Gemini API fails
            ValidationException: If file format is unsupported
        """
        logger.info(
            f"Starting analysis: type={analysis_type}, mime={mime_type}"
        )

        # Create analysis prompt
        prompt = self._create_analysis_prompt(
            analysis_type, custom_prompt
        )

        # Prepare file data as base64
        file_data_b64 = base64.standard_b64encode(
            file_content
        ).decode("utf-8")

        # Prepare file data as base64
        file_data_b64 = base64.standard_b64encode(
            file_content
        ).decode("utf-8")

        try:
            # Map mime type to file extension for proper detection
            mime_to_ext = {
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'image/gif': '.gif',
                'image/webp': '.webp',
                'video/mp4': '.mp4',
                'video/mpeg': '.mpeg',
                'video/quicktime': '.mov',
                'video/x-msvideo': '.avi',
                'video/x-matroska': '.mkv',
                'audio/mp3': '.mp3',
                'audio/mpeg': '.mp3',
                'audio/wav': '.wav',
                'audio/webm': '.webm',
            }
            
            file_ext = mime_to_ext.get(mime_type, '.tmp')
            
            # Write file to temporary location with proper extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            logger.info(f"Uploading file for analysis: {tmp_file_path} (mime: {mime_type})")
            file_upload_response = self.client.files.upload(
                file=tmp_file_path,
            )
            logger.info(f"File uploaded: {file_upload_response.uri}")
            
            # Wait for file to become ACTIVE (required by Google API)
            file_id = file_upload_response.name.split('/')[-1]  # Extract file ID from name
            max_retries = 30
            retry_count = 0
            file_obj = file_upload_response
            
            while file_obj.state.name != "ACTIVE" and retry_count < max_retries:
                retry_count += 1
                wait_time = min(2 ** retry_count, 10)  # Exponential backoff, max 10 seconds
                logger.info(f"File processing... state: {file_obj.state.name}, waiting {wait_time}s")
                time.sleep(wait_time)
                file_obj = self.client.files.get(name=file_id)
            
            if file_obj.state.name != "ACTIVE":
                raise ExternalServiceException(
                    service_name="Google Gemini",
                    detail=f"File did not reach ACTIVE state after {max_retries} attempts. Final state: {file_obj.state.name}"
                )
            
            logger.info(f"File is ACTIVE and ready for analysis")
            
            # Call Gemini API with file URI
            response = self.client.models.generate_content(
                model=self.settings.GEMINI_MODEL,
                contents=[
                    genai_types.ContentDict(
                        parts=[
                            genai_types.PartDict(
                                file_data=genai_types.FileDataDict(
                                    file_uri=file_obj.uri
                                ),
                            ),
                            genai_types.PartDict(
                                text=prompt,
                            ),
                        ],
                    ),
                ],
                config=genai_types.GenerateContentConfig(
                    temperature=self.settings.GEMINI_TEMPERATURE,
                ),
            )

            result_text = response.text

            logger.info("Analysis completed successfully")
            return result_text

        except Exception as exc:
            logger.error(
                f"Gemini API error: {str(exc)}",
                exc_info=True,
            )
            raise ExternalServiceException(
                service_name="Google Gemini",
                detail=str(exc),
            )
