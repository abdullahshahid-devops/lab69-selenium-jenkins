pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    options {
        timestamps()
    }

    environment {
        COMPOSE_PROJECT_NAME = 'lab69-jenkins'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Start Grid') {
            steps {
                sh '''
                    mkdir -p reports
                    docker compose down --remove-orphans || true
                    docker compose up -d --build selenium-hub chrome
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    int testExitCode = sh(
                        script: 'docker compose run --rm test-runner',
                        returnStatus: true
                    )

                    if (testExitCode != 0) {
                        error("Selenium tests failed with exit code ${testExitCode}")
                    }
                }
            }
            post {
                always {
                    junit testResults: 'reports/junit.xml', allowEmptyResults: true
                    publishHTML(target: [
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Selenium HTML Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: true
                    ])
                }
            }
        }

        stage('Teardown') {
            steps {
                sh 'docker compose down --remove-orphans || true'
            }
        }
    }

    post {
        always {
            sh 'docker compose down --remove-orphans || true'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
