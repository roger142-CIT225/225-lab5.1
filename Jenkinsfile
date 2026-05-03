pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/roger142'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/roger142-CIT225/225-lab5.1.git'
        KUBECONFIG = credentials('roger142-225-sp26')
    }

    stages {

        stage('Cleanup Old Services') {
            steps {
                script {
                    sh "kubectl delete service prod-service || true"
                    sh "kubectl delete service dev-service || true"
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        stage('Lint HTML') {
            steps {
                sh 'docker run --rm -v $(pwd):/workdir node:18-alpine sh -c "npm install -g htmlhint --silent && htmlhint /workdir/index.html"'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "sed -i 's|BUILD_NUMBER_PLACEHOLDER|${IMAGE_TAG}|' index.html"
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Dev') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    sh "sleep 10"
                    sh "curl -f http://10.48.229.161:32000 || error 'DEV health check failed'"
                }
            }
        }

        stage('Acceptance Tests') {
            steps {
                script {
                    sh "docker run --rm -v ${WORKSPACE}:/workdir joyzoursky/python-chromedriver:3.9-selenium python3 /workdir/selenium-test.py"
                }
            }
        }

        stage('DAST Security Scan') {
            steps {
                script {
                    sh '''
                        docker run --rm \
                          -v $(pwd):/dastardly \
                          --network=host \
                          ghcr.io/portswigger/dastardly:latest \
                          http://10.48.229.161:32000 || true
                    '''
                }
            }
        }

        stage('Deploy to Prod') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                    sh "kubectl apply -f deployment-prod.yaml"
                }
            }
        }

        stage('Check Kubernetes Cluster') {
            steps {
                script {
                    sh "kubectl get all"
                }
            }
        }
    }

    post {
        success {
            slackSend color: 'good',
                message: "Build ${BUILD_NUMBER} PASSED - ${env.JOB_NAME} | PROD: http://10.48.228.117"
        }
        unstable {
            slackSend color: 'warning',
                message: "Build ${BUILD_NUMBER} UNSTABLE - ${env.JOB_NAME}"
        }
        failure {
            slackSend color: 'danger',
                message: "Build ${BUILD_NUMBER} FAILED - ${env.JOB_NAME}"
        }
    }
}
