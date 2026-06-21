from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.logger import get_logger
from app.routes.auth_routes import router as auth_router
from app.routes import product_routes
from app.routes import cart_routes
from app.routes import wishlist_routes
from app.routes import order_routes
from app.routes import payment_routes
from app.routes import user_routes
from app.routes import dashboard_routes
from app.routes import inventory_routes
from app.routes import report_routes
from app.routes import category_routes
from app.routes import ai_routes

app = FastAPI(
    title="E-Commerce Platform API",
    description="FastAPI Backend for E-Commerce Platform with JWT Authentication",
    version="1.0.0"
)


def mask_secret(secret: str) -> str:
    if not secret:
        return "<missing>"
    if len(secret) <= 8:
        return "*" * len(secret)
    return f"{secret[:4]}{'*' * (len(secret) - 8)}{secret[-4:]}"


settings = get_settings()
startup_logger = get_logger("startup")
startup_logger.info(
    "Loaded security settings: SECRET_KEY=%s ALGORITHM=%s ACCESS_TOKEN_EXPIRE_HOURS=%s",
    mask_secret(settings.secret_key),
    settings.algorithm,
    settings.access_token_expire_hours
)

app.add_middleware(
    CORSMiddleware,
    # During local development allow all origins to avoid CORS friction from the dev server.
    # In production replace with explicit origins (do NOT use "*").
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def custom_openapi():
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="E-Commerce Platform API",
        version="1.0.0",
        description="FastAPI Backend for E-Commerce Platform with JWT Authentication",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Use a JWT access token prefixed with Bearer"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]

    auth_paths = ["/api/auth/login", "/api/auth/register", "/api/auth/token"]
    for path in auth_paths:
        if path in openapi_schema.get("paths", {}):
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = []

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "message": "Backend Running Successfully"
    }

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(product_routes.router,
                   prefix="/api/products",
                   tags=["Products"])

app.include_router(
    cart_routes.router,
    prefix="/api/cart",
    tags=["Cart"]
)

app.include_router(
    wishlist_routes.router,
    prefix="/api/wishlist",
    tags=["Wishlist"]
)

app.include_router(
    order_routes.router,
    prefix="/api/orders",
    tags=["Orders"]
)

app.include_router(
    payment_routes.router,
    prefix="/api/payments",
    tags=["Payments"]
)

app.include_router(
    user_routes.router,
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    inventory_routes.router,
    prefix="/api/inventory",
    tags=["Inventory"]
)

app.include_router(
    report_routes.router
)

app.include_router(
    dashboard_routes.router
)

app.include_router(
    category_routes.router,
    prefix="/api/categories",
    tags=["Categories"]
)

app.include_router(
    ai_routes.router
)
