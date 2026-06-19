from fastapi import APIRouter, HTTPException, Query, Depends
from app.logger import get_logger
from app.services.inventory_service import InventoryService
from app.schemas.inventory_schema import (
    InventoryCreate,
    InventoryUpdate,
    InventoryOut,
    PaginatedInventory,
)
from app.utils.auth_dependency import admin_only
from app.database.db import get_connection

logger = get_logger("inventory_routes")
router = APIRouter()


@router.post("/add", response_model=InventoryOut, status_code=201, summary="Add inventory record for an existing product")
def add_inventory(inventory: InventoryCreate, user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        result = InventoryService.add_inventory(
            cursor,
            product_id=inventory.product_id,
            available_stock=inventory.available_stock,
            reserved_stock=inventory.reserved_stock,
        )
        conn.commit()
        return result
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Create inventory failed: {exc}")
        raise HTTPException(status_code=500, detail="Failed to create inventory record")
    finally:
        cursor.close()
        conn.close()


@router.get("/all", response_model=PaginatedInventory, summary="List inventory records with pagination")
def get_all_inventory(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        return InventoryService.list_inventory_records(cursor, page=page, page_size=page_size)
    except Exception as exc:
        logger.error(f"Get inventory list failed: {exc}")
        raise HTTPException(status_code=500, detail="Failed to retrieve inventory records")
    finally:
        cursor.close()
        conn.close()


@router.get("/{product_id}", response_model=InventoryOut, summary="Get inventory details for a product")
def get_inventory(product_id: int, user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        return InventoryService.get_inventory(cursor, product_id)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Get inventory failed: {exc}")
        raise HTTPException(status_code=500, detail="Failed to retrieve inventory details")
    finally:
        cursor.close()
        conn.close()


@router.put("/update/{product_id}", response_model=InventoryOut, summary="Update inventory stock counts for a product")
def update_inventory(product_id: int, inventory: InventoryUpdate, user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        return InventoryService.update_inventory_record(
            cursor,
            product_id=product_id,
            available_stock=inventory.available_stock,
            reserved_stock=inventory.reserved_stock,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Update inventory failed: {exc}")
        raise HTTPException(status_code=500, detail="Failed to update inventory")
    finally:
        cursor.close()
        conn.close()


@router.get("/low-stock", response_model=PaginatedInventory, summary="List inventory records with low stock")
def get_low_stock(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        return InventoryService.list_low_stock(cursor, page=page, page_size=page_size)
    except Exception as exc:
        logger.error(f"Get low stock list failed: {exc}")
        raise HTTPException(status_code=500, detail="Failed to retrieve low stock inventory")
    finally:
        cursor.close()
        conn.close()
