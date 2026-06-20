from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
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
from app.utils.auth_dependency import oauth2_scheme

app = FastAPI(
    title="E-Commerce Platform API",
    description="FastAPI Backend for E-Commerce Platform with JWT Authentication",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    # During local development allow all origins to avoid CORS friction from the dev server.
    # In production replace with explicit origins (do NOT use "*").
    allow_origins=["*"],
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
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/auth/token",
                    "scopes": {}
                }
            },
            "description": "OAuth2 password flow for login - obtain a JWT access token"
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Use a JWT access token prefixed with Bearer"
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

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
