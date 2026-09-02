// Jenkinsfile - Declarative Pipeline
// This defines the stages Jenkins runs every time code is pushed to Git.
// Stages: Checkout -> Install Dependencies -> Test -> "Deploy"

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip3 install -r requirements.txt --break-system-packages'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests (Data Quality checks for the pipeline code)...'
                sh 'pytest tests/ -v'
            }
        }

        stage('Run Pipeline') {
            steps {
                echo 'Running the ETL pipeline...'
                sh 'python3 etl_pipeline.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying pipeline artifact... (simulated)'
                sh 'echo "Deployment simulated successfully at $(date)" > deployment_log.txt'
                archiveArtifacts artifacts: 'output/*.csv, deployment_log.txt', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! All stages passed.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above to see which step broke.'
        }
    }
}