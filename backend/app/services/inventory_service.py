from datetime import datetime
from app.repositories.inventory_repository import (
    get_inventory_by_product_id,
    create_inventory,
    update_inventory,
    count_inventory,
    list_inventory,
    count_low_stock,
    list_low_stock,
)
from app.services.product_service import ProductService
from app.exceptions import ResourceNotFoundError, ValidationError, DatabaseError, InsufficientStockError
from app.logger import get_logger

logger = get_logger("inventory_service")


class InventoryService:
    """Business logic for inventory management."""

    @staticmethod
    def add_inventory(cursor, product_id: int, available_stock: int, reserved_stock: int = 0):
        if available_stock < 0 or reserved_stock < 0:
            raise ValidationError("Inventory levels must be zero or greater")

        if not ProductService.product_exists(product_id, cursor=cursor):
            raise ResourceNotFoundError("Product", product_id)

        existing = get_inventory_by_product_id(cursor, product_id)
        if existing:
            raise ValidationError(f"Inventory record already exists for product {product_id}")

        create_inventory(cursor, product_id, available_stock, reserved_stock, datetime.utcnow())
        logger.info(f"Inventory created for product {product_id}")
        inventory = get_inventory_by_product_id(cursor, product_id)
        return InventoryService._map_inventory_row(inventory)

    @staticmethod
    def get_inventory(cursor, product_id: int):
        inventory = get_inventory_by_product_id(cursor, product_id)
        if not inventory:
            raise ResourceNotFoundError("Inventory", product_id)
        return InventoryService._map_inventory_row(inventory)

    @staticmethod
    def update_inventory_record(cursor, product_id: int, available_stock: int = None, reserved_stock: int = None):
        if available_stock is not None and available_stock < 0:
            raise ValidationError("Available stock must be zero or greater")
        if reserved_stock is not None and reserved_stock < 0:
            raise ValidationError("Reserved stock must be zero or greater")

        if not get_inventory_by_product_id(cursor, product_id):
            raise ResourceNotFoundError("Inventory", product_id)

        rowcount = update_inventory(cursor, product_id, available_stock, reserved_stock, datetime.utcnow())
        if rowcount == 0:
            raise DatabaseError("Inventory update failed")

        inventory = get_inventory_by_product_id(cursor, product_id)
        logger.info(f"Inventory updated for product {product_id}")
        return InventoryService._map_inventory_row(inventory)

    @staticmethod
    def list_inventory_records(cursor, page: int = 1, page_size: int = 20):
        total = count_inventory(cursor)
        rows = list_inventory(cursor, page, page_size)
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [InventoryService._map_inventory_row(row) for row in rows],
        }

    @staticmethod
    def list_low_stock(cursor, page: int = 1, page_size: int = 20):
        total = count_low_stock(cursor)
        rows = list_low_stock(cursor, page, page_size)
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [InventoryService._map_inventory_row(row) for row in rows],
        }

    @staticmethod
    def reserve_stock(cursor, product_id: int, quantity: int):
        if quantity <= 0:
            raise ValidationError("Reservation quantity must be greater than zero")

        inventory = get_inventory_by_product_id(cursor, product_id)
        product = ProductService.get_product_by_id(product_id, cursor=cursor)

        if not inventory:
            available_stock = product.get("stock", 0)
            create_inventory(cursor, product_id, available_stock, 0, datetime.utcnow())
            inventory = get_inventory_by_product_id(cursor, product_id)

        available_stock = inventory[2]
        reserved_stock = inventory[3]

        if available_stock < quantity:
            raise InsufficientStockError(product_id, quantity, available_stock)

        update_inventory(cursor, product_id, available_stock - quantity, reserved_stock + quantity, datetime.utcnow())
        logger.info(f"Reserved {quantity} units for product {product_id}")

    @staticmethod
    def release_stock(cursor, product_id: int, quantity: int):
        if quantity <= 0:
            raise ValidationError("Release quantity must be greater than zero")

        inventory = get_inventory_by_product_id(cursor, product_id)
        if not inventory:
            product = ProductService.get_product_by_id(product_id, cursor=cursor)
            create_inventory(cursor, product_id, product.get("stock", 0), 0, datetime.utcnow())
            inventory = get_inventory_by_product_id(cursor, product_id)

        available_stock = inventory[2]
        reserved_stock = inventory[3]

        if reserved_stock < quantity:
            raise ValidationError("Reserved stock is less than the release quantity")

        update_inventory(cursor, product_id, available_stock + quantity, reserved_stock - quantity, datetime.utcnow())
        logger.info(f"Released {quantity} reserved units for product {product_id}")

    @staticmethod
    def _map_inventory_row(row):
        return {
            "inventory_id": row[0],
            "product_id": row[1],
            "available_stock": row[2],
            "reserved_stock": row[3],
            "last_updated": row[4],
        }
