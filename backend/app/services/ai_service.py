from app.config import get_settings
from app.logger import get_logger
import re
from typing import List, Dict, Any

logger = get_logger("ai_service")


DESCRIPTION_TEMPLATES = {
    "electronics": "Premium {brand} {product_name} designed for optimal performance and reliability. Features advanced technology and exceptional build quality. Perfect for professionals and enthusiasts alike.",
    "clothing": "Stylish {brand} {product_name} combining comfort and fashion. Made with high-quality materials for durability and style. Ideal for everyday wear and special occasions.",
    "home": "Essential {brand} {product_name} for your home. Engineered for functionality and elegance. Enhances comfort and convenience in your daily life.",
    "sports": "Professional-grade {brand} {product_name} designed for athletes. Superior performance and durability. Engineered to withstand intense training and competition.",
    "beauty": "Premium {brand} {product_name} for beauty and skincare. Formulated with quality ingredients for effective results. Trusted by professionals for visible improvements.",
    "books": "Engaging {brand} {product_name} offering valuable insights and entertainment. Well-written and thoroughly researched. A must-read for anyone interested in the subject.",
    "default": "High-quality {brand} {product_name} delivering excellent value. Carefully crafted for performance and durability. A reliable choice for discerning customers."
}


def generate_description_openai(product_name: str, category: str, brand: str) -> str:
    
    try:
        import openai
        
        settings = get_settings()
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured, using template fallback")
            return generate_description_template(product_name, category, brand)
        
        openai.api_key = settings.openai_api_key
        
        prompt = f"""Generate a compelling and professional product description for an e-commerce listing.

Product Name: {product_name}
Category: {category}
Brand: {brand}

Requirements:
- 2-3 sentences maximum
- Focus on benefits and features
- Professional and engaging tone
- Suitable for e-commerce platform
- Highlight unique selling points

Generate only the description text, no additional labels or formatting."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert e-commerce product description writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        description = response.choices[0].message.content.strip()
        logger.info(f"Generated description for {product_name} using OpenAI")
        return description
        
    except ImportError:
        logger.warning("OpenAI library not installed, using template fallback")
        return generate_description_template(product_name, category, brand)
    except Exception as e:
        logger.error(f"OpenAI API error: {e}, using template fallback")
        return generate_description_template(product_name, category, brand)


def generate_description_template(product_name: str, category: str, brand: str) -> str:
    
    try:      
        category_lower = category.lower()
        template = DESCRIPTION_TEMPLATES.get(category_lower, DESCRIPTION_TEMPLATES["default"])
        description = template.format(
            product_name=product_name,
            brand=brand,
            category=category
        )
        
        logger.info(f"Generated template description for {product_name} in {category}")
        return description
        
    except Exception as e:
        logger.error(f"Template generation error: {e}")
        
        return f"{brand} {product_name} - Premium quality product in the {category} category. Engineered for excellence and customer satisfaction."


def generate_product_description(product_name: str, category: str, brand: str) -> str:

    settings = get_settings()
    
    if settings.openai_api_key:
        return generate_description_openai(product_name, category, brand)
    else:
        return generate_description_template(product_name, category, brand)



def parse_shopping_query(query: str) -> Dict[str, Any]:
    
    try:
        constraints = {
            "product_type": None,
            "max_price": None,
            "min_price": 0,
            "category": None,
            "search_keywords": []
        }
        
        query_lower = query.lower()
        
        price_patterns = [
            r'under\s+(\d+)',
            r'below\s+(\d+)',
            r'max\s+(\d+)',
            r'upto\s+(\d+)',
            r'up to\s+(\d+)',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, query_lower)
            if match:
                constraints["max_price"] = int(match.group(1))
                break
        
        product_keywords = {
            "phone": "Electronics",
            "smartphone": "Electronics",
            "mobile": "Electronics",
            "tablet": "Electronics",
            "laptop": "Electronics",
            "headphones": "Electronics",
            "speaker": "Electronics",
            "camera": "Electronics",
            "watch": "Electronics",

            "shirt": "Clothing",
            "pants": "Clothing",
            "dress": "Clothing",
            "shoes": "Clothing",
            "saree": "Clothing",
            "kurti": "Clothing",
            "hoodie": "Clothing",
            "jeans": "Clothing",

            "beauty": "Beauty",
            "makeup": "Beauty",
            "skincare": "Beauty",
            "cosmetics": "Beauty",

            "book": "Books",
            "lamp": "Home",
            "chair": "Home",
            "sofa": "Home"
        }
        
        if "wedding" in query_lower:
            constraints["category"] = "Clothing"

        elif "party" in query_lower:
            constraints["category"] = "Clothing"

        elif "office" in query_lower:
            constraints["category"] = "Clothing"

        elif "gym" in query_lower:
            constraints["category"] = "Clothing"

        elif "beauty" in query_lower:
            constraints["category"] = "Beauty"

        elif "skin" in query_lower:
            constraints["category"] = "Beauty"
                
        for keyword, category in product_keywords.items():
            if keyword in query_lower:
                constraints["product_type"] = keyword
                constraints["category"] = category
                break
        
        
        skip_words = {"under", "below", "max", "upto", "up", "to", "best", "suggest", "recommend", "i", "want", "need"}
        words = [w for w in query_lower.split() if len(w) > 2 and w not in skip_words]
        constraints["search_keywords"] = words[:5]
        
        logger.info(f"Parsed query: {constraints}")
        return constraints
        
    except Exception as e:
        logger.error(f"Error parsing query: {e}")
        return {"product_type": None, "max_price": None, "min_price": 0, "category": None, "search_keywords": []}


def search_products(constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
    
    try:
        from app.database.db import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        
        query = "SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, CATEGORY, BRAND, STOCK, RATING FROM PRODUCTS WHERE 1=1"
        params = []
        
        
        if constraints.get("max_price"):
            query += " AND PRICE <= :max_price"
            params.append(("max_price", constraints["max_price"]))
        
        
        if constraints.get("category"):
            query += " AND CATEGORY = :category"
            params.append(("category", constraints["category"]))
        
        
        query += " AND STOCK > 0"
        
        
        query += " ORDER BY RATING DESC, PRICE ASC"
        
        
        query = f"SELECT * FROM ({query}) WHERE ROWNUM <= 10"
        
        
        bind_vars = {}

        for key, value in params:
            bind_vars[key] = value

        cursor.execute(query, bind_vars)
        columns = [desc[0] for desc in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        logger.info(f"Found {len(products)} products matching constraints")
        return products
        
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        return []


def generate_recommendations_openai(query: str, products: List[Dict[str, Any]]) -> str:
    
    try:
        import openai
        
        settings = get_settings()
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured, using rule-based fallback")
            return generate_recommendations_rulebased(query, products)
        
        openai.api_key = settings.openai_api_key
        
        
        products_text = "\n".join([
            f"- {p.get('PRODUCT_NAME', 'Unknown')}: ₹{p.get('PRICE', 0)} ({p.get('BRAND', 'Unknown')}, Rating: {p.get('RATING', 'N/A')})"
            for p in products[:5]
        ])
        
        prompt = f"""Based on the user's query, provide personalized product recommendations.

User Query: {query}

Available Products:
{products_text if products_text else "No products found matching the criteria"}

Provide a concise, helpful recommendation (2-3 sentences) highlighting the best products and why they match the user's needs. Be friendly and specific."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful e-commerce shopping assistant providing personalized product recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content.strip()
        logger.info("Generated OpenAI recommendations")
        return answer
        
    except (ImportError, Exception) as e:
        logger.warning(f"OpenAI recommendation failed: {e}, using rule-based fallback")
        return generate_recommendations_rulebased(query, products)


def generate_recommendations_rulebased(query: str, products: List[Dict[str, Any]]) -> str:
    
    try:
        if not products:
            return f"No products found matching '{query}'. Try searching for products in different categories or price ranges."
        
        
        top_products = products[:5]
        recommendations = []
        
        for i, product in enumerate(top_products, 1):
            name = product.get('PRODUCT_NAME', 'Product')
            price = product.get('PRICE', 0)
            brand = product.get('BRAND', 'Unknown')
            rating = product.get('RATING', 'N/A')
            stock = product.get('STOCK', 0)
            
            recommendation = f"{i}. {name} by {brand} at ₹{price:,.0f}"
            if rating and rating != 'N/A':
                recommendation += f" (Rating: {rating}/5)"
            if stock > 0:
                recommendation += f" - In stock"
            
            recommendations.append(recommendation)
        
        answer = f"Based on your query '{query}', here are our top recommendations:\n\n" + "\n".join(recommendations)
        
        if len(products) > 3:
            answer += f"\n\nWe found {len(products)} products matching your criteria. Check out the full product listing for more options."
        
        logger.info("Generated rule-based recommendations")
        return answer
        
    except Exception as e:
        logger.error(f"Error generating rule-based recommendations: {e}")
        return "I couldn't find matching products. Please try a different search query."


def shopping_assistant(query: str) -> str:
    
    try:
        
        constraints = parse_shopping_query(query)
        
        
        products = search_products(constraints)
        
        
        settings = get_settings()
        if settings.openai_api_key:
            answer = generate_recommendations_openai(query, products)
        else:
            answer = generate_recommendations_rulebased(query, products)
        
        return answer
        
    except Exception as e:
        logger.error(f"Shopping assistant error: {e}")
        return "I encountered an error processing your request. Please try again."




def rag_product_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    
    try:
        from app.database.db import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        
        query_lower = query.lower().strip()
        keywords = query_lower.split()
        
        
        scoring_conditions = []
        
        
        scoring_conditions.append(f"CASE WHEN INSTR(LOWER(PRODUCT_NAME), '{query_lower}') > 0 THEN 100 ELSE 0 END")
        
        
        for keyword in keywords:
            scoring_conditions.append(f"CASE WHEN INSTR(LOWER(PRODUCT_NAME), '{keyword}') > 0 THEN 30 ELSE 0 END")
        
        
        for keyword in keywords:
            scoring_conditions.append(f"CASE WHEN INSTR(LOWER(CATEGORY), '{keyword}') > 0 THEN 20 ELSE 0 END")
        
        
        for keyword in keywords:
            scoring_conditions.append(f"CASE WHEN INSTR(LOWER(DESCRIPTION), '{keyword}') > 0 THEN 10 ELSE 0 END")
        
        score_calc = " + ".join(scoring_conditions)
        
        search_query = f"""
            SELECT * FROM (
                SELECT 
                    PRODUCT_ID,
                    PRODUCT_NAME,
                    PRICE,
                    CATEGORY,
                    BRAND,
                    STOCK,
                    RATING,
                    ({score_calc}) as RELEVANCE_SCORE
                FROM PRODUCTS
                WHERE STOCK > 0
                    AND (
                        INSTR(LOWER(PRODUCT_NAME), '{query_lower}') > 0
                        OR INSTR(LOWER(CATEGORY), '{query_lower}') > 0
                        OR INSTR(LOWER(DESCRIPTION), '{query_lower}') > 0
                    )
                ORDER BY RELEVANCE_SCORE DESC, RATING DESC, PRICE ASC
            )
            WHERE ROWNUM <= {limit}
        """
        
        cursor.execute(search_query)
        columns = [desc[0] for desc in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        logger.info(f"RAG search for '{query}' found {len(products)} results")
        return products
        
    except Exception as e:
        logger.error(f"Error in RAG product search: {e}")
        return []


