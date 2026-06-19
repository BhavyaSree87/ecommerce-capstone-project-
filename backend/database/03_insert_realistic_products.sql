-- =============================================
-- REALISTIC PRODUCT DATA - PRODUCTION READY
-- =============================================
-- 100+ products across 7 categories with unique details
-- Images sourced from Unsplash for production quality

-- Clear existing products (optional - comment out if keeping old data)
-- DELETE FROM PRODUCTS;
-- ALTER SEQUENCE PRODUCT_SEQ RESTART START WITH 1;

-- =============================================
-- MEN'S CLOTHING & FASHION (20 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Premium Cotton Casual Shirt', 1499, 'Breathable 100% cotton casual shirt perfect for weekends and office-casual environments. Features reinforced buttons and comfortable fit.', 'Men', 'Urban Style', 45, 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Slim Fit Denim Jeans', 2299, 'Classic blue denim with a modern slim fit. Durable fabric with fade-resistant wash. Suitable for casual and semi-formal occasions.', 'Men', 'Denim Co', 38, 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Oxford White Formal Shirt', 1899, 'Premium oxford cloth formal shirt with easy-care finish. Perfect for business meetings, weddings, and formal events.', 'Men', 'ClassicFit', 52, 'https://images.unsplash.com/photo-1556821552-7f41c5d440db?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Performance Athletic T-Shirt', 999, 'Moisture-wicking athletic t-shirt designed for gym and outdoor activities. Quick-dry technology keeps you comfortable throughout your workout.', 'Men', 'FitActive', 68, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wool Blend Winter Jacket', 4999, 'Premium wool blend winter jacket with insulated lining. Water-resistant exterior protects you from rain and snow. Stylish and warm.', 'Men', 'WinterGear', 28, 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Chino Shorts', 1299, 'Comfortable chino shorts perfect for summer. Soft fabric with a regular fit. Available in multiple neutral colors.', 'Men', 'ComfortWear', 41, 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Striped Polo Shirt', 1599, 'Classic striped polo shirt with three-button placket. Crafted from soft pique cotton for a polished look.', 'Men', 'PoloStyle', 55, 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Cargo Pants with Multiple Pockets', 2199, 'Durable cargo pants with functional pockets. Perfect for outdoor adventures and casual wear. Made from sturdy cotton blend.', 'Men', 'AdventureGear', 34, 'https://images.unsplash.com/photo-1473080169318-2edd8b1971e2?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Henley Neck Long Sleeve', 1399, 'Versatile henley neck long sleeve shirt. Great for layering or wearing alone. Comfortable and stylish for everyday wear.', 'Men', 'LayerLook', 47, 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500&h=500&fit=crop', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Printed Graphic T-Shirt', 799, 'Trendy graphic t-shirt with unique designs. Made from soft cotton for maximum comfort. Perfect for casual outings.', 'Men', 'GraphicTees', 72, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Linen Summer Shirt', 1699, 'Lightweight linen shirt perfect for summer holidays. Breathable and comfortable in hot weather. Effortless casual style.', 'Men', 'SummerEssentials', 43, 'https://images.unsplash.com/photo-1598033129519-e7f46c3ca4d4?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Slim Fit Blazer', 5999, 'Sophisticated slim fit blazer for formal occasions. Premium fabric with expert tailoring. Perfect for interviews and events.', 'Men', 'FormalWear', 22, 'https://images.unsplash.com/photo-1591047990016-5ec41fef8f00?w=500&h=500&fit=crop', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Crew Neck Sweatshirt', 2299, 'Cozy crew neck sweatshirt perfect for layering. Soft fleece interior provides warmth without bulk. Available in various colors.', 'Men', 'CozyWear', 36, 'https://images.unsplash.com/photo-1556821552-7f41c5d440db?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Slim Fit Trousers', 2699, 'Classic slim fit trousers in neutral colors. Ideal for business casual and formal wear. Premium fabric with excellent drape.', 'Men', 'TrouserPro', 31, 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Bomber Jacket', 3799, 'Stylish bomber jacket with modern design. Perfect for layering or wearing solo. Quality construction ensures durability.', 'Men', 'UrbanStyle', 26, 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'V-Neck Sweater', 2199, 'Classic v-neck sweater in premium wool blend. Versatile and timeless piece for your wardrobe. Comfortable and stylish.', 'Men', 'ClassicKnits', 39, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Distressed Slim Jeans', 2499, 'Trendy distressed slim jeans with ripped details. Perfect for casual streetwear look. Premium denim quality.', 'Men', 'TrendSetters', 33, 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Reversible Down Jacket', 6999, 'Premium reversible down jacket with water-resistant shell. Lightweight yet incredibly warm. Perfect for cold seasons.', 'Men', 'Premium Gear', 18, 'https://images.unsplash.com/photo-1552752091-8da1bfbd7c9b?w=500&h=500&fit=crop', 4.7);

-- =============================================
-- WOMEN'S CLOTHING & FASHION (20 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Floral Summer Dress', 2499, 'Elegant floral print summer dress with comfortable fit. Perfect for brunches, dates, and casual gatherings. Breathable fabric.', 'Women', 'Elle & Co', 54, 'https://images.unsplash.com/photo-1595777707802-c5c0cdde9e13?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'White Linen Blouse', 1799, 'Fresh white linen blouse perfect for warm weather. Can be styled with jeans or skirts. Quality construction.', 'Women', 'ClassicBlouse', 48, 'https://images.unsplash.com/photo-1551314679-9c6ae9dec224?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Black Slim Fit Jeans', 2299, 'Timeless black slim fit jeans that pair with everything. Premium denim with perfect stretch. A wardrobe staple.', 'Women', 'DenimClassics', 61, 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Pleated Midi Skirt', 2899, 'Sophisticated pleated midi skirt for work and weekend wear. Flattering cut with breathable fabric. Available in neutral colors.', 'Women', 'SkirtStyle', 38, 'https://images.unsplash.com/photo-1580541831066-7aae4d3f744e?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Cropped Denim Jacket', 2699, 'Trendy cropped denim jacket perfect for layering. Versatile piece that works with dresses and pants. Quality fabric.', 'Women', 'DenimTrend', 42, 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Cotton T-Shirt', 899, 'Soft comfortable cotton t-shirt perfect for everyday wear. Available in multiple colors. Simple yet stylish design.', 'Women', 'BasicTees', 89, 'https://images.unsplash.com/photo-1505252585461-04db1267ae5b?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wrap Around Cardigan', 2199, 'Elegant wrap cardigan perfect for layering. Soft fabric drapes beautifully. Can be dressed up or down with ease.', 'Women', 'LayerStyle', 35, 'https://images.unsplash.com/photo-1551314679-9c6ae9dec224?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'High Waist Skinny Jeans', 2599, 'Flattering high waist skinny jeans in dark blue. Comfortable fit with excellent shape retention. Perfect for any occasion.', 'Women', 'DenimPro', 44, 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Printed Casual Shorts', 1499, 'Comfortable printed shorts perfect for summer. Soft fabric with quality construction. Great for casual outings.', 'Women', 'SummerWear', 56, 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Striped Sweater', 1899, 'Classic striped sweater in nautical style. Versatile piece for casual and semi-formal wear. Comfortable and timeless.', 'Women', 'ClassicStyle', 41, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Maxi Dress Elegant', 3499, 'Stunning elegant maxi dress perfect for parties and events. Flowing fabric with beautiful drape. Sophisticated design.', 'Women', 'Elegance', 28, 'https://images.unsplash.com/photo-1595777707802-c5c0cdde9e13?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Oversized Blazer', 3899, 'Trendy oversized blazer perfect for modern style. Versatile piece for work and casual wear. Premium tailoring.', 'Women', 'ModernStyle', 32, 'https://images.unsplash.com/photo-1591047990016-5ec41fef8f00?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Tie-Dye T-Shirt', 1099, 'Colorful tie-dye t-shirt for casual cool look. 100% cotton with vibrant colors. Perfect for weekend outings.', 'Women', 'TieDyeTrend', 63, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Yoga Leggings', 1799, 'Comfortable yoga leggings with high waist. Perfect for workouts and casual wear. Moisture-wicking fabric.', 'Women', 'FitLife', 52, 'https://images.unsplash.com/photo-1506629082632-401f5e31e9e8?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Denim Jacket Vintage', 2899, 'Classic vintage style denim jacket. Timeless piece that never goes out of style. Quality construction.', 'Women', 'Vintage Style', 37, 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Leather Pants', 4599, 'Chic black leather pants for sophisticated look. Premium quality leather. Perfect for parties and special occasions.', 'Women', 'PremiumStyle', 19, 'https://images.unsplash.com/photo-1564854015560-96bd42099a9e?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Off-Shoulder Top', 1699, 'Trendy off-shoulder top perfect for casual dates. Comfortable fit with modern style. Great for warm weather.', 'Women', 'TrendyWear', 48, 'https://images.unsplash.com/photo-1595777707802-c5c0cdde9e13?w=500&h=500&fit=crop', 4.2);

-- =============================================
-- KIDS' CLOTHING (15 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Cartoon Print T-Shirt Kids', 599, 'Fun cartoon print t-shirt for kids. Soft comfortable cotton. Perfect for daily wear and play.', 'Kids', 'KidsStyle', 78, 'https://images.unsplash.com/photo-1503784444102-40cb628cb857?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Colorful Kids Shorts', 799, 'Comfortable colorful shorts for kids. Durable fabric perfect for active play. Available in multiple colors.', 'Kids', 'PlayTime', 67, 'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Denim Overall Dress', 1299, 'Cute denim overall dress for girls. Classic style with modern comfort. Perfect for casual outings.', 'Kids', 'KidsClassic', 44, 'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Animal Print Leggings', 899, 'Fun animal print leggings for kids. Stretchy comfortable fabric. Perfect for active kids.', 'Kids', 'PlayfulStyle', 55, 'https://images.unsplash.com/photo-1506629082632-401f5e31e9e8?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Striped Kids Sweater', 1099, 'Cozy striped sweater for kids. Soft fabric perfect for chilly days. Easy to care for.', 'Kids', 'CozyKids', 38, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Blue Denim Jacket Kids', 1399, 'Classic blue denim jacket for kids. Durable and stylish. Perfect for layering.', 'Kids', 'KidsWear', 41, 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Graphic Print Hoodie', 1599, 'Trendy graphic print hoodie for kids. Warm and comfortable. Perfect for casual wear.', 'Kids', 'GraphicKids', 34, 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Pink Casual Dress', 1199, 'Adorable pink casual dress for girls. Comfortable fit perfect for playdates. Quality fabric.', 'Kids', 'PrettyKids', 48, 'https://images.unsplash.com/photo-1595777707802-c5c0cdde9e13?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Dinosaur Print T-Shirt', 649, 'Fun dinosaur print t-shirt for boys. Soft cotton fabric. Perfect for daily wear.', 'Kids', 'DinoKids', 72, 'https://images.unsplash.com/photo-1503784444102-40cb628cb857?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Winter Puffer Jacket', 2299, 'Warm winter puffer jacket for kids. Lightweight yet insulated. Perfect for cold weather.', 'Kids', 'WinterKids', 26, 'https://images.unsplash.com/photo-1552752091-8da1bfbd7c9b?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Plaid Dress Shirt', 999, 'Classic plaid dress shirt for kids. Perfect for formal occasions. Quality fabric.', 'Kids', 'FormalKids', 35, 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Colorful Swim Shorts', 799, 'Vibrant colorful swim shorts for kids. Quick-dry fabric. Perfect for pool and beach.', 'Kids', 'BeachKids', 53, 'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=500&h=500&fit=crop', 4.3);

-- =============================================
-- FOOTWEAR (20 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Running Shoes Pro', 3999, 'Professional running shoes with responsive cushioning and excellent grip. Perfect for daily runs and training. Lightweight design.', 'Footwear', 'RunnerX', 42, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Basketball Sneakers', 4499, 'High-performance basketball sneakers with ankle support. Perfect for court play. Durable construction.', 'Footwear', 'CourtMaster', 28, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Sneakers White', 2299, 'Classic white casual sneakers versatile for any outfit. Comfortable fit perfect for daily wear. Quality construction.', 'Footwear', 'ClassicSteps', 67, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Formal Leather Shoes', 3599, 'Elegant formal leather shoes perfect for business and events. Premium quality leather with excellent craftsmanship.', 'Footwear', 'FormalFeet', 35, 'https://images.unsplash.com/photo-1608878551803-9a27a15565fa?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Loafers', 2899, 'Comfortable casual loafers perfect for office and casual outings. Easy to wear and maintain. Stylish design.', 'Footwear', 'ComfortSteps', 44, 'https://images.unsplash.com/photo-1608878551803-9a27a15565fa?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Gym Training Shoes', 2899, 'Specialized gym training shoes with flat sole for stability. Perfect for weightlifting and training. Durable rubber sole.', 'Footwear', 'TrainMax', 38, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Canvas Slip-Ons', 1599, 'Casual canvas slip-on shoes perfect for everyday wear. Easy to put on and take off. Comfortable and breathable.', 'Footwear', 'SlipStyle', 56, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Hiking Boots', 4999, 'Rugged hiking boots with excellent traction and ankle support. Perfect for outdoor adventures. Waterproof design.', 'Footwear', 'TrailBlazer', 24, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Sandals', 999, 'Comfortable casual sandals perfect for summer. Soft footbed provides all-day comfort. Lightweight design.', 'Footwear', 'SummerSteps', 71, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Oxford Dress Shoes', 3999, 'Classic Oxford dress shoes for formal occasions. Premium leather construction. Timeless design.', 'Footwear', 'ClassicFormal', 32, 'https://images.unsplash.com/photo-1608878551803-9a27a15565fa?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Sporty Flip Flops', 699, 'Comfortable sporty flip flops with cushioned sole. Perfect for casual beach wear. Durable material.', 'Footwear', 'BeachVibes', 89, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 3.9);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Winter Snow Boots', 5299, 'Insulated winter snow boots for extreme cold. Waterproof and warm. Perfect for snowy climates.', 'Footwear', 'FrostGuard', 18, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Cross-Training Shoes', 3299, 'Versatile cross-training shoes for gym and casual wear. Cushioned sole for comfort and support.', 'Footwear', 'CrossFit', 41, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Boat Shoes', 2499, 'Classic boat shoes perfect for casual summer style. Slip-resistant sole. Quality construction.', 'Footwear', 'NauticalStyle', 37, 'https://images.unsplash.com/photo-1608878551803-9a27a15565fa?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Platform Heels', 2999, 'Trendy platform heels perfect for parties. Comfortable with sturdy heel. Stylish design.', 'Footwear', 'HeelStyle', 28, 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop', 4.4);

-- =============================================
-- ACCESSORIES (20 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Stainless Steel Watch', 4999, 'Premium stainless steel watch with chronograph function. Water-resistant and durable. Timeless design for any occasion.', 'Accessories', 'TimeKeeper', 31, 'https://images.unsplash.com/photo-1516128748890-31d71b38bda1?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Leather Crossbody Bag', 3499, 'Elegant leather crossbody bag perfect for daily use. Premium quality leather with adjustable strap. Spacious interior.', 'Accessories', 'BagStyle', 26, 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Canvas Backpack', 2299, 'Durable canvas backpack perfect for travel and daily use. Multiple compartments for organization. Comfortable straps.', 'Accessories', 'BackpackPro', 44, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Silk Scarf Premium', 1599, 'Luxurious silk scarf with elegant patterns. Perfect for layering or wrapping. High-quality material.', 'Accessories', 'ScarfStyle', 52, 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Baseball Cap Classic', 799, 'Classic baseball cap perfect for casual wear. Adjustable strap for comfortable fit. Multiple color options.', 'Accessories', 'CapStyle', 76, 'https://images.unsplash.com/photo-1515451141207-776bdad60908?w=500&h=500&fit=crop', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Sunglasses UV Protection', 1999, 'Stylish sunglasses with 100% UV protection. Comfortable frames perfect for sunny days. Quality lenses.', 'Accessories', 'SunStyle', 48, 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Leather Wallet', 1299, 'Premium leather wallet with multiple card slots. RFID protection for security. Durable and stylish.', 'Accessories', 'WalletStyle', 57, 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Pearl Necklace', 2499, 'Elegant pearl necklace perfect for formal events. Quality pearls with secure clasp. Timeless accessory.', 'Accessories', 'JewelStyle', 22, 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Diamond Earrings', 3999, 'Stunning diamond earrings for special occasions. 18k gold setting. Premium quality gemstones.', 'Accessories', 'DiamondStyle', 15, 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Leather Belt', 999, 'Classic leather belt perfect for formal and casual wear. Durable buckle. High-quality material.', 'Accessories', 'BeltStyle', 62, 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Beanie Winter Hat', 699, 'Cozy beanie perfect for cold weather. Soft knit material. Available in multiple colors.', 'Accessories', 'WinterStyle', 81, 'https://images.unsplash.com/photo-1515451141207-776bdad60908?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Gold Bangle Set', 2199, 'Elegant gold bangle set for festive occasions. Quality gold-plated design. Perfect for celebrations.', 'Accessories', 'BangleStyle', 34, 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Pocket Square', 449, 'Stylish pocket square for formal occasions. Quality fabric. Perfect accessory detail.', 'Accessories', 'FormalStyle', 48, 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Trendy Phone Case', 599, 'Protective trendy phone case with stylish design. Durable material protects your phone. Various colors available.', 'Accessories', 'PhoneStyle', 95, 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=500&fit=crop', 4.1);

-- =============================================
-- BEAUTY & PERSONAL CARE (15 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Organic Face Serum', 1899, 'Premium organic face serum with natural ingredients. Perfect for all skin types. Nourishing and hydrating formula.', 'Beauty', 'NaturalGlow', 38, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Moisturizing Face Cream', 1599, 'Rich moisturizing cream for dry skin. With retinol and vitamin C. Smooth and radiant skin in days.', 'Beauty', 'SkinCare Pro', 45, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Lipstick Matte Finish', 799, 'Long-lasting lipstick with matte finish. Multiple trendy colors. Comfortable and hydrating formula.', 'Beauty', 'ColorLips', 72, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Hair Shampoo Premium', 599, 'Premium hair shampoo for all hair types. Sulfate-free gentle formula. Leaves hair shiny and healthy.', 'Beauty', 'HairCare', 89, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Conditioning Hair Mask', 899, 'Deep conditioning hair mask for dry and damaged hair. Nourishing formula restores shine. Weekly treatment.', 'Beauty', 'HairRevive', 56, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Eyeshadow Palette', 1299, 'Stunning eyeshadow palette with 12 colors. Pigmented and blendable. Perfect for any occasion.', 'Beauty', 'ColorEyes', 42, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Foundation Liquid', 1399, 'Long-lasting liquid foundation with full coverage. Buildable formula. Matches all skin tones beautifully.', 'Beauty', 'FaceStyle', 51, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Mascara Volumizing', 699, 'Volumizing mascara for dramatic lashes. Waterproof formula. Long-lasting and smudge-proof.', 'Beauty', 'LashPerfect', 68, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Sunscreen SPF 50', 899, 'Lightweight sunscreen with SPF 50 protection. Non-greasy formula. Protects skin from UV damage.', 'Beauty', 'SunProtect', 74, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Face Cleanser Gel', 549, 'Gentle face cleanser gel for daily use. Removes dirt and makeup. Suitable for sensitive skin.', 'Beauty', 'CleanFace', 85, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Nail Polish Set', 899, 'Beautiful nail polish set with 5 trendy colors. Long-lasting formula. Quick-drying technology.', 'Beauty', 'NailStyle', 58, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Blush Powder', 699, 'Soft blush powder for natural rosy cheeks. Blendable formula. Available in multiple shades.', 'Beauty', 'BlushPerfect', 65, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop', 4.3);

-- =============================================
-- ELECTRONICS (15 products)
-- =============================================

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wireless Bluetooth Headphones', 2999, 'Premium wireless bluetooth headphones with noise cancellation. 30-hour battery life. Crystal clear sound quality.', 'Electronics', 'SoundMax', 31, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'USB-C Fast Charger', 999, 'Fast USB-C charger for phones and tablets. 65W power output. Universal compatibility.', 'Electronics', 'ChargeMax', 87, 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Portable Phone Charger', 1599, 'Compact portable phone charger with 20000mAh capacity. Fast charging support. Multiple devices charging.', 'Electronics', 'PowerBank', 54, 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Screen Protector', 399, 'Premium tempered glass screen protector for smartphones. Anti-glare coating. Easy installation.', 'Electronics', 'ScreenSafe', 156, 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Phone Stand', 499, 'Adjustable phone stand for desk. Non-slip base. Compatible with all phone sizes.', 'Electronics', 'PhoneStand', 102, 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=500&fit=crop', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'HDMI Cable Premium', 699, 'High-speed HDMI cable for 4K video. 3-meter length. Gold-plated connectors.', 'Electronics', 'CableMax', 78, 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=500&fit=crop', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wireless Keyboard Mouse', 1999, 'Wireless keyboard and mouse combo for productivity. Quiet keys. Long battery life.', 'Electronics', 'TechCombo', 42, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'USB Hub 7-Port', 1299, 'USB hub with 7 ports for expanding connectivity. High-speed data transfer. Power adapter included.', 'Electronics', 'HubPro', 35, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Webcam 1080p', 1899, 'Full HD webcam for video calls and streaming. Auto-focus technology. Built-in microphone.', 'Electronics', 'WebVision', 48, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Laptop Stand', 1699, 'Ergonomic laptop stand for better posture. Adjustable height and angle. Supports all laptop sizes.', 'Electronics', 'ErgoLift', 39, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Portable External SSD', 4999, 'Fast portable external SSD with 1TB capacity. USB 3.1 interface. Compact and lightweight design.', 'Electronics', 'StorageMax', 28, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Tablet Stand', 899, 'Sturdy tablet stand for hands-free viewing. Adjustable angles. Non-slip base.', 'Electronics', 'TabletStand', 52, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING) 
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wireless Charging Pad', 1299, 'Fast wireless charging pad compatible with all qi-enabled devices. Non-slip surface. Compact design.', 'Electronics', 'ChargePad', 44, 'https://images.unsplash.com/photo-1587829191301-dc798b83add3?w=500&h=500&fit=crop', 4.3);

-- =============================================
-- COMMIT CHANGES
-- =============================================
COMMIT;

-- =============================================
-- VERIFICATION QUERY
-- =============================================
-- Run this to verify all products were inserted:
-- SELECT COUNT(*) as TOTAL_PRODUCTS FROM PRODUCTS;
-- SELECT DISTINCT CATEGORY, COUNT(*) as COUNT FROM PRODUCTS GROUP BY CATEGORY;
