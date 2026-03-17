import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

# Directorio base para guardar imágenes
MEDIA_DIR = Path("media")
WORKORDER_ITEMS_DIR = MEDIA_DIR / "workorder_items"


async def save_image(
    file: Optional[UploadFile], 
    prefix: str = "item",
    work_order_id: Optional[int] = None
) -> Optional[str]:
    """
    Guarda una imagen en el filesystem y retorna la URL relativa.
    
    Args:
        file: Archivo UploadFile a guardar
        prefix: Prefijo para el nombre del archivo (ej: 'before', 'after')
        work_order_id: ID de la orden de trabajo
    
    Returns:
        URL relativa del archivo guardado, o None si no se proporcionó archivo
    """
    # Verificar que el archivo existe y tiene nombre válido
    if file is None or not file.filename or file.filename.strip() == "":
        return None
    
    # Validar tipo de imagen
    if file.content_type and not file.content_type.startswith("image/"):
        return None
    
    # Crear directorio si no existe
    WORKORDER_ITEMS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre único
    ext = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Construir nombre: prefix_workorderid_timestamp_uuid.ext
    wo_suffix = f"_wo{work_order_id}" if work_order_id else ""
    filename = f"{prefix}{wo_suffix}_{timestamp}_{unique_id}{ext}"
    
    filepath = WORKORDER_ITEMS_DIR / filename
    
    # Leer contenido del archivo y escribir
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Retornar URL relativa
    return f"workorder_items/{filename}"


def get_full_image_url(relative_url: str, base_url: str = "/media") -> str:
    """Construye la URL completa para acceder a la imagen."""
    if not relative_url:
        return ""
    return f"{base_url}/{relative_url}"
