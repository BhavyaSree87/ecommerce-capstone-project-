"""User service - handles user-related business logic"""

from app.database.db import get_db_context
from app.utils.password import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.exceptions import (
    ValidationError, AuthenticationError, ResourceNotFoundError,
    ConflictError, DatabaseError
)
from app.logger import get_logger
from typing import Dict, Optional, List
from datetime import timedelta

logger = get_logger("user_service")


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def register_user(user_data: Dict) -> Dict:
        """
        Register a new user
        
        Args:
            user_data: Dictionary with user registration data
            
        Returns:
            Dictionary with user info and JWT token
            
        Raises:
            ConflictError: If email already exists
            DatabaseError: If database operation fails
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Check if email already exists
                cursor.execute(
                    "SELECT COUNT(1) FROM USERS WHERE EMAIL = :email",
                    {"email": user_data['email']}
                )
                if cursor.fetchone()[0] > 0:
                    logger.warning(f"Registration attempt with duplicate email: {user_data['email']}")
                    raise ConflictError("Email already registered")
                
                # Hash password
                hashed_password = hash_password(user_data['password'])
                
                # Insert user
                cursor.execute(
                    """
                    INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE)
                    VALUES (USER_SEQ.NEXTVAL, :name, :email, :password, :role, :mobile, :address, :city, :state, :pincode)
                    """,
                    {
                        "name": user_data['name'],
                        "email": user_data['email'],
                        "password": hashed_password,
                        "role": "CUSTOMER",
                        "mobile": user_data['mobile'],
                        "address": user_data['address'],
                        "city": user_data['city'],
                        "state": user_data['state'],
                        "pincode": user_data['pincode'],
                    }
                )
                
                # Get new user
                cursor.execute(
                    "SELECT ID, EMAIL, ROLE FROM USERS WHERE EMAIL = :email",
                    {"email": user_data['email']}
                )
                new_user = cursor.fetchone()
                
                # Create token
                token = create_access_token({
                    "user_id": new_user[0],
                    "email": new_user[1],
                    "role": new_user[2]
                })
                
                logger.info(f"New user registered: {new_user[0]}")
                
                return {
                    "access_token": token,
                    "token_type": "bearer",
                    "expires_in": 7200,
                    "user": {
                        "id": new_user[0],
                        "email": new_user[1],
                        "role": new_user[2]
                    }
                }
                
        except (ConflictError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            raise DatabaseError(f"Registration failed: {str(e)}")
    
    @staticmethod
    def login_user(email: str, password: str) -> Dict:
        """
        Authenticate user and generate token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with JWT token and user info
            
        Raises:
            AuthenticationError: If credentials are invalid
            DatabaseError: If database operation fails
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT ID, EMAIL, PASSWORD, ROLE, NAME FROM USERS WHERE EMAIL = :email",
                    {"email": email}
                )
                db_user = cursor.fetchone()
                
                if not db_user or not verify_password(password, db_user[2]):
                    logger.warning(f"Failed login attempt for email: {email}")
                    raise AuthenticationError("Invalid email or password")
                
                # Create token
                token = create_access_token({
                    "user_id": db_user[0],
                    "email": db_user[1],
                    "role": db_user[3]
                })
                
                logger.info(f"User login successful: {db_user[0]}")
                
                return {
                    "access_token": token,
                    "token_type": "bearer",
                    "expires_in": 7200,
                    "user": {
                        "id": db_user[0],
                        "email": db_user[1],
                        "role": db_user[3],
                        "name": db_user[4]
                    }
                }
                
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise DatabaseError("Login failed")
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Dict:
        """Get user by ID"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT ID, NAME, EMAIL, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE 
                    FROM USERS WHERE ID = :id
                    """,
                    {"id": user_id}
                )
                user = cursor.fetchone()
                
                if not user:
                    raise ResourceNotFoundError("User", user_id)
                
                return {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "role": user[3],
                    "mobile": user[4],
                    "address": user[5],
                    "city": user[6],
                    "state": user[7],
                    "pincode": user[8]
                }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get user failed: {e}")
            raise DatabaseError("Get user failed")
    
    @staticmethod
    def get_all_users(page: int = 1, page_size: int = 20) -> Dict:
        """Get all users with pagination"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM USERS")
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size
                
                cursor.execute(
                    """
                    SELECT * FROM (
                      SELECT a.*, ROWNUM rnum FROM (
                        SELECT ID, NAME, EMAIL, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE 
                        FROM USERS ORDER BY ID DESC
                      ) a WHERE ROWNUM <= :end
                    ) WHERE rnum >= :start
                    """,
                    {"start": start, "end": end}
                )
                
                users = []
                for row in cursor.fetchall():
                    users.append({
                        "id": row[0],
                        "name": row[1],
                        "email": row[2],
                        "role": row[3],
                        "mobile": row[4],
                        "address": row[5],
                        "city": row[6],
                        "state": row[7],
                        "pincode": row[8]
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": users
                }
        except Exception as e:
            logger.error(f"Get all users failed: {e}")
            raise DatabaseError("Get users failed")
    
    @staticmethod
    def update_user(user_id: int, update_data: Dict) -> Dict:
        """Update user information"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                update_fields = []
                params = {"id": user_id}
                
                for key, value in update_data.items():
                    if value is not None:
                        update_fields.append(f"{key.upper()} = :{key}")
                        params[key] = value
                
                if not update_fields:
                    raise ValidationError("No fields to update")
                
                query = f"UPDATE USERS SET {', '.join(update_fields)} WHERE ID = :id"
                cursor.execute(query, params)
                
                if cursor.rowcount == 0:
                    raise ResourceNotFoundError("User", user_id)
                
                logger.info(f"User {user_id} updated")
                return UserService.get_user_by_id(user_id)
                
        except (ValidationError, ResourceNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Update user failed: {e}")
            raise DatabaseError("Update user failed")
    
    @staticmethod
    def delete_user(user_id: int) -> None:
        """Delete user by ID"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM USERS WHERE ID = :id", {"id": user_id})
                
                if cursor.rowcount == 0:
                    raise ResourceNotFoundError("User", user_id)
                
                logger.info(f"User {user_id} deleted")
                
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Delete user failed: {e}")
            raise DatabaseError("Delete user failed")
