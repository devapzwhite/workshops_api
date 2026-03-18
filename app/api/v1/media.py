from typing import Annotated, Set
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db
from app.core.security import current_user
from app.models.user import User
from app.models.work_order import WorkOrder
from app.models.work_order_item import WorkOrderItem
from app.utils.image_utils import get_orphan_images, cleanup_orphan_images

router = APIRouter(prefix="/media", tags=["Media"])

# Directorio base para imágenes
MEDIA_ROOT = Path("media")
WORKORDER_ITEMS_DIR = MEDIA_ROOT / "workorder_items"


@router.get("/workorder_items/{filename}")
async def get_workorder_item_image(
    filename: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
):
    """
    Endpoint protegido para servir imágenes de WorkOrderItem.
    
    Verifica que el usuario pertenece al mismo shop_id que la orden de trabajo
    asociada a la imagen antes de servir el archivo.
    """
    # Buscar el WorkOrderItem que tiene esta imagen
    # Buscamos en before_photo_url o after_photo_url que contenga el filename
    result = await db.execute(
        select(WorkOrderItem)
        .join(WorkOrder, WorkOrderItem.work_order_id == WorkOrder.id)
        .where(
            (WorkOrderItem.before_photo_url.contains(filename)) |
            (WorkOrderItem.after_photo_url.contains(filename)),
            WorkOrder.shop_id == current_user.shop_id
        )
    )
    
    work_order_item = result.scalars().first()
    
    # Si no se encuentra o el shop_id no coincide, devolvemos 404 por seguridad
    if not work_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Verificar que el archivo existe físicamente
    filepath = WORKORDER_ITEMS_DIR / filename
    
    if not filepath.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Determinar el tipo de contenido según la extensión
    content_type = "application/octet-stream"
    ext = filepath.suffix.lower()
    if ext in [".jpg", ".jpeg"]:
        content_type = "image/jpeg"
    elif ext == ".png":
        content_type = "image/png"
    elif ext == ".gif":
        content_type = "image/gif"
    elif ext == ".webp":
        content_type = "image/webp"
    elif ext == ".bmp":
        content_type = "image/bmp"
    
    return FileResponse(
        path=filepath,
        media_type=content_type,
        filename=filename
    )


@router.post("/cleanup-orphans", status_code=status.HTTP_200_OK)
async def cleanup_orphan_images_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_user)],
):
    """
    Elimina imágenes huérfanas del filesystem que no están referenciadas 
    en la base de datos (work_order_items).
    
    Útil para limpiar fotos antiguas que quedaron sin referencia por 
    eliminaciones directas en BD u otros motivos.
    """
    # Obtener todas las URLs de fotos que están en uso
    result = await db.execute(
        select(WorkOrderItem.before_photo_url, WorkOrderItem.after_photo_url)
    )
    rows = result.all()
    
    # Crear conjunto de URLs en uso (filtrando None y vacíos)
    used_urls: Set[str] = set()
    for before_url, after_url in rows:
        if before_url:
            used_urls.add(before_url)
        if after_url:
            used_urls.add(after_url)
    
    # Encontrar imágenes huérfanas
    orphan_urls = get_orphan_images(used_urls)
    
    # Eliminar las huérfanas
    result_cleanup = cleanup_orphan_images(orphan_urls)
    
    return {
        "message": f"Se eliminaron {result_cleanup['deleted_count']} imágenes huérfanas",
        "deleted_count": result_cleanup["deleted_count"],
        "deleted_files": result_cleanup["deleted_files"],
        "total_orphans_found": len(orphan_urls)
    }
