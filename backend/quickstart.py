#!/usr/bin/env python3
"""
Quick Start Script for FastAPI E-Commerce Backend
This script helps set up and run the application
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python 3.9+ is installed"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from .env.example...")
        if Path(".env.example").exists():
            with open(".env.example", "r") as src:
                with open(".env", "w") as dst:
                    dst.write(src.read())
            print("✓ .env file created. Please configure your database credentials")
            print("  Edit .env with your Oracle connection details")
        else:
            print("❌ .env.example not found")
            sys.exit(1)

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements_prod.txt"],
            check=True
        )
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_logs_directory():
    """Create logs directory"""
    Path("logs").mkdir(exist_ok=True)
    print("✓ Logs directory created")

def test_oracle_connection():
    """Test Oracle database connection"""
    print("\n🗄️  Testing Oracle connection...")
    try:
        import oracledb
        from dotenv import load_dotenv
        
        load_dotenv()
        
        try:
            conn = oracledb.connect(
                user=os.getenv("ORACLE_USER"),
                password=os.getenv("ORACLE_PASSWORD"),
                dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
            )
            print("✓ Oracle connection successful!")
            conn.close()
        except Exception as e:
            print(f"❌ Oracle connection failed: {e}")
            print("  Please check your database credentials in .env file")
            return False
    except ImportError:
        print("⚠️  oracledb not installed yet. Install dependencies first.")
        return False
    
    return True

def run_application(reload=True):
    """Run the FastAPI application"""
    print("\n🚀 Starting FastAPI application...")
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
    ]
    
    if reload:
        cmd.append("--reload")
    
    print(f"✓ Application starting on http://localhost:8000")
    print("✓ Swagger docs available at http://localhost:8000/docs")
    print("✓ ReDoc available at http://localhost:8000/redoc")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n✓ Application stopped")

def show_help():
    """Show help message"""
    print("""
    FastAPI E-Commerce Backend - Quick Start

    Usage:
        python quickstart.py [options]

    Options:
        --help          Show this help message
        --check         Check configuration without running
        --setup         Setup and install dependencies only
        --run           Run application with auto-reload (default)
        --prod          Run application in production mode (no auto-reload)
        --test-db       Test database connection

    Examples:
        python quickstart.py              # Full setup and run
        python quickstart.py --check      # Check configuration
        python quickstart.py --prod       # Production mode
        python quickstart.py --test-db    # Test database connection

    First Run:
        1. python quickstart.py --setup
        2. Configure .env with your database credentials
        3. Create database schema: sqlplus < database/01_create_schema.sql
        4. Load sample data: sqlplus < database/02_sample_data.sql
        5. python quickstart.py --run
    """)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--prod", action="store_true")
    parser.add_argument("--test-db", action="store_true")
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        sys.exit(0)
    
    print("=" * 60)
    print("FastAPI E-Commerce Backend - Quick Start Tool")
    print("=" * 60)
    
    # Always check Python version
    check_python_version()
    
    if args.test_db:
        check_env_file()
        test_oracle_connection()
        sys.exit(0)
    
    if args.check:
        check_env_file()
        print("\n✓ Configuration check passed")
        sys.exit(0)
    
    if args.setup:
        check_env_file()
        install_dependencies()
        create_logs_directory()
        print("\n✓ Setup complete!")
        print("\nNext steps:")
        print("1. Configure database credentials in .env")
        print("2. Create database schema: sqlplus < database/01_create_schema.sql")
        print("3. Run application: python quickstart.py --run")
        sys.exit(0)
    
    # Default: full setup and run
    check_env_file()
    install_dependencies()
    create_logs_directory()
    
    if not test_oracle_connection():
        print("\n⚠️  Database connection test failed.")
        print("  Please configure .env and ensure database is running.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Run application
    reload = not args.prod
    run_application(reload=reload)
