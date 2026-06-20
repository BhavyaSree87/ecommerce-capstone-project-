from fastapi import APIRouter
from app.schemas.ai_schema import (
    GenerateDescriptionRequest, 
    GenerateDescriptionResponse,
    ShoppingAssistantRequest, 
    ShoppingAssistantResponse,
    ProductSearchRequest,
    ProductSearchResponse,
    ProductSearchResult
)
from app.services.ai_service import generate_product_description, shopping_assistant, rag_product_search
from app.logger import get_logger

logger = get_logger("ai_routes")

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)


@router.post("/generate-description", response_model=GenerateDescriptionResponse)
def generate_description(request: GenerateDescriptionRequest):
    """
    Generate AI-powered product description.
    
    Uses OpenAI API if configured, otherwise generates template-based description.
    
    Args:
        request: GenerateDescriptionRequest with product_name, category, brand
    
    Returns:
        GenerateDescriptionResponse with generated_description
    
    Example:
        POST /api/ai/generate-description
        {
            "product_name": "Wireless Headphones",
            "category": "Electronics",
            "brand": "Sony"
        }
    """
    try:
        logger.info(f"Generating description for {request.product_name}")
        
        description = generate_product_description(
            product_name=request.product_name,
            category=request.category,
            brand=request.brand
        )
        
        logger.info(f"Description generated successfully for {request.product_name}")
        return GenerateDescriptionResponse(generated_description=description)
        
    except Exception as e:
        logger.error(f"Error generating description: {e}")
        raise


@router.post("/shopping-assistant", response_model=ShoppingAssistantResponse)
def shopping_assistant_endpoint(request: ShoppingAssistantRequest):
    """
    AI-powered shopping assistant.
    
    Processes natural language queries to search products and recommend items.
    Uses OpenAI if API key configured, otherwise generates rule-based recommendations.
    
    Understands queries like:
    - "Suggest best phone under 50000"
    - "I need wireless headphones below 5000"
    - "Recommend gaming laptop"
    
    Args:
        request: ShoppingAssistantRequest with user query
    
    Returns:
        ShoppingAssistantResponse with personalized product recommendations
    
    Example:
        POST /api/ai/shopping-assistant
        {
            "query": "Suggest best phone under 50000"
        }
    """
    try:
        logger.info(f"Processing shopping query: {request.query}")
        
        answer = shopping_assistant(query=request.query)
        
        logger.info("Shopping assistant response generated")
        return ShoppingAssistantResponse(answer=answer)
        
    except Exception as e:
        logger.error(f"Error in shopping assistant: {e}")
        raise


@router.post("/product-search", response_model=ProductSearchResponse)
def product_search(request: ProductSearchRequest):
    """
    RAG-style product search endpoint.
    
    Searches products using keyword matching across product name, description, and category.
    Returns ranked results based on relevance score.
    
    No vector database - uses lightweight Oracle 11g keyword matching.
    
    Args:
        request: ProductSearchRequest with search query
    
    Returns:
        ProductSearchResponse with ranked product results
    
    Example:
        POST /api/ai/product-search
        {
            "query": "gaming laptop"
        }
    """
    try:
        logger.info(f"Processing RAG search query: {request.query}")
        
        # Perform RAG-style product search
        products = rag_product_search(query=request.query, limit=10)
        
        # Convert to response format
        results = []
        for product in products:
            result = ProductSearchResult(
                product_id=product.get('PRODUCT_ID', 0),
                product_name=product.get('PRODUCT_NAME', ''),
                price=float(product.get('PRICE', 0)),
                category=product.get('CATEGORY', ''),
                brand=product.get('BRAND', ''),
                stock=product.get('STOCK', 0),
                rating=float(product.get('RATING', 0)) if product.get('RATING') else None,
                image_url=product.get('IMAGE_URL', ''),
                relevance_score=float(product.get('RELEVANCE_SCORE', 0))
            )
            results.append(result)
        
        logger.info(f"RAG search returned {len(results)} results")
        return ProductSearchResponse(
            query=request.query,
            total_results=len(results),
            results=results
        )
        
    except Exception as e:
        logger.error(f"Error in RAG product search: {e}")
        raise


