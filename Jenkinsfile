
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

        // Lab 3-1: Checkout from GitHub
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        // Lab 3-3 / 3-5: HTML linting — pipeline stops if this fails
        stage('Lint HTML') {
            steps {
                sh 'docker run --rm -v $(pwd):/workdir cytopia/htmlhint htmlhint /workdir/index.html'
            }
        }

        // Lab 3-1: Build Docker image
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                }
            }
        }

        // Lab 3-1: Push to Docker Hub
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        // Lab 3-1 / 3-2: Deploy to DEV using NodePort
        stage('Deploy to Dev') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        // Lab 3-6: Selenium acceptance test against DEV
        stage('Acceptance Tests') {
            steps {
                script {
                    sh "docker run --rm -v ${WORKSPACE}:/workdir joyzoursky/python-chromedriver:3.9-selenium python3 /workdir/selenium-test.py"
                }
            }
        }

        // Lab 3-7: DAST security scan with DASTardly
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

        // Lab 3-4 / MetalLB: Deploy to PROD using LoadBalancer
        stage('Deploy to Prod') {
            steps {
                script {
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                    sh "kubectl apply -f deployment-prod.yaml"
                }
            }
        }

        // Lab 3-1: Verify cluster state
        stage('Check Kubernetes Cluster') {
            steps {
                script {
                    sh "kubectl get all"
                }
            }
        }
    }

    // Lab 3-2: Slack notifications
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
