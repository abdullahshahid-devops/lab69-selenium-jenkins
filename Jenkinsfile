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
                        script: '''
                            set +e

                            docker compose run \
                                --name lab69-jenkins-test-runner \
                                test-runner

                            test_exit_code=$?

                            mkdir -p "$WORKSPACE/reports"

                            docker cp \
                                lab69-jenkins-test-runner:/reports/. \
                                "$WORKSPACE/reports/"
                            copy_exit_code=$?

                            docker rm -f \
                                lab69-jenkins-test-runner \
                                >/dev/null 2>&1 || true

                            if [ "$copy_exit_code" -ne 0 ]; then
                                echo "ERROR: Could not copy Selenium reports"
                                exit "$copy_exit_code"
                            fi

                            exit "$test_exit_code"
                        ''',
                        returnStatus: true
                    )

                    if (testExitCode != 0) {
                        error(
                            "Selenium tests or report collection failed: ${testExitCode}"
                        )
                    }
                }
            }

            post {
                always {
                    junit(
                        testResults: 'reports/junit.xml',
                        allowEmptyResults: false
                    )

                    publishHTML(target: [
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Selenium HTML Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: false
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

            archiveArtifacts(
                artifacts: 'reports/**',
                allowEmptyArchive: false
            )
        }
    }
}
