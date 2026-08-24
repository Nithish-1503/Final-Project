pipeline {
    agent any

    environment {
        // Your Docker registry account (Docker Hub username, or a full registry URL).
        REGISTRY   = "nithish3990"
        IMAGE_TAG  = "latest"
        DOCKER_CREDS = "dockerhub-creds"

    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Nithish-1503/Final-Project.git'    
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker build -t $REGISTRY/trip-frontend:$IMAGE_TAG ./frontend'
                sh 'docker build -t $REGISTRY/trip-backend:$IMAGE_TAG  ./backend'
                sh 'docker build -t $REGISTRY/trip-mysql:$IMAGE_TAG    ./database'
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push $REGISTRY/trip-frontend:$IMAGE_TAG'
                    sh 'docker push $REGISTRY/trip-backend:$IMAGE_TAG'
                    sh 'docker push $REGISTRY/trip-mysql:$IMAGE_TAG'

                    
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                
                    // Apply manifests

                     sh '''
                    kubectl apply -f k8s/config-secret.yaml
                    kubectl apply -f k8s/mysql-pvc.yaml
                    kubectl apply -f k8s/mysql-deploy.yaml
                    kubectl apply -f k8s/mysql-service.yaml

                    kubectl apply -f k8s/backend-deploy.yaml
                    kubectl apply -f k8s/backend-service.yaml

                    kubectl apply -f k8s/frontend-deploy.yaml
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
            echo "✅ Deployed build ${IMAGE_TAG} successfully."
        }
        failure {
            echo "❌ Build ${IMAGE_TAG} failed. Check the logs above."
        }
        always {
            sh 'docker logout || true'
        }
    }
}
