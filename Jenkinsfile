pipeline {
agent any

environment {
    BACKEND_DIR = 'backend'
    FRONTEND_DIR = 'frontend'
    BACKEND_IMAGE = 'ecommerce-backend:latest'
    FRONTEND_IMAGE = 'ecommerce-frontend:latest'
}

stages {
    stage('Checkout Source') {
        steps {
            checkout scm
        }
    }

    stage('Install Backend Dependencies') {
        steps {
            dir("${BACKEND_DIR}") {
                bat '''
                python --version
                pip --version
                pip install --upgrade pip setuptools wheel
                pip install -r requirements_prod.txt
                '''
            }
        }
    }

    stage('Install Frontend Dependencies') {
        steps {
            dir("${FRONTEND_DIR}") {
                bat '''
                npm ci
                '''
            }
        }
    }

    stage('Run Backend Tests') {
        steps {
            dir("${BACKEND_DIR}") {
                bat '''
                pytest -q
                '''
            }
        }
    }

    stage('Build Frontend') {
        steps {
            dir("${FRONTEND_DIR}") {
                bat '''
                npm run build
                '''
            }
        }
    }

    stage('Build Backend Docker Image') {
        steps {
            bat "docker build -t ${BACKEND_IMAGE} ./backend"
        }
    }

    stage('Build Frontend Docker Image') {
        steps {
            bat "docker build -t ${FRONTEND_IMAGE} ./frontend"
        }
    }

    stage('Run Docker Compose') {
        steps {
            bat '''
            docker compose up -d --build
            '''
        }
    }

    stage('Verify Backend Health') {
        steps {
            bat '''
            powershell -Command "Invoke-WebRequest -Uri http://localhost:8000/docs -UseBasicParsing"
            '''
        }
    }

    stage('Verify Frontend Health') {
        steps {
            bat '''
            powershell -Command "Invoke-WebRequest -Uri http://localhost:5173 -UseBasicParsing"
            '''
        }
    }

    stage('Deployment Success') {
        steps {
            echo 'Deployment pipeline completed successfully.'
        }
    }
}

post {
    success {
        echo 'Build succeeded - notify stakeholders (configure notification steps).'
    }
    failure {
        echo 'Build failed - notify stakeholders (configure notification steps).'
    }
    always {
        echo 'Cleaning up docker compose'
        bat 'docker compose down --remove-orphans'
    }
}

}