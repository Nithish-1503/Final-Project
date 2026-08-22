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

                sh '''
                    kubectl apply -f k8s/mysql-secret.yaml
                    kubectl apply -f k8s/mysql-pvc.yaml
                    kubectl apply -f k8s/mysql-deployment.yaml
                    kubectl apply -f k8s/mysql-service.yaml

                    kubectl apply -f k8s/backend-deployment.yaml
                    kubectl apply -f k8s/backend-service.yaml

                    kubectl apply -f k8s/frontend-deployment.yaml
                    kubectl apply -f k8s/frontend-service.yaml

                    kubectl rollout restart deployment/mysql
                    kubectl rollout restart deployment/backend
                    kubectl rollout restart deployment/frontend

                    kubectl rollout status deployment/mysql
                    kubectl rollout status deployment/backend
                    kubectl rollout status deployment/frontend
                '''
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
