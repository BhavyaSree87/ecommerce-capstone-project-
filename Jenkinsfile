pipeline {
    agent any

    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'

        DOCKER_IMAGE_BACKEND = "bhavyasree01/ecommerce-backend:latest"
        DOCKER_IMAGE_FRONTEND = "bhavyasree01/ecommerce-frontend:latest"
    }

    stages {

        stage('Checkout Source') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Verify Project Structure') {
            steps {
                bat '''
                    if not exist backend (
                        echo ERROR: backend directory not found
                        exit /b 1
                    )

                    if not exist frontend (
                        echo ERROR: frontend directory not found
                        exit /b 1
                    )

                    if not exist backend\\requirements_prod.txt (
                        echo ERROR: requirements_prod.txt not found
                        exit /b 1
                    )

                    if not exist frontend\\package.json (
                        echo ERROR: package.json not found
                        exit /b 1
                    )

                    echo Project structure verified successfully
                '''
            }
        }

        stage('Backend Dependencies') {
            steps {
                dir("${BACKEND_DIR}") {
                    bat '''
                        echo Python Version
                        python --version || exit /b 1

                        echo Pip Version
                        pip --version || exit /b 1

                        echo Installing Backend Dependencies
                        python -m pip install --upgrade pip setuptools wheel
                        python -m pip install -r requirements_prod.txt || exit /b 1

                        echo Backend dependencies installed successfully
                    '''
                }
            }
        }

        stage('Backend Tests') {
            steps {
                dir("${BACKEND_DIR}") {
                    bat '''
                        echo Running Backend Tests
                        pytest -q
                        if errorlevel 1 (
                            echo ERROR: Backend tests failed
                            exit /b 1
                        )

                        echo Backend tests completed successfully
                    '''
                }
            }
        }

        stage('Frontend Dependencies') {
            steps {
                dir("${FRONTEND_DIR}") {
                    bat '''
                        echo Installing Frontend Dependencies
                        call npm ci

                        if errorlevel 1 (
                            echo ERROR: npm installation failed
                            exit /b 1
                        )

                        echo Frontend dependencies installed successfully
                    '''
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir("${FRONTEND_DIR}") {
                    bat '''
                        echo Building Frontend
                        call npm run build

                        if errorlevel 1 (
                            echo ERROR: Frontend build failed
                            exit /b 1
                        )

                        if not exist dist (
                            echo ERROR: dist folder not generated
                            exit /b 1
                        )

                        echo Frontend build completed successfully
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                bat '''
                    echo Building Backend Docker Image...
                    docker build -t %DOCKER_IMAGE_BACKEND% backend

                    if errorlevel 1 (
                        echo ERROR: Backend Docker image build failed
                        exit /b 1
                    )

                    echo Building Frontend Docker Image...
                    docker build -t %DOCKER_IMAGE_FRONTEND% frontend

                    if errorlevel 1 (
                        echo ERROR: Frontend Docker image build failed
                        exit /b 1
                    )

                    echo Docker images built successfully
                '''
            }
        }

        stage('Verify Docker Images') {
            steps {
                bat '''
                    docker image inspect %DOCKER_IMAGE_BACKEND% > nul

                    if errorlevel 1 (
                        echo ERROR: Backend Docker image not found
                        exit /b 1
                    )

                    docker image inspect %DOCKER_IMAGE_FRONTEND% > nul

                    if errorlevel 1 (
                        echo ERROR: Frontend Docker image not found
                        exit /b 1
                    )

                    echo Docker images verified successfully
                '''
            }
        }

        stage('Run Docker Compose') {
            steps {
                bat '''
                    docker compose up -d --build

                    if errorlevel 1 (
                        echo ERROR: Docker Compose failed
                        exit /b 1
                    )

                    echo Docker containers started successfully
                '''
            }
        }

        stage('Verify Backend Health') {
            steps {
                bat '''
                    powershell -Command "Invoke-WebRequest -Uri http://localhost:8000/docs -UseBasicParsing"

                    if errorlevel 1 (
                        echo ERROR: Backend health check failed
                        exit /b 1
                    )

                    echo Backend is healthy
                '''
            }
        }

        stage('Verify Frontend Health') {
            steps {
                bat '''
                    powershell -Command "Invoke-WebRequest -Uri http://localhost:5173 -UseBasicParsing"

                    if errorlevel 1 (
                        echo ERROR: Frontend health check failed
                        exit /b 1
                    )

                    echo Frontend is healthy
                '''
            }
        }

        stage('Push Docker Images') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    bat '''
                        echo Logging into Docker Hub...
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin

                        if errorlevel 1 (
                            echo ERROR: Docker login failed
                            exit /b 1
                        )

                        echo Pushing Backend Image...
                        docker push %DOCKER_IMAGE_BACKEND%

                        if errorlevel 1 (
                            echo ERROR: Backend image push failed
                            docker logout
                            exit /b 1
                        )

                        echo Pushing Frontend Image...
                        docker push %DOCKER_IMAGE_FRONTEND%

                        if errorlevel 1 (
                            echo ERROR: Frontend image push failed
                            docker logout
                            exit /b 1
                        )

                        docker logout
                        echo Docker images pushed successfully
                    '''
                }
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
            echo "Backend verified and deployed"
            echo "Frontend built and deployed"
            echo "Docker images created successfully"
        }

        failure {
            echo "Pipeline failed!"
            echo "Check Jenkins console output for detailed errors"
        }

        always {
            echo "Cleaning up Docker containers..."
            bat 'docker compose down --remove-orphans'
            cleanWs()
        }
    }
}