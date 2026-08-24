pipeline {
    agent any

    environment {
        // Your Docker registry account (Docker Hub username, or a full registry URL).
        REGISTRY   = "nithish3990"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        // Jenkins credentials ID for Docker registry login (create in Manage Jenkins > Credentials).
        DOCKER_CREDS = "dockerhub-creds"
        // Jenkins credentials ID for the kubeconfig file (Secret file type).
        KUBECONFIG_CRED = "kubeconfig"
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

                    // Also tag & push :latest
                    sh 'docker tag $REGISTRY/trip-frontend:$IMAGE_TAG $REGISTRY/trip-frontend:latest && docker push $REGISTRY/trip-frontend:latest'
                    sh 'docker tag $REGISTRY/trip-backend:$IMAGE_TAG  $REGISTRY/trip-backend:latest  && docker push $REGISTRY/trip-backend:latest'
                    sh 'docker tag $REGISTRY/trip-mysql:$IMAGE_TAG    $REGISTRY/trip-mysql:latest    && docker push $REGISTRY/trip-mysql:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                
                    // Apply manifests
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
