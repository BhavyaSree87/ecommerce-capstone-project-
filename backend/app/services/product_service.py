"""Product service - handles product-related business logic"""

from app.database.db import get_db_context
from app.exceptions import ResourceNotFoundError, ValidationError, DatabaseError
from app.logger import get_logger
from typing import Dict, List, Optional

logger = get_logger("product_service")


class ProductService:
    """Service class for product operations"""
    
    @staticmethod
    def create_product(product_data: Dict) -> Dict:
        """
        Create a new product
        
        Args:
            product_data: Dictionary with product information
            
        Returns:
            Created product ID
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    INSERT INTO PRODUCTS
                    (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
                    VALUES
                    (PRODUCT_SEQ.NEXTVAL, :product_name, :price, :description, :category, :brand, :stock, :image_url, :rating)
                    """
                ,
                    {
                        "product_name": product_data['product_name'],
                        "price": product_data['price'],
                        "description": product_data['description'],
                        "category": product_data['category'],
                        "brand": product_data['brand'],
                        "stock": product_data['stock'],
                        "image_url": product_data['image_url'],
                        "rating": product_data['rating']
                    }
                )
                
                logger.info(f"Product created: {product_data['product_name']}")
                
                return {"message": "Product added successfully"}
                
        except Exception as e:
            logger.error(f"Create product failed: {e}")
            raise DatabaseError(f"Product creation failed: {str(e)}")
    
    @staticmethod
    def get_product_by_id(product_id: int, cursor=None) -> Dict:
        """Get product by ID"""
        try:
            if cursor is not None:
                cursor.execute(
                    """
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                    FROM PRODUCTS WHERE PRODUCT_ID = :id
                    """,
                    {"id": product_id}
                )
                product = cursor.fetchone()
            else:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                        FROM PRODUCTS WHERE PRODUCT_ID = :id
                        """,
                        {"id": product_id}
                    )
                    product = cursor.fetchone()

            if not product:
                raise ResourceNotFoundError("Product", product_id)

            return {
                "product_id": product[0],
                "product_name": product[1],
                "price": product[2],
                "description": product[3],
                "category": product[4],
                "brand": product[5],
                "stock": product[6],
                "image_url": product[7],
                "rating": product[8]
            }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get product failed: {e}")
            raise DatabaseError("Get product failed")
    
    @staticmethod
    def get_all_products(page: int = 1, page_size: int = 20) -> Dict:
        """Get all products with pagination"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size
                
                cursor.execute(
                    """
                    SELECT * FROM (
                      SELECT a.*, ROWNUM rnum FROM (
                        SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                        FROM PRODUCTS ORDER BY PRODUCT_ID DESC
                      ) a WHERE ROWNUM <= :end
                    ) WHERE rnum >= :start
                    """,
                    {"start": start, "end": end}
                )
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "product_id": row[0],
                        "product_name": row[1],
                        "price": row[2],
                        "description": row[3],
                        "category": row[4],
                        "brand": row[5],
                        "stock": row[6],
                        "image_url": row[7],
                        "rating": row[8]
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get all products failed: {e}")
            raise DatabaseError("Get products failed")
    
    @staticmethod
    def search_products(
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        in_stock_only: bool = False
    ) -> Dict:
        """
        Search and filter products
        
        Args:
            page: Page number
            page_size: Items per page
            keyword: Search keyword
            category: Product category
            brand: Product brand
            min_price: Minimum price
            max_price: Maximum price
            min_rating: Minimum rating
            in_stock_only: Only show in-stock products
            
        Returns:
            Filtered products list
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Build WHERE clause
                where_conditions = []
                params = {}
                
                if keyword:
                    where_conditions.append(
                        "UPPER(PRODUCT_NAME) LIKE :keyword OR UPPER(DESCRIPTION) LIKE :keyword"
                    )
                    params['keyword'] = f"%{keyword.upper()}%"
                
                if category:
                    where_conditions.append("UPPER(CATEGORY) = :category")
                    params['category'] = category.upper()
                
                if brand:
                    where_conditions.append("UPPER(BRAND) = :brand")
                    params['brand'] = brand.upper()
                
                if min_price is not None:
                    where_conditions.append("PRICE >= :min_price")
                    params['min_price'] = min_price
                
                if max_price is not None:
                    where_conditions.append("PRICE <= :max_price")
                    params['max_price'] = max_price
                
                if min_rating is not None:
                    where_conditions.append("RATING >= :min_rating")
                    params['min_rating'] = min_rating
                
                if in_stock_only:
                    where_conditions.append("STOCK > 0")
                
                where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
                
                # Count total
                count_query = f"SELECT COUNT(*) FROM PRODUCTS WHERE {where_clause}"
                cursor.execute(count_query, params)
                total = cursor.fetchone()[0]
                
                # Pagination
                start = (page - 1) * page_size + 1
                end = page * page_size
                params['start'] = start
                params['end'] = end
                
                # Fetch results
                query = f"""
                SELECT * FROM (
                  SELECT a.*, ROWNUM rnum FROM (
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                    FROM PRODUCTS WHERE {where_clause} ORDER BY PRODUCT_ID DESC
                  ) a WHERE ROWNUM <= :end
                ) WHERE rnum >= :start
                """
                
                cursor.execute(query, params)
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "product_id": row[0],
                        "product_name": row[1],
                        "price": row[2],
                        "description": row[3],
                        "category": row[4],
                        "brand": row[5],
                        "stock": row[6],
                        "image_url": row[7],
                        "rating": row[8]
                    })
                
                logger.info(f"Product search completed: {total} results found")
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Product search failed: {e}")
            raise DatabaseError("Product search failed")
    
    @staticmethod
    def update_product(product_id: int, update_data: Dict) -> Dict:
        """Update product information"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Verify product exists
                cursor.execute(
                    "SELECT PRODUCT_ID FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                if not cursor.fetchone():
                    raise ResourceNotFoundError("Product", product_id)
                
                # Build update query
                update_fields = []
                params = {"id": product_id}
                
                field_mapping = {
                    "product_name": "PRODUCT_NAME",
                    "price": "PRICE",
                    "description": "DESCRIPTION",
                    "category": "CATEGORY",
                    "brand": "BRAND",
                    "stock": "STOCK",
                    "image_url": "IMAGE_URL",
                    "rating": "RATING"
                }
                
                for key, db_col in field_mapping.items():
                    if key in update_data and update_data[key] is not None:
                        update_fields.append(f"{db_col} = :{key}")
                        params[key] = update_data[key]
                
                if not update_fields:
                    raise ValidationError("No fields to update")
                
                query = f"UPDATE PRODUCTS SET {', '.join(update_fields)} WHERE PRODUCT_ID = :id"
                cursor.execute(query, params)
                
                logger.info(f"Product {product_id} updated")
                return ProductService.get_product_by_id(product_id)
                
        except (ValidationError, ResourceNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Update product failed: {e}")
            raise DatabaseError("Update product failed")
    
    @staticmethod
    def delete_product(product_id: int) -> None:
        """Delete product by ID"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM PRODUCTS WHERE PRODUCT_ID = :id", {"id": product_id})
                
                if cursor.rowcount == 0:
                    raise ResourceNotFoundError("Product", product_id)
                
                logger.info(f"Product {product_id} deleted")
                
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Delete product failed: {e}")
            raise DatabaseError("Delete product failed")
    
    @staticmethod
    def get_stock(product_id: int) -> int:
        """Get current stock for a product"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT STOCK FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                
                result = cursor.fetchone()
                if not result:
                    raise ResourceNotFoundError("Product", product_id)
                
                return result[0]
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get stock failed: {e}")
            raise DatabaseError("Get stock failed")

    @staticmethod
    def product_exists(product_id: int, cursor=None) -> bool:
        """Check if a product exists."""
        try:
            if cursor is not None:
                cursor.execute(
                    "SELECT 1 FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                return cursor.fetchone() is not None

            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Product exists check failed: {e}")
            raise DatabaseError("Product existence check failed")
    
    @staticmethod
    def reduce_stock(product_id: int, quantity: int) -> None:
        """
        Reduce product stock
        
        Args:
            product_id: Product ID
            quantity: Quantity to reduce
            
        Raises:
            InsufficientStockError: If not enough stock
        """
        from app.exceptions import InsufficientStockError
        
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Get current stock
                current_stock = ProductService.get_stock(product_id)
                
                if current_stock < quantity:
                    raise InsufficientStockError(product_id, quantity, current_stock)
                
                # Reduce stock
                cursor.execute(
                    "UPDATE PRODUCTS SET STOCK = STOCK - :qty WHERE PRODUCT_ID = :id",
                    {"qty": quantity, "id": product_id}
                )
                
                logger.info(f"Stock reduced for product {product_id}: {quantity} units")
                
        except InsufficientStockError:
            raise
        except Exception as e:
            logger.error(f"Reduce stock failed: {e}")
            raise DatabaseError("Stock reduction failed")
"""Product service - handles product-related business logic"""

from app.database.db import get_db_context
from app.exceptions import ResourceNotFoundError, ValidationError, DatabaseError
from app.logger import get_logger
from typing import Dict, List, Optional

logger = get_logger("product_service")


class ProductService:
    """Service class for product operations"""
    
    @staticmethod
    def create_product(product_data: Dict) -> Dict:
        """
        Create a new product
        
        Args:
            product_data: Dictionary with product information
            
        Returns:
            Created product ID
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    INSERT INTO PRODUCTS
                    (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
                    VALUES
                    (PRODUCT_SEQ.NEXTVAL, :product_name, :price, :description, :category, :brand, :stock, :image_url, :rating)
                    """
                ,
                    {
                        "product_name": product_data['product_name'],
                        "price": product_data['price'],
                        "description": product_data['description'],
                        "category": product_data['category'],
                        "brand": product_data['brand'],
                        "stock": product_data['stock'],
                        "image_url": product_data['image_url'],
                        "rating": product_data['rating']
                    }
                )
                
                logger.info(f"Product created: {product_data['product_name']}")
                
                return {"message": "Product added successfully"}
                
        except Exception as e:
            logger.error(f"Create product failed: {e}")
            raise DatabaseError(f"Product creation failed: {str(e)}")
    
    @staticmethod
    def get_product_by_id(product_id: int, cursor=None) -> Dict:
        """Get product by ID"""
        try:
            if cursor is not None:
                cursor.execute(
                    """
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                    FROM PRODUCTS WHERE PRODUCT_ID = :id
                    """,
                    {"id": product_id}
                )
                product = cursor.fetchone()
            else:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                        FROM PRODUCTS WHERE PRODUCT_ID = :id
                        """,
                        {"id": product_id}
                    )
                    product = cursor.fetchone()

            if not product:
                raise ResourceNotFoundError("Product", product_id)

            return {
                "product_id": product[0],
                "product_name": product[1],
                "price": product[2],
                "description": product[3],
                "category": product[4],
                "brand": product[5],
                "stock": product[6],
                "image_url": product[7],
                "rating": product[8]
            }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get product failed: {e}")
            raise DatabaseError("Get product failed")
    
    @staticmethod
    def get_all_products(page: int = 1, page_size: int = 20) -> Dict:
        """Get all products with pagination"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size
                
                cursor.execute(
                    """
                    SELECT * FROM (
                      SELECT a.*, ROWNUM rnum FROM (
                        SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                        FROM PRODUCTS ORDER BY PRODUCT_ID DESC
                      ) a WHERE ROWNUM <= :end
                    ) WHERE rnum >= :start
                    """,
                    {"start": start, "end": end}
                )
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "product_id": row[0],
                        "product_name": row[1],
                        "price": row[2],
                        "description": row[3],
                        "category": row[4],
                        "brand": row[5],
                        "stock": row[6],
                        "image_url": row[7],
                        "rating": row[8]
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get all products failed: {e}")
            raise DatabaseError("Get products failed")
    
    @staticmethod
    def search_products(
        page: int = 1,
        page_size: int = 20,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        in_stock_only: bool = False
    ) -> Dict:
        """
        Search and filter products
        
        Args:
            page: Page number
            page_size: Items per page
            keyword: Search keyword
            category: Product category
            brand: Product brand
            min_price: Minimum price
            max_price: Maximum price
            min_rating: Minimum rating
            in_stock_only: Only show in-stock products
            
        Returns:
            Filtered products list
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Build WHERE clause
                where_conditions = []
                params = {}
                
                if keyword:
                    where_conditions.append(
                        "UPPER(PRODUCT_NAME) LIKE :keyword OR UPPER(DESCRIPTION) LIKE :keyword"
                    )
                    params['keyword'] = f"%{keyword.upper()}%"
                
                if category:
                    where_conditions.append("UPPER(CATEGORY) = :category")
                    params['category'] = category.upper()
                
                if brand:
                    where_conditions.append("UPPER(BRAND) = :brand")
                    params['brand'] = brand.upper()
                
                if min_price is not None:
                    where_conditions.append("PRICE >= :min_price")
                    params['min_price'] = min_price
                
                if max_price is not None:
                    where_conditions.append("PRICE <= :max_price")
                    params['max_price'] = max_price
                
                if min_rating is not None:
                    where_conditions.append("RATING >= :min_rating")
                    params['min_rating'] = min_rating
                
                if in_stock_only:
                    where_conditions.append("STOCK > 0")
                
                where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
                
                # Count total
                count_query = f"SELECT COUNT(*) FROM PRODUCTS WHERE {where_clause}"
                cursor.execute(count_query, params)
                total = cursor.fetchone()[0]
                
                # Pagination
                start = (page - 1) * page_size + 1
                end = page * page_size
                params['start'] = start
                params['end'] = end
                
                # Fetch results
                query = f"""
                SELECT * FROM (
                  SELECT a.*, ROWNUM rnum FROM (
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
                    FROM PRODUCTS WHERE {where_clause} ORDER BY PRODUCT_ID DESC
                  ) a WHERE ROWNUM <= :end
                ) WHERE rnum >= :start
                """
                
                cursor.execute(query, params)
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "product_id": row[0],
                        "product_name": row[1],
                        "price": row[2],
                        "description": row[3],
                        "category": row[4],
                        "brand": row[5],
                        "stock": row[6],
                        "image_url": row[7],
                        "rating": row[8]
                    })
                
                logger.info(f"Product search completed: {total} results found")
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Product search failed: {e}")
            raise DatabaseError("Product search failed")
    
    @staticmethod
    def update_product(product_id: int, update_data: Dict) -> Dict:
        """Update product information"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Verify product exists
                cursor.execute(
                    "SELECT PRODUCT_ID FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                if not cursor.fetchone():
                    raise ResourceNotFoundError("Product", product_id)
                
                # Build update query
                update_fields = []
                params = {"id": product_id}
                
                field_mapping = {
                    "product_name": "PRODUCT_NAME",
                    "price": "PRICE",
                    "description": "DESCRIPTION",
                    "category": "CATEGORY",
                    "brand": "BRAND",
                    "stock": "STOCK",
                    "image_url": "IMAGE_URL",
                    "rating": "RATING"
                }
                
                for key, db_col in field_mapping.items():
                    if key in update_data and update_data[key] is not None:
                        update_fields.append(f"{db_col} = :{key}")
                        params[key] = update_data[key]
                
                if not update_fields:
                    raise ValidationError("No fields to update")
                
                query = f"UPDATE PRODUCTS SET {', '.join(update_fields)} WHERE PRODUCT_ID = :id"
                cursor.execute(query, params)
                
                logger.info(f"Product {product_id} updated")
                return ProductService.get_product_by_id(product_id)
                
        except (ValidationError, ResourceNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Update product failed: {e}")
            raise DatabaseError("Update product failed")
    
    @staticmethod
    def delete_product(product_id: int) -> None:
        """Delete product by ID"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM PRODUCTS WHERE PRODUCT_ID = :id", {"id": product_id})
                
                if cursor.rowcount == 0:
                    raise ResourceNotFoundError("Product", product_id)
                
                logger.info(f"Product {product_id} deleted")
                
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Delete product failed: {e}")
            raise DatabaseError("Delete product failed")
    
    @staticmethod
    def get_stock(product_id: int) -> int:
        """Get current stock for a product"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT STOCK FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                
                result = cursor.fetchone()
                if not result:
                    raise ResourceNotFoundError("Product", product_id)
                
                return result[0]
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get stock failed: {e}")
            raise DatabaseError("Get stock failed")

    @staticmethod
    def product_exists(product_id: int, cursor=None) -> bool:
        """Check if a product exists."""
        try:
            if cursor is not None:
                cursor.execute(
                    "SELECT 1 FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                return cursor.fetchone() is not None

            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM PRODUCTS WHERE PRODUCT_ID = :id",
                    {"id": product_id}
                )
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Product exists check failed: {e}")
            raise DatabaseError("Product existence check failed")
    
    @staticmethod
    def reduce_stock(product_id: int, quantity: int) -> None:
        """
        Reduce product stock
        
        Args:
            product_id: Product ID
            quantity: Quantity to reduce
            
        Raises:
            InsufficientStockError: If not enough stock
        """
        from app.exceptions import InsufficientStockError
        
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Get current stock
                current_stock = ProductService.get_stock(product_id)
                
                if current_stock < quantity:
                    raise InsufficientStockError(product_id, quantity, current_stock)
                
                # Reduce stock
                cursor.execute(
                    "UPDATE PRODUCTS SET STOCK = STOCK - :qty WHERE PRODUCT_ID = :id",
                    {"qty": quantity, "id": product_id}
                )
                
                logger.info(f"Stock reduced for product {product_id}: {quantity} units")
                
        except InsufficientStockError:
            raise
        except Exception as e:
            logger.error(f"Reduce stock failed: {e}")
            raise DatabaseError("Stock reduction failed")
