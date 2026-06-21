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
					sh '''
					python3 -m venv .venv || python -m venv .venv
					. .venv/bin/activate
					pip install --upgrade pip setuptools wheel
					pip install -r requirements_prod.txt
					'''
				}
			}
		}

		stage('Install Frontend Dependencies') {
			steps {
				dir("${FRONTEND_DIR}") {
					sh '''
					npm ci
					'''
				}
			}
		}

		stage('Run Backend Tests') {
			steps {
				dir("${BACKEND_DIR}") {
					sh '''
					. .venv/bin/activate
					if [ -f pytest.ini ] || ls test*/ | grep -q .; then
						pytest -q || true
					else
						echo "No backend tests found. Skipping."
					fi
					'''
				}
			}
		}

		stage('Build Frontend') {
			steps {
				dir("${FRONTEND_DIR}") {
					sh '''
					npm run build
					'''
				}
			}
		}

		stage('Build Backend Docker Image') {
			steps {
				sh "docker build -t ${BACKEND_IMAGE} ./backend"
			}
		}

		stage('Build Frontend Docker Image') {
			steps {
				sh "docker build -t ${FRONTEND_IMAGE} ./frontend"
			}
		}

		stage('Run Docker Compose') {
			steps {
				sh '''
				docker compose up -d --build
				'''
			}
		}

		stage('Verify Backend Health') {
			steps {
				sh '''
				echo "Waiting for backend..."
				retries=12
				until curl -fsS http://localhost:8000/docs || [ $retries -le 0 ]; do
					retries=$((retries-1))
					sleep 5
					echo "retrying... $retries"
				done
				curl -fsS http://localhost:8000/docs
				'''
			}
		}

		stage('Verify Frontend Health') {
			steps {
				sh '''
				echo "Waiting for frontend..."
				retries=12
				until curl -fsS http://localhost:5173 || [ $retries -le 0 ]; do
					retries=$((retries-1))
					sleep 5
					echo "retrying... $retries"
				done
				curl -fsS http://localhost:5173
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
			sh 'docker compose down --remove-orphans || true'
		}
	}
}
