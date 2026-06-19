-- =============================================
-- Replace dummy products with realistic catalog
-- File: 04_replace_dummy_with_realistic_products.sql
-- Actions:
-- 1) Delete dummy products whose names contain Shirt / Wear / Dress / Product
-- 2) Insert 80 realistic product records across categories
-- Note: Uses PRODUCT_SEQ for PRODUCT_ID
-- =============================================
SET DEFINE OFF;
-- Remove dummy entries (match anywhere in the name)
DELETE FROM PRODUCTS
WHERE PRODUCT_NAME LIKE '%Shirt %'
   OR PRODUCT_NAME LIKE '%Wear %'
   OR PRODUCT_NAME LIKE '%Dress %'
   OR PRODUCT_NAME LIKE '%Product %';

-- =============================================
-- INSERT REALISTIC PRODUCTS (80 rows)
-- =============================================

-- MEN (12)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Levi''s Slim Fit Jeans', 2599, 'Classic Levi''s slim fit jeans in deep indigo with stretch for comfort and durability.', 'Men', 'Levi''s', 120, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Tommy Hilfiger Polo T-Shirt', 1999, 'Premium cotton polo shirt with embroidered logo and breathable fabric for all-day comfort.', 'Men', 'Tommy Hilfiger', 95, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Nike Sports Jacket', 4999, 'Lightweight windproof sports jacket with Dri-FIT lining, ideal for training and city wear.', 'Men', 'Nike', 78, 'https://images.unsplash.com/photo-1544441892-3bada8eaf572?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Allen Solly Formal Shirt', 1899, 'Tailored formal shirt with easy-iron fabric and reinforced stitching for a neat office look.', 'Men', 'Allen Solly', 84, 'https://images.unsplash.com/photo-1516257967857-c0f6c4e2b910?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Peter England Casual Shirt', 1599, 'Casual button-down shirt with soft cotton blend and relaxed fit for everyday wear.', 'Men', 'Peter England', 102, 'https://images.unsplash.com/photo-1589902281671-b90b27ad1d4b?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Men''s Classic Chino Trousers', 2199, 'Versatile chino trousers with a slim cut, comfortable stretch, and reinforced pockets.', 'Men', 'Urban Basics', 76, 'https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Merino Wool V-Neck Sweater', 2999, 'Soft merino wool sweater with fine knit and breathable warmth for cool seasons.', 'Men', 'WoolWorth', 64, 'https://images.unsplash.com/photo-1551516679-9c6ae9dec224?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Performance Training Tee', 999, 'Breathable performance tee with sweat-wicking fabric and flatlock seams for comfort.', 'Men', 'ActivePro', 140, 'https://images.unsplash.com/photo-1523170335684-f042b4ef1176?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Stretch Hoodie', 1899, 'Comfort-fit hoodie with brushed interior and stretch rib cuffs for relaxed everyday wear.', 'Men', 'CozyWear', 110, 'https://images.unsplash.com/photo-1556821552-7f41c5d440db?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Executive Blazer Slim Fit', 5999, 'Structured slim-fit blazer with lining and premium stitching for business occasions.', 'Men', 'TailorMade', 34, 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=500&h=500&fit=crop&auto=format&q=80', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Everyday Breathable Socks (3-Pack)', 599, 'Soft combed-cotton socks with reinforced toes and arch support, sold in value 3-packs.', 'Men', 'FootComfort', 220, 'https://images.unsplash.com/photo-1556821552-7f41c5d440be?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Classic Leather Belt', 899, 'Full-grain leather belt with metal buckle; durable and suitable for formal and casual outfits.', 'Men', 'LeatherCraft', 150, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

-- WOMEN (12)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Floral Summer Dress', 2499, 'Lightweight floral summer dress with a flattering A-line cut and breathable cotton blend.', 'Women', 'Elle & Co', 96, 'https://images.unsplash.com/photo-1595777707802-221b5c17d883?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Elegant Cotton Kurti', 1899, 'Traditional cotton kurti with hand-stitched detailing and comfortable side slits for mobility.', 'Women', 'House of Kurta', 84, 'https://images.unsplash.com/photo-1584622181563-430f63602d4b?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Sequined Party Gown', 7999, 'Glamorous sequined party gown with fitted bodice and flowing skirt for formal occasions.', 'Women', 'GlamourWear', 26, 'https://images.unsplash.com/photo-1559639130-2d1d2e8cf5c0?w=500&h=500&fit=crop&auto=format&q=80', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual V-Neck Top', 1099, 'Soft casual V-neck top in breathable modal fabric; great for layering or solo wear.', 'Women', 'Everyday Chic', 132, 'https://images.unsplash.com/photo-1506529082632-42d441a24dc1?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Designer Silk Saree', 12999, 'Handwoven designer silk saree with intricate motifs and a luxurious sheen for celebrations.', 'Women', 'SareeCraft', 18, 'https://images.unsplash.com/photo-1593391969376-76d46edbb96f?w=500&h=500&fit=crop&auto=format&q=80', 4.9);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Pleated Midi Skirt', 2299, 'Elegant pleated midi skirt with soft lining and comfortable waistband for all-day wear.', 'Women', 'SkirtStyle', 72, 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Denim Jacket Women''s', 2899, 'Cropped denim jacket with vintage wash and secure button closures; versatile layering piece.', 'Women', 'DenimTrend', 58, 'https://images.unsplash.com/photo-1601273832048-dbc41f5d55c9?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'High Waist Trousers', 2799, 'Tailored high waist trousers with crease and stretch for comfort; perfect for office wear.', 'Women', 'TailorMade', 64, 'https://images.unsplash.com/photo-1531331271006-66dd51b1a9f0?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Silk Blend Scarf', 999, 'Light silk-blend scarf with printed pattern; a refined accessory to complement outfits.', 'Women', 'ScarfStyle', 112, 'https://images.unsplash.com/photo-1578986169035-a1d1bb6f2acb?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Breathable Yoga Leggings', 1799, 'High-performance leggings with moisture-wicking fabric and four-way stretch for workouts.', 'Women', 'FitLife', 90, 'https://images.unsplash.com/photo-1506629082632-42d441a24dc1?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Casual Knit Cardigan', 1999, 'Soft knit cardigan with button front and cozy fit; perfect for layering in cooler months.', 'Women', 'CozyWear', 76, 'https://images.unsplash.com/photo-1551551033-9f0b0e67e2a9?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Floral Wrap Dress', 2699, 'Wrap dress with floral print and adjustable tie waist for flattering fit and comfort.', 'Women', 'Flora', 68, 'https://images.unsplash.com/photo-1517457373614-b7152f800fd1?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

-- KIDS (8)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Boys Denim Jacket', 1599, 'Durable boys denim jacket with soft lining and reinforced seams for rough play.', 'Kids', 'KidsDenim', 88, 'https://images.unsplash.com/photo-1516866118175-c7e88d73b30f?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Cartoon Print T-Shirt', 599, 'Fun cartoon-print t-shirt in soft cotton, designed for comfort and play.', 'Kids', 'PlayTime', 160, 'https://images.unsplash.com/photo-1519238263413-b37ecc67ce63?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'School Uniform Set', 1299, 'Complete school uniform set including tailored shirt and trousers with durable stitching.', 'Kids', 'SchoolWear', 140, 'https://images.unsplash.com/photo-1540545551555-c8fcc7b5b5a1?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Kids Hoodie', 899, 'Warm kids hoodie with soft fleece interior and zipper fastening for easy wear.', 'Kids', 'CozyKids', 130, 'https://images.unsplash.com/photo-1555862519-38183346fd5f?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Winter Sweater Kids', 1099, 'Knitted winter sweater with ribbed cuffs and a cosy fit for chilly days.', 'Kids', 'WarmLittleOnes', 92, 'https://images.unsplash.com/photo-1527804050bfd-7aae4cba89c0?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Girls Floral Skort', 899, 'Comfortable floral skort with soft lining and elastic waistband for active kids.', 'Kids', 'KidsStyle', 110, 'https://images.unsplash.com/photo-1512941691920-25bda36dc643?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Toddler Cotton Romper', 699, 'Soft cotton romper for toddlers with snap closures for easy changing.', 'Kids', 'TinyTogs', 125, 'https://images.unsplash.com/photo-1515488846660-610b2d5ef89f?w=500&h=500&fit=crop&auto=format&q=80', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Kids Raincoat Waterproof', 1199, 'Waterproof kids raincoat with hood and reflective trims for safety in wet weather.', 'Kids', 'RainSafe', 78, 'https://images.unsplash.com/photo-1560807707-ca5ef45ab223?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

-- FOOTWEAR (14)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Nike Air Max', 6999, 'Iconic Nike Air Max with visible air cushioning, delivering comfort and style for daily wear.', 'Footwear', 'Nike', 64, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop&auto=format&q=80', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Adidas Ultraboost', 7499, 'Energy-returning midsole and Primeknit upper for a snug and responsive running experience.', 'Footwear', 'Adidas', 54, 'https://images.unsplash.com/photo-1597466765990-64ad1c35dafc?w=500&h=500&fit=crop&auto=format&q=80', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Puma Running Shoes', 3999, 'Lightweight running shoes with breathable mesh and responsive foam cushioning.', 'Footwear', 'Puma', 88, 'https://images.unsplash.com/photo-1507503207453-18ef0d55dd9d?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Woodland Boots', 4999, 'Rugged leather boots with durable grip and water-resistant finish for trekking and work.', 'Footwear', 'Woodland', 42, 'https://images.unsplash.com/photo-1608787698152-1ce6e3c3a644?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Skechers Go Walk', 2999, 'Comfort-first walking shoe with lightweight sole and responsive cushioning for long wear.', 'Footwear', 'Skechers', 96, 'https://images.unsplash.com/photo-1549298881-c1bc9c60a63b?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Leather Oxford Formal Shoes', 4399, 'Polished leather Oxford shoes with breathable lining and cushioned insole for formal comfort.', 'Footwear', 'FormalFeet', 38, 'https://images.unsplash.com/photo-1543163521-9733539c2d30?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Canvas Slip-On Sneakers', 1699, 'Easy slip-on canvas sneakers with rubber sole and casual silhouette for everyday use.', 'Footwear', 'SlipStyle', 132, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Trail Running Shoes', 4599, 'Aggressive outsole and protective upper for comfortable trail running on varied terrain.', 'Footwear', 'TrailBlazer', 46, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Women''s Ballet Flats', 1599, 'Soft leather ballet flats with padded footbed and slip-resistant sole for everyday elegance.', 'Footwear', 'ComfortSteps', 88, 'https://images.unsplash.com/photo-1554055872-e71b99a8f21c?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Kids Lightweight Sandals', 899, 'Cushioned sandals with adjustable straps and flexible sole designed for children.', 'Footwear', 'KidsFeet', 120, 'https://images.unsplash.com/photo-1519869325930-281384150665?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Slip Resistant Work Shoes', 3299, 'Durable work shoes with slip-resistant tread and reinforced toe for industrial environments.', 'Footwear', 'WorkSafe', 56, 'https://images.unsplash.com/photo-1551107696-a4b0c5a0c6f5?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Platform Heels Stylish', 3299, 'Stylish platform heels with padded insole and sturdy block heel for evening wear.', 'Footwear', 'HeelStyle', 34, 'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Running Spike Shoes', 4999, 'Competition spikes with lightweight plate and aggressive traction for track athletes.', 'Footwear', 'SpeedPro', 22, 'https://images.unsplash.com/photo-1507503207453-18ef0d55dd9d?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

-- ACCESSORIES (10)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Fossil Leather Watch', 6999, 'Classic Fossil leather-strapped watch with stainless case, mineral crystal, and chronograph.', 'Accessories', 'Fossil', 48, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&auto=format&q=80', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'RayBan Aviator Sunglasses', 4999, 'Iconic RayBan aviator sunglasses with polarized lenses and lightweight metal frame.', 'Accessories', 'RayBan', 52, 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&h=500&fit=crop&auto=format&q=80', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Genuine Leather Wallet', 1299, 'Compact genuine leather wallet with multiple card slots and RFID protection.', 'Accessories', 'LeatherCraft', 140, 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Travel Backpack 30L', 3999, 'Durable 30L travel backpack with padded laptop sleeve, water-resistant fabric, and organizational pockets.', 'Accessories', 'TravelPro', 62, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Smart Watch Series 6', 15999, 'Feature-rich smart watch with fitness tracking, heart-rate monitor, and multi-day battery life.', 'Accessories', 'SmartTech', 38, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&auto=format&q=80', 4.6);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Travel Adapter Universal', 499, 'Universal travel adapter with multi-plug support and surge protection for international trips.', 'Accessories', 'PlugIt', 200, 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Leather Card Holder', 699, 'Slim leather card holder with two quick-access slots and premium stitching.', 'Accessories', 'WalletStyle', 180, 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500&h=500&fit=crop&auto=format&q=80', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Designer Keychain', 399, 'Metal designer keychain with enamel finish; a small accessory with premium feel.', 'Accessories', 'KeyCraft', 240, 'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Travel Toiletry Kit', 1299, 'Compact toiletry kit with durable compartments and water-resistant lining for organized travel.', 'Accessories', 'TravelKit', 90, 'https://images.unsplash.com/photo-1556073361-aeb0455f7efd?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Premium Sunglasses Case', 499, 'Hard-shell sunglasses case with soft interior lining and secure zipper closure.', 'Accessories', 'CaseGuard', 150, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

-- BEAUTY & PERSONAL CARE (12)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Lakme Liquid Foundation', 999, 'Lightweight liquid foundation with buildable coverage and natural finish for all-day wear.', 'Beauty', 'Lakme', 180, 'https://images.unsplash.com/photo-1596786477185-4875e92cc0d6?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Maybelline Matte Lipstick', 599, 'Long-wear matte lipstick with smooth application and rich pigment in trending shades.', 'Beauty', 'Maybelline', 240, 'https://images.unsplash.com/photo-1595777707802-221b5c17d883?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Mamaearth Face Wash', 349, 'Gentle face wash with natural extracts and no harsh sulfates, suitable for daily cleansing.', 'Beauty', 'Mamaearth', 260, 'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Dove Nourishing Shampoo', 399, 'Nourishing shampoo with mild surfactants and moisturizing formula for healthier-looking hair.', 'Beauty', 'Dove', 320, 'https://images.unsplash.com/photo-1556073361-aeb0455f7efd?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Nivea Moisturizer Cream', 349, 'Lightweight daily moisturizer with SPF protection and nourishing ingredients for soft skin.', 'Beauty', 'Nivea', 300, 'https://images.unsplash.com/photo-1611080626919-abc8286d933d?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Vitamin C Serum', 1299, 'High potency vitamin C serum formulated to brighten skin and reduce pigmentation with daily use.', 'Beauty', 'GlowLabs', 140, 'https://images.unsplash.com/photo-1608248543803-ba4f8a70ae0b?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Retinol Night Cream', 1699, 'Overnight retinol cream to support skin renewal and smoother texture; dermatologist-tested.', 'Beauty', 'Dermalux', 98, 'https://images.unsplash.com/photo-1578926314433-8b3cefdf2f53?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Hydrating Face Mask', 499, 'Intensive hydrating sheet mask with hyaluronic acid for instant moisturization.', 'Beauty', 'MaskIt', 210, 'https://images.unsplash.com/photo-1611080626919-abc8286d933d?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'SPF 50 Sunscreen Gel', 699, 'Non-greasy SPF 50 gel sunscreen with broad-spectrum protection and quick absorption.', 'Beauty', 'SunShield', 220, 'https://images.unsplash.com/photo-1556073361-aeb0455f7efd?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Nail Polish Set (4 colors)', 699, 'Long-wear quick-dry nail polish set featuring four curated seasonal shades.', 'Beauty', 'NailStyle', 150, 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=500&h=500&fit=crop&auto=format&q=80', 4.0);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Gentle Baby Shampoo', 349, 'Tear-free gentle baby shampoo formulated for sensitive skin and daily use.', 'Beauty', 'BabyCare', 180, 'https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

-- ELECTRONICS (12)
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Apple iPhone 15 128GB', 79999, 'Latest Apple iPhone 15 with A-series chipset, 128GB storage, 48MP camera, and OLED display.', 'Electronics', 'Apple', 36, 'https://images.unsplash.com/photo-1592286927505-1def25115558?w=500&h=500&fit=crop&auto=format&q=80', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Samsung Galaxy S24 256GB', 69999, 'Samsung Galaxy S24 with advanced camera system, Snapdragon processor, and vibrant AMOLED screen.', 'Electronics', 'Samsung', 40, 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&h=500&fit=crop&auto=format&q=80', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Sony WH-1000XM5 Headphones', 24999, 'Industry-leading noise cancellation wireless headphones with exceptional sound and comfort.', 'Electronics', 'Sony', 58, 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500&h=500&fit=crop&auto=format&q=80', 4.8);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Apple Watch Series 9', 27999, 'Smartwatch with advanced health sensors, always-on display, and seamless iOS integration.', 'Electronics', 'Apple', 48, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&auto=format&q=80', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Dell Inspiron 15 Laptop', 58999, 'Dell Inspiron 15 with Intel i5 processor, 8GB RAM, 512GB SSD, and 15.6" Full HD display for productivity.', 'Electronics', 'Dell', 24, 'https://images.unsplash.com/photo-1559163489-ac8a38f0b587?w=500&h=500&fit=crop&auto=format&q=80', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Bluetooth Portable Speaker', 3999, 'Compact bluetooth speaker with 12-hour battery life and rich bass for outdoor and indoor use.', 'Electronics', 'SoundMax', 86, 'https://images.unsplash.com/photo-1589003200312-34c08553d967?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Noise Cancelling Earbuds', 5999, 'True wireless earbuds with active noise cancellation, wireless charging, and long battery life.', 'Electronics', 'SoundPods', 104, 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Smart Home Hub', 4999, 'Centralized smart home hub with voice control, multi-protocol support, and secure cloud integration.', 'Electronics', 'HomeSmart', 64, 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, '4K Smart LED TV 43"', 32999, 'Crystal-clear 4K Smart LED TV with HDR support, built-in streaming apps, and thin bezel design.', 'Electronics', 'ViewTech', 22, 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&h=500&fit=crop&auto=format&q=80', 4.4);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'External Hard Drive 2TB', 5499, 'Portable 2TB external hard drive with fast USB 3.0 transfer and durable casing.', 'Electronics', 'StorageMax', 70, 'https://images.unsplash.com/photo-1613141725399-6da0a81e7c4a?w=500&h=500&fit=crop&auto=format&q=80', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wireless Charging Stand', 1999, 'Ergonomic wireless charging stand compatible with most Qi-enabled devices.', 'Electronics', 'ChargePad', 120, 'https://images.unsplash.com/photo-1606906833191-92342f56e900?w=500&h=500&fit=crop&auto=format&q=80', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'HD Webcam 1080p', 2299, 'Full HD 1080p webcam with auto-focus and low-light correction for clear video calls.', 'Electronics', 'WebVision', 88, 'https://images.unsplash.com/photo-1598936879949-3e3e8fdf6e2c?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Ergonomic Wireless Mouse', 1299, 'Ergonomic wireless mouse with adjustable DPI and long battery life for office productivity.', 'Electronics', 'TechPeripherals', 140, 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&h=500&fit=crop&auto=format&q=80', 4.2);

-- COMMIT
COMMIT;

-- Verification queries (run after executing the script):
-- SELECT COUNT(*) AS TOTAL_PRODUCTS FROM PRODUCTS;
-- SELECT CATEGORY, COUNT(*) FROM PRODUCTS GROUP BY CATEGORY ORDER BY CATEGORY;
