pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t ecommerce-backend ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t ecommerce-frontend ./frontend'
            }
        }

        stage('Docker Compose') {
            steps {
                sh 'docker compose up -d'
            }
        }

    }
}