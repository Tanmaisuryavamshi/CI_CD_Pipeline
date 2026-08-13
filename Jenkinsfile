pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest --junitxml=report.xml --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            junit 'report.xml'
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}