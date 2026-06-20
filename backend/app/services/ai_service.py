from app.config import get_settings
from app.logger import get_logger
import re
from typing import List, Dict, Any, Union

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



def normalize_search_keywords(query: str) -> List[str]:
    cleaned = re.sub(r"[^a-z0-9\s]+", " ", query.lower())
    stop_words = {
        "under", "below", "max", "upto", "up", "to", "best", "suggest",
        "recommend", "i", "want", "need", "for", "the", "a", "an",
        "and", "with", "in", "on", "of", "my", "please", "me", "show",
        "search", "find", "buy", "shopping", "sale"
    }
    return [token for token in cleaned.split() if len(token) > 2 and token not in stop_words]


def parse_shopping_query(query: str) -> Dict[str, Any]:
    try:
        constraints = {
            "product_type": None,
            "max_price": None,
            "min_price": 0,
            "category": None,
            "search_keywords": [],
            "product_tokens": []  # tokens like 'shirt', 'dress' that indicate product type
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
            "tshirt": "Clothing",
            "pants": "Clothing",
            "jeans": "Clothing",
            "dress": "Clothing",
            "shoes": "Clothing",
            "sneakers": "Clothing",
            "hoodie": "Clothing",
            "kurti": "Clothing",
            "saree": "Clothing",
            "blouse": "Clothing",
            "top": "Clothing",
            "clothes": "Clothing",
            "clothing": "Clothing",
            "apparel": "Clothing",
            "outfit": "Clothing",
            "wedding": "Clothing",
            "party": "Clothing",
            "formal": "Clothing",
            "casual": "Clothing",
            "office": "Clothing",
            "gym": "Clothing",

            "beauty": "Beauty",
            "makeup": "Beauty",
            "skincare": "Beauty",
            "cosmetics": "Beauty",

            "book": "Books",
            "novel": "Books",
            "reading": "Books",
            "lamp": "Home",
            "chair": "Home",
            "sofa": "Home"
        }

        for keyword, category in product_keywords.items():
            if keyword in query_lower:
                # collect product tokens (e.g., 'shirt', 'dress') and map category
                constraints["product_tokens"].append(keyword)
                constraints["product_type"] = constraints.get("product_type") or keyword
                # prefer most specific category mapping
                constraints["category"] = constraints.get("category") or category

        # extract keywords preserving meaningful short tokens like 'black', 'formal', 'shirt'
        tokens = normalize_search_keywords(query)
        constraints["search_keywords"] = tokens

        logger.info(f"Parsed shopping query: query='{query}', category={constraints['category']}, product_tokens={constraints['product_tokens']}, keywords={constraints['search_keywords']}, max_price={constraints['max_price']}")
        return constraints

    except Exception as e:
        logger.error(f"Error parsing query: {e}")
        return {"product_type": None, "max_price": None, "min_price": 0, "category": None, "search_keywords": []}


def _build_search_query_and_params(constraints: Dict[str, Any]) -> (str, Dict[str, Any]):
    query = "SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING FROM PRODUCTS WHERE STOCK > 0"
    params: Dict[str, Any] = {}

    if constraints.get("max_price") is not None:
        query += " AND PRICE <= :max_price"
        params["max_price"] = constraints["max_price"]

    if constraints.get("min_price") is not None and constraints["min_price"] > 0:
        query += " AND PRICE >= :min_price"
        params["min_price"] = constraints["min_price"]

    category = constraints.get("category")
    if category:
        query += " AND UPPER(CATEGORY) LIKE :category"
        params["category"] = f"%{str(category).upper()}%"

    keywords = constraints.get("search_keywords", []) or []
    product_tokens = constraints.get("product_tokens", []) or []

    # If there are product_tokens (e.g., 'shirt', 'dress'), require that
    # the product_name or description contains those tokens
    mandatory_clauses = []
    for index, pt in enumerate(product_tokens):
        mk = f"mand_{index}"
        params[mk] = f"%{pt}%"
        mandatory_clauses.append(f"(LOWER(PRODUCT_NAME) LIKE LOWER(:{mk}) OR LOWER(DESCRIPTION) LIKE LOWER(:{mk}))")
    if mandatory_clauses:
        query += " AND " + " AND ".join(mandatory_clauses)

    # Build scoring clauses for keywords (name>category>brand>description)
    if keywords:
        # weights
        name_w = 100
        category_w = 50
        brand_w = 30
        desc_w = 10
        keyword_clauses = []
        for index, keyword in enumerate(keywords):
            key = f"kw_{index}"
            params[key] = f"%{keyword}%"
            keyword_clauses.extend([
                f"LOWER(PRODUCT_NAME) LIKE LOWER(:{key})",
                f"LOWER(DESCRIPTION) LIKE LOWER(:{key})",
                f"LOWER(CATEGORY) LIKE LOWER(:{key})",
                f"LOWER(BRAND) LIKE LOWER(:{key})",
            ])
        query += " AND (" + " OR ".join(keyword_clauses) + ")"

    return query, params


def _execute_search(conn, sql: str, params: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    final_sql = f"SELECT * FROM ({sql} ORDER BY RATING DESC NULLS LAST, PRICE ASC) WHERE ROWNUM <= :limit"
    params = {**params, "limit": limit}
    logger.info(f"Executing product search SQL: {final_sql} params={params}")
    cursor.execute(final_sql, params)
    columns = [desc[0] for desc in cursor.description]
    products = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return products


def search_products(constraints: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
    try:
        from app.database.db import get_connection

        conn = get_connection()

        keywords = constraints.get("search_keywords", []) or []
        product_tokens = constraints.get("product_tokens", []) or []

        # if nothing to search for, return empty
        if not keywords and not product_tokens and not constraints.get("category"):
            conn.close()
            return []

        # scoring weights
        name_w = 100
        category_w = 50
        brand_w = 30
        desc_w = 10

        params: Dict[str, Any] = {}
        scoring_parts = []
        filter_parts = []

        # full query
        full_q = ' '.join(keywords)
        if full_q:
            params['full_q'] = f"%{full_q}%"
            scoring_parts.extend([
                f"CASE WHEN LOWER(PRODUCT_NAME) LIKE LOWER(:full_q) THEN {name_w} ELSE 0 END",
                f"CASE WHEN LOWER(CATEGORY) LIKE LOWER(:full_q) THEN {category_w} ELSE 0 END",
                f"CASE WHEN LOWER(BRAND) LIKE LOWER(:full_q) THEN {brand_w} ELSE 0 END",
                f"CASE WHEN LOWER(DESCRIPTION) LIKE LOWER(:full_q) THEN {desc_w} ELSE 0 END",
            ])

        for i, kw in enumerate(keywords):
            k = f"kw_{i}"
            params[k] = f"%{kw}%"
            scoring_parts.extend([
                f"CASE WHEN LOWER(PRODUCT_NAME) LIKE LOWER(:{k}) THEN {name_w} ELSE 0 END",
                f"CASE WHEN LOWER(CATEGORY) LIKE LOWER(:{k}) THEN {category_w} ELSE 0 END",
                f"CASE WHEN LOWER(BRAND) LIKE LOWER(:{k}) THEN {brand_w} ELSE 0 END",
                f"CASE WHEN LOWER(DESCRIPTION) LIKE LOWER(:{k}) THEN {desc_w} ELSE 0 END",
            ])
            # permissive filter
            filter_parts.append(f"(LOWER(PRODUCT_NAME) LIKE LOWER(:{k}) OR LOWER(DESCRIPTION) LIKE LOWER(:{k}) OR LOWER(CATEGORY) LIKE LOWER(:{k}) OR LOWER(BRAND) LIKE LOWER(:{k}))")

        # mandatory product tokens: must be in PRODUCT_NAME or DESCRIPTION
        for j, pt in enumerate(product_tokens):
            mk = f"mand_{j}"
            params[mk] = f"%{pt}%"
            filter_parts.append(f"(LOWER(PRODUCT_NAME) LIKE LOWER(:{mk}) OR LOWER(DESCRIPTION) LIKE LOWER(:{mk}))")

        # optional category filtering
        if constraints.get('category'):
            params['cat_q'] = f"%{str(constraints.get('category')).lower()}%"
            filter_parts.append("LOWER(CATEGORY) LIKE LOWER(:cat_q)")

        if not filter_parts:
            conn.close()
            return []

        score_calc = ' + '.join(scoring_parts) if scoring_parts else '0'

        sql = (
            "SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING, (" + score_calc + ") AS RELEVANCE_SCORE "
            "FROM PRODUCTS WHERE STOCK > 0 AND (" + ' OR '.join(filter_parts) + ") "
            "ORDER BY RELEVANCE_SCORE DESC, RATING DESC NULLS LAST, PRICE ASC"
        )

        cursor = conn.cursor()
        logger.info(f"Executing scored search sql with params={params}")
        cursor.execute(f"SELECT * FROM ({sql}) WHERE ROWNUM <= :limit", {**params, 'limit': min(limit, 5)})
        cols = [d[0] for d in cursor.description]
        rows = [dict(zip(cols, r)) for r in cursor.fetchall()]
        cursor.close()
        conn.close()

        # dedupe
        seen = set()
        results = []
        for r in rows:
            pid = r.get('PRODUCT_ID')
            if pid in seen:
                continue
            seen.add(pid)
            results.append(r)

        return results[:5]

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


def shopping_assistant(query: str) -> Dict[str, Any]:
    try:
        constraints = parse_shopping_query(query)
        products = search_products(constraints, limit=10)

        if not products:
            return {
                "success": False,
                "message": "No matching products found.",
                "answer": "No matching products found.",
                "products": []
            }

        settings = get_settings()
        if settings.openai_api_key:
            answer = generate_recommendations_openai(query, products)
        else:
            answer = generate_recommendations_rulebased(query, products)

        return {
            "success": True,
            "message": "Found matching products",
            "answer": answer,
            "products": [
                {
                    "product_id": product.get("PRODUCT_ID", 0),
                    "product_name": product.get("PRODUCT_NAME", ""),
                    "price": float(product.get("PRICE", 0) or 0),
                    "category": product.get("CATEGORY", ""),
                    "brand": product.get("BRAND", ""),
                    "stock": int(product.get("STOCK", 0) or 0),
                    "rating": float(product.get("RATING", 0)) if product.get("RATING") is not None else None,
                    "image_url": product.get("IMAGE_URL", "")
                }
                for product in products
            ]
        }

    except Exception as e:
        logger.error(f"Shopping assistant error: {e}")
        return {
            "success": False,
            "message": "I encountered an error processing your request.",
            "answer": "I encountered an error processing your request. Please try again.",
            "products": []
        }


def rag_product_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    
    try:
        from app.database.db import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query_lower = query.lower().strip()
        cleaned_query = re.sub(r"[^a-z0-9\s]+", " ", query_lower)
        keywords = [word for word in cleaned_query.split() if len(word) > 2]

        params: Dict[str, Any] = {
            "full_query": f"%{query_lower}%"
        }

        scoring_conditions = [
            "CASE WHEN LOWER(PRODUCT_NAME) LIKE :full_query THEN 100 ELSE 0 END",
            "CASE WHEN LOWER(CATEGORY) LIKE :full_query THEN 80 ELSE 0 END",
            "CASE WHEN LOWER(DESCRIPTION) LIKE :full_query THEN 40 ELSE 0 END",
            "CASE WHEN LOWER(BRAND) LIKE :full_query THEN 30 ELSE 0 END"
        ]

        for index, keyword in enumerate(keywords):
            key = f"kw_{index}"
            params[key] = f"%{keyword}%"
            scoring_conditions.extend([
                f"CASE WHEN LOWER(PRODUCT_NAME) LIKE :{key} THEN 30 ELSE 0 END",
                f"CASE WHEN LOWER(CATEGORY) LIKE :{key} THEN 20 ELSE 0 END",
                f"CASE WHEN LOWER(DESCRIPTION) LIKE :{key} THEN 10 ELSE 0 END",
                f"CASE WHEN LOWER(BRAND) LIKE :{key} THEN 10 ELSE 0 END"
            ])

        score_calc = " + ".join(scoring_conditions)

        keyword_conditions = [
            "LOWER(PRODUCT_NAME) LIKE :full_query",
            "LOWER(CATEGORY) LIKE :full_query",
            "LOWER(DESCRIPTION) LIKE :full_query",
            "LOWER(BRAND) LIKE :full_query"
        ]

        for index, keyword in enumerate(keywords):
            key = f"kw_{index}"
            keyword_conditions.extend([
                f"LOWER(PRODUCT_NAME) LIKE :{key}",
                f"LOWER(CATEGORY) LIKE :{key}",
                f"LOWER(DESCRIPTION) LIKE :{key}",
                f"LOWER(BRAND) LIKE :{key}"
            ])

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
                    IMAGE_URL,
                    ({score_calc}) AS RELEVANCE_SCORE
                FROM PRODUCTS
                WHERE STOCK > 0
                    AND (
                        {' OR '.join(keyword_conditions)}
                    )
                ORDER BY RELEVANCE_SCORE DESC, RATING DESC NULLS LAST, PRICE ASC
            )
            WHERE ROWNUM <= :limit
        """

        logger.info(f"Executing RAG product search SQL for query='{query}' with params={params}")
        cursor.execute(search_query, params)
        columns = [desc[0] for desc in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        if not products:
            logger.info("RAG search returned no exact matches, searching for top products fallback")
            fallback_sql = "SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, CATEGORY, BRAND, STOCK, RATING, IMAGE_URL FROM PRODUCTS WHERE STOCK > 0 ORDER BY RATING DESC NULLS LAST, PRICE ASC"
            cursor.execute(fallback_sql)
            products = [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()[:limit]]

        cursor.close()
        conn.close()
        
        logger.info(f"RAG search for '{query}' found {len(products)} results")
        return products
        
    except Exception as e:
        logger.error(f"Error in RAG product search: {e}")
        return []

        
        cursor.close()
        conn.close()
        
        logger.info(f"RAG search for '{query}' found {len(products)} results")
        return products
        
    except Exception as e:
        logger.error(f"Error in RAG product search: {e}")
        return []


