# API Test Report

- **Endpoint**: /api/auth/register
  - **Request**: {"name": "API Test User", "email": "apitest_1781774478@example.com", "password": "TestPass123!", "mobile": "9876543210", "address": "123 Test St", "city": "Hyderabad", "state": "TS", "pincode": "500001"}
  - **Status**: 201
  - **Response**: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozNCwiZW1haWwiOiJhcGl0ZXN0XzE3ODE3NzQ0NzhAZXhhbXBsZS5jb20iLCJyb2xlIjoiQ1VTVE9NRVIiLCJleHAiOjE3ODE3ODE2Nzl9.WU_kUYEJeBrzncQXBUQWyjiMtKJyxCiKfZqHi8mmHqQ", "token_type": "bearer", "expires_in": 7200, "user": {"id": 34, "name": "API Test User", "email": "apitest_1781774478@example.com", "role": "CUSTOMER", "mobile": "9876543210", "address": "123 Test St", "city": "Hyderabad", "state": "TS", "pincode": "500001", "created_at": null}}
  - **Result**: PASS

- **Endpoint**: /api/users/34
  - **Request**: "GET with auth"
  - **Status**: 200
  - **Response**: {"id": 34, "name": "API Test User", "email": "apitest_1781774478@example.com", "role": "CUSTOMER", "mobile": "9876543210", "address": "123 Test St", "city": "Hyderabad", "state": "TS", "pincode": "500001"}
  - **Result**: PASS

- **Endpoint**: /api/products/all
  - **Request**: "GET"
  - **Status**: 200
  - **Response**: {"total": 9, "page": 1, "page_size": 20, "items": [{"product_name": "Authorize Test Product", "price": 11.11, "description": "Created in bearer auth test", "category": "Test", "brand": "Test", "stock": 5, "image_url": null, "rating": 4.5, "product_id": 10}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 92, "image_url": null, "rating": 4.5, "product_id": 9}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": null, "rating": 4.5, "product_id": 8}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": null, "rating": 4.5, "product_id": 7}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": null, "rating": 4.5, "product_id": 6}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": null, "rating": 4.5, "product_id": 5}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": null, "rating": 4.5, "product_id": 4}, {"product_name": "Test Product", "price": 9.99, "description": "Inserted by tests", "category": "Test", "brand": "Tester", "stock": 100, "image_url": null, "rating": 4.5, "product_id": 3}, {"product_name": "iPhone 15 Pro", "price": 85000.0, "description": "Apple Premium Mobile", "category": "Electronics", "brand": "Apple", "stock": 50, "image_url": "iphone15pro.jpg", "rating": 4.9, "product_id": 1}]}
  - **Result**: PASS

- **Endpoint**: /api/products/10
  - **Request**: "GET"
  - **Status**: 200
  - **Response**: {"product_name": "Authorize Test Product", "price": 11.11, "description": "Created in bearer auth test", "category": "Test", "brand": "Test", "stock": 5, "image_url": null, "rating": 4.5, "product_id": 10}
  - **Result**: PASS

- **Endpoint**: /api/cart/add
  - **Request**: {"product_id": 10, "quantity": 1}
  - **Status**: 200
  - **Response**: {"message": "Item Added To Cart"}
  - **Result**: PASS

- **Endpoint**: /api/cart/
  - **Request**: "GET"
  - **Status**: 200
  - **Response**: [[15, 34, 10, 1]]
  - **Result**: PASS

- **Endpoint**: /api/cart/delete/15
  - **Request**: "DELETE"
  - **Status**: 200
  - **Response**: {"message": "Cart Item Deleted"}
  - **Result**: PASS

- **Endpoint**: /api/wishlist/add
  - **Request**: {"product_id": 10}
  - **Status**: 200
  - **Response**: {"message": "Added To Wishlist"}
  - **Result**: PASS

- **Endpoint**: /api/wishlist/
  - **Request**: "GET"
  - **Status**: 200
  - **Response**: [[15, 34, 10]]
  - **Result**: PASS

- **Endpoint**: /api/wishlist/delete/15
  - **Request**: "DELETE"
  - **Status**: 200
  - **Response**: {"message": "Wishlist Item Deleted"}
  - **Result**: PASS

- **Endpoint**: /api/orders/create
  - **Request**: {"items": [{"product_id": 10, "quantity": 1, "price": 11.11}], "shipping_address": "123 Test St", "billing_address": "123 Test St", "payment_method": "Test", "notes": ""}
  - **Status**: 200
  - **Response**: {"order_id": 27, "user_id": 34, "total_amount": 11.11, "status": "Order Placed", "items": [{"order_id": 27, "item_id": 28, "product_id": 10, "quantity": 1, "price": 11.11, "subtotal": 11.11}], "message": "Order placed successfully"}
  - **Result**: PASS

- **Endpoint**: /api/orders/user/34
  - **Request**: "GET"
  - **Status**: 200
  - **Response**: {"total": 1, "page": 1, "page_size": 20, "items": [[27, 28, 10, 1, 11.11, "Order Placed", 34, "2026-06-18T14:51:19.964000", 1]]}
  - **Result**: PASS

- **Endpoint**: /api/payments/pay
  - **Request**: {"order_id": 27, "payment_method": "Test", "payment_status": "PAID", "amount": 9.99}
  - **Status**: 200
  - **Response**: {"payment_id": 6, "order_id": 27, "payment_method": "Test", "payment_status": "PAID", "amount": 9.99, "transaction_id": null, "created_at": null}
  - **Result**: PASS

- **Endpoint**: /api/payments/order/27
  - **Request**: "GET"
  - **Status**: 200
  - **Response**: {"payment_id": 6, "order_id": 27, "payment_method": "Test", "payment_status": "PAID", "amount": 9.99}
  - **Result**: PASS

- **Endpoint**: /api/dashboard/stats
  - **Request**: "GET as admin"
  - **Status**: 200
  - **Response**: {"total_users": 25, "total_products": 9, "total_orders": 9, "total_payments": 5}
  - **Result**: PASS


Total: 15, Passed: 15, Failed: 0
