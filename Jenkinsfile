pipeline {

    agent any

    environment {

        DOCKER_USERNAME = "nithish3990"

        FRONTEND_IMAGE = "nithish3990/trip-planner-frontend"
        BACKEND_IMAGE  = "nithish3990/trip-planner-backend"
        DATABASE_IMAGE = "nithish3990/trip-planner-database"

        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout GitHub') {

            steps {

                git branch: 'main',
                    url: 'https://github.com/Nithish-1503/Docker-CI-CD.git'
            }
        }


        stage('Build Frontend Image') {

            steps {

                sh '''
                    docker build \
                    -t ${FRONTEND_IMAGE}:${IMAGE_TAG} \
                    ./forntend
                '''
            }
        }


        stage('Build Backend Image') {

            steps {

                sh '''
                    docker build \
                    -t ${BACKEND_IMAGE}:${IMAGE_TAG} \
                    ./backend
                '''
            }
        }


        stage('Build Database Image') {

            steps {

                sh '''
                    docker build \
                    -t ${DATABASE_IMAGE}:${IMAGE_TAG} \
                    ./database
                '''
            }
        }


        stage('Docker Hub Login') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''
                }
            }
        }


        stage('Push Docker Images') {

            steps {

                sh '''
                    docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}
                    docker push ${BACKEND_IMAGE}:${IMAGE_TAG}
                    docker push ${DATABASE_IMAGE}:${IMAGE_TAG}
                '''
            }
        }


        stage('Deploy to Kubernetes') {

            steps {

                 sh 'kubectl apply -f k8s/'

                    // Roll the deployments to the freshly built tag
                    sh 'kubectl -n trip-planner set image deployment/frontend frontend=$REGISTRY/trip-frontend:$IMAGE_TAG'
                    sh 'kubectl -n trip-planner set image deployment/backend  backend=$REGISTRY/trip-backend:$IMAGE_TAG'
                    sh 'kubectl -n trip-planner set image deployment/mysql    mysql=$REGISTRY/trip-mysql:$IMAGE_TAG'

                    // Wait for rollout
                    sh 'kubectl -n trip-planner rollout status deployment/backend'
                    sh 'kubectl -n trip-planner rollout status deployment/frontend'
                
            }
        }
    }


    post {

        success {

            echo 'Trip Planner CI/CD pipeline completed successfully!'
        }

        failure {

            echo 'Trip Planner CI/CD pipeline failed!'
        }
    }
}
