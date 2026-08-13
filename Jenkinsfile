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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=report.xml --alluredir=allure-results
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
