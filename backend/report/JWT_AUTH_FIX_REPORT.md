# JWT Authentication Fix Report

## Summary
This fix addressed JWT authentication and Swagger OAuth2 flow issues in the FastAPI backend.

## Root Causes
1. `current_user` and `admin_only` used `Depends` instead of `Security`, so FastAPI did not expose protected endpoints as security-requiring in OpenAPI.
2. OpenAPI security schema was configured, but authentication paths still inherited global security requirements; auth endpoints needed explicit exemption.
3. `/api/auth/token` was implemented, but failed for legacy password hashes stored in the database (e.g. plaintext `12345`), causing 500 errors.
4. Existing login flow returned a valid token, but Swagger password flow and API docs were inconsistent with actual behavior.

## Fixes Applied
- `backend/app/utils/auth_dependency.py`
  - Changed `current_user` to use `Security(oauth2_scheme)`.
  - Changed `admin_only` to use `Security(current_user)`.
- `backend/app/main.py`
  - Added OAuth2 password flow security scheme under `components.securitySchemes`.
  - Added `BearerAuth` scheme for JWT bearer support.
  - Added global security rules and exempted `/api/auth/login`, `/api/auth/register`, `/api/auth/token` from requiring security.
- `backend/app/routes/auth_routes.py`
  - Added `/api/auth/token` route to support OAuth2PasswordRequestForm and Swagger token acquisition.
- `backend/app/utils/password.py`
  - Added fallback for `passlib.exc.UnknownHashError` to handle legacy/plain-text password hashes during verification.

## Validation
- Direct bearer auth test succeeded: `POST /api/products/add` returned `200` and inserted a product into Oracle DB.
- Full API suite executed successfully via `backend/run_api_tests.py`.
- Swagger OpenAPI schema now exposes the token endpoint and correct security schemes.

## Result
Protected endpoints now accept `Authorization: Bearer <token>` and return success for authorized requests.

## Notes
- Legacy password hashes in the DB are now handled gracefully during verification.
- Swagger authorize flow is now consistent with the running API.
