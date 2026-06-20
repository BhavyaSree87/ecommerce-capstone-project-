# FastAPI E-Commerce Backend - Production Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Setup

Create `.env` file in backend directory:

```env
# Database Configuration
ORACLE_USER=system
ORACLE_PASSWORD=your_secure_password
ORACLE_HOST=your_oracle_host
ORACLE_PORT=1521
ORACLE_SERVICE=XE
ORACLE_CLIENT_LIB_DIR=/path/to/instantclient

# Security Configuration
SECRET_KEY=your-extremely-secure-random-string-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=2

# Logging
LOG_LEVEL=INFO

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
```

### 2. Database Preparation

```bash
# Connect to Oracle as DBA
sqlplus system/password@localhost:1521/XE

# Execute schema creation
@database/01_create_schema.sql

# Load sample data
@database/02_sample_data.sql

# Verify tables
SELECT table_name FROM user_tables;
```

### 3. Dependencies Installation

```bash
# Install dependencies from requirements_prod.txt
pip install -r requirements_prod.txt

# Or upgrade existing
pip install --upgrade -r requirements_prod.txt
```

## Running the Application

### Development

```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access Swagger docs
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

### Production with Uvicorn

```bash
# Simple production run
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With logging
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 \
  --log-level info --access-log
```

### Production with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker app.main:app
```

### Production with PM2 (Recommended)

```bash
# Install PM2 globally
npm install -g pm2

# Create ecosystem.config.js
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'ecommerce-backend',
    script: 'uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    instances: 4,
    exec_mode: 'cluster',
    env: {
      LOG_LEVEL: 'INFO'
    },
    error_file: 'logs/err.log',
    out_file: 'logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
EOF

# Start with PM2
pm2 start ecosystem.config.js

# Monitor
pm2 monit
pm2 logs

# Auto-restart on system reboot
pm2 startup
pm2 save
```

### Production with Supervisor

```bash
# Create /etc/supervisor/conf.d/ecommerce.conf
cat > /etc/supervisor/conf.d/ecommerce.conf << 'EOF'
[program:ecommerce-backend]
directory=/path/to/backend
command=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
stderr_logfile=/var/log/ecommerce_err.log
stdout_logfile=/var/log/ecommerce_out.log
environment=LOG_LEVEL=INFO
EOF

# Reload and start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ecommerce-backend
```

## Reverse Proxy Configuration (Nginx)

```nginx
upstream ecommerce_app {
    least_conn;
    server localhost:8000 max_fails=3 fail_timeout=30s;
    server localhost:8001 max_fails=3 fail_timeout=30s;
    server localhost:8002 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name api.ecommerce.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain application/json;
    
    location / {
        proxy_pass http://ecommerce_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Swagger docs
    location /docs {
        proxy_pass http://ecommerce_app/docs;
    }
    
    location /redoc {
        proxy_pass http://ecommerce_app/redoc;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.ecommerce.com;
    return 301 https://$server_name$request_uri;
}
```

## Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_prod.txt .
RUN pip install --no-cache-dir -r requirements_prod.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t ecommerce-backend:latest .
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name ecommerce-api \
  ecommerce-backend:latest
```

## Monitoring & Maintenance

### Health Check

```bash
# Check API health
curl http://localhost:8000/health

# Check Swagger docs availability
curl http://localhost:8000/docs
```

### Logs

```bash
# View application logs
tail -f logs/app_*.log

# View error logs
tail -f logs/errors_*.log

# Search logs
grep -i "error" logs/app_*.log
```

### Database Maintenance

```sql
-- Analyze tables for optimization
ANALYZE TABLE USERS;
ANALYZE TABLE PRODUCTS;
ANALYZE TABLE ORDERS;

-- Check index usage
SELECT index_name, used FROM v$object_usage;

-- Monitor locks
SELECT * FROM v$lock;

-- Backup database
RMAN> BACKUP DATABASE;
```

## Troubleshooting

### Connection Issues

```bash
# Test Oracle connection
python -c "
import oracledb
conn = oracledb.connect(user='system', password='password', dsn='localhost:1521/XE')
print('Connected successfully')
"
```

### Performance Issues

1. Check database indexes
2. Analyze slow queries
3. Review logs for errors
4. Monitor resource usage (CPU, RAM, Disk)

### Common Errors

- `ORA-12514`: Service name not found
  - Check ORACLE_SERVICE name
  
- `JWT verification failed`: Token expired or invalid secret key
  - Verify SECRET_KEY configuration
  
- `Connection refused`: Application not running
  - Check if service is running and port is open

## Security Best Practices

1. ✓ Use environment variables for secrets
2. ✓ Enable HTTPS/TLS
3. ✓ Use strong passwords (min 12 characters)
4. ✓ Implement rate limiting
5. ✓ Keep dependencies updated
6. ✓ Use Web Application Firewall (WAF)
7. ✓ Enable database encryption
8. ✓ Regular security audits
9. ✓ Monitor access logs
10. ✓ Implement backup strategy

## Performance Tuning

1. **Database Connection Pooling**
   - Configure connection pool size
   - Set connection timeout

2. **Caching**
   - Implement Redis for frequently accessed data
   - Cache product listings

3. **Load Balancing**
   - Use multiple application instances
   - Route with Nginx/HAProxy

4. **Database Optimization**
   - Create appropriate indexes
   - Analyze query execution plans
   - Archive old data

## Deployment Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Preparation | 1-2 days | Setup infra, configure env |
| Testing | 2-3 days | Run test checklist |
| Staging | 1 day | Deploy to staging, final tests |
| Production | 1-2 hours | Deploy to prod, monitor |

## Rollback Plan

```bash
# If deployment fails:
1. Identify issue in logs
2. Fix and rebuild
3. If database schema issue, restore backup:
   - RMAN> RESTORE DATABASE FROM BACKUP;
4. Restart application
```

## Support & Maintenance

- Monitor logs daily
- Review performance metrics weekly
- Update dependencies monthly
- Backup database daily
- Test disaster recovery quarterly

## Contact & Escalation

- DevOps Team: devops@company.com
- Database Team: dba@company.com
- On-Call Engineer: check PagerDuty
