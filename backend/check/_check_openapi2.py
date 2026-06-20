from app.main import app
spec = app.openapi()
print('security:', spec.get('security'))
print('securitySchemes:', spec.get('components', {}).get('securitySchemes'))
print('/api/auth/token present:', '/api/auth/token' in spec['paths'])
print('/api/products/add security:', spec['paths']['/api/products/add'].get('security'))
