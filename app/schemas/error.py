from typing import Any, Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Modelo estándar para respuestas de error"""
    error: str = Field(..., description="Código de error")
    message: str = Field(..., description="Descripción legible del error")
    details: Optional[Any] = Field(None, description="Información adicional del error")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "RESOURCE_NOT_FOUND",
                "message": "El recurso solicitado no fue encontrado",
                "details": {"resource_id": 123}
            }
        }


class ValidationErrorResponse(ErrorResponse):
    """Modelo para errores de validación (422)"""
    error: str = "VALIDATION_ERROR"


class NotFoundErrorResponse(ErrorResponse):
    """Modelo para errores de recurso no encontrado (404)"""
    error: str = "NOT_FOUND"


class ConflictErrorResponse(ErrorResponse):
    """Modelo para errores de conflicto (409)"""
    error: str = "CONFLICT"


class UnauthorizedErrorResponse(ErrorResponse):
    """Modelo para errores de autenticación (401)"""
    error: str = "UNAUTHORIZED"


class ForbiddenErrorResponse(ErrorResponse):
    """Modelo para errores de autorización (403)"""
    error: str = "FORBIDDEN"


class InternalServerErrorResponse(ErrorResponse):
    """Modelo para errores internos del servidor (500)"""
    error: str = "INTERNAL_SERVER_ERROR"
